"""
Measurement Error Mitigation (M3) - IBM Production-Ready Implementation
=========================================================================

Production workflow for measurement error mitigation on IBM hardware.
Uses per-qubit calibration and M3-style correction for scalability.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
M3 (Matrix-free Measurement Mitigation): Scalable readout error
correction that calibrates per-qubit error rates and corrects only
the observed subspace of measurement outcomes.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/mitigation/01_measurement_error_mitigation/production_results"


# =============================================================================
# CALIBRATION
# =============================================================================

def build_calibration_circuits(qubits: List[int], n_total: int) -> List[QuantumCircuit]:
    """
    Build per-qubit calibration circuits for M3.

    Per-qubit calibration (see explanation_physicist.md, Section 3.2):
        Prepare |0> and |1> on each qubit individually, measure.
        2 circuits per qubit, 2n total.

    Args:
        qubits: List of physical qubit indices to calibrate.
        n_total: Total number of qubits on the device.

    Returns:
        List of calibration circuits.
    """
    circuits = []

    for qubit in qubits:
        for prep_state in [0, 1]:
            qr = QuantumRegister(n_total, 'q')
            cr = ClassicalRegister(1, 'c')
            label = f'cal_q{qubit}_s{prep_state}'
            qc = QuantumCircuit(qr, cr, name=label)

            if prep_state == 1:
                qc.x(qr[qubit])

            qc.measure(qr[qubit], cr[0])
            circuits.append(qc)

    return circuits


def extract_per_qubit_matrices(
    calibration_results: List[Dict[str, int]],
    qubits: List[int]
) -> Dict[int, np.ndarray]:
    """
    Extract per-qubit 2x2 assignment matrices from calibration data.

    Assignment matrix (see explanation_physicist.md, Section 2.2):
        A_k = [[1-e_0, e_1], [e_0, 1-e_1]] for qubit k

    Args:
        calibration_results: List of counts from calibration circuits.
        qubits: List of qubit indices.

    Returns:
        Dictionary mapping qubit index to 2x2 assignment matrix.
    """
    matrices = {}

    for idx, qubit in enumerate(qubits):
        A_q = np.zeros((2, 2))

        for prep_state in [0, 1]:
            circuit_idx = idx * 2 + prep_state
            counts = calibration_results[circuit_idx]
            total = sum(counts.values())

            for bitstring, count in counts.items():
                measured_bit = int(bitstring[-1])
                A_q[measured_bit, prep_state] = count / total

        matrices[qubit] = A_q

    return matrices


# =============================================================================
# M3 CORRECTION
# =============================================================================

def apply_m3_correction(
    raw_counts: Dict[str, int],
    qubit_matrices: Dict[int, np.ndarray],
    qubit_order: List[int]
) -> Dict[str, float]:
    """
    Apply M3 correction using reduced assignment matrix.

    M3 algorithm (see explanation_physicist.md, Section 5.2):
        Build and invert reduced matrix over observed bitstrings only.
        Complexity: O(k^2 * n + k^3) where k = number of observed bitstrings.

    Args:
        raw_counts: Raw measurement counts.
        qubit_matrices: Per-qubit assignment matrices.
        qubit_order: Order of qubits in the bitstring (MSB first).

    Returns:
        Corrected probability distribution.
    """
    total_shots = sum(raw_counts.values())
    observed = sorted(raw_counts.keys())
    k = len(observed)
    n = len(qubit_order)

    # Build reduced assignment matrix
    A_reduced = np.zeros((k, k))
    for i, bs_i in enumerate(observed):
        for j, bs_j in enumerate(observed):
            product = 1.0
            for m, qubit in enumerate(qubit_order):
                bit_i = int(bs_i[m])
                bit_j = int(bs_j[m])
                A_q = qubit_matrices[qubit]
                product *= A_q[bit_i, bit_j]
            A_reduced[i, j] = product

    # Measured probability vector
    p_measured = np.array([raw_counts[bs] / total_shots for bs in observed])

    # Invert and correct
    try:
        p_corrected = np.linalg.solve(A_reduced, p_measured)
    except np.linalg.LinAlgError:
        p_corrected = np.linalg.lstsq(A_reduced, p_measured, rcond=None)[0]

    # Clip and renormalize
    p_corrected = np.maximum(p_corrected, 0)
    if p_corrected.sum() > 0:
        p_corrected /= p_corrected.sum()

    result = {}
    for i, bs in enumerate(observed):
        if p_corrected[i] > 1e-10:
            result[bs] = float(p_corrected[i])

    return result


# =============================================================================
# TARGET CIRCUIT
# =============================================================================

def build_target_circuit(n_qubits: int = 3) -> QuantumCircuit:
    """
    Build a target circuit for mitigation demonstration.

    GHZ state: ideal output is 50% |00...0> + 50% |11...1>.

    Args:
        n_qubits: Number of qubits.

    Returns:
        Target quantum circuit with measurements.
    """
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='target_ghz')

    qc.h(qr[0])
    for i in range(1, n_qubits):
        qc.cx(qr[0], qr[i])

    qc.barrier()
    qc.measure(qr, cr)

    return qc


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full production workflow for M3 measurement error mitigation.

    Steps:
        1. Select backend and qubits
        2. Run calibration circuits
        3. Build per-qubit assignment matrices
        4. Run target circuit
        5. Apply M3 correction
        6. Save results and analysis

    Args:
        use_simulator: If True, use AerSimulator. If False, use IBM hardware.
    """
    print("=" * 70)
    print("M3 Measurement Error Mitigation - Production Workflow")
    print("=" * 70)

    n_qubits = 3
    shots = 8192
    qubits = list(range(n_qubits))

    # -----------------------------------------------------------------
    # Step 1: Backend setup
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        from qiskit_aer.noise import NoiseModel, ReadoutError
        noise_model = NoiseModel()
        for q in qubits:
            p1g0 = 0.02 + 0.01 * q
            p0g1 = 0.04 + 0.02 * q
            re = ReadoutError([[1 - p1g0, p1g0], [p0g1, 1 - p0g1]])
            noise_model.add_readout_error(re, [q])
        backend = AerSimulator(noise_model=noise_model)
        print(f"  Using AerSimulator with per-qubit readout noise")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        print("  IBM hardware mode (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Calibration
    # -----------------------------------------------------------------
    print(f"\nStep 2: Running calibration ({2 * n_qubits} circuits, {shots} shots each)")
    cal_circuits = build_calibration_circuits(qubits, n_qubits)
    cal_results = []
    for qc in cal_circuits:
        result = backend.run(qc, shots=shots).result()
        cal_results.append(result.get_counts())

    # -----------------------------------------------------------------
    # Step 3: Build assignment matrices
    # -----------------------------------------------------------------
    print("\nStep 3: Building per-qubit assignment matrices")
    qubit_matrices = extract_per_qubit_matrices(cal_results, qubits)
    for q, A_q in qubit_matrices.items():
        e0 = A_q[1, 0]
        e1 = A_q[0, 1]
        print(f"  Qubit {q}: e_0 = {e0:.4f}, e_1 = {e1:.4f}")

    # -----------------------------------------------------------------
    # Step 4: Run target circuit
    # -----------------------------------------------------------------
    print(f"\nStep 4: Running target circuit ({shots} shots)")
    target_qc = build_target_circuit(n_qubits)

    if not use_simulator:
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        target_qc = pm.run(target_qc)

    result = backend.run(target_qc, shots=shots).result()
    raw_counts = result.get_counts()
    total = sum(raw_counts.values())
    raw_dist = {k: v / total for k, v in raw_counts.items()}

    print(f"  Raw results ({len(raw_counts)} distinct outcomes):")
    for k, v in sorted(raw_dist.items(), key=lambda x: -x[1])[:8]:
        print(f"    {k}: {v:.4f}")

    # -----------------------------------------------------------------
    # Step 5: Apply M3 correction
    # -----------------------------------------------------------------
    print("\nStep 5: Applying M3 correction")
    qubit_order = list(range(n_qubits))
    corrected_dist = apply_m3_correction(raw_counts, qubit_matrices, qubit_order)

    print(f"  Corrected results:")
    for k, v in sorted(corrected_dist.items(), key=lambda x: -x[1])[:8]:
        print(f"    {k}: {v:.4f}")

    # -----------------------------------------------------------------
    # Step 6: Analysis and save
    # -----------------------------------------------------------------
    print("\nStep 6: Analysis")
    ideal_dist = {format(0, f'0{n_qubits}b'): 0.5,
                  format(2**n_qubits - 1, f'0{n_qubits}b'): 0.5}

    all_keys = sorted(set(list(ideal_dist.keys()) + list(raw_dist.keys()) +
                          list(corrected_dist.keys())))
    tvd_raw = 0.5 * sum(abs(ideal_dist.get(k, 0) - raw_dist.get(k, 0)) for k in all_keys)
    tvd_corr = 0.5 * sum(abs(ideal_dist.get(k, 0) - corrected_dist.get(k, 0)) for k in all_keys)

    print(f"  TVD(raw, ideal)       = {tvd_raw:.4f}")
    print(f"  TVD(corrected, ideal) = {tvd_corr:.4f}")
    print(f"  Improvement: {tvd_raw / tvd_corr:.2f}x" if tvd_corr > 0 else "  Perfect correction!")

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        "timestamp": datetime.now().isoformat(),
        "n_qubits": n_qubits,
        "shots": shots,
        "readout_errors": {str(q): {"e0": float(A[1, 0]), "e1": float(A[0, 1])}
                          for q, A in qubit_matrices.items()},
        "raw_distribution": raw_dist,
        "corrected_distribution": corrected_dist,
        "tvd_raw": tvd_raw,
        "tvd_corrected": tvd_corr,
    }

    filepath = os.path.join(RESULTS_DIR, "m3_mitigation_results.json")
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run M3 measurement error mitigation production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
