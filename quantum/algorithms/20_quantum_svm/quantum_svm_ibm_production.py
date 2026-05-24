"""
Quantum SVM (Rebentrost-Mohseni-Lloyd) - IBM Production-Ready Implementation
==============================================================================

Production pipeline for the Quantum SVM algorithm:
    1. Dataset creation and train/test split
    2. Classical baselines (sklearn SVC linear + RBF)
    3. Quantum kernel computation via swap test with shots (AerSimulator)
    4. Dual system solve (classical, standing in for HHL)
    5. Quantum kernel classification
    6. Results comparison and JSON export

This implements the quantum kernel portion of the QSVM-RML pipeline on
a shot-based simulator. The HHL portion is solved classically because:
    (a) HHL on a 40x40 system requires thousands of qubits
    (b) QRAM is not physically available
    (c) The quantum kernel itself is the demonstrable quantum component

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

References:
    - Rebentrost, Mohseni, Lloyd (2014). PRL 113, 130503
    - HHL algorithm: see Topic 19
"""

import json
import os
from datetime import datetime

import numpy as np
import matplotlib
matplotlib.use("Agg")

from sklearn.datasets import make_blobs
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# =============================================================================
# IBM RUNTIME (uncomment for real hardware deployment)
# =============================================================================
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session
# service = QiskitRuntimeService(channel="ibm_quantum")
# backend = service.least_busy(min_num_qubits=3, operational=True)


# =============================================================================
# CONFIGURATION
# =============================================================================

RESULTS_DIR = "quantum/algorithms/20_quantum_svm/production_results"
SHOTS = 8192
RANDOM_SEED = 42


# =============================================================================
# DATASET
# =============================================================================

def create_problem(n_samples=40):
    """
    Generate a binary classification problem for QSVM demonstration.

    Creates a 2D blob dataset, converts labels to {-1, +1},
    scales features to [0, pi], and splits into train/test.

    Parameters
    ----------
    n_samples : int
        Total number of samples (split 70/30 train/test).

    Returns
    -------
    X_train : ndarray, shape (n_train, 2)
        Training features scaled to [0, pi].
    X_test : ndarray, shape (n_test, 2)
        Test features scaled to [0, pi].
    y_train : ndarray, shape (n_train,)
        Training labels in {-1, +1}.
    y_test : ndarray, shape (n_test,)
        Test labels in {-1, +1}.
    """
    X, y = make_blobs(
        n_samples=n_samples,
        centers=[[1.0, 1.0], [3.0, 3.0]],
        cluster_std=0.8,
        random_state=RANDOM_SEED
    )
    y[y == 0] = -1  # Convert {0, 1} -> {-1, +1}

    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y
    )

    print(f"  Dataset: {n_samples} samples, 2 features")
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"  Class balance (train): +1={np.sum(y_train == 1)}, -1={np.sum(y_train == -1)}")

    return X_train, X_test, y_train, y_test


# =============================================================================
# CLASSICAL BASELINES
# =============================================================================

def solve_classically(X_train, y_train, X_test):
    """
    Compute classical SVM baselines using sklearn.

    Trains both a linear and RBF kernel SVC for comparison
    with the quantum kernel approach.

    Parameters
    ----------
    X_train : ndarray, shape (n_train, 2)
        Training features.
    y_train : ndarray, shape (n_train,)
        Training labels.
    X_test : ndarray, shape (n_test, 2)
        Test features.

    Returns
    -------
    results : dict
        Dictionary with predictions and accuracies for both kernels.
    """
    results = {}

    # Linear SVC
    svc_lin = SVC(kernel="linear", C=1.0, random_state=RANDOM_SEED)
    svc_lin.fit(X_train, y_train)
    y_pred_lin = svc_lin.predict(X_test)
    results["linear_predictions"] = y_pred_lin
    results["linear_accuracy"] = float(accuracy_score(y_train, svc_lin.predict(X_train)))
    results["linear_test_accuracy"] = float(accuracy_score(X_test[:, 0] * 0 + 1, y_pred_lin * 0 + 1))  # placeholder
    results["linear_n_sv"] = int(np.sum(svc_lin.n_support_))

    # RBF SVC
    svc_rbf = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=RANDOM_SEED)
    svc_rbf.fit(X_train, y_train)
    y_pred_rbf = svc_rbf.predict(X_test)
    results["rbf_predictions"] = y_pred_rbf
    results["rbf_accuracy"] = float(accuracy_score(y_train, svc_rbf.predict(X_train)))
    results["rbf_n_sv"] = int(np.sum(svc_rbf.n_support_))

    return results, y_pred_lin, y_pred_rbf


# =============================================================================
# QUANTUM KERNEL VIA SWAP TEST (SHOT-BASED)
# =============================================================================

def build_swap_test_circuit(x_i, x_j):
    """
    Build a swap test circuit with measurement for shot-based execution.

    Circuit:
        ancilla: |0> --[H]--[ctrl]--[H]--[M]
        state_i: |0> --[Ry]--[SWAP]-------
        state_j: |0> --[Ry]--[SWAP]-------

    Measurement result on ancilla:
        P(0) = (1 + |<x_i|x_j>|^2) / 2
        K(x_i, x_j) = 2*P(0) - 1

    Parameters
    ----------
    x_i : array-like, shape (2,)
        First data point.
    x_j : array-like, shape (2,)
        Second data point.

    Returns
    -------
    qc : QuantumCircuit
        3-qubit swap test circuit with measurement on ancilla.
    """
    ancilla = QuantumRegister(1, "anc")
    state_i = QuantumRegister(1, "si")
    state_j = QuantumRegister(1, "sj")

    qc = QuantumCircuit(ancilla, state_i, state_j)

    # Amplitude encode: Ry(2*arccos(x0/||x||))
    norm_i = np.linalg.norm(x_i)
    norm_j = np.linalg.norm(x_j)

    if norm_i > 1e-10:
        theta_i = 2.0 * np.arccos(np.clip(x_i[0] / norm_i, -1.0, 1.0))
        qc.ry(theta_i, state_i[0])
    if norm_j > 1e-10:
        theta_j = 2.0 * np.arccos(np.clip(x_j[0] / norm_j, -1.0, 1.0))
        qc.ry(theta_j, state_j[0])

    # Swap test protocol
    qc.h(ancilla[0])
    qc.cswap(ancilla[0], state_i[0], state_j[0])
    qc.h(ancilla[0])

    # Measure ancilla only
    qc.measure_all()

    return qc


def compute_quantum_kernel_shots(X, shots=SHOTS):
    """
    Compute the quantum kernel matrix using shot-based swap test simulation.

    For each pair (i, j), runs the swap test circuit with `shots` shots
    on the AerSimulator and extracts K_ij from the measurement statistics.

    Parameters
    ----------
    X : ndarray, shape (N, 2)
        Data matrix.
    shots : int
        Number of shots per swap test.

    Returns
    -------
    K : ndarray, shape (N, N)
        Shot-based quantum kernel matrix.
    total_circuits : int
        Total number of circuits executed.
    post_selection_rates : list of float
        Post-selection success rates for each pair.
    """
    N = len(X)
    K = np.zeros((N, N))
    total_circuits = 0
    post_selection_rates = []

    sim = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=sim)

    for i in range(N):
        K[i, i] = 1.0
        for j in range(i + 1, N):
            qc = build_swap_test_circuit(X[i], X[j])
            qc_t = pm.run(qc)

            result = sim.run(qc_t, shots=shots).result()
            counts = result.get_counts()

            # Extract P(ancilla=0) from counts
            # In measure_all(), the bit string is in the order of qubit registers.
            # Ancilla is qubit 0, so ancilla=0 means the rightmost bit is '0'
            # in Qiskit's little-endian convention.
            p0_count = 0
            total_count = 0
            for bitstring, count in counts.items():
                # Remove spaces if present
                bits = bitstring.replace(" ", "")
                # Ancilla is the last character (little-endian, qubit 0)
                if bits[-1] == "0":
                    p0_count += count
                total_count += count

            p0 = p0_count / total_count
            k_val = 2.0 * p0 - 1.0

            # Clamp to valid kernel range [0, 1]
            k_val = np.clip(k_val, 0.0, 1.0)

            K[i, j] = k_val
            K[j, i] = k_val

            post_selection_rates.append(p0)
            total_circuits += 1

    return K, total_circuits, post_selection_rates


# =============================================================================
# DUAL SYSTEM SOLVER (CLASSICAL STAND-IN FOR HHL)
# =============================================================================

def solve_dual(K, y_labels, lam=0.1):
    """
    Solve the LS-SVM dual system: (K + lambda * I) alpha = y.

    Classical implementation standing in for the HHL quantum solver.
    In production QSVM-RML, HHL would solve this in O(log(N) * kappa^2).

    Parameters
    ----------
    K : ndarray, shape (N, N)
        Kernel matrix.
    y_labels : ndarray, shape (N,)
        Training labels in {-1, +1}.
    lam : float
        Regularization parameter.

    Returns
    -------
    alpha : ndarray, shape (N,)
        Dual coefficients.
    condition_number : float
        Condition number of the system matrix A = K + lambda * I.
    """
    N = len(y_labels)
    A = K + lam * np.eye(N)
    condition_number = float(np.linalg.cond(A))

    alpha = np.linalg.solve(A, y_labels.astype(float))

    return alpha, condition_number


# =============================================================================
# CLASSIFICATION
# =============================================================================

def classify(X_train, X_test, y_train, alpha, shots=SHOTS):
    """
    Classify test points using the quantum kernel SVM decision function.

    f(x) = sign( sum_i alpha_i * y_i * K(x_i, x) + b )

    Uses shot-based swap test for kernel values between test and train points.

    Parameters
    ----------
    X_train : ndarray, shape (N_train, 2)
        Training data.
    X_test : ndarray, shape (N_test, 2)
        Test data.
    y_train : ndarray, shape (N_train,)
        Training labels.
    alpha : ndarray, shape (N_train,)
        Dual coefficients.
    shots : int
        Shots per swap test.

    Returns
    -------
    predictions : ndarray, shape (N_test,)
        Predicted labels in {-1, +1}.
    K_test_train : ndarray, shape (N_test, N_train)
        Kernel matrix between test and training points.
    """
    N_train = len(X_train)
    N_test = len(X_test)

    sim = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=sim)

    # Compute kernel between test and train points
    K_test_train = np.zeros((N_test, N_train))

    for t in range(N_test):
        for i in range(N_train):
            qc = build_swap_test_circuit(X_test[t], X_train[i])
            qc_t = pm.run(qc)
            result = sim.run(qc_t, shots=shots).result()
            counts = result.get_counts()

            p0_count = 0
            total_count = 0
            for bitstring, count in counts.items():
                bits = bitstring.replace(" ", "")
                if bits[-1] == "0":
                    p0_count += count
                total_count += count

            p0 = p0_count / total_count
            K_test_train[t, i] = np.clip(2.0 * p0 - 1.0, 0.0, 1.0)

    # Compute bias
    K_train, _, _ = compute_quantum_kernel_shots(X_train, shots=shots // 4)
    b = np.mean(y_train - K_train @ (alpha * y_train))

    # Decision function
    decision_values = K_test_train @ (alpha * y_train) + b
    predictions = np.sign(decision_values)
    predictions[predictions == 0] = 1

    return predictions, K_test_train


# =============================================================================
# PRODUCTION PIPELINE
# =============================================================================

def run_production():
    """
    Execute the full QSVM production pipeline.

    Steps:
        1. Create problem (dataset, train/test split)
        2. Compute classical baselines (sklearn SVC)
        3. Compute quantum kernel matrix (swap test with shots)
        4. Solve the dual system (classical, HHL stand-in)
        5. Classify test points using quantum kernel
        6. Compare all methods
        7. Save results to JSON
        8. Print production notes
    """
    print("=" * 70)
    print("QUANTUM SVM (Rebentrost-Mohseni-Lloyd) - Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Shots: {SHOTS}")
    print(f"Backend: AerSimulator (production would use IBM hardware)")
    print()

    # --- Step 1: Create problem ---
    print("[1/7] Creating problem...")
    X_train, X_test, y_train, y_test = create_problem(n_samples=40)
    print()

    # --- Step 2: Classical baselines ---
    print("[2/7] Computing classical baselines...")
    classical_results, y_pred_lin, y_pred_rbf = solve_classically(
        X_train, y_train, X_test
    )
    acc_linear = accuracy_score(y_test, y_pred_lin)
    acc_rbf = accuracy_score(y_test, y_pred_rbf)
    print(f"  Linear SVC accuracy: {acc_linear:.4f}")
    print(f"  RBF SVC accuracy:    {acc_rbf:.4f}")
    print()

    # --- Step 3: Quantum kernel computation ---
    print("[3/7] Computing quantum kernel matrix (swap test, {0} shots)...".format(SHOTS))
    K_quantum, n_circuits, ps_rates = compute_quantum_kernel_shots(X_train, shots=SHOTS)
    mean_ps_rate = float(np.mean(ps_rates)) if ps_rates else 0.0
    print(f"  Kernel matrix size: {K_quantum.shape}")
    print(f"  Circuits executed: {n_circuits}")
    print(f"  Mean P(ancilla=0): {mean_ps_rate:.4f}")
    print(f"  Kernel range: [{K_quantum.min():.4f}, {K_quantum.max():.4f}]")
    print()

    # --- Step 4: Solve dual system ---
    print("[4/7] Solving LS-SVM dual system (classical, HHL stand-in)...")
    lam = 0.1
    alpha, cond_num = solve_dual(K_quantum, y_train, lam=lam)
    sv_threshold = 0.01 * np.max(np.abs(alpha))
    n_sv = int(np.sum(np.abs(alpha) > sv_threshold))
    print(f"  Regularization lambda: {lam}")
    print(f"  Condition number: {cond_num:.2f}")
    print(f"  Alpha range: [{alpha.min():.4f}, {alpha.max():.4f}]")
    print(f"  Support vectors: {n_sv} / {len(y_train)}")
    print()

    # --- Step 5: Classify test points ---
    print("[5/7] Classifying test points with quantum kernel SVM...")
    y_pred_qsvm, K_test_train = classify(
        X_train, X_test, y_train, alpha, shots=SHOTS
    )
    acc_qsvm = accuracy_score(y_test, y_pred_qsvm)
    print(f"  QSVM accuracy: {acc_qsvm:.4f}")
    print()

    # --- Step 6: Compare methods ---
    print("[6/7] Results comparison:")
    print("-" * 55)
    print(f"  {'Method':<30} {'Accuracy':>10} {'Correct':>12}")
    print("  " + "-" * 53)
    print(f"  {'QSVM (swap test + LS-SVM)':<30} {acc_qsvm:>10.4f} "
          f"{int(acc_qsvm * len(y_test)):>8}/{len(y_test)}")
    print(f"  {'sklearn SVC (linear)':<30} {acc_linear:>10.4f} "
          f"{int(acc_linear * len(y_test)):>8}/{len(y_test)}")
    print(f"  {'sklearn SVC (RBF)':<30} {acc_rbf:>10.4f} "
          f"{int(acc_rbf * len(y_test)):>8}/{len(y_test)}")
    print("-" * 55)
    print()

    # --- Step 7: Save results ---
    print("[7/7] Saving results...")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    results = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "Quantum SVM (Rebentrost-Mohseni-Lloyd)",
        "qiskit_version": "2.4.1",
        "config": {
            "shots": SHOTS,
            "backend": "AerSimulator",
            "regularization_lambda": lam,
            "random_seed": RANDOM_SEED,
            "n_qubits_per_swap_test": 3,
            "encoding": "amplitude (Ry rotation)"
        },
        "dataset_info": {
            "n_samples": 40,
            "n_features": 2,
            "n_train": int(len(X_train)),
            "n_test": int(len(X_test)),
            "class_balance_train": {
                "+1": int(np.sum(y_train == 1)),
                "-1": int(np.sum(y_train == -1))
            },
            "feature_range": "[0, pi]"
        },
        "classical_results": {
            "linear_svc_accuracy": float(acc_linear),
            "linear_svc_n_support_vectors": classical_results["linear_n_sv"],
            "rbf_svc_accuracy": float(acc_rbf),
            "rbf_svc_n_support_vectors": classical_results["rbf_n_sv"]
        },
        "quantum_results": {
            "qsvm_accuracy": float(acc_qsvm),
            "n_support_vectors": n_sv,
            "condition_number": float(cond_num),
            "n_swap_test_circuits": n_circuits,
            "mean_post_selection_rate": float(mean_ps_rate),
            "kernel_matrix_range": {
                "min": float(K_quantum.min()),
                "max": float(K_quantum.max()),
                "mean_off_diagonal": float(
                    np.mean(K_quantum[np.triu_indices(len(K_quantum), k=1)])
                )
            },
            "alpha_range": {
                "min": float(alpha.min()),
                "max": float(alpha.max()),
                "mean_abs": float(np.mean(np.abs(alpha)))
            }
        },
        "comparison": {
            "qsvm_vs_linear": f"{'+' if acc_qsvm >= acc_linear else '-'}"
                              f"{abs(acc_qsvm - acc_linear):.4f}",
            "qsvm_vs_rbf": f"{'+' if acc_qsvm >= acc_rbf else '-'}"
                           f"{abs(acc_qsvm - acc_rbf):.4f}",
            "note": ("QSVM uses quantum kernel (swap test) + classical dual solver. "
                     "Full QSVM-RML would use HHL for dual solve and QRAM for data loading.")
        }
    }

    json_path = os.path.join(RESULTS_DIR, "qsvm_results.json")
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to: {json_path}")
    print()

    # --- Production Notes ---
    print("=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print("""
    1. WHAT WAS DEMONSTRATED:
       - Quantum kernel computation via swap test (shot-based, AerSimulator)
       - LS-SVM dual system solved classically (numpy, standing in for HHL)
       - Full classification pipeline with quantum kernel values

    2. WHAT FULL QSVM-RML REQUIRES (NOT YET AVAILABLE):
       - QRAM: O(log(Nd)) data loading (no physical implementation exists)
       - Fault-tolerant HHL: O(log(N) * kappa^2) dual system solver
       - Quantum classification: swap test with weight state |alpha>

    3. NEAR-TERM RECOMMENDATION:
       - For practical quantum kernel methods, use QSVC (Topic 11)
       - QSVC uses parameterized feature maps (ZZFeatureMap) which provide
         richer kernel expressivity on NISQ hardware
       - QSVC does not require QRAM or fault tolerance

    4. LIMITATIONS OF FULL QSVM-RML:
       - Tang (2019) dequantization: classical algorithms can match speedup
         for low-rank data matrices, which covers most practical datasets
       - QRAM hardware: even theoretical proposals (bucket-brigade) require
         O(Nd) physical qubits with error correction
       - Input/output problem: loading classical data and reading quantum
         results can negate the exponential speedup

    5. WHEN TO USE WHAT:
       - Small-medium datasets (< 10K points): classical SVM (sklearn)
       - Exploring quantum kernels on real hardware: QSVC (Topic 11)
       - Theoretical complexity analysis: QSVM-RML (this topic)
       - Full quantum advantage: wait for QRAM + fault tolerance
    """)

    return results


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    results = run_production()
    print("Production pipeline completed successfully.")
