"""
Dynamical Decoupling (DD) - IBM Production-Ready Implementation
=================================================================

Production workflow for dynamical decoupling on IBM hardware.
Note: Qiskit Runtime has built-in DD support via transpilation options.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
DD inserts pulse sequences (Hahn, CPMG, XY-4) during idle periods
to suppress low-frequency decoherence. Average Hamiltonian theory
shows that the toggling-frame interaction averages to zero.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import XGate, YGate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/mitigation/03_dynamical_decoupling/production_results"


# =============================================================================
# DD INSERTION
# =============================================================================

def insert_dd_sequence(
    circuit: QuantumCircuit,
    qubit: int,
    n_slots: int,
    sequence_type: str = 'xy4'
):
    """
    Insert DD pulse sequence into a circuit during idle slots.

    DD sequences (see explanation_physicist.md, Section 3):
        - 'hahn': Single X pulse (first-order dephasing cancellation)
        - 'cpmg': Multiple X pulses (broadband suppression)
        - 'xy4':  X-Y-X-Y (self-compensating, universal protection)

    Args:
        circuit: Circuit to modify.
        qubit: Qubit index.
        n_slots: Number of gate-time slots available.
        sequence_type: Type of DD sequence.
    """
    if sequence_type == 'hahn':
        half = n_slots // 2
        for _ in range(half):
            circuit.id(qubit)
        circuit.x(qubit)
        for _ in range(n_slots - half - 1):
            circuit.id(qubit)

    elif sequence_type == 'xy4':
        if n_slots < 4:
            for _ in range(n_slots):
                circuit.id(qubit)
            return
        spacing = (n_slots - 4) // 4
        for gate_fn in [circuit.x, circuit.y, circuit.x, circuit.y]:
            for _ in range(spacing):
                circuit.id(qubit)
            gate_fn(qubit)
        for _ in range(n_slots - 4 - 4 * spacing):
            circuit.id(qubit)

    elif sequence_type == 'cpmg':
        n_pulses = max(2, n_slots // 8)
        spacing = max(0, (n_slots - n_pulses) // (n_pulses + 1))
        for p in range(n_pulses):
            for _ in range(spacing):
                circuit.id(qubit)
            circuit.x(qubit)
        remaining = n_slots - n_pulses - n_pulses * spacing
        for _ in range(max(0, remaining)):
            circuit.id(qubit)


# =============================================================================
# TARGET CIRCUIT
# =============================================================================

def build_ghz_with_idle(
    n_qubits: int = 3,
    n_idle_slots: int = 20,
    use_dd: bool = False,
    dd_type: str = 'xy4'
) -> QuantumCircuit:
    """
    Build GHZ circuit with idle period (optionally with DD).

    The idle period simulates a scenario where qubits wait after
    entanglement (e.g., between state prep and algorithm steps).

    Args:
        n_qubits: Number of qubits.
        n_idle_slots: Number of idle gate slots.
        use_dd: Whether to insert DD during idle.
        dd_type: DD sequence type.

    Returns:
        GHZ circuit with idle period and measurements.
    """
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    name = f'ghz_{"dd" if use_dd else "no_dd"}_{n_idle_slots}'
    qc = QuantumCircuit(qr, cr, name=name)

    # Prepare GHZ
    qc.h(qr[0])
    for i in range(n_qubits - 1):
        qc.cx(qr[i], qr[i + 1])

    qc.barrier()

    # Idle period (with or without DD)
    for q in range(n_qubits):
        if use_dd:
            insert_dd_sequence(qc, q, n_idle_slots, dd_type)
        else:
            for _ in range(n_idle_slots):
                qc.id(qr[q])

    qc.barrier()
    qc.measure(qr, cr)

    return qc


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full DD production workflow.

    Steps:
        1. Configure backend
        2. Build circuits with and without DD
        3. Transpile for target backend
        4. Run circuits
        5. Compare fidelities
        6. Save results

    Args:
        use_simulator: If True, use noisy AerSimulator.
    """
    print("=" * 70)
    print("Dynamical Decoupling - Production Workflow")
    print("=" * 70)

    n_qubits = 3
    shots = 8192
    n_idle_slots = 40

    # -----------------------------------------------------------------
    # Step 1: Backend
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        noise_model = NoiseModel()
        t1, t2 = 50000, 30000  # ns
        gate_1q, gate_2q = 50, 300  # ns

        err_1q = thermal_relaxation_error(t1, t2, gate_1q)
        for gate in ['x', 'y', 'h', 'id', 'sx', 'rz']:
            noise_model.add_all_qubit_quantum_error(err_1q, gate)

        err_2q = thermal_relaxation_error(t1, t2, gate_2q).expand(
            thermal_relaxation_error(t1, t2, gate_2q)
        )
        noise_model.add_all_qubit_quantum_error(err_2q, 'cx')

        backend = AerSimulator(noise_model=noise_model)
        print(f"  AerSimulator: T1={t1/1000}us, T2={t2/1000}us")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        # Note: Runtime has built-in DD:
        # options.dynamical_decoupling.enable = True
        # options.dynamical_decoupling.sequence_type = "XY4"
        print("  IBM hardware (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Build circuits
    # -----------------------------------------------------------------
    print(f"\nStep 2: Building circuits (idle={n_idle_slots} slots)")

    qc_no_dd = build_ghz_with_idle(n_qubits, n_idle_slots, use_dd=False)
    qc_hahn = build_ghz_with_idle(n_qubits, n_idle_slots, use_dd=True, dd_type='hahn')
    qc_xy4 = build_ghz_with_idle(n_qubits, n_idle_slots, use_dd=True, dd_type='xy4')

    circuits = {
        'No DD': qc_no_dd,
        'Hahn Echo': qc_hahn,
        'XY-4': qc_xy4,
    }

    # -----------------------------------------------------------------
    # Step 3: Transpile (for real backend)
    # -----------------------------------------------------------------
    print("\nStep 3: Transpilation")
    if not use_simulator:
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        circuits = {k: pm.run(v) for k, v in circuits.items()}
    print("  Skipped (simulator mode)")

    # -----------------------------------------------------------------
    # Step 4: Run
    # -----------------------------------------------------------------
    print(f"\nStep 4: Running circuits ({shots} shots each)")
    results = {}
    for name, qc in circuits.items():
        result = backend.run(qc, shots=shots).result()
        results[name] = result.get_counts()

    # -----------------------------------------------------------------
    # Step 5: Analysis
    # -----------------------------------------------------------------
    print("\nStep 5: Fidelity analysis")
    ideal_dist = {'0' * n_qubits: 0.5, '1' * n_qubits: 0.5}

    print(f"\n  {'Method':<16} {'F(ideal)':<12} {'P(000)':<10} {'P(111)':<10}")
    print(f"  {'-'*48}")

    fidelity_results = {}
    for name, counts in results.items():
        total = sum(counts.values())
        dist = {k: v / total for k, v in counts.items()}

        all_keys = set(list(dist.keys()) + list(ideal_dist.keys()))
        fid = sum(np.sqrt(dist.get(k, 0) * ideal_dist.get(k, 0)) for k in all_keys) ** 2

        p000 = dist.get('0' * n_qubits, 0)
        p111 = dist.get('1' * n_qubits, 0)
        print(f"  {name:<16} {fid:<12.4f} {p000:<10.4f} {p111:<10.4f}")
        fidelity_results[name] = fid

    # -----------------------------------------------------------------
    # Step 6: Save
    # -----------------------------------------------------------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    save_data = {
        "timestamp": datetime.now().isoformat(),
        "n_qubits": n_qubits,
        "shots": shots,
        "n_idle_slots": n_idle_slots,
        "fidelities": fidelity_results,
        "counts": {k: dict(v) for k, v in results.items()},
    }

    filepath = os.path.join(RESULTS_DIR, "dd_results.json")
    with open(filepath, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run dynamical decoupling production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
