"""
Quantum Support Vector Classifier (QSVC) - Local Simulator Implementation
===========================================================================

This script demonstrates the QSVC algorithm, which uses a quantum kernel
with a classical SVM for binary classification.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
QSVC workflow:
    1. Encode data x -> |phi(x)> = U_phi(x)|0>^n   (quantum feature map)
    2. Compute kernel: K(x_i,x_j) = |<phi(x_i)|phi(x_j)>|^2  (fidelity)
    3. Build N x N kernel matrix K
    4. Solve classical SVM dual:
        max sum_i alpha_i - (1/2) sum_{ij} alpha_i alpha_j y_i y_j K_ij
    5. Classify: f(x) = sign(sum_{s in SV} alpha_s y_s K(x_s, x) + b)

Key difference from VQC (Topic 12):
    - QSVC: no trainable quantum parameters, quantum used only for kernel
    - VQC: trainable variational circuit, end-to-end optimization
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

from qiskit.circuit.library import ZFeatureMap, ZZFeatureMap
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_machine_learning.kernels import FidelityQuantumKernel
from qiskit_machine_learning.algorithms import QSVC


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_dataset(n_samples=100, dataset_type="moons"):
    """
    Create synthetic dataset scaled to [0, pi] for quantum encoding.

    The ZZFeatureMap encoding uses exp(i x_k Z_k) and exp(i (pi-x_i)(pi-x_j) Z_i Z_j),
    so features in [0, pi] span the full encoding range.
    """
    if dataset_type == "moons":
        X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=42)
    else:
        X, y = make_circles(n_samples=n_samples, noise=0.1, factor=0.5, random_state=42)

    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


# =============================================================================
# PART A: QSVC with ZZFeatureMap
# =============================================================================

def demo_qsvc():
    """
    Demonstrate the full QSVC pipeline.

    The QSVC class in qiskit_machine_learning wraps:
        1. FidelityQuantumKernel (computes K(x_i, x_j))
        2. sklearn.svm.SVC (solves the dual QP)

    This is the most practical near-term QML algorithm because:
        - No variational optimization (no barren plateaus)
        - Well-understood classical theory (SVM generalization bounds)
        - Quantum computer used only for kernel computation

    See explanation_physicist.md, Section 5 for the full algorithm.
    """
    print("\n" + "=" * 70)
    print("PART A: QSVC Classification Pipeline")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_dataset(n_samples=80, dataset_type="moons")
    num_qubits = 2

    print(f"Dataset: make_moons, {len(X_train)} train / {len(X_test)} test")

    # --- Step 1: Feature Map ---
    # ZZFeatureMap with pairwise entanglement (Section 4.2)
    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=2)

    print(f"\nStep 1: Feature Map")
    print(f"  ZZFeatureMap: {num_qubits} qubits, reps=2")
    print(f"  Encoding: exp(i x_k Z_k) * exp(i (pi-x_i)(pi-x_j) Z_i Z_j)")
    print(f"  Circuit depth: {feature_map.depth()}")
    print(f"\n{feature_map.draw(output='text', fold=80)}")

    # --- Step 2: Quantum Kernel ---
    # FidelityQuantumKernel computes K(x_i, x_j) = |<0|U(x_i)^dag U(x_j)|0>|^2
    # using the compute-uncompute method (Section 3.4)
    kernel = FidelityQuantumKernel(feature_map=feature_map)

    print(f"\nStep 2: Quantum Kernel (FidelityQuantumKernel)")
    print(f"  Method: compute-uncompute (no ancilla qubits)")
    print(f"  K(x_i,x_j) = P(00...0) from circuit U(x_i)^dag U(x_j)")

    # --- Step 3: QSVC Training ---
    # QSVC combines quantum kernel + classical SVM
    # The SVM dual (Section 2.2):
    #   max sum_i alpha_i - (1/2) sum_{ij} alpha_i alpha_j y_i y_j K_ij
    #   s.t. 0 <= alpha_i <= C, sum_i alpha_i y_i = 0
    qsvc = QSVC(quantum_kernel=kernel)

    print(f"\nStep 3: Training QSVC...")
    print(f"  Computing kernel matrix ({len(X_train)}x{len(X_train)}) + SVM optimization")
    qsvc.fit(X_train, y_train)

    # --- Step 4: Prediction ---
    # For each test point, compute K(x_test, x_s) for support vectors
    # Then: f(x) = sign(sum_{s in SV} alpha_s y_s K(x_s, x) + b)
    print(f"\nStep 4: Prediction")
    y_pred_train = qsvc.predict(X_train)
    y_pred_test = qsvc.predict(X_test)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    print(f"  Train accuracy: {train_acc:.4f}")
    print(f"  Test accuracy:  {test_acc:.4f}")

    return qsvc, X_train, X_test, y_train, y_test, test_acc


# =============================================================================
# PART B: Feature Map Comparison
# =============================================================================

def demo_feature_map_comparison():
    """
    Compare ZFeatureMap vs ZZFeatureMap for QSVC.

    From explanation_physicist.md, Section 4:
        ZFeatureMap:  no entanglement, product kernel
            K_Z(x,y) = prod_k cos^2(x_k - y_k)
            -> separable, no quantum advantage

        ZZFeatureMap: entangled, non-separable kernel
            ZZ term: exp(i(pi-x_i)(pi-x_j) Z_i Z_j)
            -> captures pairwise correlations
            -> potentially classically intractable for high reps
    """
    print("\n" + "=" * 70)
    print("PART B: Feature Map Comparison for QSVC")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_dataset(n_samples=80, dataset_type="moons")
    num_qubits = 2

    feature_maps = {
        "ZFeatureMap (reps=1)": ZFeatureMap(feature_dimension=num_qubits, reps=1),
        "ZFeatureMap (reps=2)": ZFeatureMap(feature_dimension=num_qubits, reps=2),
        "ZZFeatureMap (reps=1)": ZZFeatureMap(feature_dimension=num_qubits, reps=1),
        "ZZFeatureMap (reps=2)": ZZFeatureMap(feature_dimension=num_qubits, reps=2),
    }

    results = {}
    for name, fm in feature_maps.items():
        kernel = FidelityQuantumKernel(feature_map=fm)
        qsvc = QSVC(quantum_kernel=kernel)
        qsvc.fit(X_train, y_train)
        acc = accuracy_score(y_test, qsvc.predict(X_test))
        results[name] = acc
        print(f"  {name:30s}: accuracy = {acc:.4f}")

    print(f"\n  ZZFeatureMap with entanglement generally outperforms ZFeatureMap")
    print(f"  because entanglement enables non-separable feature correlations.")

    return results


# =============================================================================
# PART C: Classical SVM Comparison
# =============================================================================

def demo_classical_comparison(X_train, X_test, y_train, y_test, quantum_acc):
    """
    Compare QSVC with classical SVM kernels.

    From explanation_physicist.md, Section 6:
        - Quantum advantage requires: K_Q is classically hard AND relevant to data
        - For most real datasets: classical RBF is competitive or better
        - Quantum advantage proven for cryptographic distributions (Havlicek 2019)
        - Practical advantage metric: geometric difference g(K_C, K_Q)
          (Huang et al., 2021): if g >> 1, quantum wins
    """
    print("\n" + "=" * 70)
    print("PART C: QSVC vs Classical SVM")
    print("=" * 70)

    classifiers = {
        "SVM (Linear)": SVC(kernel='linear', C=1.0),
        "SVM (RBF, gamma=auto)": SVC(kernel='rbf', gamma='auto', C=1.0),
        "SVM (Poly, d=3)": SVC(kernel='poly', degree=3, C=1.0),
    }

    results = {"QSVC (ZZFeatureMap)": quantum_acc}
    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        acc = accuracy_score(y_test, clf.predict(X_test))
        results[name] = acc
        print(f"  {name:25s}: accuracy = {acc:.4f}")

    print(f"  {'QSVC (ZZFeatureMap)':25s}: accuracy = {quantum_acc:.4f}")

    return results


# =============================================================================
# PART D: Kernel Matrix Analysis
# =============================================================================

def demo_kernel_analysis():
    """
    Analyze the quantum kernel matrix structure.

    Key properties (explanation_physicist.md, Section 4.1):
        - K(x,x) = 1 (self-similarity is maximal)
        - K is symmetric: K(x,y) = K(y,x)
        - K is PSD (positive semi-definite) by Mercer's theorem
        - Eigenspectrum reveals effective dimensionality

    For a good kernel, same-class pairs should have high K values
    and different-class pairs should have low K values.
    """
    print("\n" + "=" * 70)
    print("PART D: Kernel Matrix Analysis")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_dataset(n_samples=60, dataset_type="moons")
    num_qubits = 2

    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=2)
    kernel = FidelityQuantumKernel(feature_map=feature_map)

    print(f"  Computing kernel matrix ({len(X_train)}x{len(X_train)})...")
    K = kernel.evaluate(X_train)

    # Sort by class for visualization
    sorted_idx = np.argsort(y_train)
    K_sorted = K[sorted_idx][:, sorted_idx]
    y_sorted = y_train[sorted_idx]

    # Same-class vs different-class kernel values
    n0 = np.sum(y_train == 0)
    same_class = []
    diff_class = []
    for i in range(len(y_train)):
        for j in range(i + 1, len(y_train)):
            if y_train[i] == y_train[j]:
                same_class.append(K[i, j])
            else:
                diff_class.append(K[i, j])

    print(f"\n  Same-class kernel values:  mean={np.mean(same_class):.4f}, "
          f"std={np.std(same_class):.4f}")
    print(f"  Diff-class kernel values:  mean={np.mean(diff_class):.4f}, "
          f"std={np.std(diff_class):.4f}")

    # Eigendecomposition
    eigenvalues = np.sort(np.linalg.eigvalsh(K))[::-1]
    print(f"\n  Top 5 eigenvalues: {eigenvalues[:5]}")
    print(f"  Effective rank (eigenvalues > 0.01): {np.sum(eigenvalues > 0.01)}")

    # Kernel-target alignment (Section 6.1)
    # K* = y * y^T (ideal kernel)
    K_star = np.outer(2 * y_train - 1, 2 * y_train - 1)
    alignment = np.sum(K * K_star) / (np.linalg.norm(K, 'fro') * np.linalg.norm(K_star, 'fro'))
    print(f"\n  Kernel-target alignment: {alignment:.4f}")
    print(f"  (Higher = better separation in kernel space)")

    return K_sorted, y_sorted, eigenvalues, same_class, diff_class


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(qsvc, X_train, X_test, y_train, y_test,
                 fm_results, classical_results,
                 K_sorted, eigenvalues, same_class, diff_class):
    """Comprehensive QSVC visualization."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))

    # --- Plot 1: Decision boundary ---
    ax = axes[0, 0]
    h = 0.05
    x_min, x_max = X_test[:, 0].min() - 0.2, X_test[:, 0].max() + 0.2
    y_min, y_max = X_test[:, 1].min() - 0.2, X_test[:, 1].max() + 0.2
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    grid = np.c_[xx.ravel(), yy.ravel()]
    Z = qsvc.predict(grid).reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap='RdBu', edgecolors='k', s=40)
    ax.set_title('QSVC Decision Boundary', fontsize=12)
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')

    # --- Plot 2: Kernel matrix (sorted by class) ---
    ax = axes[0, 1]
    im = ax.imshow(K_sorted, cmap='viridis', aspect='auto')
    plt.colorbar(im, ax=ax, label='K(x_i, x_j)')
    ax.set_title('Kernel Matrix (sorted by class)', fontsize=12)
    ax.set_xlabel('Sample')
    ax.set_ylabel('Sample')

    # --- Plot 3: Eigenspectrum ---
    ax = axes[0, 2]
    ax.bar(range(min(20, len(eigenvalues))), eigenvalues[:20], color='#3498db')
    ax.set_xlabel('Eigenvalue index', fontsize=11)
    ax.set_ylabel('Eigenvalue', fontsize=11)
    ax.set_title('Kernel Matrix Eigenspectrum', fontsize=12)
    ax.grid(True, alpha=0.3)

    # --- Plot 4: Feature map comparison ---
    ax = axes[1, 0]
    if fm_results:
        names = list(fm_results.keys())
        accs = list(fm_results.values())
        colors = ['#e74c3c', '#e74c3c', '#3498db', '#3498db']
        bars = ax.barh(range(len(names)), accs, color=colors)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=9)
        ax.set_xlabel('Test Accuracy')
        ax.set_title('Feature Map Comparison', fontsize=12)
        ax.set_xlim(0, 1.1)

    # --- Plot 5: Classical vs quantum ---
    ax = axes[1, 1]
    if classical_results:
        names = list(classical_results.keys())
        accs = list(classical_results.values())
        colors = ['#9b59b6'] + ['#3498db'] * (len(names) - 1)
        bars = ax.barh(range(len(names)), accs, color=colors)
        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=9)
        ax.set_xlabel('Test Accuracy')
        ax.set_title('Quantum vs Classical', fontsize=12)
        ax.set_xlim(0, 1.1)

    # --- Plot 6: Kernel value distribution ---
    ax = axes[1, 2]
    ax.hist(same_class, bins=20, alpha=0.6, label='Same class', color='#2ecc71')
    ax.hist(diff_class, bins=20, alpha=0.6, label='Diff class', color='#e74c3c')
    ax.set_xlabel('Kernel value K(x_i, x_j)', fontsize=11)
    ax.set_ylabel('Count', fontsize=11)
    ax.set_title('Kernel Value Distribution', fontsize=12)
    ax.legend()

    plt.tight_layout()
    plt.savefig("quantum/algorithms/11_QSVC/qsvc_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/11_QSVC/qsvc_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Quantum Support Vector Classifier (QSVC) - Local Simulator")
    print("=" * 70)
    print("Qiskit 2.4.1 | AerSimulator")

    # Part A: QSVC pipeline
    qsvc, X_train, X_test, y_train, y_test, test_acc = demo_qsvc()

    # Part B: Feature map comparison
    fm_results = demo_feature_map_comparison()

    # Part C: Classical comparison
    classical_results = demo_classical_comparison(X_train, X_test, y_train, y_test, test_acc)

    # Part D: Kernel analysis
    K_sorted, y_sorted, eigenvalues, same_class, diff_class = demo_kernel_analysis()

    # Visualization
    plot_results(qsvc, X_train, X_test, y_train, y_test,
                 fm_results, classical_results,
                 K_sorted, eigenvalues, same_class, diff_class)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    QSVC demonstrated:

    A. Full Pipeline:
       - Feature map encodes data: x -> |phi(x)> = U(x)|0>^n
       - Quantum kernel: K(x_i,x_j) = |<phi(x_i)|phi(x_j)>|^2
       - Classical SVM solves: max sum alpha_i - (1/2) alpha^T K alpha
       - No barren plateaus (no variational parameters)

    B. Feature Maps:
       - ZFeatureMap: product kernel, no entanglement
       - ZZFeatureMap: non-separable kernel, entanglement captures correlations
       - More reps = more nonlinearity but risk of concentration

    C. Classical Comparison:
       - QSVC competitive with classical SVM on simple datasets
       - Quantum advantage requires data-structure alignment

    D. Kernel Analysis:
       - Same-class pairs should have high kernel values
       - Eigenspectrum reveals effective dimensionality
       - Kernel-target alignment measures quality
    """)


if __name__ == "__main__":
    main()