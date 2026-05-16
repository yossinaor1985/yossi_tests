"""
Quantum Kernel Methods - IBM Production-Ready Implementation
==============================================================

Production quantum kernel workflow for IBM hardware with session
management, error mitigation, and result persistence.

Qiskit Version: 2.4.1

Production considerations:
    - Kernel matrix requires O(N^2) circuit evaluations
    - Sessions batch these efficiently on IBM backends
    - Shot budget: O(1/epsilon^2) per kernel entry for precision epsilon
    - Readout error mitigation improves kernel quality
    - Cache kernel matrices to avoid recomputation

NOT ACTUALLY DEPLOYED - uses AerSimulator for demonstration.
"""

import json
import os
from datetime import datetime

import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC

from qiskit.circuit.library import ZZFeatureMap
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_machine_learning.kernels import FidelityQuantumKernel

# =============================================================================
# IBM RUNTIME SETUP (uncomment for real hardware)
# =============================================================================
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session
#
# service = QiskitRuntimeService(channel="ibm_quantum")
#
# def get_backend(service, min_qubits=2):
#     """Select least busy backend with sufficient qubits."""
#     backends = service.backends(
#         filters=lambda b: (
#             b.configuration().n_qubits >= min_qubits
#             and b.status().operational
#             and not b.configuration().simulator
#         )
#     )
#     return min(backends, key=lambda b: b.status().pending_jobs)


# =============================================================================
# CONFIGURATION
# =============================================================================

RESULTS_DIR = "quantum/algorithms/10_quantum_kernels/production_results"
NUM_QUBITS = 2
FEATURE_MAP_REPS = 1      # Shallow for hardware
SHOTS = 8192               # Higher shots for kernel precision
SVM_C = 1.0                # SVM regularization
RANDOM_SEED = 42


# =============================================================================
# DATA PREPARATION
# =============================================================================

def prepare_data(n_samples=100):
    """Prepare dataset with production preprocessing."""
    X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=RANDOM_SEED)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y
    )
    print(f"Dataset: {len(X_train)} train / {len(X_test)} test")
    return X_train, X_test, y_train, y_test, scaler


# =============================================================================
# KERNEL COMPUTATION WITH CACHING
# =============================================================================

def compute_or_load_kernel(kernel, X_train, X_test, cache_dir):
    """
    Compute kernel matrices or load from cache.

    Kernel computation is the bottleneck:
        N_train=70 -> 70*71/2 = 2485 circuits for training kernel
        N_test=30 -> 30*70 = 2100 circuits for test kernel

    Caching avoids recomputation when tuning SVM hyperparameters.
    """
    os.makedirs(cache_dir, exist_ok=True)
    train_cache = os.path.join(cache_dir, "K_train.npy")
    test_cache = os.path.join(cache_dir, "K_test.npy")

    if os.path.exists(train_cache) and os.path.exists(test_cache):
        print("  Loading cached kernel matrices...")
        K_train = np.load(train_cache)
        K_test = np.load(test_cache)
    else:
        print(f"  Computing training kernel ({len(X_train)}x{len(X_train)})...")
        K_train = kernel.evaluate(X_train)
        print(f"  Computing test kernel ({len(X_test)}x{len(X_train)})...")
        K_test = kernel.evaluate(X_test, X_train)

        np.save(train_cache, K_train)
        np.save(test_cache, K_test)
        print(f"  Kernel matrices cached to {cache_dir}")

    return K_train, K_test


# =============================================================================
# SVM HYPERPARAMETER TUNING
# =============================================================================

def tune_svm(K_train, y_train):
    """
    Tune SVM regularization parameter C using cross-validation.

    Since kernel computation is expensive, we tune only the classical
    SVM hyperparameters (C) while keeping the quantum kernel fixed.

    For quantum kernel alignment (QKA), see explanation_physicist.md Section 6.
    """
    print(f"\n  Tuning SVM C parameter via 5-fold cross-validation...")
    C_values = [0.1, 0.5, 1.0, 5.0, 10.0]
    best_c, best_score = None, 0

    for C in C_values:
        svc = SVC(kernel='precomputed', C=C)
        scores = cross_val_score(svc, K_train, y_train, cv=5, scoring='accuracy')
        mean_score = scores.mean()
        print(f"    C={C:5.1f}: accuracy = {mean_score:.4f} (+/- {scores.std():.4f})")

        if mean_score > best_score:
            best_score = mean_score
            best_c = C

    print(f"  Best C: {best_c} (CV accuracy: {best_score:.4f})")
    return best_c


# =============================================================================
# PRODUCTION PIPELINE
# =============================================================================

def run_production():
    print("=" * 70)
    print("Quantum Kernel Methods - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Step 1: Data
    print(f"\n--- Step 1: Data Preparation ---")
    X_train, X_test, y_train, y_test, scaler = prepare_data(n_samples=100)

    # Step 2: Feature map
    print(f"\n--- Step 2: Feature Map ---")
    feature_map = ZZFeatureMap(
        feature_dimension=NUM_QUBITS,
        reps=FEATURE_MAP_REPS,
    )
    print(f"  ZZFeatureMap: {NUM_QUBITS} qubits, reps={FEATURE_MAP_REPS}")
    print(f"  Circuit depth: {feature_map.depth()}")

    # Step 3: Transpilation (for real hardware)
    print(f"\n--- Step 3: Transpilation ---")
    # For real hardware:
    # backend = get_backend(service, min_qubits=NUM_QUBITS)
    # pm = generate_preset_pass_manager(optimization_level=2, backend=backend)
    # transpiled_fm = pm.run(feature_map)
    # print(f"  Transpiled depth: {transpiled_fm.depth()}")
    print("  Using AerSimulator (no transpilation needed)")

    # Step 4: Kernel computation
    print(f"\n--- Step 4: Kernel Computation ---")

    # For real hardware with session:
    # with Session(service=service, backend=backend) as session:
    #     sampler = SamplerV2(session=session)
    #     sampler.options.default_shots = SHOTS
    #     kernel = FidelityQuantumKernel(feature_map=feature_map)
    #     K_train, K_test = compute_or_load_kernel(kernel, X_train, X_test, RESULTS_DIR)

    kernel = FidelityQuantumKernel(feature_map=feature_map)
    K_train, K_test = compute_or_load_kernel(kernel, X_train, X_test, RESULTS_DIR)

    # Kernel quality check
    eigenvalues = np.linalg.eigvalsh(K_train)
    print(f"\n  Kernel quality check:")
    print(f"    Symmetric: {np.allclose(K_train, K_train.T)}")
    print(f"    PSD (min eigenvalue): {eigenvalues.min():.6f}")
    print(f"    Rank: {np.sum(eigenvalues > 1e-10)}/{len(eigenvalues)}")

    # Step 5: SVM tuning
    print(f"\n--- Step 5: SVM Hyperparameter Tuning ---")
    best_c = tune_svm(K_train, y_train)

    # Step 6: Final evaluation
    print(f"\n--- Step 6: Evaluation ---")
    svc = SVC(kernel='precomputed', C=best_c)
    svc.fit(K_train, y_train)

    y_pred_train = svc.predict(K_train)
    y_pred_test = svc.predict(K_test)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    print(f"  Train accuracy: {train_acc:.4f}")
    print(f"  Test accuracy:  {test_acc:.4f}")
    print(f"  Support vectors: {svc.n_support_}")
    print(f"\n{classification_report(y_test, y_pred_test, target_names=['Class 0', 'Class 1'])}")

    # Step 7: Save results
    print(f"--- Step 7: Save Results ---")
    results = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "num_qubits": NUM_QUBITS,
            "feature_map_reps": FEATURE_MAP_REPS,
            "shots": SHOTS,
            "svm_C": best_c,
        },
        "metrics": {
            "train_accuracy": float(train_acc),
            "test_accuracy": float(test_acc),
            "n_support_vectors": int(sum(svc.n_support_)),
            "kernel_rank": int(np.sum(eigenvalues > 1e-10)),
        },
    }

    os.makedirs(RESULTS_DIR, exist_ok=True)
    results_path = os.path.join(RESULTS_DIR, "results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to {results_path}")

    # Summary
    print(f"\n{'='*70}")
    print("PRODUCTION SUMMARY")
    print(f"{'='*70}")
    print(f"""
    Quantum Kernel SVM:
        Feature map: ZZFeatureMap ({NUM_QUBITS} qubits, reps={FEATURE_MAP_REPS})
        SVM C: {best_c}
        Test accuracy: {test_acc:.4f}
        Support vectors: {sum(svc.n_support_)}

    Production notes:
        - Kernel caching avoids recomputation (~4500 circuits for N=100)
        - For real hardware: use Session for batched execution
        - Enable readout error mitigation for better kernel quality
        - Higher shots (8192+) improve kernel precision
        - SVM hyperparameters are cheap to tune after kernel is computed
        - For larger datasets (N>500), consider QSVC with projected kernels
    """)


if __name__ == "__main__":
    run_production()