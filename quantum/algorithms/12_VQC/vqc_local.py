"""
Variational Quantum Classifier (VQC) - Local Simulator Implementation
======================================================================

This script demonstrates the VQC algorithm for binary and multi-class
classification using parameterized quantum circuits.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
VQC pipeline:
    1. Feature map U_phi(x): encodes classical data into quantum state
    2. Variational ansatz U(theta): trainable unitary
    3. Measurement: extract class probabilities

    |psi(x,theta)> = U(theta) U_phi(x) |0>^n

    Classification via: f(x,theta) = <psi| O |psi>

The key difference from QSVC (Topic 11):
    - QSVC: quantum kernel + classical SVM (no variational parameters)
    - VQC: fully variational (learns both feature representation and decision boundary)

Gradient computation uses the parameter shift rule (Section 3 of physicist.md):
    df/d(theta_j) = (1/2)[f(theta_j + pi/2) - f(theta_j - pi/2)]
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, ZFeatureMap, RealAmplitudes, EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import EstimatorV2 as AerEstimator, SamplerV2 as AerSampler
from qiskit_machine_learning.algorithms import VQC
from qiskit_algorithms.optimizers import COBYLA, L_BFGS_B, SPSA


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_binary_dataset(n_samples=150, noise=0.15):
    """
    Create a synthetic binary classification dataset (moons).

    Features are scaled to [0, pi] for quantum encoding via ZZFeatureMap.
    The ZZFeatureMap uses trigonometric functions of the input, so [0, pi]
    provides full coverage of the encoding Fourier components
    (see explanation_physicist.md, Section 2.2).
    """
    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=42)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


def create_multiclass_dataset(n_samples=150, n_classes=3):
    """
    Create a synthetic multi-class dataset.

    For multi-class VQC, we use multiple readout qubits
    (see explanation_physicist.md, Section 7).
    """
    X, y = make_blobs(
        n_samples=n_samples, centers=n_classes,
        n_features=2, random_state=42, cluster_std=1.5
    )
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


# =============================================================================
# PART A: Binary VQC with ZZFeatureMap + RealAmplitudes
# =============================================================================

def demo_binary_vqc():
    """
    Demonstrate binary classification with VQC.

    Architecture (see explanation_physicist.md, Section 2):
        Feature map: ZZFeatureMap (2 qubits, encodes pairwise interactions)
            U_ZZ(x) = exp(i sum_k x_k Z_k) * exp(i (pi-x1)(pi-x2) Z1Z2) * H^2

        Ansatz: RealAmplitudes (R_Y rotations + CNOT entanglement)
            U(theta) = prod_l [CNOT * prod_i R_Y(theta_{l,i})]

        Observable: Z on qubit 0
            f(x,theta) = <psi(x,theta)| Z_0 |psi(x,theta)> in [-1, 1]

    Loss: Cross-entropy (handled internally by VQC class)
    Optimizer: COBYLA (gradient-free, robust to noise)
    """
    print("\n" + "=" * 70)
    print("PART A: Binary VQC (ZZFeatureMap + RealAmplitudes)")
    print("=" * 70)

    # --- Dataset ---
    X_train, X_test, y_train, y_test = create_binary_dataset(n_samples=120)
    print(f"Dataset: make_moons, {len(X_train)} train / {len(X_test)} test")
    print(f"Features scaled to [0, pi] for quantum encoding")

    # --- Feature Map ---
    # ZZFeatureMap creates entanglement-based encoding
    # (see explanation_physicist.md, Section 4.2)
    # This encodes x into:
    #   exp(i (pi - x_1)(pi - x_2) Z_1 Z_2) * exp(i x_k Z_k) * H^n
    # The ZZ interaction makes the kernel non-separable (captures feature correlations)
    num_qubits = 2
    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=2)

    # --- Ansatz ---
    # RealAmplitudes: R_Y rotations + linear CNOT entanglement
    # (see explanation_physicist.md, Section 2.3)
    # Real-valued amplitudes are sufficient for classification
    # reps=2 gives 2*(n+1) = 6 trainable parameters for n=2
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=2, entanglement='linear')

    print(f"\nCircuit architecture:")
    print(f"  Feature map: ZZFeatureMap (reps=2, {feature_map.num_parameters} input params)")
    print(f"  Ansatz: RealAmplitudes (reps=2, {ansatz.num_parameters} trainable params)")

    # Display the full circuit
    qc = QuantumCircuit(num_qubits)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)
    print(f"  Total depth: {qc.depth()}")
    print(f"\n{qc.draw(output='text', fold=80)}")

    # --- Training ---
    # COBYLA: gradient-free optimizer
    # (see explanation_physicist.md, Section 6.2)
    # Good for noisy quantum hardware since it doesn't need gradient estimates
    loss_history = []

    def callback(weights, loss):
        """Track training loss at each iteration."""
        loss_history.append(loss)
        if len(loss_history) % 10 == 0:
            print(f"  Iteration {len(loss_history):3d}: loss = {loss:.4f}")

    optimizer = COBYLA(maxiter=80)
    sampler = AerSampler()

    # VQC automatically:
    # 1. Constructs the classification circuit (feature_map + ansatz + measurement)
    # 2. Uses SamplerQNN internally for probability-based classification
    # 3. Optimizes cross-entropy loss
    vqc = VQC(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=optimizer,
        sampler=sampler,
        callback=callback,
    )

    print(f"\nTraining VQC (COBYLA, max 80 iterations)...")
    vqc.fit(X_train, y_train)

    # --- Evaluation ---
    y_pred_train = vqc.predict(X_train)
    y_pred_test = vqc.predict(X_test)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    print(f"\nResults:")
    print(f"  Train accuracy: {train_acc:.4f}")
    print(f"  Test accuracy:  {test_acc:.4f}")

    return vqc, X_train, X_test, y_train, y_test, loss_history


# =============================================================================
# PART B: Ansatz Comparison
# =============================================================================

def demo_ansatz_comparison():
    """
    Compare different ansatz choices and depths.

    From explanation_physicist.md, Section 4:
        - RealAmplitudes: R_Y + CNOT, real-valued amplitudes only
        - EfficientSU2: R_Y + R_Z + CNOT, full SU(2) rotations, more expressive

    From Section 5.3 (Barren Plateaus):
        - Deeper circuits are more expressive but harder to train
        - Var[dL/dtheta] ~ 2^{-n} for deep random circuits
        - Keep depth O(log n) to avoid barren plateaus
    """
    print("\n" + "=" * 70)
    print("PART B: Ansatz Comparison (RealAmplitudes vs EfficientSU2)")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_binary_dataset(n_samples=100)
    num_qubits = 2

    # Fixed feature map for fair comparison
    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=1)

    configs = [
        ("RealAmplitudes (reps=1)", RealAmplitudes(num_qubits, reps=1, entanglement='linear')),
        ("RealAmplitudes (reps=3)", RealAmplitudes(num_qubits, reps=3, entanglement='linear')),
        ("EfficientSU2 (reps=1)", EfficientSU2(num_qubits, reps=1, entanglement='linear')),
        ("EfficientSU2 (reps=3)", EfficientSU2(num_qubits, reps=3, entanglement='linear')),
    ]

    results = []

    for name, ansatz in configs:
        print(f"\n  {name}: {ansatz.num_parameters} params")

        optimizer = COBYLA(maxiter=60)
        sampler = AerSampler()
        losses = []

        vqc = VQC(
            feature_map=feature_map,
            ansatz=ansatz,
            optimizer=optimizer,
            sampler=sampler,
            callback=lambda w, l: losses.append(l),
        )

        vqc.fit(X_train, y_train)
        test_acc = accuracy_score(y_test, vqc.predict(X_test))
        print(f"    Test accuracy: {test_acc:.4f} ({len(losses)} iterations)")

        results.append({
            "name": name,
            "params": ansatz.num_parameters,
            "accuracy": test_acc,
            "losses": losses,
        })

    return results


# =============================================================================
# PART C: Classical Comparison
# =============================================================================

def demo_classical_comparison(X_train, X_test, y_train, y_test, vqc_accuracy):
    """
    Compare VQC with classical SVC.

    From explanation_physicist.md, Section 5.1:
        VQC operates in a 2^n dimensional Hilbert space
        Classical SVM with RBF kernel operates in infinite-dimensional RKHS
        Quantum advantage requires specific data structure alignment
    """
    print("\n" + "=" * 70)
    print("PART C: VQC vs Classical SVM Comparison")
    print("=" * 70)

    # Classical SVM with RBF kernel
    svc_rbf = SVC(kernel='rbf', gamma='auto', C=1.0)
    svc_rbf.fit(X_train, y_train)
    rbf_acc = accuracy_score(y_test, svc_rbf.predict(X_test))

    # Classical SVM with linear kernel
    svc_lin = SVC(kernel='linear', C=1.0)
    svc_lin.fit(X_train, y_train)
    lin_acc = accuracy_score(y_test, svc_lin.predict(X_test))

    # Classical SVM with polynomial kernel
    svc_poly = SVC(kernel='poly', degree=3, C=1.0)
    svc_poly.fit(X_train, y_train)
    poly_acc = accuracy_score(y_test, svc_poly.predict(X_test))

    print(f"  VQC (quantum):       {vqc_accuracy:.4f}")
    print(f"  SVM (RBF kernel):    {rbf_acc:.4f}")
    print(f"  SVM (linear kernel): {lin_acc:.4f}")
    print(f"  SVM (poly kernel):   {poly_acc:.4f}")

    print(f"\n  Note: For make_moons, classical RBF kernel typically matches or")
    print(f"  exceeds VQC. Quantum advantage requires data with quantum-native")
    print(f"  structure (see Huang et al., 2021).")

    return {
        "vqc": vqc_accuracy,
        "rbf": rbf_acc,
        "linear": lin_acc,
        "poly": poly_acc,
    }


# =============================================================================
# PART D: Feature Map Comparison
# =============================================================================

def demo_feature_map_comparison():
    """
    Compare ZFeatureMap (no entanglement) vs ZZFeatureMap (with entanglement).

    From explanation_physicist.md, Section 4:
        ZFeatureMap:  product kernel, each qubit encodes one feature independently
            K_Z(x,y) = prod_k cos^2((x_k - y_k)/2)

        ZZFeatureMap: entangled kernel, captures pairwise feature interactions
            The ZZ term exp(i(pi-x_k)(pi-x_m) Z_k Z_m) creates non-separable features
    """
    print("\n" + "=" * 70)
    print("PART D: Feature Map Comparison (ZFeatureMap vs ZZFeatureMap)")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_binary_dataset(n_samples=100)
    num_qubits = 2
    ansatz = RealAmplitudes(num_qubits, reps=2, entanglement='linear')

    feature_maps = {
        "ZFeatureMap (no entanglement)": ZFeatureMap(feature_dimension=num_qubits, reps=2),
        "ZZFeatureMap (with entanglement)": ZZFeatureMap(feature_dimension=num_qubits, reps=2),
    }

    fm_results = {}
    for name, fm in feature_maps.items():
        print(f"\n  {name}:")
        optimizer = COBYLA(maxiter=60)
        sampler = AerSampler()

        vqc = VQC(
            feature_map=fm,
            ansatz=ansatz,
            optimizer=optimizer,
            sampler=sampler,
        )
        vqc.fit(X_train, y_train)
        acc = accuracy_score(y_test, vqc.predict(X_test))
        print(f"    Test accuracy: {acc:.4f}")
        fm_results[name] = acc

    print(f"\n  The ZZFeatureMap typically performs better because it captures")
    print(f"  pairwise feature interactions via entanglement.")

    return fm_results


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(vqc_model, X_train, X_test, y_train, y_test,
                 loss_history, ansatz_results, classical_results):
    """Generate comprehensive visualization of VQC results."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # --- Plot 1: Training loss curve ---
    ax = axes[0, 0]
    ax.plot(loss_history, 'b-', linewidth=1.5, alpha=0.7)
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Loss', fontsize=12)
    ax.set_title('VQC Training Loss', fontsize=13)
    ax.grid(True, alpha=0.3)

    # --- Plot 2: Decision boundary ---
    ax = axes[0, 1]
    h = 0.05
    x_min, x_max = X_test[:, 0].min() - 0.2, X_test[:, 0].max() + 0.2
    y_min, y_max = X_test[:, 1].min() - 0.2, X_test[:, 1].max() + 0.2
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    grid_points = np.c_[xx.ravel(), yy.ravel()]

    Z = vqc_model.predict(grid_points)
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu')
    ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap='RdBu',
               edgecolors='k', s=40)
    ax.set_xlabel('Feature 1', fontsize=12)
    ax.set_ylabel('Feature 2', fontsize=12)
    ax.set_title('VQC Decision Boundary (Test Set)', fontsize=13)

    # --- Plot 3: Ansatz comparison ---
    ax = axes[1, 0]
    if ansatz_results:
        names = [r["name"] for r in ansatz_results]
        accs = [r["accuracy"] for r in ansatz_results]
        params = [r["params"] for r in ansatz_results]
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']
        bars = ax.bar(range(len(names)), accs, color=colors[:len(names)])
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels([f"{n}\n({p} params)" for n, p in zip(names, params)],
                           fontsize=8, rotation=15, ha='right')
        ax.set_ylabel('Test Accuracy', fontsize=12)
        ax.set_title('Ansatz Comparison', fontsize=13)
        ax.set_ylim(0, 1.1)
        for bar, acc in zip(bars, accs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{acc:.3f}', ha='center', fontsize=10)

    # --- Plot 4: VQC vs Classical ---
    ax = axes[1, 1]
    if classical_results:
        methods = list(classical_results.keys())
        accs = list(classical_results.values())
        labels = ['VQC\n(Quantum)', 'SVM\n(RBF)', 'SVM\n(Linear)', 'SVM\n(Poly)']
        colors = ['#9b59b6', '#3498db', '#2ecc71', '#e74c3c']
        bars = ax.bar(range(len(labels)), accs, color=colors)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylabel('Test Accuracy', fontsize=12)
        ax.set_title('Quantum vs Classical Comparison', fontsize=13)
        ax.set_ylim(0, 1.1)
        for bar, acc in zip(bars, accs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{acc:.3f}', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/12_VQC/vqc_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/12_VQC/vqc_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Variational Quantum Classifier (VQC) - Local Simulator")
    print("=" * 70)
    print("Qiskit 2.4.1 | AerSimulator")

    # Part A: Binary VQC
    vqc, X_train, X_test, y_train, y_test, loss_history = demo_binary_vqc()
    vqc_acc = accuracy_score(y_test, vqc.predict(X_test))

    # Part B: Ansatz comparison
    ansatz_results = demo_ansatz_comparison()

    # Part C: Classical comparison
    classical_results = demo_classical_comparison(
        X_train, X_test, y_train, y_test, vqc_acc
    )

    # Part D: Feature map comparison
    fm_results = demo_feature_map_comparison()

    # Visualization
    plot_results(vqc, X_train, X_test, y_train, y_test,
                 loss_history, ansatz_results, classical_results)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    VQC demonstrated:

    A. Binary Classification:
       - ZZFeatureMap encodes data with entanglement-based correlations
       - RealAmplitudes ansatz provides trainable decision boundary
       - COBYLA optimizer (gradient-free) is robust to quantum noise
       - Cross-entropy loss for probability-based classification

    B. Ansatz Comparison:
       - More parameters (deeper circuits) can improve expressivity
       - But risk of barren plateaus grows with depth (Section 5.3)
       - EfficientSU2 is more expressive than RealAmplitudes

    C. Classical vs Quantum:
       - For simple 2D datasets, classical SVM is competitive
       - Quantum advantage requires specific data structure (Huang et al.)
       - VQC's strength: exponential feature space in 2^n dimensions

    D. Feature Maps:
       - ZZFeatureMap (entangled) outperforms ZFeatureMap (product)
       - Entanglement captures pairwise feature interactions
       - Feature map choice is as important as ansatz choice

    Key insight: VQC is a hybrid algorithm where the classical optimizer
    tunes quantum circuit parameters to minimize classification loss.
    The parameter shift rule enables exact gradient computation.
    """)


if __name__ == "__main__":
    main()