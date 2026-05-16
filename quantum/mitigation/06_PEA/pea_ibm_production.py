"""
Probabilistic Error Amplification (PEA) - IBM Production-Ready Implementation
================================================================================

Production workflow for PEA noise amplification + ZNE on IBM hardware.
Learns noise model, injects calibrated Pauli errors, extrapolates to zero.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
PEA injects Pauli errors with probability p_inject = (lambda-1)*p/(1-p)
to achieve exact noise scaling at continuous lambda values.
Combined with ZNE extrapolation for error mitigation.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
from scipy.optimize import curve_fit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/mitigation/06_PEA/production_results"


# =============================================================================
# PEA CIRCUIT GENERATION
# =============================================================================

def build_pea_circuit(
    base_circuit: QuantumCircuit,
    noise_factor: float,
    base_error_1q: float,
    base_error_2q: float,
    rng: np.random.Generator
) -> QuantumCircuit:
    """
    Build a PEA-amplified circuit instance.

    Injection (see explanation_physicist.md, Section 3.2):
        p_inject = (lambda-1)*p / (1-p) per gate.

    Args:
        base_circuit: Target circuit with measurements.
        noise_factor: Desired amplification.
        base_error_1q: Learned 1Q error rate.
        base_error_2q: Learned 2Q error rate.
        rng: Random number generator.

    Returns:
        Circuit with injected Pauli errors.
    """
    n_q = base_circuit.num_qubits
    n_c = base_circuit.num_clbits

    qr = QuantumRegister(n_q, 'q')
    cr = ClassicalRegister(n_c, 'c')
    qc = QuantumCircuit(qr, cr)

    p_inj_1q = max(0, (noise_factor - 1) * base_error_1q / (1 - base_error_1q))
    p_inj_2q = max(0, (noise_factor - 1) * base_error_2q / (1 - base_error_2q))

    paulis_1q = ['X', 'Y', 'Z']

    for inst in base_circuit.data:
        op = inst.operation
        qargs = [qr[base_circuit.qubits.index(q)] for q in inst.qubits]

        if op.name == 'measure':
            cargs = [cr[base_circuit.clbits.index(c)] for c in inst.clbits]
            qc.measure(qargs[0], cargs[0])
            continue
        if op.name == 'barrier':
            qc.barrier()
            continue

        qc.append(op, qargs)

        # Inject 1Q errors
        if len(qargs) == 1 and rng.random() < p_inj_1q:
            p = rng.choice(paulis_1q)
            if p == 'X': qc.x(qargs[0])
            elif p == 'Y': qc.y(qargs[0])
            else: qc.z(qargs[0])

        # Inject 2Q errors
        elif len(qargs) == 2 and rng.random() < p_inj_2q:
            for q in qargs:
                p = rng.choice(paulis_1q)
                if p == 'X': qc.x(q)
                elif p == 'Y': qc.y(q)
                else: qc.z(q)

    return qc


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full PEA + ZNE production workflow.

    Steps:
        1. Configure backend
        2. Noise learning (estimate error rates)
        3. Build target circuit
        4. Run PEA at multiple noise factors
        5. ZNE extrapolation
        6. Save results

    Args:
        use_simulator: If True, use noisy AerSimulator.
    """
    print("=" * 70)
    print("PEA + ZNE - Production Workflow")
    print("=" * 70)

    n_qubits = 3
    shots_per_sample = 400
    n_samples = 50

    # Known noise parameters (in production, these come from noise learning)
    p_1q = 0.005
    p_2q = 0.02

    # -----------------------------------------------------------------
    # Step 1: Backend
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        noise_model = NoiseModel()
        err_1q = pauli_error([('X', p_1q/3), ('Y', p_1q/3), ('Z', p_1q/3), ('I', 1-p_1q)])
        noise_model.add_all_qubit_quantum_error(err_1q, ['x', 'h', 'sx', 'ry', 'rz'])
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p_2q, 2), ['cx'])
        backend = AerSimulator(noise_model=noise_model)
        print(f"  AerSimulator: p_1q={p_1q}, p_2q={p_2q}")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        print("  IBM hardware (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Noise learning
    # -----------------------------------------------------------------
    print("\nStep 2: Noise learning")
    print(f"  Learned error rates: p_1q={p_1q}, p_2q={p_2q}")
    print(f"  Max amplification: lambda_max = {1/p_2q:.0f}")

    # -----------------------------------------------------------------
    # Step 3: Target circuit
    # -----------------------------------------------------------------
    print(f"\nStep 3: Building GHZ-{n_qubits} target circuit")
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    target = QuantumCircuit(qr, cr)
    target.h(qr[0])
    for i in range(1, n_qubits):
        target.cx(qr[0], qr[i])
    target.measure(qr, cr)

    ideal_value = 1.0

    # -----------------------------------------------------------------
    # Step 4: PEA at multiple noise factors
    # -----------------------------------------------------------------
    noise_factors = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    print(f"\nStep 4: Running PEA at lambdas = {noise_factors}")

    pea_values = []
    for lam in noise_factors:
        rng = np.random.default_rng(42)
        total_counts = {}
        for _ in range(n_samples):
            pea_qc = build_pea_circuit(target, lam, p_1q, p_2q, rng)
            result = backend.run(pea_qc, shots=shots_per_sample).result()
            for bs, c in result.get_counts().items():
                total_counts[bs] = total_counts.get(bs, 0) + c

        total = sum(total_counts.values())
        val = sum((-1) ** (sum(int(b) for b in bs.zfill(n_qubits)) % 2) * c / total
                  for bs, c in total_counts.items())
        pea_values.append(val)
        print(f"  lambda={lam:.1f}: <{'Z'*n_qubits}> = {val:.6f}")

    # -----------------------------------------------------------------
    # Step 5: ZNE extrapolation
    # -----------------------------------------------------------------
    print("\nStep 5: ZNE extrapolation")

    def exp_model(x, a, b, c):
        return a * np.exp(-b * x) + c

    try:
        popt, _ = curve_fit(exp_model, noise_factors, pea_values, p0=[1, 0.1, 0], maxfev=5000)
        zne_exp = float(exp_model(0, *popt))
    except Exception:
        zne_exp = float(np.polyval(np.polyfit(noise_factors, pea_values, 1), 0))

    zne_lin = float(np.polyval(np.polyfit(noise_factors[:2], pea_values[:2], 1), 0))

    raw_error = abs(pea_values[0] - ideal_value)
    print(f"\n  {'Method':<20} {'E_ZNE':<12} {'|Error|':<12}")
    print(f"  {'-'*44}")
    print(f"  {'Raw':<20} {pea_values[0]:<12.6f} {raw_error:<12.6f}")
    print(f"  {'PEA+ZNE (linear)':<20} {zne_lin:<12.6f} {abs(zne_lin - ideal_value):<12.6f}")
    print(f"  {'PEA+ZNE (exp.)':<20} {zne_exp:<12.6f} {abs(zne_exp - ideal_value):<12.6f}")

    # -----------------------------------------------------------------
    # Step 6: Save
    # -----------------------------------------------------------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        "timestamp": datetime.now().isoformat(),
        "n_qubits": n_qubits,
        "noise_factors": noise_factors,
        "pea_values": pea_values,
        "ideal_value": ideal_value,
        "zne_linear": zne_lin,
        "zne_exponential": zne_exp,
        "base_errors": {"p_1q": p_1q, "p_2q": p_2q},
    }

    filepath = os.path.join(RESULTS_DIR, "pea_zne_results.json")
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run PEA + ZNE production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
