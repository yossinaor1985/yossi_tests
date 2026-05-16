"""
Quantum Kernel Methods (FidelityQuantumKernel) - Local Simulator Implementation
=================================================================================

This script demonstrates quantum kernel computation and SVM classification
using the FidelityQuantumKernel from qiskit_machine_learning.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Quantum kernel:
    K(x_i, x_j) = |<phi(x_i)|phi(x_j)>|^2
                 = |<0|^n U(x_i)^dag U(x_j) |0>^n|^2

This is the transition probability (fidelity) between two quantum states.
It satisfies Mercer's conditions (Section 2.2) and operates in a 4^n
dimensional feature space (Section 4.2, proof of PSD property).

The kernel is evaluated by running the circuit:
    |0>^n -> U(x_j) -> U(x_i)^dag -> Measure all qubits
    P(0...0) = K(x_i, x_j)
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

from qiskit.circuit.library import ZFeatureMap, ZZFeatureMap, PauliFeatureMap
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_machine_learning.kernels import FidelityQuantumKernel


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_dataset(n_samples=100, dataset_type="moons"):
    """
    Create a synthetic classification dataset.

    Features scaled to [0, pi] for quantum encoding.
    ZZFeatureMap uses trigonometric encoding, so [0, pi] spans
    the full period of cos and sin functions.
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
# PART A: ZFeatureMap Kernel (No Entanglement)
# =============================================================================

def demo_z_feature_map_kernel():
    """
    Demonstrate quantum kernel with ZFeatureMap (no entanglement).

    ZFeatureMap (see explanation_physicist.md, Section 3.2):
        U_Z(x) = [prod_{l=1}^{r} H^n * prod_i exp(i x_i Z_i)]

    This encodes each feature x_i into independent qubit rotations.
    No entanglement -> product kernel:
        K_Z(x, y) = prod_k cos^2(x_k - y_k)

    This is equivalent to a separable classical kernel -- no quantum advantage.
    """
    print("\n" + "=" * 70)
    print("PART A: ZFeatureMap Kernel (No Entanglement)")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_dataset(n_samples=80, dataset_type="moons")
    num_qubits = 2

    # ZFeatureMap: single-qubit Z rotations only
    feature_map = ZFeatureMap(feature_dimension=num_qubits, reps=2)
    print(f"\nZFeatureMap circuit (reps=2):")
    print(f"  Qubits: {num_qubits}")
    print(f"  Parameters: {feature_map.num_parameters}")
    print(f"  Depth: {feature_map.depth()}")
    print(f"\n{feature_map.draw(output='text', fold=80)}")

    # Create quantum kernel
    sampler = AerSampler()
    kernel = FidelityQuantumKernel(feature_map=feature_map, fidelity=None)

    # Compute kernel matrix
    # This evaluates K(x_i, x_j) for all pairs in the training set
    # Each entry requires one circuit evaluation + shots
    # Total circuits: N_train * (N_train + 1) / 2 (symmetric)
    print(f"\nComputing training kernel matrix ({len(X_train)}x{len(X_train)})...")
    K_train = kernel.evaluate(X_train)
    print(f"  Shape: {K_train.shape}")
    print(f"  Diagonal (self-similarity): all {K_train[0,0]:.4f}")
    print(f"  Off-diagonal range: [{K_train[np.triu_indices_from(K_train, k=1)].min():.4f}, "
          f"{K_train[np.triu_indices_from(K_train, k=1)].max():.4f}]")

    # SVM classification with quantum kernel
    svc = SVC(kernel='precomputed', C=1.0)
    svc.fit(K_train, y_train)

    # For test prediction, compute kernel between test and train
    K_test = kernel.evaluate(X_test, X_train)
    y_pred = svc.predict(K_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"\n  ZFeatureMap SVC accuracy: {acc:.4f}")
    print(f"  (Limited by product kernel structure -- no feature interactions)")

    return K_train, acc


# =============================================================================
# PART B: ZZFeatureMap Kernel (With Entanglement)
# =============================================================================

def demo_zz_feature_map_kernel():
    """
    Demonstrate quantum kernel with ZZFeatureMap (entangled).

    ZZFeatureMap (see explanation_physicist.md, Section 3.3):
        U_ZZ(x) = prod_l [H^n * prod_i exp(i x_i Z_i)
                          * prod_{i<j} exp(i (pi-x_i)(pi-x_j) Z_i Z_j)]

    The ZZ interaction creates entanglement between qubits, making the
    kernel non-separable. This captures pairwise feature correlations
    that the ZFeatureMap cannot.

    The circuit for exp(i phi Z_i Z_j):
        --*--------*--
          |        |
        --X--RZ(2phi)--X--
    """
    print("\n" + "=" * 70)
    print("PART B: ZZFeatureMap Kernel (With Entanglement)")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_dataset(n_samples=80, dataset_type="moons")
    num_qubits = 2

    # ZZFeatureMap: adds pairwise ZZ interactions
    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=2)
    print(f"\nZZFeatureMap circuit (reps=2):")
    print(f"  Qubits: {num_qubits}")
    print(f"  Parameters: {feature_map.num_parameters}")
    print(f"  Depth: {feature_map.depth()}")
    print(f"\n{feature_map.draw(output='text', fold=80)}")

    # Create quantum kernel
    kernel = FidelityQuantumKernel(feature_map=feature_map)

    # Compute kernel matrices
    print(f"\nComputing training kernel matrix ({len(X_train)}x{len(X_train)})...")
    K_train = kernel.evaluate(X_train)

    print(f"  Diagonal (self-similarity): all {K_train[0,0]:.4f}")
    print(f"  Off-diagonal range: [{K_train[np.triu_indices_from(K_train, k=1)].min():.4f}, "
          f"{K_train[np.triu_indices_from(K_train, k=1)].max():.4f}]")

    # Verify kernel matrix properties (see explanation_physicist.md, Section 4.1):
    #   1. Symmetric: K = K^T
    #   2. PSD: all eigenvalues >= 0
    #   3. Diagonal = 1: K(x, x) = 1
    eigenvalues = np.linalg.eigvalsh(K_train)
    print(f"\n  Kernel matrix verification:")
    print(f"    Symmetric: {np.allclose(K_train, K_train.T)}")
    print(f"    PSD (min eigenvalue): {eigenvalues.min():.6f}")
    print(f"    Diagonal = 1: {np.allclose(np.diag(K_train), 1.0)}")

    # SVM classification
    svc = SVC(kernel='precomputed', C=1.0)
    svc.fit(K_train, y_train)

    K_test = kernel.evaluate(X_test, X_train)
    y_pred = svc.predict(K_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"\n  ZZFeatureMap SVC accuracy: {acc:.4f}")
    print(f"  (Entanglement enables non-separable kernel -> better boundaries)")

    return kernel, K_train, K_test, X_train, X_test, y_train, y_test, acc


# =============================================================================
# PART C: Classical Kernel Comparison
# =============================================================================

def demo_classical_comparison(X_train, X_test, y_train, y_test, quantum_acc):
    """
    Compare quantum kernel with classical kernels.

    From explanation_physicist.md, Section 8:
        - Quantum advantage requires the kernel to align with data structure
        - For most real datasets, classical RBF kernel is competitive
        - Quantum advantage is proven for data with group-theoretic structure
          (Liu et al., 2021)
    """
    print("\n" + "=" * 70)
    print("PART C: Quantum vs Classical Kernel Comparison")
    print("=" * 70)

    classifiers = {
        "Linear": SVC(kernel='linear', C=1.0),
        "RBF (gamma=auto)": SVC(kernel='rbf', gamma='auto', C=1.0),
        "RBF (gamma=1.0)": SVC(kernel='rbf', gamma=1.0, C=1.0),
        "Polynomial (d=3)": SVC(kernel='poly', degree=3, C=1.0),
    }

    results = {"Quantum (ZZFeatureMap)": quantum_acc}

    for name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        acc = accuracy_score(y_test, clf.predict(X_test))
        results[name] = acc
        print(f"  {name:25s}: accuracy = {acc:.4f}")

    print(f"\n  Quantum (ZZFeatureMap):    accuracy = {quantum_acc:.4f}")

    return results


# =============================================================================
# PART D: Kernel Concentration Analysis
# =============================================================================

def demo_kernel_concentration():
    """
    Demonstrate the exponential concentration phenomenon.

    From explanation_physicist.md, Section 5.4 (Thanasilp et al., 2022):
        For generic quantum kernels with expressive feature maps:
        K(x_i, x_j) -> 2^{-n} for x_i != x_j as n -> infinity

    When the kernel matrix approaches the identity, classification fails
    because all points appear equally "far" from each other.

    We demonstrate this by increasing the number of qubits and observing
    how off-diagonal kernel values shrink.
    """
    print("\n" + "=" * 70)
    print("PART D: Kernel Concentration Analysis")
    print("=" * 70)

    print("  Testing how off-diagonal kernel values change with qubit count...")
    print("  (see explanation_physicist.md, Section 5.4)\n")

    # Generate a small dataset with increasing dimensions
    rng = np.random.default_rng(42)
    n_samples = 10
    qubit_counts = [2, 3, 4, 5, 6]

    concentration_data = []

    for n_qubits in qubit_counts:
        # Random data points in [0, pi]^n
        X = rng.uniform(0, np.pi, size=(n_samples, n_qubits))

        feature_map = ZZFeatureMap(feature_dimension=n_qubits, reps=2)
        kernel = FidelityQuantumKernel(feature_map=feature_map)
        K = kernel.evaluate(X)

        # Off-diagonal values
        off_diag = K[np.triu_indices_from(K, k=1)]
        mean_off = np.mean(off_diag)
        std_off = np.std(off_diag)
        theoretical = 1.0 / (2 ** n_qubits)

        concentration_data.append({
            "n_qubits": n_qubits,
            "mean_off_diag": mean_off,
            "std_off_diag": std_off,
            "theoretical_limit": theoretical,
        })

        print(f"  n={n_qubits} qubits: mean(K_off) = {mean_off:.4f} +/- {std_off:.4f}  "
              f"(theory: 1/2^n = {theoretical:.4f})")

    print(f"\n  As n increases, off-diagonal values shrink toward 1/2^n.")
    print(f"  Mitigation: use shallow feature maps, problem-informed encoding,")
    print(f"  or quantum kernel alignment (Section 6).")

    return concentration_data


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(K_train_z, K_train_zz, X_train, y_train, X_test, y_test,
                 classical_results, concentration_data):
    """Comprehensive visualization of quantum kernel analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # --- Plot 1: ZFeatureMap kernel matrix ---
    ax = axes[0, 0]
    im = ax.imshow(K_train_z, cmap='viridis', aspect='auto')
    plt.colorbar(im, ax=ax, label='K(x_i, x_j)')
    ax.set_title('ZFeatureMap Kernel Matrix\n(Product Kernel, No Entanglement)', fontsize=11)
    ax.set_xlabel('Sample index')
    ax.set_ylabel('Sample index')

    # --- Plot 2: ZZFeatureMap kernel matrix ---
    ax = axes[0, 1]
    im = ax.imshow(K_train_zz, cmap='viridis', aspect='auto')
    plt.colorbar(im, ax=ax, label='K(x_i, x_j)')
    ax.set_title('ZZFeatureMap Kernel Matrix\n(Entangled Kernel)', fontsize=11)
    ax.set_xlabel('Sample index')
    ax.set_ylabel('Sample index')

    # --- Plot 3: Classical vs Quantum accuracy ---
    ax = axes[1, 0]
    names = list(classical_results.keys())
    accs = list(classical_results.values())
    colors = ['#9b59b6'] + ['#3498db'] * (len(names) - 1)
    bars = ax.barh(range(len(names)), accs, color=colors)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('Test Accuracy', fontsize=12)
    ax.set_title('Quantum vs Classical Kernels', fontsize=13)
    ax.set_xlim(0, 1.1)
    for bar, acc in zip(bars, accs):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{acc:.3f}', va='center', fontsize=10)

    # --- Plot 4: Kernel concentration ---
    ax = axes[1, 1]
    if concentration_data:
        n_q = [d["n_qubits"] for d in concentration_data]
        means = [d["mean_off_diag"] for d in concentration_data]
        theory = [d["theoretical_limit"] for d in concentration_data]
        ax.plot(n_q, means, 'bo-', linewidth=2, markersize=8, label='Measured mean(K_off)')
        ax.plot(n_q, theory, 'r--', linewidth=2, label='Theoretical 1/2^n')
        ax.set_xlabel('Number of Qubits', fontsize=12)
        ax.set_ylabel('Mean Off-Diagonal Kernel Value', fontsize=12)
        ax.set_title('Kernel Concentration\n(Thanasilp et al., 2022)', fontsize=11)
        ax.legend(fontsize=10)
        ax.set_yscale('log')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/10_quantum_kernels/quantum_kernels_results.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/10_quantum_kernels/quantum_kernels_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Quantum Kernel Methods (FidelityQuantumKernel) - Local Simulator")
    print("=" * 70)
    print("Qiskit 2.4.1 | AerSimulator")

    # Part A: ZFeatureMap kernel (no entanglement)
    K_train_z, z_acc = demo_z_feature_map_kernel()

    # Part B: ZZFeatureMap kernel (with entanglement)
    (kernel_zz, K_train_zz, K_test_zz,
     X_train, X_test, y_train, y_test, zz_acc) = demo_zz_feature_map_kernel()

    # Part C: Classical comparison
    classical_results = demo_classical_comparison(X_train, X_test, y_train, y_test, zz_acc)

    # Part D: Kernel concentration
    concentration_data = demo_kernel_concentration()

    # Visualization
    plot_results(K_train_z, K_train_zz, X_train, y_train, X_test, y_test,
                 classical_results, concentration_data)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Quantum Kernel Methods demonstrated:

    A. ZFeatureMap (No Entanglement):
       - Product kernel: K(x,y) = prod_k cos^2(x_k - y_k)
       - No quantum advantage (classically simulable)
       - Equivalent to independent per-feature similarity

    B. ZZFeatureMap (With Entanglement):
       - Non-separable kernel capturing pairwise interactions
       - Operates in 4^n dimensional feature space
       - Entanglement creates classically hard-to-compute kernel

    C. Classical Comparison:
       - For simple 2D data, classical RBF is competitive
       - Quantum advantage requires structure alignment (Huang et al.)

    D. Kernel Concentration:
       - Off-diagonal values -> 1/2^n as qubit count grows
       - This is the "curse of exponentiality" (Thanasilp et al.)
       - Mitigation: shallow maps, problem-informed encoding

    Workflow: Quantum computer computes K(x_i, x_j) -> classical SVM classifies
    """)


if __name__ == "__main__":
    main()