"""
Quantum Boosted Ensemble (PQC Weak Learners + Classical AdaBoost) - Local Simulator
=====================================================================================

This script demonstrates quantum boosted ensemble classification:
    1. Shallow PQCs (2 qubits, 1 rep) serve as weak learners
    2. Classical AdaBoost combines them via weighted majority vote
    3. Each round trains a PQC on reweighted data
    4. Comparison with single deep VQC and classical AdaBoost

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Instead of using quantum optimization to SELECT classical classifiers (QBoost,
Topic 23), here we use quantum circuits AS the weak learners themselves.

Each weak learner is a shallow PQC:
    |0>^n --[ZFeatureMap(x)]--[RealAmplitudes(theta)]--[Measure Z_0]

Prediction: h(x) = sign(<Z_0>), where <Z_0> is the expectation value of Z
on qubit 0.

AdaBoost combines T weak learners:
    H(x) = sign(sum_{t=1}^{T} alpha_t * h_t(x))

where alpha_t = (1/2) * ln((1 - epsilon_t) / epsilon_t) weights each learner
by its performance. Sample weights are updated to focus on misclassified points.

Advantage for NISQ: shallow circuits have low gate error. Boosting combines
multiple noisy-but-cheap circuits instead of one deep expensive circuit.

References:
    - Freund & Schapire (1997). J. Comput. Syst. Sci. 55(1), 119-139
    - Schuld, Sweke, Meyer (2021). Phys. Rev. A 103(3), 032430
    - Abbas et al. (2021). Nat. Comput. Sci. 1(6), 403-409
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZFeatureMap, RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_algorithms.optimizers import COBYLA


# =============================================================================
# CONFIGURATION
# =============================================================================

np.random.seed(42)
SAVE_DIR = "quantum/algorithms/24_quantum_boosted_ensemble"


# =============================================================================
# STEP 1: DATA GENERATION
# =============================================================================

def create_data(n_samples=150):
    """
    Create a binary classification dataset from make_moons.

    Features are scaled to [0, pi] for quantum encoding.
    Labels are converted to {-1, +1} for AdaBoost compatibility.

    Parameters
    ----------
    n_samples : int
        Total number of samples.

    Returns
    -------
    X_train : ndarray, shape (n_train, 2)
        Training features in [0, pi].
    X_test : ndarray, shape (n_test, 2)
        Test features in [0, pi].
    y_train : ndarray, shape (n_train,)
        Training labels in {-1, +1}.
    y_test : ndarray, shape (n_test,)
        Test labels in {-1, +1}.
    """
    X, y = make_moons(n_samples=n_samples, noise=0.20, random_state=42)

    # Convert labels: {0, 1} -> {-1, +1}
    y = 2 * y - 1

    # Scale features to [0, pi]
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    return X_train, X_test, y_train, y_test


# =============================================================================
# STEP 2: BUILD WEAK PQC
# =============================================================================

def build_weak_pqc(num_qubits=2):
    """
    Build a SHALLOW parameterized quantum circuit for use as a weak learner.

    Architecture:
        ZFeatureMap(num_qubits, reps=1) + RealAmplitudes(num_qubits, reps=1)

    The shallow depth (reps=1) limits expressibility, making this a "weak"
    classifier that performs only slightly better than random. This is exactly
    what AdaBoost requires.

    Parameters
    ----------
    num_qubits : int
        Number of qubits (must match feature dimension).

    Returns
    -------
    circuit : QuantumCircuit
        The combined feature map + ansatz circuit (not yet bound).
    num_features : int
        Number of feature parameters (= num_qubits for ZFeatureMap reps=1).
    num_trainable : int
        Number of trainable parameters in the ansatz.
    """
    feature_map = ZFeatureMap(num_qubits, reps=1)
    ansatz = RealAmplitudes(num_qubits, reps=1, entanglement="linear")

    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    num_features = feature_map.num_parameters
    num_trainable = ansatz.num_parameters

    return circuit, num_features, num_trainable


# =============================================================================
# STEP 3: PQC PREDICTION
# =============================================================================

def predict_pqc(circuit, params, X, num_features):
    """
    Predict class labels {-1, +1} using a trained PQC.

    For each sample x:
        1. Bind feature parameters to x and trainable parameters to params
        2. Compute the statevector |psi(x, params)>
        3. Measure <Z_0> = <psi| Z tensor I |psi>
        4. Predict sign(<Z_0>)

    Parameters
    ----------
    circuit : QuantumCircuit
        The PQC circuit with unbound parameters.
    params : ndarray
        Trained parameter values for the ansatz.
    X : ndarray, shape (n_samples, n_features)
        Input data (each row is a sample).
    num_features : int
        Number of feature parameters in the circuit.

    Returns
    -------
    predictions : ndarray, shape (n_samples,)
        Predicted labels in {-1, +1}.
    raw_expectations : ndarray, shape (n_samples,)
        Raw <Z_0> expectation values (useful for debugging).
    """
    n_samples = X.shape[0]
    n_qubits = circuit.num_qubits
    predictions = np.zeros(n_samples)
    raw_expectations = np.zeros(n_samples)

    # Z operator on qubit 0: Z tensor I tensor I ...
    z_op = SparsePauliOp.from_list([("Z" + "I" * (n_qubits - 1), 1.0)])

    all_params = circuit.parameters
    feature_params = list(all_params[:num_features])
    trainable_params = list(all_params[num_features:])

    for i in range(n_samples):
        # Build parameter binding dictionary
        bind_dict = {}
        for j, fp in enumerate(feature_params):
            bind_dict[fp] = float(X[i, j])
        for j, tp in enumerate(trainable_params):
            bind_dict[tp] = float(params[j])

        bound_circuit = circuit.assign_parameters(bind_dict)
        sv = Statevector(bound_circuit)
        exp_val = sv.expectation_value(z_op).real

        raw_expectations[i] = exp_val
        predictions[i] = 1.0 if exp_val > 0 else -1.0

    return predictions, raw_expectations


# =============================================================================
# STEP 4: WEIGHTED PQC TRAINING
# =============================================================================

def train_weighted_pqc(circuit, num_features, X, y, weights, maxiter=50):
    """
    Train a PQC on weighted data using COBYLA optimizer.

    Loss function (weighted misclassification proxy):
        L(theta) = sum_i w_i * (1 - y_i * <Z_0>_i) / 2

    This loss is 0 when f(x_i) = y_i and 1 when f(x_i) = -y_i.
    Sample weights w_i = D_t(i) from AdaBoost ensure focus on hard examples.

    Parameters
    ----------
    circuit : QuantumCircuit
        The PQC circuit with unbound parameters.
    num_features : int
        Number of feature parameters.
    X : ndarray, shape (n_samples, n_features)
        Training data.
    y : ndarray, shape (n_samples,)
        Labels in {-1, +1}.
    weights : ndarray, shape (n_samples,)
        Sample weights D_t(i) from AdaBoost (sum to 1).
    maxiter : int
        Maximum number of COBYLA iterations.

    Returns
    -------
    optimal_params : ndarray
        Optimal trainable parameters.
    weighted_error : float
        Weighted classification error epsilon_t.
    """
    n_qubits = circuit.num_qubits
    all_params = circuit.parameters
    feature_params = list(all_params[:num_features])
    trainable_params = list(all_params[num_features:])
    num_trainable = len(trainable_params)

    # Z operator on qubit 0
    z_op = SparsePauliOp.from_list([("Z" + "I" * (n_qubits - 1), 1.0)])

    iteration_count = [0]

    def loss_fn(theta):
        """Compute weighted loss over all training samples."""
        total_loss = 0.0
        for i in range(len(X)):
            bind_dict = {}
            for j, fp in enumerate(feature_params):
                bind_dict[fp] = float(X[i, j])
            for j, tp in enumerate(trainable_params):
                bind_dict[tp] = float(theta[j])

            bound_circuit = circuit.assign_parameters(bind_dict)
            sv = Statevector(bound_circuit)
            exp_val = sv.expectation_value(z_op).real

            # Weighted hinge-like loss: w_i * (1 - y_i * <Z_0>) / 2
            sample_loss = weights[i] * (1.0 - y[i] * exp_val) / 2.0
            total_loss += sample_loss

        iteration_count[0] += 1
        return total_loss

    # Random initial parameters
    initial_params = np.random.uniform(-np.pi, np.pi, num_trainable)

    # Optimize with COBYLA
    optimizer = COBYLA(maxiter=maxiter)
    result = optimizer.minimize(fun=loss_fn, x0=initial_params)
    optimal_params = result.x

    # Compute weighted error
    predictions, _ = predict_pqc(circuit, optimal_params, X, num_features)
    misclassified = (predictions != y).astype(float)
    weighted_error = np.sum(weights * misclassified)

    # Clip error to avoid log(0) or negative alpha
    weighted_error = np.clip(weighted_error, 1e-10, 1.0 - 1e-10)

    return optimal_params, weighted_error


# =============================================================================
# STEP 5: QUANTUM ADABOOST
# =============================================================================

def adaboost_quantum(X_train, y_train, T=5, num_qubits=2):
    """
    Run AdaBoost with PQC weak learners.

    Algorithm (Freund & Schapire, 1997):
        1. Initialize uniform weights D_1(i) = 1/m
        2. For t = 1..T:
           a. Train PQC h_t on weighted data (D_t, X, y)
           b. Compute weighted error epsilon_t
           c. Compute learner weight alpha_t = (1/2) ln((1-eps)/(eps))
           d. Update D_{t+1}(i) proportional to D_t(i) exp(-alpha_t y_i h_t(x_i))
        3. Return list of (params_t, alpha_t) pairs

    Parameters
    ----------
    X_train : ndarray, shape (m, d)
        Training features.
    y_train : ndarray, shape (m,)
        Training labels in {-1, +1}.
    T : int
        Number of boosting rounds.
    num_qubits : int
        Number of qubits for each weak PQC.

    Returns
    -------
    classifiers_info : list of tuples
        Each element is (params_t, alpha_t) for one boosting round.
    circuit : QuantumCircuit
        The shared PQC architecture (same for all weak learners).
    num_features : int
        Number of feature parameters.
    round_errors : list of float
        Weighted error epsilon_t for each round.
    round_alphas : list of float
        Learner weight alpha_t for each round.
    """
    m = len(y_train)
    circuit, num_features, num_trainable = build_weak_pqc(num_qubits)

    # Initialize uniform sample weights
    D = np.ones(m) / m

    classifiers_info = []
    round_errors = []
    round_alphas = []

    print(f"\n  Running Quantum AdaBoost with T={T} rounds, {num_qubits} qubits, "
          f"{num_trainable} trainable params per weak learner\n")
    print(f"  {'Round':>5} | {'Epsilon_t':>10} | {'Alpha_t':>10} | {'Max Weight':>10}")
    print("  " + "-" * 50)

    for t in range(T):
        # Train weak PQC on weighted data
        params_t, epsilon_t = train_weighted_pqc(
            circuit, num_features, X_train, y_train, D, maxiter=50
        )

        # Compute learner weight
        alpha_t = 0.5 * np.log((1.0 - epsilon_t) / epsilon_t)

        # Store classifier info
        classifiers_info.append((params_t, alpha_t))
        round_errors.append(epsilon_t)
        round_alphas.append(alpha_t)

        # Update sample weights
        predictions, _ = predict_pqc(circuit, params_t, X_train, num_features)
        D = D * np.exp(-alpha_t * y_train * predictions)
        D = D / np.sum(D)  # Normalize

        print(f"  {t+1:>5} | {epsilon_t:>10.4f} | {alpha_t:>10.4f} | {np.max(D):>10.4f}")

    return classifiers_info, circuit, num_features, round_errors, round_alphas


# =============================================================================
# STEP 6: BOOSTED PREDICTION
# =============================================================================

def predict_boosted(classifiers_info, circuit, X, num_features):
    """
    Make predictions using the boosted ensemble.

    Final classifier:
        H(x) = sign(sum_{t=1}^{T} alpha_t * h_t(x))

    Parameters
    ----------
    classifiers_info : list of (params_t, alpha_t) tuples
        The trained weak learners and their weights.
    circuit : QuantumCircuit
        The shared PQC architecture.
    X : ndarray, shape (n_samples, n_features)
        Input data.
    num_features : int
        Number of feature parameters.

    Returns
    -------
    predictions : ndarray, shape (n_samples,)
        Ensemble predictions in {-1, +1}.
    weighted_sum : ndarray, shape (n_samples,)
        Raw weighted sum before sign (for decision boundary plotting).
    """
    n_samples = X.shape[0]
    weighted_sum = np.zeros(n_samples)

    for params_t, alpha_t in classifiers_info:
        preds_t, _ = predict_pqc(circuit, params_t, X, num_features)
        weighted_sum += alpha_t * preds_t

    predictions = np.sign(weighted_sum)
    predictions[predictions == 0] = 1.0  # Break ties toward +1

    return predictions, weighted_sum


# =============================================================================
# STEP 7: SINGLE DEEP VQC FOR COMPARISON
# =============================================================================

def train_single_deep_vqc(X_train, y_train, num_qubits=2, reps=3):
    """
    Train a single deep VQC (RealAmplitudes with reps=3) for comparison.

    This represents the alternative to boosting: use one deep circuit
    instead of many shallow ones.

    Parameters
    ----------
    X_train : ndarray, shape (n_train, 2)
        Training features.
    y_train : ndarray, shape (n_train,)
        Training labels in {-1, +1}.
    num_qubits : int
        Number of qubits.
    reps : int
        Number of repetition layers (higher = deeper circuit).

    Returns
    -------
    circuit : QuantumCircuit
        The deep VQC circuit.
    optimal_params : ndarray
        Optimal trainable parameters.
    num_features : int
        Number of feature parameters.
    """
    feature_map = ZFeatureMap(num_qubits, reps=1)
    ansatz = RealAmplitudes(num_qubits, reps=reps, entanglement="linear")

    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    num_features = feature_map.num_parameters
    num_trainable = ansatz.num_parameters
    n_qubits = circuit.num_qubits

    z_op = SparsePauliOp.from_list([("Z" + "I" * (n_qubits - 1), 1.0)])
    all_params = circuit.parameters
    feature_params = list(all_params[:num_features])
    trainable_params = list(all_params[num_features:])

    def loss_fn(theta):
        total_loss = 0.0
        for i in range(len(X_train)):
            bind_dict = {}
            for j, fp in enumerate(feature_params):
                bind_dict[fp] = float(X_train[i, j])
            for j, tp in enumerate(trainable_params):
                bind_dict[tp] = float(theta[j])

            bound_circuit = circuit.assign_parameters(bind_dict)
            sv = Statevector(bound_circuit)
            exp_val = sv.expectation_value(z_op).real

            sample_loss = (1.0 - y_train[i] * exp_val) / 2.0
            total_loss += sample_loss / len(X_train)

        return total_loss

    initial_params = np.random.uniform(-np.pi, np.pi, num_trainable)

    print(f"  Training single deep VQC: {num_qubits} qubits, reps={reps}, "
          f"{num_trainable} parameters...")

    optimizer = COBYLA(maxiter=100)
    result = optimizer.minimize(fun=loss_fn, x0=initial_params)

    return circuit, result.x, num_features


# =============================================================================
# STEP 8: VISUALIZATION
# =============================================================================

def plot_decision_boundary(ax, predict_fn, X, y, title, resolution=50):
    """
    Plot the decision boundary for a classifier on a 2D dataset.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Subplot axis to plot on.
    predict_fn : callable
        Function that takes X and returns predictions.
    X : ndarray, shape (n_samples, 2)
        Data points for scatter overlay.
    y : ndarray, shape (n_samples,)
        True labels for scatter coloring.
    title : str
        Subplot title.
    resolution : int
        Grid resolution for the boundary mesh.
    """
    x_min, x_max = X[:, 0].min() - 0.3, X[:, 0].max() + 0.3
    y_min, y_max = X[:, 1].min() - 0.3, X[:, 1].max() + 0.3

    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, resolution),
        np.linspace(y_min, y_max, resolution)
    )
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = predict_fn(grid_points)
    Z = Z.reshape(xx.shape)

    ax.contourf(xx, yy, Z, levels=[-2, 0, 2], colors=["#FFCCCC", "#CCCCFF"], alpha=0.6)
    ax.contour(xx, yy, Z, levels=[0], colors=["black"], linewidths=1.5)
    ax.scatter(X[y == -1, 0], X[y == -1, 1], c="red", marker="o",
               edgecolors="k", s=30, label="Class -1")
    ax.scatter(X[y == 1, 0], X[y == 1, 1], c="blue", marker="^",
               edgecolors="k", s=30, label="Class +1")
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Feature 0")
    ax.set_ylabel("Feature 1")
    ax.legend(fontsize=7, loc="upper left")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("QUANTUM BOOSTED ENSEMBLE (PQC Weak Learners + Classical AdaBoost)")
    print("=" * 70)

    # -----------------------------------------------------------------
    # STEP 1: Generate data
    # -----------------------------------------------------------------
    print("\n[STEP 1] Generating make_moons dataset...")
    X_train, X_test, y_train, y_test = create_data(n_samples=150)
    print(f"  Train: {len(X_train)} samples | Test: {len(X_test)} samples")
    print(f"  Features scaled to [0, pi]")
    print(f"  Labels: {{-1, +1}}")
    print(f"  Class balance (train): +1={np.sum(y_train == 1)}, -1={np.sum(y_train == -1)}")

    # -----------------------------------------------------------------
    # STEP 2: Build weak PQC and display
    # -----------------------------------------------------------------
    print("\n[STEP 2] Building weak PQC architecture...")
    demo_circuit, n_feat, n_train_params = build_weak_pqc(num_qubits=2)
    print(f"  Qubits: 2")
    print(f"  Feature parameters: {n_feat}")
    print(f"  Trainable parameters: {n_train_params}")
    print(f"  Feature map: ZFeatureMap(2, reps=1)")
    print(f"  Ansatz: RealAmplitudes(2, reps=1, entanglement='linear')")
    print(f"\n  Circuit:\n{demo_circuit.draw(output='text')}")

    # -----------------------------------------------------------------
    # STEP 3: Run Quantum AdaBoost
    # -----------------------------------------------------------------
    print("\n[STEP 3] Running Quantum AdaBoost (T=5 rounds)...")
    classifiers_info, circuit, num_features, round_errors, round_alphas = (
        adaboost_quantum(X_train, y_train, T=5, num_qubits=2)
    )

    # -----------------------------------------------------------------
    # STEP 4: Evaluate boosted ensemble on test data
    # -----------------------------------------------------------------
    print("\n[STEP 4] Evaluating boosted ensemble on test data...")
    y_pred_boosted_train, _ = predict_boosted(
        classifiers_info, circuit, X_train, num_features
    )
    y_pred_boosted_test, _ = predict_boosted(
        classifiers_info, circuit, X_test, num_features
    )
    acc_boosted_train = accuracy_score(y_train, y_pred_boosted_train)
    acc_boosted_test = accuracy_score(y_test, y_pred_boosted_test)
    print(f"  Boosted PQC Ensemble (T=5):")
    print(f"    Train accuracy: {acc_boosted_train:.4f}")
    print(f"    Test accuracy:  {acc_boosted_test:.4f}")

    # -----------------------------------------------------------------
    # STEP 5: Train single deep VQC for comparison
    # -----------------------------------------------------------------
    print("\n[STEP 5] Training single deep VQC for comparison...")
    deep_circuit, deep_params, deep_n_feat = train_single_deep_vqc(
        X_train, y_train, num_qubits=2, reps=3
    )
    y_pred_deep_train, _ = predict_pqc(deep_circuit, deep_params, X_train, deep_n_feat)
    y_pred_deep_test, _ = predict_pqc(deep_circuit, deep_params, X_test, deep_n_feat)
    acc_deep_train = accuracy_score(y_train, y_pred_deep_train)
    acc_deep_test = accuracy_score(y_test, y_pred_deep_test)
    print(f"  Single Deep VQC (reps=3):")
    print(f"    Train accuracy: {acc_deep_train:.4f}")
    print(f"    Test accuracy:  {acc_deep_test:.4f}")

    # -----------------------------------------------------------------
    # STEP 6: Run classical AdaBoost (sklearn) for comparison
    # -----------------------------------------------------------------
    print("\n[STEP 6] Running classical AdaBoost (sklearn)...")
    clf_classical = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1),
        n_estimators=5,
        algorithm="SAMME",
        random_state=42,
    )
    clf_classical.fit(X_train, y_train)
    y_pred_classical_train = clf_classical.predict(X_train)
    y_pred_classical_test = clf_classical.predict(X_test)
    acc_classical_train = accuracy_score(y_train, y_pred_classical_train)
    acc_classical_test = accuracy_score(y_test, y_pred_classical_test)
    print(f"  Classical AdaBoost (T=5, decision stumps):")
    print(f"    Train accuracy: {acc_classical_train:.4f}")
    print(f"    Test accuracy:  {acc_classical_test:.4f}")

    # -----------------------------------------------------------------
    # STEP 7: Comparison table
    # -----------------------------------------------------------------
    print("\n[STEP 7] Comparison Table")
    print("=" * 70)
    print(f"  {'Method':<35} {'Train Acc':>10} {'Test Acc':>10}")
    print("  " + "-" * 57)
    print(f"  {'Boosted PQC Ensemble (T=5)':<35} {acc_boosted_train:>10.4f} {acc_boosted_test:>10.4f}")
    print(f"  {'Single Deep VQC (reps=3)':<35} {acc_deep_train:>10.4f} {acc_deep_test:>10.4f}")
    print(f"  {'Classical AdaBoost (T=5)':<35} {acc_classical_train:>10.4f} {acc_classical_test:>10.4f}")
    print("=" * 70)

    # -----------------------------------------------------------------
    # STEP 8: Visualization (2x2 plot)
    # -----------------------------------------------------------------
    print("\n[STEP 8] Generating visualization...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    fig.suptitle(
        "Quantum Boosted Ensemble: PQC Weak Learners + Classical AdaBoost",
        fontsize=14, fontweight="bold"
    )

    # --- (0,0) Weak learner errors + alpha weights across boosting rounds ---
    ax0 = axes[0, 0]
    rounds = np.arange(1, len(round_errors) + 1)
    bar_width = 0.35
    bars1 = ax0.bar(rounds - bar_width / 2, round_errors, bar_width,
                    color="salmon", edgecolor="black", label="Epsilon_t (error)")
    bars2 = ax0.bar(rounds + bar_width / 2, round_alphas, bar_width,
                    color="steelblue", edgecolor="black", label="Alpha_t (weight)")
    ax0.set_xlabel("Boosting Round")
    ax0.set_ylabel("Value")
    ax0.set_title("Per-Round Error and Learner Weight")
    ax0.set_xticks(rounds)
    ax0.axhline(y=0.5, color="red", linestyle="--", linewidth=0.8, label="Random (0.5)")
    ax0.legend(fontsize=8)
    ax0.set_ylim(0, max(max(round_errors), max(round_alphas)) * 1.3)

    # --- (0,1) Accuracy comparison bar chart ---
    ax1 = axes[0, 1]
    methods = ["Boosted PQC\n(T=5)", "Single Deep\nVQC (reps=3)", "Classical\nAdaBoost (T=5)"]
    train_accs = [acc_boosted_train, acc_deep_train, acc_classical_train]
    test_accs = [acc_boosted_test, acc_deep_test, acc_classical_test]
    x_pos = np.arange(len(methods))
    bars_train = ax1.bar(x_pos - 0.2, train_accs, 0.35, color="lightgreen",
                         edgecolor="black", label="Train")
    bars_test = ax1.bar(x_pos + 0.2, test_accs, 0.35, color="mediumpurple",
                        edgecolor="black", label="Test")
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(methods, fontsize=9)
    ax1.set_ylabel("Accuracy")
    ax1.set_title("Accuracy Comparison")
    ax1.set_ylim(0.0, 1.1)
    ax1.axhline(y=0.5, color="red", linestyle="--", linewidth=0.8, label="Random")
    ax1.legend(fontsize=8)
    for bar in bars_train + bars_test:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.02,
                 f"{height:.2f}", ha="center", va="bottom", fontsize=8)

    # --- (1,0) Decision boundary for boosted quantum ensemble ---
    def boosted_predict_fn(X_grid):
        preds, _ = predict_boosted(classifiers_info, circuit, X_grid, num_features)
        return preds

    plot_decision_boundary(
        axes[1, 0], boosted_predict_fn, X_test, y_test,
        "Boosted PQC Ensemble (T=5)", resolution=40
    )

    # --- (1,1) Decision boundary for single deep VQC ---
    def deep_predict_fn(X_grid):
        preds, _ = predict_pqc(deep_circuit, deep_params, X_grid, deep_n_feat)
        return preds

    plot_decision_boundary(
        axes[1, 1], deep_predict_fn, X_test, y_test,
        "Single Deep VQC (reps=3)", resolution=40
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_path = f"{SAVE_DIR}/quantum_boosted_ensemble_results.png"
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved figure to: {save_path}")

    # -----------------------------------------------------------------
    # STEP 9: Summary
    # -----------------------------------------------------------------
    print("\n[STEP 9] Summary")
    print("=" * 70)
    print("  Quantum Boosted Ensemble combines shallow PQC weak learners")
    print("  with classical AdaBoost to build a strong classifier.")
    print()
    print("  Key results:")
    print(f"  - Boosted PQC (5 rounds, 4 params each): test acc = {acc_boosted_test:.4f}")
    print(f"  - Single deep VQC (reps=3, 8 params):    test acc = {acc_deep_test:.4f}")
    print(f"  - Classical AdaBoost (5 stumps):          test acc = {acc_classical_test:.4f}")
    print()
    print("  NISQ advantage: each weak PQC uses only reps=1 (very shallow).")
    print("  Lower gate errors per circuit. Boosting compensates for weakness.")
    print("  Total ensemble parameters: 5 * 4 = 20 (distributed across")
    print("  5 independent shallow circuits, not one deep circuit).")
    print("=" * 70)


if __name__ == "__main__":
    main()
