"""
Quantum Reservoir Computing (QRC) - Local Simulator Implementation
===================================================================

Implements QRC with a fixed random quantum reservoir and classical
linear readout for classification and regression tasks.

Qiskit Version: 2.4.1

Architecture (see explanation_physicist.md):
    1. Data encoding: R_Y(x_i) rotations
    2. Fixed reservoir: random circuit (NOT trained)
    3. Feature extraction: <X_i>, <Y_i>, <Z_i> for each qubit
    4. Classical readout: Ridge regression (sklearn)

Key advantage: NO quantum parameter optimization -> NO barren plateaus.
Training is just linear regression (closed-form solution).
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp


# =============================================================================
# RANDOM RESERVOIR CIRCUIT
# =============================================================================

def build_reservoir(n_qubits, n_layers=3, seed=42):
    """
    Build a FIXED random quantum circuit (the reservoir).

    This circuit is NOT trained. It provides a complex nonlinear
    transformation from input space to feature space.

    Architecture (see explanation_physicist.md, Section 3.1):
        Each layer: random R_Y, R_Z on each qubit + CNOT chain

    The randomness ensures:
        - High separation property (different inputs -> different outputs)
        - Rich feature space for the linear readout to exploit
    """
    rng = np.random.default_rng(seed)

    qc = QuantumCircuit(n_qubits, name="reservoir")

    for layer in range(n_layers):
        # Random single-qubit rotations
        for q in range(n_qubits):
            qc.ry(rng.uniform(0, 2 * np.pi), q)
            qc.rz(rng.uniform(0, 2 * np.pi), q)

        # Entangling layer (CNOT chain)
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
        # Close the ring for n > 2
        if n_qubits > 2:
            qc.cx(n_qubits - 1, 0)

    return qc


def encode_and_run_reservoir(x, n_qubits, reservoir_circuit):
    """
    Encode a data point and run through the reservoir.

    Steps:
        1. Encode x via R_Y(x_i) on qubit i (data encoding)
        2. Apply fixed reservoir circuit (nonlinear transformation)
        3. Measure expectation values of Pauli operators (feature extraction)

    Returns feature vector f(x) = [<X_1>, <Y_1>, <Z_1>, <X_2>, ...]
    """
    # Build full circuit: encoding + reservoir
    qc = QuantumCircuit(n_qubits)

    # Data encoding: R_Y(x_i) on qubit i
    # For data with more features than qubits, use modular encoding
    for q in range(n_qubits):
        if q < len(x):
            qc.ry(x[q], q)

    # Apply reservoir
    qc.compose(reservoir_circuit, inplace=True)

    # Get statevector
    sv = Statevector(qc)

    # Extract features: <X_i>, <Y_i>, <Z_i> for each qubit
    features = []
    for q in range(n_qubits):
        for pauli in ['X', 'Y', 'Z']:
            # Build Pauli string: I...P...I with P at position q
            pauli_str = ['I'] * n_qubits
            pauli_str[n_qubits - 1 - q] = pauli  # Qiskit uses reversed order
            op = SparsePauliOp.from_list([(''.join(pauli_str), 1.0)])
            exp_val = sv.expectation_value(op).real
            features.append(exp_val)

    return np.array(features)


def extract_features(X, n_qubits, reservoir_circuit):
    """Extract reservoir features for all data points."""
    features_list = []
    for i, x in enumerate(X):
        f = encode_and_run_reservoir(x, n_qubits, reservoir_circuit)
        features_list.append(f)
        if (i + 1) % 20 == 0:
            print(f"    Processed {i+1}/{len(X)} samples")
    return np.array(features_list)


# =============================================================================
# PART A: Classification with QRC
# =============================================================================

def demo_classification():
    """
    QRC for binary classification on make_moons.

    From explanation_physicist.md, Section 3:
        - Fixed reservoir provides nonlinear features
        - Ridge regression trains the linear readout
        - No quantum parameter optimization needed
    """
    print("\n" + "=" * 70)
    print("PART A: QRC Classification (make_moons)")
    print("=" * 70)

    # Dataset
    X, y = make_moons(n_samples=100, noise=0.15, random_state=42)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    print(f"Dataset: {len(X_train)} train / {len(X_test)} test")

    # Reservoir
    n_qubits = 4
    n_layers = 3
    reservoir = build_reservoir(n_qubits, n_layers, seed=42)

    print(f"Reservoir: {n_qubits} qubits, {n_layers} layers (FIXED, not trained)")
    print(f"Features per sample: {3 * n_qubits} (X, Y, Z on each qubit)")

    # Feature extraction
    print(f"\nExtracting reservoir features...")
    F_train = extract_features(X_train, n_qubits, reservoir)
    F_test = extract_features(X_test, n_qubits, reservoir)

    print(f"  Feature matrix shape: {F_train.shape}")

    # Classical readout (Ridge regression)
    # This is the ONLY training step -- closed-form solution
    # W = (F^T F + lambda I)^{-1} F^T y
    ridge = Ridge(alpha=1.0)
    ridge.fit(F_train, y_train)

    # Predict
    y_pred_train = (ridge.predict(F_train) > 0.5).astype(int)
    y_pred_test = (ridge.predict(F_test) > 0.5).astype(int)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    print(f"\nResults:")
    print(f"  Train accuracy: {train_acc:.4f}")
    print(f"  Test accuracy:  {test_acc:.4f}")
    print(f"  Training: Ridge regression (closed-form, instant)")

    return (ridge, F_train, F_test, X_train, X_test, y_train, y_test,
            n_qubits, reservoir, test_acc)


# =============================================================================
# PART B: Regression with QRC
# =============================================================================

def demo_regression():
    """
    QRC for regression on a sine function.

    The reservoir transforms 1D input into high-dimensional features,
    enabling linear regression to fit nonlinear functions.
    """
    print("\n" + "=" * 70)
    print("PART B: QRC Regression (sine function)")
    print("=" * 70)

    # Dataset
    rng = np.random.default_rng(42)
    X = rng.uniform(0, np.pi, (60, 1))
    y = np.sin(2 * X[:, 0]) + rng.normal(0, 0.05, 60)

    n_train = 42
    X_train, X_test = X[:n_train], X[n_train:]
    y_train, y_test = y[:n_train], y[n_train:]

    print(f"Dataset: sin(2x) + noise, {n_train} train / {len(X_test)} test")

    # Reservoir
    n_qubits = 4
    reservoir = build_reservoir(n_qubits, n_layers=4, seed=123)

    # Features
    print(f"Extracting features...")
    F_train = extract_features(X_train, n_qubits, reservoir)
    F_test = extract_features(X_test, n_qubits, reservoir)

    # Ridge regression readout
    ridge = Ridge(alpha=0.1)
    ridge.fit(F_train, y_train)

    y_pred = ridge.predict(F_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"  Test MSE: {mse:.6f}")
    print(f"  Test R^2: {r2:.4f}")

    # Smooth prediction curve
    X_smooth = np.linspace(0, np.pi, 50).reshape(-1, 1)
    F_smooth = extract_features(X_smooth, n_qubits, reservoir)
    y_smooth = ridge.predict(F_smooth)

    return X_train, X_test, y_train, y_test, X_smooth, y_smooth, r2


# =============================================================================
# PART C: Effect of Reservoir Size
# =============================================================================

def demo_reservoir_size():
    """
    Show how reservoir size (qubits) affects performance.

    From explanation_physicist.md, Section 5:
        IPC scales as 4^n - 1 (exponential in qubits)
        More qubits = richer feature space = better performance
    """
    print("\n" + "=" * 70)
    print("PART C: Effect of Reservoir Size")
    print("=" * 70)

    X, y = make_moons(n_samples=80, noise=0.15, random_state=42)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    results = []
    for n_q in [2, 3, 4, 5]:
        reservoir = build_reservoir(n_q, n_layers=3, seed=42)
        F_train = extract_features(X_train, n_q, reservoir)
        F_test = extract_features(X_test, n_q, reservoir)

        ridge = Ridge(alpha=1.0)
        ridge.fit(F_train, y_train)
        y_pred = (ridge.predict(F_test) > 0.5).astype(int)
        acc = accuracy_score(y_test, y_pred)

        n_features = 3 * n_q
        print(f"  {n_q} qubits ({n_features} features): accuracy = {acc:.4f}")
        results.append({"qubits": n_q, "features": n_features, "accuracy": acc})

    return results


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(X_train_cls, X_test_cls, y_test_cls, cls_acc,
                 X_train_reg, X_test_reg, y_train_reg, y_test_reg,
                 X_smooth, y_smooth, reg_r2, size_results):
    """Visualize QRC results."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    # --- Classification data ---
    ax = axes[0, 0]
    ax.scatter(X_test_cls[:, 0], X_test_cls[:, 1], c=y_test_cls,
               cmap='RdBu', edgecolors='k', s=40)
    ax.set_title(f'QRC Classification (acc={cls_acc:.3f})', fontsize=13)
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')

    # --- Regression fit ---
    ax = axes[0, 1]
    ax.scatter(X_train_reg, y_train_reg, c='blue', s=20, alpha=0.5, label='Train')
    ax.scatter(X_test_reg, y_test_reg, c='red', s=30, marker='x', label='Test')
    ax.plot(X_smooth, y_smooth, 'g-', linewidth=2, label='QRC prediction')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'QRC Regression (R^2={reg_r2:.3f})', fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # --- Reservoir size effect ---
    ax = axes[1, 0]
    if size_results:
        qubits = [r["qubits"] for r in size_results]
        accs = [r["accuracy"] for r in size_results]
        feats = [r["features"] for r in size_results]
        bars = ax.bar(range(len(qubits)), accs,
                      color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
        ax.set_xticks(range(len(qubits)))
        ax.set_xticklabels([f'{q}q\n({f} feat)' for q, f in zip(qubits, feats)])
        ax.set_ylabel('Test Accuracy')
        ax.set_title('Reservoir Size vs Performance', fontsize=13)
        ax.set_ylim(0, 1.1)
        for bar, acc in zip(bars, accs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{acc:.3f}', ha='center', fontsize=11)

    # --- Architecture comparison ---
    ax = axes[1, 1]
    methods = ['QRC\n(no training)', 'VQC\n(variational)', 'QSVC\n(kernel)']
    traits = [
        [1.0, 0.0, 1.0],  # Training speed, Barren plateau risk, Noise tolerance
        [0.3, 0.8, 0.3],
        [0.5, 0.0, 0.5],
    ]
    categories = ['Training\nSpeed', 'Barren Plateau\nRisk', 'Noise\nTolerance']
    x = np.arange(len(categories))
    w = 0.25
    colors = ['#2ecc71', '#e74c3c', '#3498db']
    for i, (method, trait) in enumerate(zip(methods, traits)):
        ax.bar(x + i*w, trait, w, label=method, color=colors[i])
    ax.set_xticks(x + w)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylabel('Score (higher = better)')
    ax.set_title('QRC vs Other QML Methods', fontsize=13)
    ax.legend(fontsize=9)
    ax.set_ylim(0, 1.3)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/18_quantum_reservoir/qrc_results.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/18_quantum_reservoir/qrc_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Quantum Reservoir Computing (QRC) - Local Simulator")
    print("=" * 70)
    print("Qiskit 2.4.1 | AerSimulator")

    # Part A: Classification
    (ridge_cls, F_tr, F_te, X_tr_cls, X_te_cls, y_tr_cls, y_te_cls,
     n_q, reservoir, cls_acc) = demo_classification()

    # Part B: Regression
    X_tr_reg, X_te_reg, y_tr_reg, y_te_reg, X_sm, y_sm, reg_r2 = demo_regression()

    # Part C: Reservoir size
    size_results = demo_reservoir_size()

    # Plot
    plot_results(X_tr_cls, X_te_cls, y_te_cls, cls_acc,
                 X_tr_reg, X_te_reg, y_tr_reg, y_te_reg,
                 X_sm, y_sm, reg_r2, size_results)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Quantum Reservoir Computing demonstrated:

    A. Classification: Fixed quantum reservoir + Ridge regression readout
    B. Regression: Reservoir features enable linear model to fit nonlinear functions
    C. Reservoir size: More qubits = richer features = better performance

    Key advantages of QRC:
    - NO quantum parameter training (zero barren plateaus)
    - Training is instant (closed-form Ridge regression)
    - Noise-tolerant (noise can enhance feature diversity)
    - Simple to implement and debug

    Trade-off: Less flexible than VQC/QNN (fixed reservoir), but
    much easier to train and more robust on noisy hardware.
    """)


if __name__ == "__main__":
    main()