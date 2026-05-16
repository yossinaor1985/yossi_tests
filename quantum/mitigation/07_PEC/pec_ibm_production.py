"""
Probabilistic Error Cancellation (PEC) - IBM Production-Ready Implementation
==============================================================================

Production workflow for PEC on IBM hardware.
Uses noise learning, quasi-probability decomposition, and Monte Carlo
sampling for exact (unbiased) error mitigation.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
PEC: G_ideal = sum_i eta_i G_noisy_i (quasi-probability decomposition).
Exact in expectation. Sampling overhead gamma^2 = (sum |eta_i|)^2.
In Qiskit Runtime: resilience_level = 3 enables PEC automatically.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Session

RESULTS_DIR = "quantum/mitigation/07_PEC/production_results"


# =============================================================================
# QUASI-PROBABILITY COMPUTATION
# =============================================================================

def compute_quasi_probs(p_1q: float, p_2q: float) -> Dict:
    """
    Compute quasi-probability decompositions for depolarizing noise.

    Quasi-probabilities (see explanation_physicist.md, Section 3.2):
        1Q: eta_I = (3-3p)/(3-4p), eta_{X,Y,Z} = -p/(3-4p)
        gamma_1q = (3+2p)/(3-4p)

    Args:
        p_1q: 1Q depolarizing rate.
        p_2q: 2Q depolarizing rate.

    Returns:
        Dictionary with decomposition parameters.
    """
    # 1Q decomposition
    d1 = 3 - 4 * p_1q
    eta_I_1q = (3 - 3 * p_1q) / d1
    eta_P_1q = -p_1q / d1
    gamma_1q = (3 + 2 * p_1q) / d1

    # 2Q decomposition
    d2 = 15 - 16 * p_2q
    eta_II = (15 - 15 * p_2q) / d2
    eta_P_2q = -p_2q / d2
    gamma_2q = (15 + 14 * p_2q) / d2

    return {
        '1q': {'eta_I': eta_I_1q, 'eta_P': eta_P_1q, 'gamma': gamma_1q},
        '2q': {'eta_II': eta_II, 'eta_P': eta_P_2q, 'gamma': gamma_2q},
    }


# =============================================================================
# PEC SAMPLING
# =============================================================================

def build_pec_instance(
    base_circuit: QuantumCircuit,
    qp_data: Dict,
    rng: np.random.Generator
) -> Tuple[QuantumCircuit, float, float]:
    """
    Build one PEC circuit instance.

    Sampling (see explanation_physicist.md, Section 6.1):
        For each gate, sample correction from quasi-probability distribution.
        Track cumulative gamma and sign.

    Args:
        base_circuit: Original circuit.
        qp_data: Quasi-probability parameters.
        rng: Random generator.

    Returns:
        Tuple of (modified circuit, total_gamma, total_sign).
    """
    n_q = base_circuit.num_qubits
    n_c = base_circuit.num_clbits
    qr = QuantumRegister(n_q, 'q')
    cr = ClassicalRegister(n_c, 'c')
    qc = QuantumCircuit(qr, cr)

    gamma_total = 1.0
    sign_total = 1.0

    paulis_1q = ['I', 'X', 'Y', 'Z']
    probs_1q = [abs(qp_data['1q']['eta_I'])] + [abs(qp_data['1q']['eta_P'])] * 3
    probs_1q = np.array(probs_1q) / sum(probs_1q)
    signs_1q = [1 if qp_data['1q']['eta_I'] >= 0 else -1] + \
               [1 if qp_data['1q']['eta_P'] >= 0 else -1] * 3

    for inst in base_circuit.data:
        op = inst.operation
        qargs = [qr[base_circuit.qubits.index(q)] for q in inst.qubits]

        if op.name == 'measure':
            cargs = [cr[base_circuit.clbits.index(c)] for c in inst.clbits]
            qc.measure(qargs[0], cargs[0])
            continue
        if op.name == 'barrier':
            continue

        qc.append(op, qargs)

        if len(qargs) == 1:
            idx = rng.choice(4, p=probs_1q)
            gamma_total *= qp_data['1q']['gamma']
            sign_total *= signs_1q[idx]
            p_label = paulis_1q[idx]
            if p_label == 'X': qc.x(qargs[0])
            elif p_label == 'Y': qc.y(qargs[0])
            elif p_label == 'Z': qc.z(qargs[0])

        elif len(qargs) == 2:
            gamma_total *= qp_data['2q']['gamma']
            # Simplified: sample identity vs random 2Q Pauli
            if rng.random() < abs(qp_data['2q']['eta_II']) / qp_data['2q']['gamma']:
                sign_total *= (1 if qp_data['2q']['eta_II'] >= 0 else -1)
            else:
                sign_total *= (1 if qp_data['2q']['eta_P'] >= 0 else -1)
                for q in qargs:
                    p = rng.choice(['X', 'Y', 'Z'])
                    if p == 'X': qc.x(q)
                    elif p == 'Y': qc.y(q)
                    else: qc.z(q)

    return qc, gamma_total, sign_total


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full PEC production workflow.

    Steps:
        1. Configure backend
        2. Noise learning
        3. Compute quasi-probabilities
        4. Build target circuit
        5. Run PEC Monte Carlo sampling
        6. Compute corrected expectation value
        7. Save results

    Args:
        use_simulator: If True, use noisy AerSimulator.
    """
    print("=" * 70)
    print("Probabilistic Error Cancellation - Production Workflow")
    print("=" * 70)

    n_qubits = 2
    n_pec_samples = 2000
    p_1q, p_2q = 0.01, 0.03

    # -----------------------------------------------------------------
    # Step 1: Backend
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        noise_model = NoiseModel()
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p_1q, 1), ['h', 'x', 'sx'])
        noise_model.add_all_qubit_quantum_error(depolarizing_error(p_2q, 2), ['cx'])
        backend = AerSimulator(noise_model=noise_model)
        print(f"  AerSimulator: p_1q={p_1q}, p_2q={p_2q}")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        # Note: Runtime PEC: options.resilience_level = 3
        print("  IBM hardware (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Noise learning
    # -----------------------------------------------------------------
    print("\nStep 2: Noise learning (using known parameters for demo)")
    print(f"  p_1q = {p_1q}, p_2q = {p_2q}")

    # -----------------------------------------------------------------
    # Step 3: Quasi-probability decomposition
    # -----------------------------------------------------------------
    print("\nStep 3: Computing quasi-probability decomposition")
    qp_data = compute_quasi_probs(p_1q, p_2q)
    print(f"  1Q gamma = {qp_data['1q']['gamma']:.6f}")
    print(f"  2Q gamma = {qp_data['2q']['gamma']:.6f}")

    # -----------------------------------------------------------------
    # Step 4: Target circuit (Bell state)
    # -----------------------------------------------------------------
    print("\nStep 4: Building target circuit (Bell state)")
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    target = QuantumCircuit(qr, cr)
    target.h(qr[0])
    target.cx(qr[0], qr[1])
    target.measure(qr, cr)
    ideal_zz = 1.0

    # Raw measurement
    raw_result = backend.run(target, shots=20000).result()
    raw_counts = raw_result.get_counts()
    raw_total = sum(raw_counts.values())
    raw_zz = sum((-1) ** (int(bs[0]) ^ int(bs[1])) * c / raw_total
                 for bs, c in raw_counts.items())

    # -----------------------------------------------------------------
    # Step 5: PEC sampling
    # -----------------------------------------------------------------
    print(f"\nStep 5: PEC Monte Carlo sampling ({n_pec_samples} samples)")
    rng = np.random.default_rng(42)
    pec_values = []

    for i in range(n_pec_samples):
        pec_qc, gamma, sign = build_pec_instance(target, qp_data, rng)
        result = backend.run(pec_qc, shots=1).result()
        counts = result.get_counts()
        bs = list(counts.keys())[0].zfill(2)
        parity = (int(bs[0]) ^ int(bs[1]))
        o_val = (-1) ** parity
        pec_values.append(gamma * sign * o_val)

    pec_estimate = np.mean(pec_values)
    pec_stderr = np.std(pec_values) / np.sqrt(len(pec_values))

    # -----------------------------------------------------------------
    # Step 6: Results
    # -----------------------------------------------------------------
    print("\nStep 6: Results")
    print(f"  Ideal <ZZ>:   {ideal_zz:.6f}")
    print(f"  Raw <ZZ>:     {raw_zz:.6f} (error: {abs(raw_zz - ideal_zz):.6f})")
    print(f"  PEC <ZZ>:     {pec_estimate:.6f} +/- {pec_stderr:.6f}")
    print(f"  PEC error:    {abs(pec_estimate - ideal_zz):.6f}")

    # -----------------------------------------------------------------
    # Step 7: Save
    # -----------------------------------------------------------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        "timestamp": datetime.now().isoformat(),
        "n_qubits": n_qubits,
        "n_pec_samples": n_pec_samples,
        "noise_params": {"p_1q": p_1q, "p_2q": p_2q},
        "ideal_zz": ideal_zz,
        "raw_zz": raw_zz,
        "pec_estimate": pec_estimate,
        "pec_stderr": pec_stderr,
    }

    filepath = os.path.join(RESULTS_DIR, "pec_results.json")
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {filepath}")


def main():
    """Run PEC production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
