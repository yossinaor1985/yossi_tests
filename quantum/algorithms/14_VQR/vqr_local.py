"""
Variational Quantum Regressor (VQR) - Local Simulator Implementation
=====================================================================

This script demonstrates quantum regression using VQR from
qiskit_machine_learning for fitting continuous-valued functions.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
VQR prediction: f(x; theta) = <psi(x,theta)| O |psi(x,theta)>
Loss: MSE = (1/N) sum (y_i - f(x_i; theta))^2

The output is bounded in [-1, 1] for O = Z, so targets must be
rescaled accordingly. With data re-uploading, the model generates
a truncated Fourier series (Schuld et al., 2021).
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import ZZFeatureMap, ZFeatureMap, RealAmplitudes, EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_machine_learning.neural_networks import EstimatorQNN
from qiskit_machine_learning.algorithms import VQR
from qiskit_algorithms.optimizers import COBYLA, L_BFGS_B


# =============================================================================
# DATA GENERATION
# =============================================================================

def create_1d_regression_data(func, n_samples=80, noise_std=0.05):
    """
    Create 1D regression dataset.

    Features scaled to [0, pi] for quantum encoding.
    Targets scaled to [-1, 1] to match Z expectation value range
    (see explanation_physicist.md, Section 2.3).
    """
    rng = np.random.default_rng(42)
    X = rng.uniform(0, 1, (n_samples, 1))
    y_true = func(X[:, 0])
    y = y_true + rng.normal(0, noise_std, n_samples)

    # Scale features to [0, pi]
    X_scaler = MinMaxScaler(feature_range=(0, np.pi))
    X_scaled = X_scaler.fit_transform(X)

    # Scale targets to [-0.9, 0.9] (within [-1, 1] with margin)
    y_scaler = MinMaxScaler(feature_range=(-0.9, 0.9))
    y_scaled = y_scaler.fit_transform(y.reshape(-1, 1)).flatten()

    # Split
    n_train = int(0.7 * n_samples)
    idx = rng.permutation(n_samples)
    train_idx, test_idx = idx[:n_train], idx[n_train:]

    return (X_scaled[train_idx], X_scaled[test_idx],
            y_scaled[train_idx], y_scaled[test_idx],
            X_scaler, y_scaler)


def create_2d_regression_data(n_samples=100, noise_std=0.05):
    """Create 2D regression dataset: y = sin(x1) * cos(x2)."""
    rng = np.random.default_rng(42)
    X = rng.uniform(0, 1, (n_samples, 2))
    y = np.sin(2 * np.pi * X[:, 0]) * np.cos(2 * np.pi * X[:, 1])
    y += rng.normal(0, noise_std, n_samples)

    X_scaler = MinMaxScaler(feature_range=(0, np.pi))
    X_scaled = X_scaler.fit_transform(X)

    y_scaler = MinMaxScaler(feature_range=(-0.9, 0.9))
    y_scaled = y_scaler.fit_transform(y.reshape(-1, 1)).flatten()

    n_train = int(0.7 * n_samples)
    idx = rng.permutation(n_samples)

    return (X_scaled[idx[:n_train]], X_scaled[idx[n_train:]],
            y_scaled[idx[:n_train]], y_scaled[idx[n_train:]],
            X_scaler, y_scaler)


# =============================================================================
# PART A: 1D Sine Regression
# =============================================================================

def demo_1d_regression():
    """
    Fit a sine function using VQR.

    From explanation_physicist.md, Section 3.1:
        With data re-uploading, VQR generates a Fourier series:
        f(x) = sum_k c_k exp(i k omega x)

        L re-uploading layers -> 2L+1 Fourier terms
        A sine function needs at least 1 layer (frequency 1 component)
    """
    print("\n" + "=" * 70)
    print("PART A: 1D Sine Regression")
    print("=" * 70)

    sine_func = lambda x: np.sin(2 * np.pi * x)
    X_train, X_test, y_train, y_test, X_sc, y_sc = create_1d_regression_data(
        sine_func, n_samples=60, noise_std=0.05
    )

    print(f"Dataset: sin(2*pi*x), {len(X_train)} train / {len(X_test)} test")
    print(f"Target range: [{y_train.min():.2f}, {y_train.max():.2f}] (scaled to ~[-0.9, 0.9])")

    # Build VQR: 1 qubit, ZFeatureMap + RealAmplitudes
    # For 1D data, 1 qubit is sufficient
    num_qubits = 1
    feature_map = ZFeatureMap(feature_dimension=num_qubits, reps=1)
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=3, entanglement='linear')

    print(f"\nCircuit: ZFeatureMap(1q, reps=1) + RealAmplitudes(reps=3)")
    print(f"  Trainable parameters: {ansatz.num_parameters}")

    # Train
    loss_history = []
    def callback(weights, loss):
        loss_history.append(loss)
        if len(loss_history) % 20 == 0:
            print(f"  Iter {len(loss_history):3d}: MSE = {loss:.6f}")

    estimator = AerEstimator()
    optimizer = COBYLA(maxiter=100)

    vqr = VQR(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=optimizer,
        estimator=estimator,
        callback=callback,
    )

    print(f"\nTraining (COBYLA, max 100 iterations)...")
    vqr.fit(X_train, y_train)

    # Evaluate
    y_pred_train = vqr.predict(X_train)
    y_pred_test = vqr.predict(X_test)

    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    r2_test = r2_score(y_test, y_pred_test)

    print(f"\nResults:")
    print(f"  Train MSE: {mse_train:.6f}")
    print(f"  Test MSE:  {mse_test:.6f}")
    print(f"  Test R^2:  {r2_test:.4f}")

    return vqr, X_train, X_test, y_train, y_test, loss_history, X_sc, y_sc


# =============================================================================
# PART B: 2D Regression
# =============================================================================

def demo_2d_regression():
    """
    Fit a 2D function: y = sin(x1) * cos(x2).

    Uses 2 qubits with ZZFeatureMap to capture the interaction
    between x1 and x2 (the product sin*cos requires cross-terms).

    From explanation_physicist.md, Section 3.2:
        ZZFeatureMap creates entanglement-based feature interactions
        essential for capturing multi-variable correlations.
    """
    print("\n" + "=" * 70)
    print("PART B: 2D Regression (y = sin(x1)*cos(x2))")
    print("=" * 70)

    X_train, X_test, y_train, y_test, X_sc, y_sc = create_2d_regression_data(
        n_samples=80, noise_std=0.05
    )
    print(f"Dataset: sin(x1)*cos(x2), {len(X_train)} train / {len(X_test)} test")

    num_qubits = 2
    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=2)
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=2, entanglement='linear')

    print(f"Circuit: ZZFeatureMap(2q, reps=2) + RealAmplitudes(reps=2)")
    print(f"  Trainable parameters: {ansatz.num_parameters}")

    loss_history = []
    estimator = AerEstimator()
    optimizer = COBYLA(maxiter=80)

    vqr = VQR(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=optimizer,
        estimator=estimator,
        callback=lambda w, l: loss_history.append(l),
    )

    print(f"\nTraining (COBYLA, max 80 iterations)...")
    vqr.fit(X_train, y_train)

    y_pred_test = vqr.predict(X_test)
    mse = mean_squared_error(y_test, y_pred_test)
    r2 = r2_score(y_test, y_pred_test)

    print(f"  Test MSE: {mse:.6f}")
    print(f"  Test R^2: {r2:.4f}")

    return vqr, X_test, y_test, y_pred_test, loss_history


# =============================================================================
# PART C: Ansatz Depth Comparison
# =============================================================================

def demo_ansatz_depth():
    """
    Compare regression quality with different ansatz depths.

    From explanation_physicist.md, Section 4.3:
        - reps=1: smooth, low-frequency functions
        - reps=3: complex, high-frequency functions
        - Too deep: barren plateaus
    """
    print("\n" + "=" * 70)
    print("PART C: Ansatz Depth Comparison for Regression")
    print("=" * 70)

    # Complex target function
    func = lambda x: np.sin(4 * np.pi * x) * np.exp(-x)
    X_train, X_test, y_train, y_test, X_sc, y_sc = create_1d_regression_data(
        func, n_samples=60, noise_std=0.03
    )

    results = []
    for reps in [1, 2, 3]:
        feature_map = ZFeatureMap(feature_dimension=1, reps=1)
        ansatz = RealAmplitudes(num_qubits=1, reps=reps, entanglement='linear')

        estimator = AerEstimator()
        optimizer = COBYLA(maxiter=80)

        vqr = VQR(
            feature_map=feature_map,
            ansatz=ansatz,
            optimizer=optimizer,
            estimator=estimator,
        )
        vqr.fit(X_train, y_train)

        y_pred = vqr.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"  reps={reps}: params={ansatz.num_parameters}, MSE={mse:.6f}, R^2={r2:.4f}")
        results.append({"reps": reps, "params": ansatz.num_parameters,
                        "mse": mse, "r2": r2, "y_pred": y_pred})

    return results, X_test, y_test


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(vqr_1d, X_train_1d, X_test_1d, y_train_1d, y_test_1d,
                 loss_1d, X_sc, y_sc, results_2d, depth_results, X_test_depth, y_test_depth):
    """Comprehensive VQR visualization."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    # --- Plot 1: 1D Regression fit ---
    ax = axes[0, 0]
    # Generate smooth prediction curve
    X_smooth = np.linspace(X_train_1d.min(), X_train_1d.max(), 100).reshape(-1, 1)
    y_smooth = vqr_1d.predict(X_smooth)
    ax.scatter(X_train_1d, y_train_1d, c='blue', s=20, alpha=0.5, label='Train')
    ax.scatter(X_test_1d, y_test_1d, c='red', s=30, marker='x', label='Test')
    ax.plot(X_smooth, y_smooth, 'g-', linewidth=2, label='VQR prediction')
    ax.set_xlabel('x (scaled)', fontsize=11)
    ax.set_ylabel('y (scaled)', fontsize=11)
    ax.set_title('1D Sine Regression', fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # --- Plot 2: Training loss ---
    ax = axes[0, 1]
    ax.plot(loss_1d, 'b-', linewidth=1.5)
    ax.set_xlabel('Iteration', fontsize=11)
    ax.set_ylabel('MSE Loss', fontsize=11)
    ax.set_title('Training Loss (1D Regression)', fontsize=13)
    ax.grid(True, alpha=0.3)

    # --- Plot 3: 2D regression (predicted vs actual) ---
    ax = axes[1, 0]
    if results_2d is not None:
        vqr_2d, X_test_2d, y_test_2d, y_pred_2d, loss_2d = results_2d
        ax.scatter(y_test_2d, y_pred_2d, c='#3498db', s=30, alpha=0.7)
        lims = [min(y_test_2d.min(), y_pred_2d.min()), max(y_test_2d.max(), y_pred_2d.max())]
        ax.plot(lims, lims, 'r--', linewidth=2, label='Perfect prediction')
        ax.set_xlabel('Actual y', fontsize=11)
        ax.set_ylabel('Predicted y', fontsize=11)
        ax.set_title('2D Regression: Predicted vs Actual', fontsize=13)
        ax.legend()
        ax.grid(True, alpha=0.3)

    # --- Plot 4: Ansatz depth comparison ---
    ax = axes[1, 1]
    if depth_results:
        reps_list = [r["reps"] for r in depth_results]
        r2_list = [r["r2"] for r in depth_results]
        params_list = [r["params"] for r in depth_results]
        colors = ['#3498db', '#2ecc71', '#e74c3c']
        bars = ax.bar(range(len(reps_list)), r2_list, color=colors)
        ax.set_xticks(range(len(reps_list)))
        ax.set_xticklabels([f'reps={r}\n({p} params)' for r, p in zip(reps_list, params_list)])
        ax.set_ylabel('R^2 Score', fontsize=11)
        ax.set_title('Ansatz Depth vs Regression Quality', fontsize=13)
        for bar, val in zip(bars, r2_list):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{val:.3f}', ha='center', fontsize=11)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/14_VQR/vqr_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/14_VQR/vqr_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Variational Quantum Regressor (VQR) - Local Simulator")
    print("=" * 70)
    print("Qiskit 2.4.1 | AerSimulator")

    # Part A: 1D regression
    vqr_1d, X_tr, X_te, y_tr, y_te, loss_1d, X_sc, y_sc = demo_1d_regression()

    # Part B: 2D regression
    results_2d = demo_2d_regression()

    # Part C: Ansatz depth
    depth_results, X_test_d, y_test_d = demo_ansatz_depth()

    # Visualization
    plot_results(vqr_1d, X_tr, X_te, y_tr, y_te, loss_1d, X_sc, y_sc,
                 results_2d, depth_results, X_test_d, y_test_d)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    VQR demonstrated:

    A. 1D Sine Regression:
       - f(x;theta) = <psi(x,theta)| Z |psi(x,theta)>
       - Output in [-1,1], targets scaled accordingly
       - Data re-uploading enables Fourier series approximation

    B. 2D Regression:
       - ZZFeatureMap captures cross-feature interactions
       - Essential for fitting y = sin(x1)*cos(x2) (product of features)

    C. Ansatz Depth:
       - Deeper ansatz = more complex functions
       - But risk of barren plateaus and overfitting
       - Optimal depth depends on target function complexity

    Key difference from VQC:
       - VQC: discrete class labels from measurement probabilities
       - VQR: continuous values from expectation value <Z>
    """)


if __name__ == "__main__":
    main()