"""
QBoost -- QUBO Ensemble Selection - IBM Production-Ready
=========================================================

This script demonstrates a production-quality QBoost workflow for binary
classification ensemble selection, designed for execution on IBM Quantum
hardware.

Qiskit Version: 2.4.1

Key production features:
    1. Configurable classifier pool and regularization
    2. QUBO sparsification for larger problems
    3. Backend-aware circuit transpilation
    4. Warm-starting QAOA from classical heuristics
    5. Result persistence (JSON) and analysis
    6. Comparison with classical boosting (AdaBoost)
    7. Convergence tracking and diagnostics

NOTE: Execution on real hardware is commented out. Set your IBM token
and uncomment the relevant sections to run on a real backend.
"""

import json
import os
from datetime import datetime

import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

from qiskit import QuantumCircuit
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_aer.primitives import EstimatorV2 as AerEstimator, SamplerV2 as AerSampler

# IBM Runtime imports (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, SamplerV2, Session


# =============================================================================
# Configuration
# =============================================================================

CONFIG = {
    # Data
    "n_samples": 200,
    "noise": 0.3,
    "test_size": 0.2,
    "random_state": 42,

    # Weak classifiers
    "n_classifiers": 8,         # N: number of qubits = number of classifiers
    "max_depth": 1,             # Decision stump depth
    "bootstrap_fraction": 0.8,  # Fraction of training data per stump

    # QUBO
    "reg_lambda": 2.0,          # Regularization (controls ensemble size)
    "sparsify_threshold": 0.0,  # Zero out |Q_ij| below this (0 = no sparsification)

    # QAOA
    "qaoa_depth": 2,            # Number of QAOA layers (p)
    "max_iterations": 500,      # Optimizer max iterations
    "shots": 8192,              # Shots per circuit evaluation
    "use_warm_start": True,     # Initialize from classical heuristic

    # Output
    "output_dir": "quantum/algorithms/23_qboost_qubo/results",
}


def create_classification_data(config):
    """
    Generate binary classification data (make_moons).

    Labels are converted to {-1, +1} as required by QBoost.

    Args:
        config: Configuration dictionary

    Returns:
        X_train, X_test, y_train, y_test
    """
    X, y = make_moons(
        n_samples=config["n_samples"],
        noise=config["noise"],
        random_state=config["random_state"]
    )
    y = 2 * y - 1  # {0,1} -> {-1,+1}

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config["test_size"],
        random_state=config["random_state"]
    )
    return X_train, X_test, y_train, y_test


def train_weak_classifiers(X_train, y_train, config):
    """
    Train a pool of diverse weak classifiers (decision stumps).

    Diversity is achieved through bootstrap subsampling and different
    random seeds. In production, you might also vary:
    - max_depth (1, 2, 3)
    - Feature subsets (random subspaces)
    - Different classifier families (stumps, linear, RBF kernels)

    Args:
        X_train: Training features
        y_train: Training labels in {-1, +1}
        config: Configuration dictionary

    Returns:
        classifiers: List of trained classifiers
        predictions: (S, N) array of training predictions in {-1, +1}
    """
    n_classifiers = config["n_classifiers"]
    random_state = config["random_state"]
    rng = np.random.RandomState(random_state)

    classifiers = []
    predictions = np.zeros((len(X_train), n_classifiers))

    for i in range(n_classifiers):
        n_train = len(X_train)
        subsample_idx = rng.choice(
            n_train,
            size=int(config["bootstrap_fraction"] * n_train),
            replace=True
        )

        clf = DecisionTreeClassifier(
            max_depth=config["max_depth"],
            random_state=random_state + i
        )
        clf.fit(X_train[subsample_idx], y_train[subsample_idx])
        classifiers.append(clf)
        predictions[:, i] = clf.predict(X_train)

    return classifiers, predictions


def build_qboost_qubo(predictions, y_train, reg_lambda, sparsify_threshold=0.0):
    """
    Build the QUBO matrix for QBoost with optional sparsification.

    The QUBO objective:
        L(w) = sum_s (sum_i w_i h_i(x_s) - y_s)^2 + lambda sum_i w_i

    Expands to w^T Q w where:
        Q_ij = sum_s h_i(x_s) h_j(x_s)                            (i != j)
        Q_ii = S - 2 sum_s y_s h_i(x_s) + lambda                  (diagonal)

    For large N, sparsification zeros out small off-diagonal entries,
    reducing the number of ZZ gates in QAOA. This is valid when weak
    classifiers with small cross-correlation contribute negligible
    coupling energy.

    Args:
        predictions: (S, N) array of predictions in {-1, +1}
        y_train: Labels in {-1, +1}
        reg_lambda: Regularization parameter
        sparsify_threshold: Zero out |Q_ij| < threshold (off-diagonal)

    Returns:
        Q: (N, N) QUBO matrix
        sparsity_info: Dict with sparsification statistics
    """
    S, N = predictions.shape

    Q = predictions.T @ predictions  # (N, N)

    for i in range(N):
        correlation = np.dot(predictions[:, i], y_train)
        Q[i, i] += -2 * correlation + reg_lambda

    # Sparsification
    sparsity_info = {
        "original_nonzeros": int(np.sum(np.abs(Q) > 1e-10)),
        "total_entries": N * N,
    }

    if sparsify_threshold > 0:
        mask = np.abs(Q) >= sparsify_threshold
        np.fill_diagonal(mask, True)  # Never zero out diagonal
        Q = Q * mask
        sparsity_info["threshold"] = sparsify_threshold
        sparsity_info["after_nonzeros"] = int(np.sum(np.abs(Q) > 1e-10))
        sparsity_info["entries_removed"] = (
            sparsity_info["original_nonzeros"] - sparsity_info["after_nonzeros"]
        )

    return Q, sparsity_info


def qubo_to_ising(Q, num_qubits):
    """
    Convert QUBO matrix to Ising Hamiltonian (SparsePauliOp).

    Substitution: w_i = (1 - Z_i) / 2

    For the diagonal (w_i^2 = w_i):
        Q_ii * w_i = Q_ii * (1 - Z_i) / 2

    For off-diagonal (i < j):
        (Q_ij + Q_ji) * w_i w_j = (Q_ij + Q_ji) * (1 - Z_i - Z_j + Z_i Z_j) / 4

    Qiskit uses little-endian qubit ordering.

    Args:
        Q: QUBO matrix (N, N)
        num_qubits: Number of qubits

    Returns:
        SparsePauliOp: Ising Hamiltonian
    """
    N = num_qubits
    Q_sym = (Q + Q.T) / 2.0
    pauli_list = []
    offset = 0.0

    for i in range(N):
        for j in range(N):
            if i == j:
                offset += Q_sym[i, i] / 2.0
                z_label = ["I"] * N
                z_label[N - 1 - i] = "Z"
                pauli_list.append(("".join(z_label), -Q_sym[i, i] / 2.0))
            elif i < j:
                coeff = Q_sym[i, j] / 2.0
                if abs(coeff) < 1e-12:
                    continue  # Skip near-zero terms (from sparsification)

                offset += coeff

                z_label_i = ["I"] * N
                z_label_i[N - 1 - i] = "Z"
                pauli_list.append(("".join(z_label_i), -coeff))

                z_label_j = ["I"] * N
                z_label_j[N - 1 - j] = "Z"
                pauli_list.append(("".join(z_label_j), -coeff))

                zz_label = ["I"] * N
                zz_label[N - 1 - i] = "Z"
                zz_label[N - 1 - j] = "Z"
                pauli_list.append(("".join(zz_label), coeff))

    id_label = "I" * N
    pauli_list.append((id_label, offset))

    return SparsePauliOp.from_list(pauli_list).simplify()


def warm_start_initial_point(num_qubits, p):
    """
    Generate warm-start initial parameters for QAOA.

    Strategy:
    - p=1: Use analytically motivated starting point
    - p>1: Linear ramp (mimics adiabatic schedule)

    For QUBO problems, the cost landscape is different from MaxCut,
    so we use a more conservative initialization.

    Args:
        num_qubits: Number of qubits
        p: Number of QAOA layers

    Returns:
        np.array: Initial parameters [gamma_1,...,gamma_p, beta_1,...,beta_p]
    """
    if p == 1:
        return np.array([np.pi / 6, np.pi / 4])

    gammas = np.linspace(0.05, np.pi / 3, p)
    betas = np.linspace(np.pi / 3, 0.05, p)
    return np.concatenate([gammas, betas])


def exact_brute_force_qubo(Q, num_qubits):
    """
    Solve QUBO exactly via brute force (for small N <= 20).

    Used as a benchmark for QAOA quality.

    Args:
        Q: QUBO matrix (N, N)
        num_qubits: Number of variables

    Returns:
        best_w: Optimal binary vector
        best_energy: Minimum QUBO energy
        all_energies: Dict mapping bitstring -> energy
    """
    best_energy = float('inf')
    best_w = None
    all_energies = {}

    for idx in range(2**num_qubits):
        w = np.array([int(b) for b in format(idx, f'0{num_qubits}b')])
        energy = float(w @ Q @ w)
        bitstring = format(idx, f'0{num_qubits}b')
        all_energies[bitstring] = energy
        if energy < best_energy:
            best_energy = energy
            best_w = w.copy()

    return best_w, best_energy, all_energies


def evaluate_ensemble(classifiers, selection, X, y):
    """
    Evaluate ensemble by majority vote of selected classifiers.

    Args:
        classifiers: List of classifiers
        selection: Binary array indicating selected classifiers
        X: Features
        y: Labels in {-1, +1}

    Returns:
        accuracy: Classification accuracy
        predictions: Ensemble predictions
    """
    selected_idx = np.where(selection == 1)[0]

    if len(selected_idx) == 0:
        predictions = np.ones(len(y))
        return accuracy_score(y, predictions), predictions

    votes = np.zeros(len(X))
    for idx in selected_idx:
        votes += classifiers[idx].predict(X)

    predictions = np.sign(votes)
    predictions[predictions == 0] = 1

    return accuracy_score(y, predictions), predictions


def run_qboost_production():
    """
    Full production QBoost pipeline.
    """
    print("=" * 70)
    print("QBoost -- QUBO Ensemble Selection (Production Pipeline)")
    print("=" * 70)

    config = CONFIG.copy()

    # =========================================================================
    # Print Configuration
    # =========================================================================

    print(f"\nConfiguration:")
    for key, value in config.items():
        print(f"  {key}: {value}")

    # =========================================================================
    # STEP 1: IBM Quantum Service
    # =========================================================================

    print("\n--- Step 1: Backend Selection ---")
    print("Using local Aer simulator for demonstration.")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # service = QiskitRuntimeService(
    #     channel="ibm_quantum",
    #     token="YOUR_TOKEN"
    # )
    # backend = service.least_busy(
    #     simulator=False,
    #     min_num_qubits=config["n_classifiers"],
    #     operational=True
    # )
    # print(f"Backend: {backend.name}")
    #
    # # Create session for efficient job batching
    # session = Session(backend=backend)
    # estimator = EstimatorV2(session=session)
    # sampler = SamplerV2(session=session)
    # -------------------------------------------------------------------------

    # =========================================================================
    # STEP 2: Data Preparation
    # =========================================================================

    print("\n--- Step 2: Data Preparation ---")

    X_train, X_test, y_train, y_test = create_classification_data(config)

    print(f"Dataset: make_moons")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Label balance (train): +1={np.sum(y_train==1)}, -1={np.sum(y_train==-1)}")

    # =========================================================================
    # STEP 3: Train Weak Classifiers
    # =========================================================================

    print("\n--- Step 3: Train Weak Classifiers ---")

    classifiers, predictions = train_weak_classifiers(X_train, y_train, config)

    individual_train_accs = []
    individual_test_accs = []
    for i, clf in enumerate(classifiers):
        train_acc = accuracy_score(y_train, clf.predict(X_train))
        test_acc = accuracy_score(y_test, clf.predict(X_test))
        individual_train_accs.append(train_acc)
        individual_test_accs.append(test_acc)

    print(f"Trained {config['n_classifiers']} decision stumps")
    print(f"Mean accuracy: train={np.mean(individual_train_accs):.3f}, "
          f"test={np.mean(individual_test_accs):.3f}")
    print(f"Accuracy range: [{min(individual_test_accs):.3f}, "
          f"{max(individual_test_accs):.3f}]")

    # =========================================================================
    # STEP 4: Build QUBO
    # =========================================================================

    print("\n--- Step 4: Build QUBO Matrix ---")

    Q, sparsity_info = build_qboost_qubo(
        predictions, y_train,
        reg_lambda=config["reg_lambda"],
        sparsify_threshold=config["sparsify_threshold"]
    )

    print(f"QUBO matrix: {Q.shape[0]}x{Q.shape[1]}")
    print(f"Regularization: lambda={config['reg_lambda']}")
    print(f"Non-zero entries: {sparsity_info['original_nonzeros']}/{sparsity_info['total_entries']}")
    if config["sparsify_threshold"] > 0:
        print(f"Sparsification: {sparsity_info['entries_removed']} entries zeroed "
              f"(threshold={config['sparsify_threshold']})")
    print(f"Q diagonal range: [{np.diag(Q).min():.1f}, {np.diag(Q).max():.1f}]")
    print(f"Q off-diag range: [{Q[~np.eye(Q.shape[0], dtype=bool)].min():.1f}, "
          f"{Q[~np.eye(Q.shape[0], dtype=bool)].max():.1f}]")

    # =========================================================================
    # STEP 5: Exact Solution (Benchmark)
    # =========================================================================

    print("\n--- Step 5: Exact QUBO Solution (Brute Force) ---")

    N = config["n_classifiers"]
    if N <= 20:
        best_w, best_energy, all_energies = exact_brute_force_qubo(Q, N)
        exact_acc, _ = evaluate_ensemble(classifiers, best_w, X_test, y_test)

        print(f"Exact optimal selection: {best_w}")
        print(f"Exact optimal energy: {best_energy:.4f}")
        print(f"Classifiers selected: {list(np.where(best_w == 1)[0])}")
        print(f"Exact ensemble accuracy: {exact_acc:.4f}")
    else:
        print(f"N={N} too large for brute force (2^{N} = {2**N} states)")
        best_w = None
        best_energy = None
        exact_acc = None

    # =========================================================================
    # STEP 6: Convert QUBO to Ising Hamiltonian
    # =========================================================================

    print("\n--- Step 6: QUBO to Ising Conversion ---")

    hamiltonian = qubo_to_ising(Q, N)
    print(f"Hamiltonian: {hamiltonian.num_qubits} qubits, {len(hamiltonian)} Pauli terms")

    # =========================================================================
    # STEP 7: QAOA Ansatz Construction
    # =========================================================================

    print("\n--- Step 7: QAOA Ansatz ---")

    p = config["qaoa_depth"]
    qaoa_ansatz = QAOAAnsatz(
        cost_operator=hamiltonian,
        reps=p,
    )
    print(f"QAOA depth (p): {p}")
    print(f"Ansatz parameters: {qaoa_ansatz.num_parameters}")
    print(f"Ansatz gate depth: {qaoa_ansatz.depth()}")

    # =========================================================================
    # STEP 8: Transpilation
    # =========================================================================

    print("\n--- Step 8: Transpilation ---")
    print("Would transpile for real backend topology.")
    print("Key: minimize 2-qubit gate count for dense QUBO couplings.")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
    # transpiled_ansatz = pm.run(qaoa_ansatz)
    # print(f"Original depth: {qaoa_ansatz.depth()}")
    # print(f"Transpiled depth: {transpiled_ansatz.depth()}")
    # print(f"2Q gates: {transpiled_ansatz.count_ops().get('ecr', 0)}")
    # -------------------------------------------------------------------------

    # =========================================================================
    # STEP 9: Run QAOA
    # =========================================================================

    print("\n--- Step 9: Running QAOA ---")

    estimator = AerEstimator()
    sampler = AerSampler()

    # Warm start
    if config["use_warm_start"]:
        initial_point = warm_start_initial_point(N, p)
        print(f"Warm-start initial point: {initial_point}")
    else:
        initial_point = None
        print("Random initialization")

    # Convergence tracking
    energy_history = []

    def callback(eval_count, parameters, value, metadata):
        energy_history.append(float(value))
        if eval_count % 100 == 0:
            print(f"  Eval {eval_count}: energy = {value:.4f}")

    optimizer = COBYLA(maxiter=config["max_iterations"])

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=optimizer,
        reps=p,
        initial_point=initial_point,
        callback=callback,
    )

    print(f"\nOptimizing QAOA (p={p}, max_iter={config['max_iterations']})...\n")
    result = qaoa.compute_minimum_eigenvalue(hamiltonian)

    # Extract solution
    qaoa_energy = result.eigenvalue.real
    selected = np.zeros(N, dtype=int)
    if hasattr(result, 'best_measurement') and result.best_measurement:
        bitstring = result.best_measurement.get('bitstring', '0' * N)
        for i, bit in enumerate(reversed(bitstring)):
            selected[i] = int(bit)

    selected_idx = np.where(selected == 1)[0]

    print(f"\nQAOA energy: {qaoa_energy:.4f}")
    if best_energy is not None:
        print(f"Exact energy: {best_energy:.4f}")
        energy_ratio = best_energy / qaoa_energy if qaoa_energy != 0 else 0
        print(f"Energy ratio (exact/QAOA): {energy_ratio:.4f}")
    print(f"Selected classifiers: {list(selected_idx)}")
    print(f"Ensemble size: {len(selected_idx)} / {N}")
    print(f"Evaluations: {result.cost_function_evals}")

    # =========================================================================
    # STEP 10: Evaluate Results
    # =========================================================================

    print("\n--- Step 10: Evaluation ---")

    # QBoost ensemble
    qboost_acc, _ = evaluate_ensemble(classifiers, selected, X_test, y_test)
    print(f"QBoost accuracy: {qboost_acc:.4f}")

    # AdaBoost baseline
    ada = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1),
        n_estimators=N,
        random_state=config["random_state"],
        algorithm="SAMME"
    )
    ada.fit(X_train, y_train)
    ada_acc = accuracy_score(y_test, ada.predict(X_test))
    print(f"AdaBoost accuracy: {ada_acc:.4f}")

    # All-vote baseline
    all_sel = np.ones(N, dtype=int)
    all_acc, _ = evaluate_ensemble(classifiers, all_sel, X_test, y_test)
    print(f"All-vote accuracy: {all_acc:.4f}")

    # Best single
    best_single_acc = max(individual_test_accs)
    best_single_idx = int(np.argmax(individual_test_accs))
    print(f"Best single (h_{best_single_idx}): {best_single_acc:.4f}")

    if exact_acc is not None:
        print(f"Exact optimal: {exact_acc:.4f}")

    # =========================================================================
    # STEP 11: Save Results
    # =========================================================================

    print("\n--- Step 11: Saving Results ---")

    output_dir = config["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "QBoost_QUBO",
        "qiskit_version": "2.4.1",
        "config": {
            "n_samples": config["n_samples"],
            "noise": config["noise"],
            "n_classifiers": config["n_classifiers"],
            "reg_lambda": config["reg_lambda"],
            "sparsify_threshold": config["sparsify_threshold"],
            "qaoa_depth": config["qaoa_depth"],
            "max_iterations": config["max_iterations"],
            "shots": config["shots"],
            "warm_start": config["use_warm_start"],
            "backend": "aer_simulator (demo)",
        },
        "weak_classifiers": {
            "type": "DecisionTreeClassifier(max_depth=1)",
            "individual_train_accuracies": [float(a) for a in individual_train_accs],
            "individual_test_accuracies": [float(a) for a in individual_test_accs],
            "mean_train_accuracy": float(np.mean(individual_train_accs)),
            "mean_test_accuracy": float(np.mean(individual_test_accs)),
        },
        "qubo": {
            "matrix_size": f"{N}x{N}",
            "sparsity": sparsity_info,
            "diagonal_range": [float(np.diag(Q).min()), float(np.diag(Q).max())],
        },
        "qaoa_results": {
            "energy": float(qaoa_energy),
            "exact_energy": float(best_energy) if best_energy is not None else None,
            "selected_classifiers": [int(i) for i in selected_idx],
            "ensemble_size": int(len(selected_idx)),
            "num_evaluations": int(result.cost_function_evals),
            "optimal_parameters": {str(k): float(v)
                                   for k, v in result.optimal_parameters.items()},
            "convergence_history": energy_history,
        },
        "accuracy": {
            "qboost": float(qboost_acc),
            "adaboost": float(ada_acc),
            "all_vote": float(all_acc),
            "best_single": float(best_single_acc),
            "exact_optimal": float(exact_acc) if exact_acc is not None else None,
        },
    }

    filepath = os.path.join(output_dir, "qboost_qubo_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"Results saved to {filepath}")

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print("""
    QBoost Production Considerations:

    1. Qubit Scaling:
       - N qubits = N classifiers (one qubit per weak learner)
       - Current NISQ limit: N <= ~20 classifiers on IBM hardware
       - Each QAOA layer has O(N^2) ZZ gates for dense QUBO
       - Practical circuit depth: p * N^2 two-qubit gates

    2. QUBO Sparsification:
       - For large N, zero out small |Q_ij| entries (threshold tuning)
       - Reduces ZZ gate count from O(N^2) to O(k) where k = nonzeros
       - Trade-off: sparsification introduces approximation error
       - Rule of thumb: keep entries with |Q_ij| > 0.1 * max(|Q|)

    3. Warm-Starting QAOA:
       - Random initialization often fails for large N (barren plateaus)
       - Classical heuristic: greedily add classifiers, use as initial point
       - Interp strategy: optimize p=1 first, interpolate to p=2, etc.
       - Transfer learning: use parameters from similar problem instances

    4. Comparison with Simulated Annealing:
       - For small N (~8), brute force is faster than QAOA
       - For medium N (~15-30), simulated annealing is a strong baseline
       - Quantum advantage expected only for large, structured QUBOs
       - D-Wave quantum annealers handle N~5000 (sparse QUBO) natively

    5. Error Mitigation:
       - TREX for readout errors (resilience_level=1 on IBM)
       - Dynamical decoupling for idle qubits
       - Pauli twirling for coherent error suppression
       - Consider zero-noise extrapolation for critical applications

    6. Scaling Beyond NISQ:
       - Hierarchical QBoost: partition N classifiers into blocks,
         QBoost within each block, then QBoost across block winners
       - Feature-space decomposition: separate classifiers by feature
         subsets, run independent QBoost instances
       - Classical pre-filtering: use mutual information or
         correlation screening to reduce N before quantum optimization

    7. Hyperparameter Tuning:
       - lambda controls ensemble size: too small -> overfitting
         (many classifiers), too large -> underfitting (too few)
       - Cross-validate lambda in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
       - QAOA depth p: diminishing returns beyond p=3 on noisy hardware
    """)


if __name__ == "__main__":
    run_qboost_production()
