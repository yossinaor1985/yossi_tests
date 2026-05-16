"""
Measurement Error Mitigation (M3) - Local Simulator Implementation
====================================================================

Demonstrates calibration of readout errors, construction of the confusion
(assignment) matrix, and correction via matrix inversion. Compares raw
(noisy) measurement results with mitigated results.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Readout errors: P_measured = A * P_ideal
Calibration: prepare basis states, build confusion matrix A
Correction: P_ideal = A^{-1} * P_measured
M3 approach: work only with observed bitstrings (reduced submatrix)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError


# =============================================================================
# READOUT ERROR MODEL
# =============================================================================

def create_readout_noise_model(
    n_qubits: int,
    p1_given0: float = 0.02,
    p0_given1: float = 0.05
) -> NoiseModel:
    """
    Create a noise model with only readout errors.

    Readout error model (see explanation_physicist.md, Section 2.1):
        P(measure 1 | state 0) = p1_given0 (false positive)
        P(measure 0 | state 1) = p0_given1 (false negative / T1 during readout)

    Typically p0_given1 > p1_given0 on superconducting hardware because
    T1 relaxation during measurement drives |1> -> |0>.

    Args:
        n_qubits: Number of qubits.
        p1_given0: Probability of reading 1 when state is 0.
        p0_given1: Probability of reading 0 when state is 1.

    Returns:
        NoiseModel with readout errors on all qubits.
    """
    noise_model = NoiseModel()

    # Assignment matrix for each qubit (see explanation_physicist.md, Section 2.2):
    # A = [[1-p1_given0, p0_given1],
    #      [p1_given0,   1-p0_given1]]
    readout_error = ReadoutError([
        [1 - p1_given0, p1_given0],      # P(outcome | state=0)
        [p0_given1,     1 - p0_given1]    # P(outcome | state=1)
    ])

    for qubit in range(n_qubits):
        noise_model.add_readout_error(readout_error, [qubit])

    return noise_model


def create_asymmetric_readout_noise_model(
    qubit_errors: List[Tuple[float, float]]
) -> NoiseModel:
    """
    Create noise model with per-qubit asymmetric readout errors.

    Different qubits may have different readout fidelities in practice.

    Args:
        qubit_errors: List of (p1_given0, p0_given1) for each qubit.

    Returns:
        NoiseModel with per-qubit readout errors.
    """
    noise_model = NoiseModel()

    for qubit_idx, (p1g0, p0g1) in enumerate(qubit_errors):
        re = ReadoutError([
            [1 - p1g0, p1g0],
            [p0g1,     1 - p0g1]
        ])
        noise_model.add_readout_error(re, [qubit_idx])

    return noise_model


# =============================================================================
# CALIBRATION CIRCUITS
# =============================================================================

def build_calibration_circuits(n_qubits: int) -> List[QuantumCircuit]:
    """
    Build calibration circuits for full confusion matrix.

    Calibration procedure (see explanation_physicist.md, Section 3.1):
        For each basis state |j>, prepare it and measure.
        Column j of A = empirical distribution of measurement outcomes.

    For n qubits, this requires 2^n circuits (exponential cost).
    For the per-qubit (tensor product) model, only 2n circuits suffice.

    Args:
        n_qubits: Number of qubits.

    Returns:
        List of 2^n calibration circuits.
    """
    n_states = 2 ** n_qubits
    circuits = []

    for state_idx in range(n_states):
        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        qc = QuantumCircuit(qr, cr, name=f'cal_{state_idx:0{n_qubits}b}')

        # Prepare computational basis state |state_idx>
        bitstring = format(state_idx, f'0{n_qubits}b')
        for bit_pos, bit_val in enumerate(bitstring):
            if bit_val == '1':
                qc.x(qr[n_qubits - 1 - bit_pos])  # Qiskit bit ordering

        qc.measure(qr, cr)
        circuits.append(qc)

    return circuits


def build_per_qubit_calibration_circuits(n_qubits: int) -> List[QuantumCircuit]:
    """
    Build per-qubit calibration circuits (tensor product model).

    Tensor product calibration (see explanation_physicist.md, Section 3.2):
        For each qubit k, prepare |0> and |1>, measure.
        Total: 2n circuits (linear cost).

    Args:
        n_qubits: Number of qubits.

    Returns:
        List of 2*n_qubits calibration circuits.
    """
    circuits = []

    for qubit_idx in range(n_qubits):
        for prep_state in [0, 1]:
            qr = QuantumRegister(n_qubits, 'q')
            cr = ClassicalRegister(n_qubits, 'c')
            label = f'cal_q{qubit_idx}_s{prep_state}'
            qc = QuantumCircuit(qr, cr, name=label)

            if prep_state == 1:
                qc.x(qr[qubit_idx])

            # Measure only the target qubit
            qc.measure(qr[qubit_idx], cr[qubit_idx])
            circuits.append(qc)

    return circuits


# =============================================================================
# CONFUSION MATRIX CONSTRUCTION
# =============================================================================

def build_confusion_matrix(
    calibration_counts: List[Dict[str, int]],
    n_qubits: int
) -> np.ndarray:
    """
    Build the full confusion matrix from calibration results.

    Assignment matrix (see explanation_physicist.md, Section 2.2):
        A[i,j] = P(measure bitstring i | prepared bitstring j)
        Column j = probability distribution when state j was prepared.

    Args:
        calibration_counts: List of counts dicts from calibration circuits.
        n_qubits: Number of qubits.

    Returns:
        2^n x 2^n confusion matrix A.
    """
    n_states = 2 ** n_qubits
    A = np.zeros((n_states, n_states))

    for j, counts in enumerate(calibration_counts):
        total = sum(counts.values())
        for bitstring, count in counts.items():
            # Convert bitstring to index
            i = int(bitstring, 2)
            A[i, j] = count / total

    return A


def build_per_qubit_matrices(
    calibration_counts: List[Dict[str, int]],
    n_qubits: int,
    shots: int
) -> List[np.ndarray]:
    """
    Build per-qubit 2x2 assignment matrices from per-qubit calibration.

    Tensor product model (see explanation_physicist.md, Section 2.3):
        A_total = A_1 (x) A_2 (x) ... (x) A_n

    Args:
        calibration_counts: Counts from per-qubit calibration circuits.
        n_qubits: Number of qubits.
        shots: Number of shots per calibration circuit.

    Returns:
        List of n 2x2 assignment matrices.
    """
    matrices = []

    for qubit_idx in range(n_qubits):
        A_q = np.zeros((2, 2))

        for prep_state in [0, 1]:
            circuit_idx = qubit_idx * 2 + prep_state
            counts = calibration_counts[circuit_idx]
            total = sum(counts.values())

            for bitstring, count in counts.items():
                # Extract the bit for the target qubit
                measured_bit = int(bitstring[n_qubits - 1 - qubit_idx])
                A_q[measured_bit, prep_state] = count / total

        matrices.append(A_q)

    return matrices


# =============================================================================
# CORRECTION METHODS
# =============================================================================

def correct_matrix_inversion(
    raw_counts: Dict[str, int],
    confusion_matrix: np.ndarray,
    n_qubits: int
) -> Dict[str, float]:
    """
    Correct measurement results by inverting the confusion matrix.

    Direct inversion (see explanation_physicist.md, Section 4.1):
        P_ideal = A^{-1} * P_measured

    Note: A^{-1} can produce negative probabilities. We clip and renormalize.

    Args:
        raw_counts: Raw measurement counts.
        confusion_matrix: The assignment matrix A.
        n_qubits: Number of qubits.

    Returns:
        Corrected probability distribution.
    """
    n_states = 2 ** n_qubits
    total_shots = sum(raw_counts.values())

    # Build measured probability vector
    p_measured = np.zeros(n_states)
    for bitstring, count in raw_counts.items():
        idx = int(bitstring, 2)
        p_measured[idx] = count / total_shots

    # Invert: P_ideal = A^{-1} * P_measured
    A_inv = np.linalg.inv(confusion_matrix)
    p_corrected = A_inv @ p_measured

    # Clip negative values and renormalize
    p_corrected = np.maximum(p_corrected, 0)
    if p_corrected.sum() > 0:
        p_corrected /= p_corrected.sum()

    # Convert back to dictionary
    result = {}
    for idx in range(n_states):
        if p_corrected[idx] > 1e-10:
            bitstring = format(idx, f'0{n_qubits}b')
            result[bitstring] = p_corrected[idx]

    return result


def correct_least_squares(
    raw_counts: Dict[str, int],
    confusion_matrix: np.ndarray,
    n_qubits: int
) -> Dict[str, float]:
    """
    Correct via constrained least squares.

    Least-squares correction (see explanation_physicist.md, Section 4.3):
        Minimize ||A * P_ideal - P_measured||^2
        subject to P_ideal >= 0 and sum(P_ideal) = 1

    Uses scipy's bounded least squares as a practical approximation.

    Args:
        raw_counts: Raw measurement counts.
        confusion_matrix: The assignment matrix A.
        n_qubits: Number of qubits.

    Returns:
        Corrected probability distribution.
    """
    from scipy.optimize import minimize

    n_states = 2 ** n_qubits
    total_shots = sum(raw_counts.values())

    p_measured = np.zeros(n_states)
    for bitstring, count in raw_counts.items():
        idx = int(bitstring, 2)
        p_measured[idx] = count / total_shots

    def objective(p):
        return np.sum((confusion_matrix @ p - p_measured) ** 2)

    # Equality constraint: sum = 1
    constraints = {'type': 'eq', 'fun': lambda p: np.sum(p) - 1.0}
    bounds = [(0, 1)] * n_states
    x0 = p_measured.copy()

    result_opt = minimize(objective, x0, method='SLSQP',
                          bounds=bounds, constraints=constraints)

    p_corrected = result_opt.x

    # Convert to dict
    result = {}
    for idx in range(n_states):
        if p_corrected[idx] > 1e-10:
            bitstring = format(idx, f'0{n_qubits}b')
            result[bitstring] = p_corrected[idx]

    return result


def correct_m3_reduced(
    raw_counts: Dict[str, int],
    per_qubit_matrices: List[np.ndarray],
    n_qubits: int
) -> Dict[str, float]:
    """
    M3-style correction using reduced assignment matrix.

    M3 algorithm (see explanation_physicist.md, Section 5.2):
        1. Identify k observed bitstrings
        2. Build k x k reduced assignment matrix
        3. Invert the reduced matrix
        4. Apply correction

    This avoids constructing the full 2^n x 2^n matrix.

    Args:
        raw_counts: Raw measurement counts.
        per_qubit_matrices: Per-qubit 2x2 assignment matrices.
        n_qubits: Number of qubits.

    Returns:
        Corrected probability distribution.
    """
    total_shots = sum(raw_counts.values())

    # Get observed bitstrings
    observed = sorted(raw_counts.keys())
    k = len(observed)

    # Build reduced assignment matrix (see explanation_physicist.md, Section 5.2)
    # A_reduced[i,j] = Product_{m} A_m[b_i[m], b_j[m]]
    A_reduced = np.zeros((k, k))
    for i, bs_i in enumerate(observed):
        for j, bs_j in enumerate(observed):
            product = 1.0
            for m in range(n_qubits):
                bit_i = int(bs_i[n_qubits - 1 - m])
                bit_j = int(bs_j[n_qubits - 1 - m])
                product *= per_qubit_matrices[m][bit_i, bit_j]
            A_reduced[i, j] = product

    # Build measured probability vector
    p_measured = np.array([raw_counts[bs] / total_shots for bs in observed])

    # Invert reduced matrix
    try:
        A_inv = np.linalg.inv(A_reduced)
        p_corrected = A_inv @ p_measured
    except np.linalg.LinAlgError:
        print("  Warning: Singular reduced matrix, using pseudoinverse")
        A_inv = np.linalg.pinv(A_reduced)
        p_corrected = A_inv @ p_measured

    # Clip and renormalize
    p_corrected = np.maximum(p_corrected, 0)
    if p_corrected.sum() > 0:
        p_corrected /= p_corrected.sum()

    result = {}
    for i, bs in enumerate(observed):
        if p_corrected[i] > 1e-10:
            result[bs] = p_corrected[i]

    return result


# =============================================================================
# TEST CIRCUITS
# =============================================================================

def build_ghz_circuit(n_qubits: int) -> QuantumCircuit:
    """
    Build GHZ state circuit.

    |GHZ> = (|00...0> + |11...1>) / sqrt(2)

    Ideal measurement: 50% |00...0> and 50% |11...1>

    Args:
        n_qubits: Number of qubits.

    Returns:
        GHZ state preparation + measurement circuit.
    """
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='GHZ')

    qc.h(qr[0])
    for i in range(1, n_qubits):
        qc.cx(qr[0], qr[i])

    qc.measure(qr, cr)
    return qc


def build_w_state_circuit(n_qubits: int) -> QuantumCircuit:
    """
    Build W state circuit (approximate for demonstration).

    |W> = (|100...0> + |010...0> + ... + |000...1>) / sqrt(n)

    Ideal measurement: uniform 1/n probability for each single-excitation state.

    Args:
        n_qubits: Number of qubits in W state.

    Returns:
        W state preparation + measurement circuit.
    """
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='W_state')

    # Prepare |W> via sequential rotations and CNOTs
    # First qubit: Ry(2*arccos(sqrt(1/n)))
    import math
    qc.ry(2 * math.acos(math.sqrt(1 / n_qubits)), qr[0])

    for i in range(1, n_qubits):
        remaining = n_qubits - i
        if remaining > 0:
            angle = 2 * math.acos(math.sqrt(1 / (remaining + 1)))
            qc.cry(angle, qr[i - 1], qr[i])
        qc.cx(qr[i], qr[i - 1])

    qc.measure(qr, cr)
    return qc


# =============================================================================
# ANALYSIS AND VISUALIZATION
# =============================================================================

def compute_tvd(p: Dict[str, float], q: Dict[str, float]) -> float:
    """
    Compute Total Variation Distance between two distributions.

    TVD(P, Q) = 0.5 * sum_x |P(x) - Q(x)|

    Args:
        p: First probability distribution.
        q: Second probability distribution.

    Returns:
        TVD between p and q.
    """
    all_keys = set(list(p.keys()) + list(q.keys()))
    tvd = 0.5 * sum(abs(p.get(k, 0) - q.get(k, 0)) for k in all_keys)
    return tvd


def plot_comparison(
    ideal: Dict[str, float],
    noisy: Dict[str, float],
    corrected: Dict[str, float],
    title: str = "Measurement Error Mitigation",
    save_path: Optional[str] = None
):
    """
    Plot ideal vs noisy vs corrected distributions.

    Args:
        ideal: Ideal probability distribution.
        noisy: Noisy (raw) probability distribution.
        corrected: Mitigated probability distribution.
        title: Plot title.
        save_path: Optional path to save figure.
    """
    all_keys = sorted(set(list(ideal.keys()) + list(noisy.keys()) + list(corrected.keys())))
    n = len(all_keys)

    x = np.arange(n)
    width = 0.25

    ideal_vals = [ideal.get(k, 0) for k in all_keys]
    noisy_vals = [noisy.get(k, 0) for k in all_keys]
    corrected_vals = [corrected.get(k, 0) for k in all_keys]

    fig, ax = plt.subplots(1, 1, figsize=(max(10, n * 0.8), 6))
    ax.bar(x - width, ideal_vals, width, label='Ideal', color='green', alpha=0.7)
    ax.bar(x, noisy_vals, width, label='Noisy (raw)', color='red', alpha=0.7)
    ax.bar(x + width, corrected_vals, width, label='Corrected', color='blue', alpha=0.7)

    ax.set_xlabel('Bitstring')
    ax.set_ylabel('Probability')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(all_keys, rotation=45 if n > 8 else 0)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"  Figure saved to {save_path}")
    plt.show()


# =============================================================================
# DEMONSTRATIONS
# =============================================================================

def demo_full_calibration():
    """
    Demonstrate full confusion matrix calibration and correction.

    This demo:
    1. Creates readout noise model
    2. Builds and runs calibration circuits
    3. Constructs the full confusion matrix
    4. Runs a test circuit (GHZ state) with noise
    5. Corrects the results using matrix inversion
    6. Compares raw vs corrected vs ideal
    """
    print("=" * 70)
    print("DEMO 1: Full Confusion Matrix Calibration (3 qubits)")
    print("=" * 70)

    n_qubits = 3
    shots = 10000
    p1g0, p0g1 = 0.03, 0.06

    print(f"\n  Readout error parameters:")
    print(f"    P(1|0) = {p1g0} (false positive)")
    print(f"    P(0|1) = {p0g1} (false negative / T1 relaxation)")

    # Create noise model
    noise_model = create_readout_noise_model(n_qubits, p1g0, p0g1)
    sim = AerSimulator(noise_model=noise_model)

    # Step 1: Build and run calibration circuits
    print(f"\n  Step 1: Building {2**n_qubits} calibration circuits...")
    cal_circuits = build_calibration_circuits(n_qubits)
    cal_counts = []
    for qc in cal_circuits:
        result = sim.run(qc, shots=shots).result()
        cal_counts.append(result.get_counts())

    # Step 2: Build confusion matrix
    print("  Step 2: Building confusion matrix...")
    A = build_confusion_matrix(cal_counts, n_qubits)
    print(f"\n  Confusion matrix A (8x8):")
    print(f"  Diagonal (correct readout probabilities):")
    for i in range(2**n_qubits):
        bs = format(i, f'0{n_qubits}b')
        print(f"    P(read {bs} | prep {bs}) = {A[i, i]:.4f}")

    # Step 3: Run test circuit (GHZ state)
    print(f"\n  Step 3: Running GHZ state circuit with readout noise...")
    ghz = build_ghz_circuit(n_qubits)
    result = sim.run(ghz, shots=shots).result()
    raw_counts = result.get_counts()

    # Ideal distribution
    ideal_dist = {'000': 0.5, '111': 0.5}

    # Raw distribution
    total = sum(raw_counts.values())
    raw_dist = {k: v / total for k, v in raw_counts.items()}

    print(f"\n  Ideal distribution: {ideal_dist}")
    print(f"  Raw (noisy) distribution:")
    for k, v in sorted(raw_dist.items()):
        print(f"    {k}: {v:.4f}")

    # Step 4: Correct via matrix inversion
    print(f"\n  Step 4: Correcting via matrix inversion...")
    corrected_dist = correct_matrix_inversion(raw_counts, A, n_qubits)
    print(f"  Corrected distribution:")
    for k, v in sorted(corrected_dist.items()):
        print(f"    {k}: {v:.4f}")

    # Step 5: Compare TVDs
    tvd_raw = compute_tvd(ideal_dist, raw_dist)
    tvd_corrected = compute_tvd(ideal_dist, corrected_dist)
    print(f"\n  Total Variation Distance:")
    print(f"    Raw -> Ideal:       {tvd_raw:.4f}")
    print(f"    Corrected -> Ideal: {tvd_corrected:.4f}")
    print(f"    Improvement factor: {tvd_raw / tvd_corrected:.2f}x" if tvd_corrected > 0 else "    Perfect correction!")

    return ideal_dist, raw_dist, corrected_dist


def demo_m3_correction():
    """
    Demonstrate M3-style (matrix-free) measurement mitigation.

    This demo:
    1. Per-qubit calibration (2n circuits instead of 2^n)
    2. Builds per-qubit assignment matrices
    3. Uses reduced matrix approach for correction
    4. Compares with full matrix inversion
    """
    print("\n" + "=" * 70)
    print("DEMO 2: M3 Matrix-Free Measurement Mitigation (4 qubits)")
    print("=" * 70)

    n_qubits = 4
    shots = 20000

    # Asymmetric per-qubit readout errors (realistic scenario)
    qubit_errors = [
        (0.02, 0.04),  # Qubit 0: low error
        (0.03, 0.07),  # Qubit 1: moderate error
        (0.01, 0.03),  # Qubit 2: very low error
        (0.04, 0.08),  # Qubit 3: higher error
    ]

    print(f"\n  Per-qubit readout error rates:")
    for i, (p1g0, p0g1) in enumerate(qubit_errors):
        print(f"    Qubit {i}: P(1|0) = {p1g0}, P(0|1) = {p0g1}")

    # Create noise model with per-qubit errors
    noise_model = create_asymmetric_readout_noise_model(qubit_errors)
    sim = AerSimulator(noise_model=noise_model)

    # Step 1: Per-qubit calibration
    print(f"\n  Step 1: Running {2 * n_qubits} per-qubit calibration circuits...")
    cal_circuits = build_per_qubit_calibration_circuits(n_qubits)
    cal_counts = []
    for qc in cal_circuits:
        result = sim.run(qc, shots=shots).result()
        cal_counts.append(result.get_counts())

    # Step 2: Build per-qubit matrices
    print("  Step 2: Building per-qubit assignment matrices...")
    per_qubit_A = build_per_qubit_matrices(cal_counts, n_qubits, shots)
    for i, A_q in enumerate(per_qubit_A):
        print(f"    Qubit {i}: A = [[{A_q[0,0]:.4f}, {A_q[0,1]:.4f}], [{A_q[1,0]:.4f}, {A_q[1,1]:.4f}]]")

    # Step 3: Run GHZ circuit with noise
    print(f"\n  Step 3: Running GHZ-4 circuit with readout noise...")
    ghz = build_ghz_circuit(n_qubits)
    result = sim.run(ghz, shots=shots).result()
    raw_counts = result.get_counts()

    ideal_dist = {'0000': 0.5, '1111': 0.5}
    total = sum(raw_counts.values())
    raw_dist = {k: v / total for k, v in raw_counts.items()}

    print(f"\n  Ideal: {ideal_dist}")
    print(f"  Raw measurement ({len(raw_dist)} distinct bitstrings observed):")
    for k, v in sorted(raw_dist.items(), key=lambda x: -x[1])[:10]:
        print(f"    {k}: {v:.4f}")
    if len(raw_dist) > 10:
        print(f"    ... and {len(raw_dist) - 10} more bitstrings")

    # Step 4: M3-style correction
    print(f"\n  Step 4: Applying M3 correction (reduced {len(raw_dist)}x{len(raw_dist)} matrix)...")
    corrected_dist = correct_m3_reduced(raw_counts, per_qubit_A, n_qubits)
    print(f"  Corrected distribution:")
    for k, v in sorted(corrected_dist.items(), key=lambda x: -x[1])[:10]:
        print(f"    {k}: {v:.4f}")

    # Compare
    tvd_raw = compute_tvd(ideal_dist, raw_dist)
    tvd_corrected = compute_tvd(ideal_dist, corrected_dist)
    print(f"\n  Total Variation Distance:")
    print(f"    Raw -> Ideal:       {tvd_raw:.4f}")
    print(f"    Corrected -> Ideal: {tvd_corrected:.4f}")
    improvement = tvd_raw / tvd_corrected if tvd_corrected > 0 else float('inf')
    print(f"    Improvement factor: {improvement:.2f}x")

    return ideal_dist, raw_dist, corrected_dist


def demo_least_squares():
    """
    Demonstrate least-squares correction method.

    Compares matrix inversion (which can produce negative values)
    with constrained least-squares (always non-negative).
    """
    print("\n" + "=" * 70)
    print("DEMO 3: Constrained Least-Squares Correction")
    print("=" * 70)

    n_qubits = 2
    shots = 5000

    # Higher noise to show difference between methods
    p1g0, p0g1 = 0.08, 0.12
    print(f"\n  Higher readout errors to stress-test methods:")
    print(f"    P(1|0) = {p1g0}, P(0|1) = {p0g1}")

    noise_model = create_readout_noise_model(n_qubits, p1g0, p0g1)
    sim = AerSimulator(noise_model=noise_model)

    # Calibrate
    cal_circuits = build_calibration_circuits(n_qubits)
    cal_counts = [sim.run(qc, shots=shots).result().get_counts() for qc in cal_circuits]
    A = build_confusion_matrix(cal_counts, n_qubits)

    # Prepare Bell state: |Phi+> = (|00> + |11>) / sqrt(2)
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr, name='Bell')
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.measure(qr, cr)

    result = sim.run(qc, shots=shots).result()
    raw_counts = result.get_counts()

    ideal_dist = {'00': 0.5, '11': 0.5}
    total = sum(raw_counts.values())
    raw_dist = {k: v / total for k, v in raw_counts.items()}

    # Matrix inversion
    corrected_inv = correct_matrix_inversion(raw_counts, A, n_qubits)

    # Least squares
    corrected_ls = correct_least_squares(raw_counts, A, n_qubits)

    print(f"\n  Results comparison:")
    print(f"  {'Bitstring':<12} {'Ideal':<10} {'Raw':<10} {'Inv.':<10} {'LS':<10}")
    print(f"  {'-'*52}")
    all_keys = sorted(set(list(ideal_dist.keys()) + list(raw_dist.keys())))
    for k in all_keys:
        print(f"  {k:<12} {ideal_dist.get(k, 0):<10.4f} {raw_dist.get(k, 0):<10.4f} "
              f"{corrected_inv.get(k, 0):<10.4f} {corrected_ls.get(k, 0):<10.4f}")

    tvd_raw = compute_tvd(ideal_dist, raw_dist)
    tvd_inv = compute_tvd(ideal_dist, corrected_inv)
    tvd_ls = compute_tvd(ideal_dist, corrected_ls)
    print(f"\n  TVD from ideal:")
    print(f"    Raw:              {tvd_raw:.4f}")
    print(f"    Matrix inversion: {tvd_inv:.4f}")
    print(f"    Least squares:    {tvd_ls:.4f}")


def demo_scaling_comparison():
    """
    Compare full vs M3 calibration cost for different qubit counts.
    """
    print("\n" + "=" * 70)
    print("DEMO 4: Calibration Scaling Comparison")
    print("=" * 70)

    print(f"\n  {'n_qubits':<12} {'Full cal. circuits':<22} {'Per-qubit circuits':<22} {'Speedup':<10}")
    print(f"  {'-'*65}")
    for n in range(1, 16):
        full = 2 ** n
        per_qubit = 2 * n
        speedup = full / per_qubit
        flag = " <-- intractable" if full > 10000 else ""
        print(f"  {n:<12} {full:<22} {per_qubit:<22} {speedup:<10.1f}{flag}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run all measurement error mitigation demonstrations.

    Covers:
    - Full confusion matrix calibration and inversion
    - M3 matrix-free mitigation with per-qubit calibration
    - Least-squares constrained correction
    - Scaling comparison of calibration methods
    """
    print("Measurement Error Mitigation (M3) - Local Demonstrations")
    print("=" * 70)
    print("See explanation_physicist.md for theoretical background.")
    print("See explanation_simple.md for intuitive explanation.")
    print()

    # Demo 1: Full calibration
    ideal1, raw1, corr1 = demo_full_calibration()

    # Demo 2: M3 correction
    ideal2, raw2, corr2 = demo_m3_correction()

    # Demo 3: Least-squares
    demo_least_squares()

    # Demo 4: Scaling
    demo_scaling_comparison()

    # Final visualization (Demo 1 results)
    print("\n" + "=" * 70)
    print("Generating comparison plot...")
    plot_comparison(ideal1, raw1, corr1,
                    title="GHZ-3 State: Measurement Error Mitigation")

    print("\nAll demonstrations complete.")


if __name__ == '__main__':
    main()
