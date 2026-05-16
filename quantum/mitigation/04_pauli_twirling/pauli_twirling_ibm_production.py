"""
Pauli Twirling - IBM Production-Ready Implementation
======================================================

Production workflow for Pauli twirling on IBM hardware.
Randomizes gate noise to convert coherent errors to Pauli channels.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Pauli twirling conjugates each CNOT with random Pauli pairs,
converting general CPTP noise to a Pauli channel (diagonal PTM).
Coherent errors that accumulate as O(L*epsilon) become stochastic
errors that accumulate as O(sqrt(L)*epsilon).
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, coherent_unitary_error

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/mitigation/04_pauli_twirling/production_results"

# CNOT twirl table (see explanation_physicist.md, Section 3.2)
CNOT_TWIRL_TABLE = [
    ('I', 'I', 'I', 'I'), ('I', 'X', 'I', 'X'),
    ('I', 'Y', 'Z', 'Y'), ('I', 'Z', 'Z', 'Z'),
    ('X', 'I', 'X', 'X'), ('X', 'X', 'X', 'I'),
    ('X', 'Y', 'Y', 'Z'), ('X', 'Z', 'Y', 'Y'),
    ('Y', 'I', 'Y', 'X'), ('Y', 'X', 'Y', 'I'),
    ('Y', 'Y', 'X', 'Z'), ('Y', 'Z', 'X', 'Y'),
    ('Z', 'I', 'Z', 'I'), ('Z', 'X', 'Z', 'X'),
    ('Z', 'Y', 'I', 'Y'), ('Z', 'Z', 'I', 'Z'),
]


def apply_pauli(qc, label, qubit):
    """Apply a named Pauli gate."""
    if label == 'X': qc.x(qubit)
    elif label == 'Y': qc.y(qubit)
    elif label == 'Z': qc.z(qubit)


def generate_twirled_circuits(
    base_circuit: QuantumCircuit,
    n_twirls: int,
    seed: int = 42
) -> List[QuantumCircuit]:
    """
    Generate Pauli-twirled variants of a circuit for production.

    Twirling (see explanation_physicist.md, Section 5.1):
        For each CNOT, sample a random twirl pair and insert
        the before/after Paulis. Single-qubit Paulis compile
        into adjacent gates.

    Args:
        base_circuit: Original circuit.
        n_twirls: Number of random twirl instances.
        seed: Random seed.

    Returns:
        List of twirled circuits.
    """
    rng = np.random.default_rng(seed)
    n_cnots = sum(1 for inst in base_circuit.data if inst.operation.name == 'cx')

    circuits = []
    for _ in range(n_twirls):
        indices = rng.integers(0, 16, size=n_cnots)
        n_q = base_circuit.num_qubits
        n_c = base_circuit.num_clbits

        qr = QuantumRegister(n_q, 'q')
        cr = ClassicalRegister(n_c, 'c') if n_c > 0 else None
        qc = QuantumCircuit(qr, cr) if cr else QuantumCircuit(qr)

        cnot_idx = 0
        for inst in base_circuit.data:
            op = inst.operation
            qargs = [qr[base_circuit.qubits.index(q)] for q in inst.qubits]

            if op.name == 'cx':
                bc, bt, ac, at = CNOT_TWIRL_TABLE[indices[cnot_idx]]
                cnot_idx += 1
                apply_pauli(qc, bc, qargs[0])
                apply_pauli(qc, bt, qargs[1])
                qc.cx(qargs[0], qargs[1])
                apply_pauli(qc, ac, qargs[0])
                apply_pauli(qc, at, qargs[1])
            elif op.name == 'measure':
                cargs = [cr[base_circuit.clbits.index(c)] for c in inst.clbits]
                qc.measure(qargs[0], cargs[0])
            else:
                qc.append(op, qargs)

        circuits.append(qc)

    return circuits


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full Pauli twirling production workflow.

    Steps:
        1. Configure backend
        2. Build target circuit
        3. Generate twirled variants
        4. Run all circuits
        5. Average results
        6. Compare with untwirled
        7. Save results

    Args:
        use_simulator: If True, use AerSimulator with coherent noise.
    """
    print("=" * 70)
    print("Pauli Twirling - Production Workflow")
    print("=" * 70)

    n_qubits = 2
    shots = 8192
    n_twirls = 32

    # -----------------------------------------------------------------
    # Step 1: Backend
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        epsilon = 0.1
        zz = np.diag([1, -1, -1, 1]).astype(complex)
        u_err = np.cos(epsilon) * np.eye(4) - 1j * np.sin(epsilon) * zz
        noise_model = NoiseModel()
        noise_model.add_all_qubit_quantum_error(
            coherent_unitary_error(u_err), 'cx'
        )
        backend = AerSimulator(noise_model=noise_model)
        print(f"  AerSimulator with coherent ZZ error (epsilon={epsilon})")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        print("  IBM hardware (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Target circuit
    # -----------------------------------------------------------------
    print("\nStep 2: Building target circuit (Bell state)")
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    target = QuantumCircuit(qr, cr, name='bell')
    target.h(qr[0])
    target.cx(qr[0], qr[1])
    target.measure(qr, cr)

    # -----------------------------------------------------------------
    # Step 3: Generate twirled variants
    # -----------------------------------------------------------------
    print(f"\nStep 3: Generating {n_twirls} twirled circuits")
    twirled = generate_twirled_circuits(target, n_twirls, seed=42)

    # -----------------------------------------------------------------
    # Step 4: Run
    # -----------------------------------------------------------------
    print(f"\nStep 4: Running {n_twirls + 1} circuits ({shots} shots each)")

    # Raw (no twirling)
    raw_result = backend.run(target, shots=shots).result()
    raw_counts = raw_result.get_counts()

    # Twirled
    twirl_total = {}
    for tc in twirled:
        res = backend.run(tc, shots=shots // n_twirls).result()
        for bs, count in res.get_counts().items():
            twirl_total[bs] = twirl_total.get(bs, 0) + count

    # -----------------------------------------------------------------
    # Step 5: Compare
    # -----------------------------------------------------------------
    print("\nStep 5: Results comparison")
    ideal = {'00': 0.5, '11': 0.5}

    raw_total = sum(raw_counts.values())
    raw_dist = {k: v / raw_total for k, v in raw_counts.items()}

    tw_total_shots = sum(twirl_total.values())
    tw_dist = {k: v / tw_total_shots for k, v in twirl_total.items()}

    print(f"\n  {'Bitstring':<12} {'Ideal':<10} {'Raw':<10} {'Twirled':<10}")
    print(f"  {'-'*42}")
    keys = sorted(set(list(ideal.keys()) + list(raw_dist.keys()) + list(tw_dist.keys())))
    for k in keys:
        print(f"  {k:<12} {ideal.get(k, 0):<10.4f} {raw_dist.get(k, 0):<10.4f} "
              f"{tw_dist.get(k, 0):<10.4f}")

    tvd_raw = 0.5 * sum(abs(ideal.get(k, 0) - raw_dist.get(k, 0)) for k in keys)
    tvd_tw = 0.5 * sum(abs(ideal.get(k, 0) - tw_dist.get(k, 0)) for k in keys)
    print(f"\n  TVD (raw):     {tvd_raw:.4f}")
    print(f"  TVD (twirled): {tvd_tw:.4f}")

    # -----------------------------------------------------------------
    # Step 6: Save
    # -----------------------------------------------------------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        "timestamp": datetime.now().isoformat(),
        "n_twirls": n_twirls,
        "shots": shots,
        "raw_distribution": raw_dist,
        "twirled_distribution": tw_dist,
        "tvd_raw": tvd_raw,
        "tvd_twirled": tvd_tw,
    }

    filepath = os.path.join(RESULTS_DIR, "pauli_twirling_results.json")
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run Pauli twirling production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
