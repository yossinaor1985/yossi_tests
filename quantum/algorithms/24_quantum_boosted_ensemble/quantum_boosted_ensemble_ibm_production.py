"""
Quantum Boosted Ensemble (PQC Weak Learners + Classical AdaBoost) - IBM Production
====================================================================================

Production-ready pipeline for quantum boosted ensemble classification:
    1. Configurable PQC weak learner architecture
    2. AdaBoost loop with PQC training and sample reweighting
    3. Comparison against single deep VQC and classical AdaBoost
    4. JSON result persistence
    5. IBM hardware integration (commented out, ready to uncomment)

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Each weak learner is a shallow PQC: ZFeatureMap + RealAmplitudes (reps=1).
Prediction: h(x) = sign(<Z_0>).
AdaBoost combines T weak learners: H(x) = sign(sum alpha_t h_t(x)).
Shallow circuits reduce hardware errors; boosting compensates for weakness.

Production Notes:
    - Shallow circuits (reps=1) minimize decoherence and gate errors
    - Weak learners can be trained in parallel on multiple QPUs
    - Sample weighting can be implemented via shot allocation
    - Scaling: O(T * m * maxiter) circuit evaluations total
    - Warm-start: use previous round's parameters as initialization

References:
    - Freund & Schapire (1997). J. Comput. Syst. Sci. 55(1), 119-139
    - Schuld, Sweke, Meyer (2021). Phys. Rev. A 103(3), 032430
    - Abbas et al. (2021). Nat. Comput. Sci. 1(6), 403-409
"""

import json
import os
from datetime import datetime

import numpy as np
import matplotlib
matplotlib.use("Agg")

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZFeatureMap, RealAmplitudes
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_algorithms.optimizers import COBYLA


# =============================================================================
# IBM RUNTIME (uncomment for real hardware deployment)
# =============================================================================
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session
# service = QiskitRuntimeService(channel="ibm_quantum")
# backend = service.least_busy(min_num_qubits=NUM_QUBITS, operational=True)


# =============================================================================
# CONFIGURATION
# =============================================================================

N_BOOSTING_ROUNDS = 5          # Number of AdaBoost rounds (T)
PQC_REPS = 1                   # Repetition layers for weak PQC (keep shallow!)
DEEP_VQC_REPS = 3              # Repetition layers for comparison deep VQC
NUM_QUBITS = 2                 # Qubits per weak learner
N_SAMPLES = 150                # Total dataset size
TEST_SIZE = 0.3                # Train/test split ratio
COBYLA_MAXITER_WEAK = 50       # Max optimizer iterations per weak learner
COBYLA_MAXITER_DEEP = 100      # Max optimizer iterations for deep VQC
WARM_START = True              # Use previous round params as initialization
RANDOM_SEED = 42               # Reproducibility seed

RESULTS_DIR = "quantum/algorithms/24_quantum_boosted_ensemble/results"
RESULTS_FILE = "quantum_boosted_ensemble_results.json"


# =============================================================================
# DATASET
# =============================================================================

def create_problem(n_samples=N_SAMPLES, test_size=TEST_SIZE):
    """
    Generate a binary classification problem for ensemble demonstration.

    Creates make_moons data, converts labels to {-1, +1}, scales
    features to [0, pi], and splits into train/test.

    Parameters
    ----------
    n_samples : int
        Total number of samples.
    test_size : float
        Fraction reserved for testing.

    Returns
    -------
    X_train, X_test : ndarray
        Feature matrices scaled to [0, pi].
    y_train, y_test : ndarray
        Label vectors in {-1, +1}.
    """
    np.random.seed(RANDOM_SEED)

    X, y = make_moons(n_samples=n_samples, noise=0.20, random_state=RANDOM_SEED)
    y = 2 * y - 1  # Convert {0, 1} -> {-1, +1}

    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_SEED, stratify=y
    )

    print(f"  Dataset: {n_samples} samples, 2 features (make_moons)")
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"  Class balance (train): +1={np.sum(y_train == 1)}, "
          f"-1={np.sum(y_train == -1)}")

    return X_train, X_test, y_train, y_test


# =============================================================================
# PQC BUILDING
# =============================================================================

def build_pqc(num_qubits=NUM_QUBITS, reps=PQC_REPS):
    """
    Build a parameterized quantum circuit.

    Architecture:
        ZFeatureMap(num_qubits, reps=1) + RealAmplitudes(num_qubits, reps=reps)

    Parameters
    ----------
    num_qubits : int
        Number of qubits.
    reps : int
        Number of ansatz repetition layers.

    Returns
    -------
    circuit : QuantumCircuit
        The combined circuit with unbound parameters.
    num_features : int
        Number of feature parameters.
    num_trainable : int
        Number of trainable ansatz parameters.
    """
    feature_map = ZFeatureMap(num_qubits, reps=1)
    ansatz = RealAmplitudes(num_qubits, reps=reps, entanglement="linear")

    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    num_features = feature_map.num_parameters
    num_trainable = ansatz.num_parameters

    return circuit, num_features, num_trainable


# =============================================================================
# PQC INFERENCE
# =============================================================================

def predict_pqc(circuit, params, X, num_features):
    """
    Predict labels using a PQC via statevector simulation.

    For each sample: bind parameters -> statevector -> <Z_0> -> sign.

    Parameters
    ----------
    circuit : QuantumCircuit
        PQC with unbound parameters.
    params : ndarray
        Trainable parameter values.
    X : ndarray, shape (n_samples, n_features)
        Input data.
    num_features : int
        Number of feature parameters.

    Returns
    -------
    predictions : ndarray, shape (n_samples,)
        Labels in {-1, +1}.
    expectations : ndarray, shape (n_samples,)
        Raw <Z_0> values.
    """
    n_samples = X.shape[0]
    n_qubits = circuit.num_qubits
    predictions = np.zeros(n_samples)
    expectations = np.zeros(n_samples)

    z_op = SparsePauliOp.from_list([("Z" + "I" * (n_qubits - 1), 1.0)])

    all_params = circuit.parameters
    feature_params = list(all_params[:num_features])
    trainable_params = list(all_params[num_features:])

    for i in range(n_samples):
        bind_dict = {}
        for j, fp in enumerate(feature_params):
            bind_dict[fp] = float(X[i, j])
        for j, tp in enumerate(trainable_params):
            bind_dict[tp] = float(params[j])

        bound_circuit = circuit.assign_parameters(bind_dict)
        sv = Statevector(bound_circuit)
        exp_val = sv.expectation_value(z_op).real

        expectations[i] = exp_val
        predictions[i] = 1.0 if exp_val > 0 else -1.0

    return predictions, expectations


# =============================================================================
# WEIGHTED PQC TRAINING
# =============================================================================

def train_weighted_pqc(circuit, num_features, X, y, weights,
                       maxiter=COBYLA_MAXITER_WEAK, initial_params=None):
    """
    Train a PQC on weighted data using COBYLA.

    Loss: L(theta) = sum_i w_i * (1 - y_i * <Z_0>_i) / 2

    Supports warm-start via initial_params from a previous round.

    Parameters
    ----------
    circuit : QuantumCircuit
        PQC with unbound parameters.
    num_features : int
        Number of feature parameters.
    X : ndarray, shape (n_samples, n_features)
        Training data.
    y : ndarray, shape (n_samples,)
        Labels in {-1, +1}.
    weights : ndarray, shape (n_samples,)
        Sample weights from AdaBoost (sum to 1).
    maxiter : int
        Maximum COBYLA iterations.
    initial_params : ndarray or None
        Warm-start parameters. If None, uses random initialization.

    Returns
    -------
    optimal_params : ndarray
        Optimized trainable parameters.
    weighted_error : float
        Weighted error epsilon_t.
    final_loss : float
        Final loss value.
    """
    n_qubits = circuit.num_qubits
    all_params = circuit.parameters
    feature_params = list(all_params[:num_features])
    trainable_params = list(all_params[num_features:])
    num_trainable = len(trainable_params)

    z_op = SparsePauliOp.from_list([("Z" + "I" * (n_qubits - 1), 1.0)])

    def loss_fn(theta):
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

            sample_loss = weights[i] * (1.0 - y[i] * exp_val) / 2.0
            total_loss += sample_loss

        return total_loss

    # Initialize: warm-start or random
    if initial_params is not None and len(initial_params) == num_trainable:
        x0 = initial_params.copy()
    else:
        x0 = np.random.uniform(-np.pi, np.pi, num_trainable)

    optimizer = COBYLA(maxiter=maxiter)
    result = optimizer.minimize(fun=loss_fn, x0=x0)
    optimal_params = result.x
    final_loss = result.fun

    # Compute weighted error
    predictions, _ = predict_pqc(circuit, optimal_params, X, num_features)
    misclassified = (predictions != y).astype(float)
    weighted_error = np.sum(weights * misclassified)
    weighted_error = np.clip(weighted_error, 1e-10, 1.0 - 1e-10)

    return optimal_params, weighted_error, final_loss


# =============================================================================
# QUANTUM ADABOOST
# =============================================================================

def adaboost_quantum(X_train, y_train, T=N_BOOSTING_ROUNDS,
                     num_qubits=NUM_QUBITS, warm_start=WARM_START):
    """
    Run AdaBoost with PQC weak learners.

    Implements the full Freund-Schapire AdaBoost algorithm with parameterized
    quantum circuits as the weak hypothesis class.

    Parameters
    ----------
    X_train : ndarray, shape (m, d)
        Training features.
    y_train : ndarray, shape (m,)
        Training labels in {-1, +1}.
    T : int
        Number of boosting rounds.
    num_qubits : int
        Qubits per weak PQC.
    warm_start : bool
        If True, use previous round's parameters as initialization.

    Returns
    -------
    classifiers_info : list of (params_t, alpha_t) tuples
    circuit : QuantumCircuit
    num_features : int
    round_details : list of dict
        Per-round metrics: error, alpha, loss, max_weight.
    """
    m = len(y_train)
    circuit, num_features, num_trainable = build_pqc(num_qubits, reps=PQC_REPS)

    D = np.ones(m) / m  # Uniform initial weights
    classifiers_info = []
    round_details = []
    prev_params = None

    print(f"\n  Quantum AdaBoost: T={T}, qubits={num_qubits}, "
          f"PQC_reps={PQC_REPS}, params/learner={num_trainable}, "
          f"warm_start={warm_start}")
    print(f"  {'Round':>5} | {'Epsilon':>9} | {'Alpha':>9} | "
          f"{'Loss':>9} | {'Max Wt':>9}")
    print("  " + "-" * 55)

    for t in range(T):
        # Warm-start: pass previous params if enabled
        init_p = prev_params if (warm_start and prev_params is not None) else None

        params_t, epsilon_t, loss_t = train_weighted_pqc(
            circuit, num_features, X_train, y_train, D,
            maxiter=COBYLA_MAXITER_WEAK, initial_params=init_p
        )

        alpha_t = 0.5 * np.log((1.0 - epsilon_t) / epsilon_t)

        classifiers_info.append((params_t, alpha_t))
        prev_params = params_t

        # Update sample weights
        predictions, _ = predict_pqc(circuit, params_t, X_train, num_features)
        D = D * np.exp(-alpha_t * y_train * predictions)
        D = D / np.sum(D)

        round_info = {
            "round": t + 1,
            "epsilon_t": float(epsilon_t),
            "alpha_t": float(alpha_t),
            "loss": float(loss_t),
            "max_weight": float(np.max(D)),
            "params": params_t.tolist()
        }
        round_details.append(round_info)

        print(f"  {t+1:>5} | {epsilon_t:>9.4f} | {alpha_t:>9.4f} | "
              f"{loss_t:>9.4f} | {np.max(D):>9.4f}")

    return classifiers_info, circuit, num_features, round_details


def predict_boosted(classifiers_info, circuit, X, num_features):
    """
    Weighted majority vote: H(x) = sign(sum alpha_t h_t(x)).

    Parameters
    ----------
    classifiers_info : list of (params_t, alpha_t)
    circuit : QuantumCircuit
    X : ndarray
    num_features : int

    Returns
    -------
    predictions : ndarray, labels in {-1, +1}
    weighted_sum : ndarray, raw scores before sign
    """
    n_samples = X.shape[0]
    weighted_sum = np.zeros(n_samples)

    for params_t, alpha_t in classifiers_info:
        preds_t, _ = predict_pqc(circuit, params_t, X, num_features)
        weighted_sum += alpha_t * preds_t

    predictions = np.sign(weighted_sum)
    predictions[predictions == 0] = 1.0

    return predictions, weighted_sum


# =============================================================================
# SINGLE DEEP VQC (COMPARISON BASELINE)
# =============================================================================

def train_single_deep_vqc(X_train, y_train, num_qubits=NUM_QUBITS,
                          reps=DEEP_VQC_REPS):
    """
    Train a single deep VQC for comparison with the boosted ensemble.

    Uses RealAmplitudes with more repetition layers (deeper circuit).

    Parameters
    ----------
    X_train : ndarray
        Training features.
    y_train : ndarray
        Training labels in {-1, +1}.
    num_qubits : int
        Number of qubits.
    reps : int
        Ansatz repetition layers.

    Returns
    -------
    circuit : QuantumCircuit
    optimal_params : ndarray
    num_features : int
    final_loss : float
    """
    circuit, num_features, num_trainable = build_pqc(num_qubits, reps=reps)
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

    x0 = np.random.uniform(-np.pi, np.pi, num_trainable)

    print(f"  Deep VQC: {num_qubits} qubits, reps={reps}, "
          f"{num_trainable} params, maxiter={COBYLA_MAXITER_DEEP}")

    optimizer = COBYLA(maxiter=COBYLA_MAXITER_DEEP)
    result = optimizer.minimize(fun=loss_fn, x0=x0)

    return circuit, result.x, num_features, float(result.fun)


# =============================================================================
# CLASSICAL BASELINE
# =============================================================================

def run_classical_adaboost(X_train, y_train, X_test, y_test):
    """
    Run sklearn AdaBoost with decision stumps for comparison.

    Parameters
    ----------
    X_train, y_train, X_test, y_test : ndarray
        Standard train/test split.

    Returns
    -------
    results : dict
        Train/test accuracies and predictions.
    """
    clf = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1),
        n_estimators=N_BOOSTING_ROUNDS,
        algorithm="SAMME",
        random_state=RANDOM_SEED,
    )
    clf.fit(X_train, y_train)

    y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)

    return {
        "train_accuracy": float(accuracy_score(y_train, y_pred_train)),
        "test_accuracy": float(accuracy_score(y_test, y_pred_test)),
        "y_pred_train": y_pred_train.tolist(),
        "y_pred_test": y_pred_test.tolist()
    }


# =============================================================================
# PRODUCTION PIPELINE
# =============================================================================

def run_production():
    """
    Execute the full quantum boosted ensemble production pipeline.

    Steps:
        1. Create problem (dataset, train/test split)
        2. Run quantum AdaBoost with PQC weak learners
        3. Evaluate boosted ensemble
        4. Train single deep VQC baseline
        5. Run classical AdaBoost baseline
        6. Compare all methods
        7. Save results to JSON
        8. Print production notes
    """
    print("=" * 70)
    print("QUANTUM BOOSTED ENSEMBLE - Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Backend: Statevector (production would use IBM hardware)")
    print(f"Config: T={N_BOOSTING_ROUNDS}, PQC_reps={PQC_REPS}, "
          f"qubits={NUM_QUBITS}, warm_start={WARM_START}")
    print()

    # --- Step 1: Create problem ---
    print("[1/8] Creating problem...")
    X_train, X_test, y_train, y_test = create_problem()
    print()

    # --- Step 2: Quantum AdaBoost ---
    print("[2/8] Running Quantum AdaBoost...")
    classifiers_info, circuit, num_features, round_details = adaboost_quantum(
        X_train, y_train
    )
    print()

    # --- Step 3: Evaluate boosted ensemble ---
    print("[3/8] Evaluating boosted ensemble...")
    y_pred_boost_train, _ = predict_boosted(
        classifiers_info, circuit, X_train, num_features
    )
    y_pred_boost_test, _ = predict_boosted(
        classifiers_info, circuit, X_test, num_features
    )
    acc_boost_train = float(accuracy_score(y_train, y_pred_boost_train))
    acc_boost_test = float(accuracy_score(y_test, y_pred_boost_test))
    print(f"  Boosted PQC Ensemble:")
    print(f"    Train accuracy: {acc_boost_train:.4f}")
    print(f"    Test accuracy:  {acc_boost_test:.4f}")
    print()

    # --- Step 4: Single deep VQC ---
    print("[4/8] Training single deep VQC baseline...")
    deep_circuit, deep_params, deep_n_feat, deep_loss = train_single_deep_vqc(
        X_train, y_train
    )
    y_pred_deep_train, _ = predict_pqc(
        deep_circuit, deep_params, X_train, deep_n_feat
    )
    y_pred_deep_test, _ = predict_pqc(
        deep_circuit, deep_params, X_test, deep_n_feat
    )
    acc_deep_train = float(accuracy_score(y_train, y_pred_deep_train))
    acc_deep_test = float(accuracy_score(y_test, y_pred_deep_test))
    print(f"  Single Deep VQC (reps={DEEP_VQC_REPS}):")
    print(f"    Train accuracy: {acc_deep_train:.4f}")
    print(f"    Test accuracy:  {acc_deep_test:.4f}")
    print()

    # --- Step 5: Classical AdaBoost ---
    print("[5/8] Running classical AdaBoost baseline...")
    classical_results = run_classical_adaboost(X_train, y_train, X_test, y_test)
    print(f"  Classical AdaBoost (T={N_BOOSTING_ROUNDS}, decision stumps):")
    print(f"    Train accuracy: {classical_results['train_accuracy']:.4f}")
    print(f"    Test accuracy:  {classical_results['test_accuracy']:.4f}")
    print()

    # --- Step 6: Comparison ---
    print("[6/8] Results comparison:")
    print("-" * 65)
    print(f"  {'Method':<35} {'Train Acc':>10} {'Test Acc':>10}")
    print("  " + "-" * 57)
    print(f"  {'Boosted PQC Ensemble (T=' + str(N_BOOSTING_ROUNDS) + ')':<35} "
          f"{acc_boost_train:>10.4f} {acc_boost_test:>10.4f}")
    print(f"  {'Single Deep VQC (reps=' + str(DEEP_VQC_REPS) + ')':<35} "
          f"{acc_deep_train:>10.4f} {acc_deep_test:>10.4f}")
    print(f"  {'Classical AdaBoost (T=' + str(N_BOOSTING_ROUNDS) + ')':<35} "
          f"{classical_results['train_accuracy']:>10.4f} "
          f"{classical_results['test_accuracy']:>10.4f}")
    print("-" * 65)
    print()

    # --- Step 7: Save results ---
    print("[7/8] Saving results...")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    results = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "Quantum Boosted Ensemble (PQC + AdaBoost)",
        "qiskit_version": "2.4.1",
        "config": {
            "n_boosting_rounds": N_BOOSTING_ROUNDS,
            "pqc_reps": PQC_REPS,
            "deep_vqc_reps": DEEP_VQC_REPS,
            "num_qubits": NUM_QUBITS,
            "n_samples": N_SAMPLES,
            "test_size": TEST_SIZE,
            "cobyla_maxiter_weak": COBYLA_MAXITER_WEAK,
            "cobyla_maxiter_deep": COBYLA_MAXITER_DEEP,
            "warm_start": WARM_START,
            "random_seed": RANDOM_SEED,
            "backend": "Statevector (production: IBM hardware)",
            "feature_map": "ZFeatureMap(2, reps=1)",
            "ansatz_weak": f"RealAmplitudes(2, reps={PQC_REPS}, entanglement='linear')",
            "ansatz_deep": f"RealAmplitudes(2, reps={DEEP_VQC_REPS}, entanglement='linear')",
        },
        "dataset_info": {
            "source": "make_moons",
            "n_samples": N_SAMPLES,
            "n_features": 2,
            "n_train": int(len(y_train)),
            "n_test": int(len(y_test)),
            "class_balance_train": {
                "+1": int(np.sum(y_train == 1)),
                "-1": int(np.sum(y_train == -1)),
            },
            "feature_range": "[0, pi]",
            "label_set": "{-1, +1}",
        },
        "boosted_ensemble": {
            "train_accuracy": acc_boost_train,
            "test_accuracy": acc_boost_test,
            "n_weak_learners": N_BOOSTING_ROUNDS,
            "params_per_learner": int(round_details[0]["params"].__len__()),
            "total_params": N_BOOSTING_ROUNDS * len(round_details[0]["params"]),
            "round_details": round_details,
        },
        "single_deep_vqc": {
            "train_accuracy": acc_deep_train,
            "test_accuracy": acc_deep_test,
            "reps": DEEP_VQC_REPS,
            "final_loss": deep_loss,
            "params": deep_params.tolist(),
        },
        "classical_adaboost": {
            "train_accuracy": classical_results["train_accuracy"],
            "test_accuracy": classical_results["test_accuracy"],
            "n_estimators": N_BOOSTING_ROUNDS,
            "base_learner": "DecisionTreeClassifier(max_depth=1)",
        },
    }

    results_path = os.path.join(RESULTS_DIR, RESULTS_FILE)
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved results to: {results_path}")
    print()

    # --- Step 8: Production notes ---
    print("[8/8] Production Notes")
    print("=" * 70)
    print("  1. SHALLOW CIRCUITS REDUCE HARDWARE ERRORS")
    print(f"     Each weak PQC uses reps={PQC_REPS} (minimal depth).")
    print("     Gate fidelity: F ~ exp(-N_gates * p_error).")
    print(f"     Shallow PQC: ~{2 + 2 * NUM_QUBITS} gates vs deep VQC: "
          f"~{2 + (DEEP_VQC_REPS + 1) * NUM_QUBITS + DEEP_VQC_REPS} gates.")
    print()
    print("  2. PARALLEL TRAINING OF WEAK LEARNERS")
    print("     While boosting rounds are sequential (D_t depends on h_{t-1}),")
    print("     within each round, circuit evaluations for different samples")
    print("     can be parallelized across multiple QPUs.")
    print()
    print("  3. SAMPLE WEIGHTING VIA SHOT ALLOCATION")
    print("     Alternative to loss-function weighting: allocate shots")
    print("     proportional to D_t(i). High-weight samples get more shots,")
    print("     reducing measurement noise where it matters most.")
    print()
    print("  4. SCALING WITH BOOSTING ROUNDS")
    print(f"     Total circuit evaluations: O(T * m * maxiter)")
    print(f"     Current: {N_BOOSTING_ROUNDS} * {len(y_train)} * "
          f"{COBYLA_MAXITER_WEAK} = "
          f"{N_BOOSTING_ROUNDS * len(y_train) * COBYLA_MAXITER_WEAK} max evals.")
    print("     Each evaluation is a shallow circuit -> fast on hardware.")
    print()
    print("  5. WARM-START OPTIMIZATION")
    print(f"     Warm-start enabled: {WARM_START}.")
    print("     Previous round parameters initialize next round.")
    print("     D_t and D_{t+1} differ by a reweighting -> similar optima.")
    print("     Reduces COBYLA iterations needed per round.")
    print("=" * 70)

    return results


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    run_production()
