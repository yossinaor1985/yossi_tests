"""
QBoost -- QUBO Ensemble Selection - Local Simulator
=====================================================

This script demonstrates QBoost applied to binary classification using
the local Aer simulator. QBoost formulates the problem of selecting an
optimal ensemble of weak classifiers as a QUBO (Quadratic Unconstrained
Binary Optimization), which is then solved using QAOA.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Given N weak classifiers h_1, ..., h_N trained on labeled data
{(x_s, y_s)}, QBoost finds binary weights w in {0,1}^N to form the
strong classifier:

    H(x) = sign( sum_i w_i h_i(x) )

The optimal weights minimize the QBoost objective:

    L(w) = sum_s ( sum_i w_i h_i(x_s) - y_s )^2 + lambda * sum_i w_i

This expands to a QUBO:  w^T Q w  (absorbing linear terms into diagonal)

where:
    Q_ij = sum_s h_i(x_s) h_j(x_s)                         (off-diagonal)
    Q_ii = sum_s h_i(x_s)^2 - 2 sum_s y_s h_i(x_s) + lambda  (diagonal)

The QUBO is converted to an Ising Hamiltonian via w_i = (1 - Z_i) / 2
and solved with QAOA. The ground-state bitstring gives the selected
classifiers.

Algorithm:
    1. Train N decision stumps on make_moons data
    2. Build QUBO matrix Q from classifier predictions
    3. Convert QUBO to Ising Hamiltonian (SparsePauliOp)
    4. Solve with QAOA (p = 1, 2, 3 layers)
    5. Evaluate ensemble accuracy vs. AdaBoost baseline
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer import AerSimulator
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer.primitives import SamplerV2 as AerSampler, EstimatorV2 as AerEstimator


def create_classification_data(n_samples=200, noise=0.3, random_state=42):
    """
    Generate a binary classification dataset using make_moons.

    make_moons produces two interleaving half-circles in 2D, a standard
    benchmark for nonlinear classifiers.

    Labels are converted to {-1, +1} (required by QBoost formulation).

    Args:
        n_samples: Total number of samples
        noise: Standard deviation of Gaussian noise added to the data
        random_state: Random seed for reproducibility

    Returns:
        X_train: Training features (n_train x 2)
        X_test: Test features (n_test x 2)
        y_train: Training labels in {-1, +1}
        y_test: Test labels in {-1, +1}
    """
    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=random_state)

    # Convert labels from {0, 1} to {-1, +1} for QBoost
    y = 2 * y - 1

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    return X_train, X_test, y_train, y_test


def train_weak_classifiers(X_train, y_train, n_classifiers=8, random_state=42):
    """
    Train N weak classifiers (decision stumps) on the training data.

    A decision stump is a decision tree of depth 1 (single split).
    Each stump partitions the feature space with one threshold on one
    feature, achieving accuracy slightly above 50%.

    To get diverse stumps, we use different random seeds and bootstrap
    subsampling (each stump sees a random 80% of the training data).

    Args:
        X_train: Training features
        y_train: Training labels in {-1, +1}
        n_classifiers: Number of weak classifiers to train
        random_state: Base random seed

    Returns:
        classifiers: List of trained DecisionTreeClassifier objects
        predictions: Array of shape (n_train, n_classifiers) with
                     predictions h_i(x_s) in {-1, +1}
    """
    classifiers = []
    predictions = np.zeros((len(X_train), n_classifiers))
    rng = np.random.RandomState(random_state)

    for i in range(n_classifiers):
        # Bootstrap subsample for diversity
        n_train = len(X_train)
        subsample_idx = rng.choice(n_train, size=int(0.8 * n_train), replace=True)

        clf = DecisionTreeClassifier(
            max_depth=1,
            random_state=random_state + i
        )
        clf.fit(X_train[subsample_idx], y_train[subsample_idx])
        classifiers.append(clf)

        # Store predictions on FULL training set
        predictions[:, i] = clf.predict(X_train)

    return classifiers, predictions


def build_qboost_qubo(predictions, y_train, reg_lambda=0.5):
    """
    Build the QUBO matrix Q for the QBoost problem.

    The QBoost objective (see explanation_physicist.md, Section 2.2):

        L(w) = sum_s ( sum_i w_i h_i(x_s) - y_s )^2 + lambda sum_i w_i

    Expanding:
        L(w) = w^T (P^T P) w - 2 (P^T y)^T w + y^T y + lambda 1^T w

    Since w_i in {0,1} implies w_i^2 = w_i, we absorb linear terms
    into the diagonal of Q:

        Q_ij = sum_s h_i(x_s) h_j(x_s)                        (i != j)
        Q_ii = sum_s h_i(x_s)^2 - 2 sum_s y_s h_i(x_s) + lambda

    Note: h_i(x_s) in {-1,+1} so h_i(x_s)^2 = 1 and
          sum_s h_i(x_s)^2 = S (number of training samples).

    Args:
        predictions: Array (S, N) of classifier predictions in {-1, +1}
        y_train: Training labels in {-1, +1}, shape (S,)
        reg_lambda: Regularization parameter (controls ensemble size)

    Returns:
        Q: QUBO matrix of shape (N, N)
    """
    S, N = predictions.shape

    # Off-diagonal: Q_ij = sum_s h_i(x_s) * h_j(x_s) = (P^T P)_{ij}
    Q = predictions.T @ predictions  # shape (N, N)

    # Diagonal modification: add linear terms
    # Q_ii += -2 * sum_s y_s h_i(x_s) + lambda
    # Note: P^T P already has sum_s h_i(x_s)^2 = S on diagonal
    for i in range(N):
        correlation_with_labels = np.dot(predictions[:, i], y_train)
        Q[i, i] += -2 * correlation_with_labels + reg_lambda

    return Q


def qubo_to_ising(Q, num_qubits):
    """
    Convert a QUBO matrix to an Ising Hamiltonian (SparsePauliOp).

    Using the substitution w_i = (1 - Z_i) / 2:

        w_i w_j = (1 - Z_i)(1 - Z_j) / 4
                = (1 - Z_i - Z_j + Z_i Z_j) / 4

        w_i = (1 - Z_i) / 2    (for diagonal/linear terms)

    The Ising Hamiltonian becomes:

        H = sum_{i<j} (Q_ij/4) Z_i Z_j
          + sum_i [ (-sum_j Q_ij) / 4  +  Q_ii / 4  -  Q_ii / 2 ] Z_i
          + constant

    Simplifying the linear coefficient of Z_i:

        h_i = -sum_{j!=i} Q_ij / 4  -  Q_ii / 4

    Note: Qiskit uses little-endian ordering (qubit 0 is rightmost).

    Args:
        Q: QUBO matrix of shape (N, N)
        num_qubits: Number of qubits (= N classifiers)

    Returns:
        SparsePauliOp: The Ising Hamiltonian
    """
    N = num_qubits
    pauli_list = []

    # Constant (energy offset)
    constant = 0.0
    for i in range(N):
        for j in range(N):
            constant += Q[i, j] / 4.0
    # Also subtract the linear contribution: sum_i Q_ii / 2
    # From w_i = (1 - Z_i)/2, the Q_ii w_i term gives Q_ii/2 - Q_ii Z_i/2
    # But Q_ii w_i^2 = Q_ii w_i since w_i in {0,1}
    # Full expansion: Q_ii * (1 - Z_i)/2 for diagonal, Q_ij * (1-Z_i)(1-Z_j)/4 for off-diag

    # Let's be precise. For the full QUBO w^T Q w:
    # = sum_i Q_ii w_i + sum_{i<j} (Q_ij + Q_ji) w_i w_j   (since w_i^2 = w_i)
    # But Q is not necessarily symmetric from our construction, so let's symmetrize:
    Q_sym = (Q + Q.T) / 2.0

    # Now: sum_i Q_sym_ii w_i + sum_{i<j} 2*Q_sym_ij w_i w_j
    # Substitute w_i = (1 - Z_i)/2:
    # w_i = (1 - Z_i)/2
    # w_i w_j = (1 - Z_i - Z_j + Z_i Z_j)/4

    # ZZ terms: coefficient of Z_i Z_j (i < j) = 2 * Q_sym_ij / 4 = Q_sym_ij / 2
    # But since Q is already symmetric, Q_sym_ij = Q_ij
    # Actually: the off-diagonal terms in w^T Q w are sum_{i!=j} Q_ij w_i w_j
    # = sum_{i<j} (Q_ij + Q_ji) w_i w_j = sum_{i<j} 2*Q_sym_ij * (1-Z_i-Z_j+Z_iZ_j)/4
    # ZZ coefficient for pair (i,j): 2 * Q_sym_ij / 4 = Q_sym_ij / 2

    # Diagonal terms: Q_ii w_i = Q_ii (1-Z_i)/2
    # Z_i coefficient from diagonal: -Q_ii / 2

    # Z_i coefficient from off-diagonal: sum_{j!=i} 2*Q_sym_ij * (-1/4 - 1/4)
    # Wait, let me redo this carefully.

    # Off-diagonal contribution to Z_i from pair (i,j) where i<j:
    #   2*Q_sym_ij * (1 - Z_i - Z_j + Z_i Z_j)/4
    #   Z_i coefficient: 2*Q_sym_ij * (-1/4) = -Q_sym_ij / 2
    # Same from pair (j,i) where j<i: Z_i coefficient = -Q_sym_ji / 2

    # Total Z_i coefficient:
    #   From diagonal: -Q_ii / 2
    #   From off-diagonal: -sum_{j!=i} Q_sym_ij / 2
    #   = -sum_j Q_sym_ij / 2

    # Constant:
    #   From diagonal: sum_i Q_ii / 2
    #   From off-diagonal: sum_{i<j} 2*Q_sym_ij / 4 = sum_{i<j} Q_sym_ij / 2
    #   Total: sum_i Q_ii / 2 + sum_{i<j} Q_sym_ij / 2
    #        = (sum_i Q_ii + sum_{i<j} (Q_ij + Q_ji)/2 * ... ) ... let me just compute directly

    pauli_list = []
    offset = 0.0

    # Compute all terms from the substitution
    for i in range(N):
        for j in range(N):
            if i == j:
                # Diagonal: Q_ii * w_i = Q_ii * (1 - Z_i) / 2
                # Constant: + Q_ii / 2
                offset += Q_sym[i, i] / 2.0

                # Z_i: - Q_ii / 2
                z_label = ["I"] * N
                z_label[N - 1 - i] = "Z"  # little-endian
                pauli_list.append(("".join(z_label), -Q_sym[i, i] / 2.0))

            elif i < j:
                # Off-diagonal: 2*Q_sym_ij * w_i w_j (factor of 2 for symmetry)
                # = 2*Q_sym_ij * (1 - Z_i - Z_j + Z_i Z_j) / 4
                # = Q_sym_ij * (1 - Z_i - Z_j + Z_i Z_j) / 2
                coeff = Q_sym[i, j] / 2.0

                # Constant: + coeff
                offset += coeff

                # Z_i: - coeff
                z_label_i = ["I"] * N
                z_label_i[N - 1 - i] = "Z"
                pauli_list.append(("".join(z_label_i), -coeff))

                # Z_j: - coeff
                z_label_j = ["I"] * N
                z_label_j[N - 1 - j] = "Z"
                pauli_list.append(("".join(z_label_j), -coeff))

                # Z_i Z_j: + coeff
                zz_label = ["I"] * N
                zz_label[N - 1 - i] = "Z"
                zz_label[N - 1 - j] = "Z"
                pauli_list.append(("".join(zz_label), coeff))

    # Add constant (identity) term
    id_label = "I" * N
    pauli_list.append((id_label, offset))

    hamiltonian = SparsePauliOp.from_list(pauli_list).simplify()
    return hamiltonian


def solve_with_qaoa(hamiltonian, num_qubits, p=2):
    """
    Solve the Ising Hamiltonian using QAOA.

    QAOA prepares the state (see algorithm 02 and explanation_physicist.md):
        |gamma, beta> = U_M(beta_p) U_C(gamma_p) ... U_M(beta_1) U_C(gamma_1) |+>^N

    The parameters are optimized to minimize <H_Ising>.

    We use Qiskit's built-in QAOA with Aer primitives:
    - EstimatorV2 for expectation value computation
    - SamplerV2 for sampling the final state
    - COBYLA optimizer (gradient-free, noise-robust)

    Args:
        hamiltonian: SparsePauliOp Ising Hamiltonian to minimize
        num_qubits: Number of qubits
        p: Number of QAOA layers (circuit depth parameter)

    Returns:
        result: QAOA result object
        selected: Binary array of selected classifiers
    """
    estimator = AerEstimator()
    sampler = AerSampler()

    optimizer = COBYLA(maxiter=500)

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=optimizer,
        reps=p,
    )

    # QAOA minimizes the Hamiltonian. Our QUBO is already a minimization
    # problem, so we pass the Hamiltonian directly.
    result = qaoa.compute_minimum_eigenvalue(hamiltonian)

    # Extract the best bitstring from the measurement
    selected = np.zeros(num_qubits, dtype=int)
    if hasattr(result, 'best_measurement') and result.best_measurement:
        bitstring = result.best_measurement.get('bitstring', '0' * num_qubits)
        # Qiskit bitstring is in little-endian: bitstring[0] = qubit N-1
        # We need w_i for qubit i, so reverse the string
        for i, bit in enumerate(reversed(bitstring)):
            selected[i] = int(bit)
    else:
        # Fallback: use eigenstate if available
        print("  Warning: No best_measurement found, using fallback.")
        # Try to get from eigenstate
        if result.eigenstate is not None:
            probs = np.abs(result.eigenstate) ** 2
            best_idx = np.argmax(probs)
            bitstring = format(best_idx, f'0{num_qubits}b')
            for i, bit in enumerate(reversed(bitstring)):
                selected[i] = int(bit)

    return result, selected


def evaluate_ensemble(classifiers, selection, X_test, y_test):
    """
    Evaluate the QBoost ensemble on test data.

    The ensemble prediction is by majority vote of selected classifiers:
        H(x) = sign( sum_{i: w_i=1} h_i(x) )

    If the sum is zero (tie), we predict +1 by convention.

    Args:
        classifiers: List of trained classifier objects
        selection: Binary array (N,) indicating selected classifiers
        X_test: Test features
        y_test: Test labels in {-1, +1}

    Returns:
        accuracy: Classification accuracy on test set
        predictions: Ensemble predictions in {-1, +1}
    """
    selected_indices = np.where(selection == 1)[0]

    if len(selected_indices) == 0:
        print("  Warning: No classifiers selected! Predicting all +1.")
        predictions = np.ones(len(y_test))
        accuracy = accuracy_score(y_test, predictions)
        return accuracy, predictions

    # Accumulate votes from selected classifiers
    votes = np.zeros(len(X_test))
    for idx in selected_indices:
        votes += classifiers[idx].predict(X_test)

    # Majority vote: sign of sum (ties go to +1)
    predictions = np.sign(votes)
    predictions[predictions == 0] = 1

    accuracy = accuracy_score(y_test, predictions)
    return accuracy, predictions


def run_adaboost_comparison(X_train, y_train, X_test, y_test, n_estimators=8):
    """
    Run sklearn AdaBoostClassifier as a classical baseline.

    AdaBoost uses greedy sequential selection with sample reweighting.
    Each round:
        1. Train a weak classifier on reweighted samples
        2. Compute its weighted error
        3. Assign a real-valued weight (higher for better classifiers)
        4. Reweight samples (misclassified samples get higher weight)

    Args:
        X_train, y_train: Training data (labels in {-1, +1})
        X_test, y_test: Test data
        n_estimators: Number of boosting rounds

    Returns:
        accuracy: Test accuracy
        model: Trained AdaBoostClassifier
    """
    model = AdaBoostClassifier(
        estimator=DecisionTreeClassifier(max_depth=1),
        n_estimators=n_estimators,
        random_state=42,
        algorithm="SAMME"
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return accuracy, model


def main():
    print("=" * 70)
    print("QBoost -- QUBO Ensemble Selection (Local Simulator)")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Generate Classification Data
    # =========================================================================

    print("\n--- Step 1: Generate Classification Data ---")

    X_train, X_test, y_train, y_test = create_classification_data(
        n_samples=200, noise=0.3, random_state=42
    )

    print(f"Dataset: make_moons (2D, binary classification)")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Label distribution (train): +1: {np.sum(y_train == 1)}, "
          f"-1: {np.sum(y_train == -1)}")
    print(f"Feature range: x1 in [{X_train[:,0].min():.2f}, {X_train[:,0].max():.2f}], "
          f"x2 in [{X_train[:,1].min():.2f}, {X_train[:,1].max():.2f}]")

    # =========================================================================
    # STEP 2: Train Weak Classifiers
    # =========================================================================

    print("\n--- Step 2: Train Weak Classifiers (Decision Stumps) ---")

    N_CLASSIFIERS = 8
    classifiers, predictions = train_weak_classifiers(
        X_train, y_train, n_classifiers=N_CLASSIFIERS, random_state=42
    )

    print(f"Number of weak classifiers: {N_CLASSIFIERS}")
    print(f"Classifier type: DecisionTreeClassifier(max_depth=1)")
    print(f"\nIndividual training accuracies:")

    individual_train_accs = []
    individual_test_accs = []
    for i, clf in enumerate(classifiers):
        train_acc = accuracy_score(y_train, clf.predict(X_train))
        test_acc = accuracy_score(y_test, clf.predict(X_test))
        individual_train_accs.append(train_acc)
        individual_test_accs.append(test_acc)
        print(f"  h_{i}: train={train_acc:.3f}, test={test_acc:.3f}")

    print(f"\nMean individual accuracy: train={np.mean(individual_train_accs):.3f}, "
          f"test={np.mean(individual_test_accs):.3f}")

    # =========================================================================
    # STEP 3: Build QUBO Matrix
    # =========================================================================

    print("\n--- Step 3: Build QUBO Matrix ---")

    REG_LAMBDA = 2.0
    Q = build_qboost_qubo(predictions, y_train, reg_lambda=REG_LAMBDA)

    print(f"Regularization lambda: {REG_LAMBDA}")
    print(f"QUBO matrix Q ({N_CLASSIFIERS}x{N_CLASSIFIERS}):")
    print(f"  Diagonal (self-terms):  {np.diag(Q)}")
    print(f"  Q range: [{Q.min():.1f}, {Q.max():.1f}]")
    print(f"  Q sparsity: {np.sum(np.abs(Q) < 1e-10)} / {Q.size} entries near zero")

    # Print the full Q matrix for inspection
    print(f"\n  Full QUBO matrix:")
    for i in range(N_CLASSIFIERS):
        row = "  [" + ", ".join(f"{Q[i,j]:7.1f}" for j in range(N_CLASSIFIERS)) + "]"
        print(row)

    # =========================================================================
    # STEP 4: Convert to Ising Hamiltonian
    # =========================================================================

    print("\n--- Step 4: Convert QUBO to Ising Hamiltonian ---")

    hamiltonian = qubo_to_ising(Q, N_CLASSIFIERS)
    print(f"Number of Pauli terms: {len(hamiltonian)}")
    print(f"Number of qubits: {hamiltonian.num_qubits}")

    # Verify by computing exact ground state
    H_matrix = hamiltonian.to_matrix()
    eigvals = np.linalg.eigvalsh(H_matrix)
    print(f"Exact ground state energy: {eigvals[0].real:.4f}")
    print(f"Exact max energy: {eigvals[-1].real:.4f}")
    print(f"Spectral gap: {(eigvals[1] - eigvals[0]).real:.4f}")

    # Find the exact optimal selection by brute force
    best_energy = float('inf')
    best_selection = None
    for idx in range(2**N_CLASSIFIERS):
        w = np.array([int(b) for b in format(idx, f'0{N_CLASSIFIERS}b')])
        energy = w @ Q @ w
        if energy < best_energy:
            best_energy = energy
            best_selection = w.copy()

    print(f"\nExact optimal selection (brute force): {best_selection}")
    print(f"Exact optimal QUBO energy: {best_energy:.4f}")
    print(f"Number of classifiers selected: {np.sum(best_selection)}")

    # =========================================================================
    # STEP 5: Solve with QAOA (p = 1, 2, 3)
    # =========================================================================

    print("\n--- Step 5: Solve with QAOA ---")

    qaoa_results = {}
    for p in [1, 2, 3]:
        print(f"\n  --- QAOA with p = {p} layers ---")

        result, selected = solve_with_qaoa(hamiltonian, N_CLASSIFIERS, p=p)

        energy = result.eigenvalue.real
        selected_indices = np.where(selected == 1)[0]

        print(f"  QAOA energy: {energy:.4f}")
        print(f"  Selected classifiers: {selected}")
        print(f"  Selected indices: {list(selected_indices)}")
        print(f"  Number selected: {len(selected_indices)}")
        print(f"  Evaluations: {result.cost_function_evals}")

        qaoa_results[p] = {
            'result': result,
            'selected': selected,
            'energy': energy,
        }

    # =========================================================================
    # STEP 6: Evaluate QBoost Ensemble
    # =========================================================================

    print("\n--- Step 6: Evaluate QBoost Ensemble ---")

    # Use best QAOA result (highest p)
    best_p = max(qaoa_results.keys())
    best_selected = qaoa_results[best_p]['selected']

    qboost_accuracy, qboost_predictions = evaluate_ensemble(
        classifiers, best_selected, X_test, y_test
    )

    selected_idx = np.where(best_selected == 1)[0]
    print(f"QBoost ensemble (p={best_p}):")
    print(f"  Selected classifiers: {list(selected_idx)}")
    print(f"  Ensemble size: {len(selected_idx)} / {N_CLASSIFIERS}")
    print(f"  Test accuracy: {qboost_accuracy:.4f}")

    # Also evaluate all QAOA depths
    print(f"\n  QBoost accuracy by QAOA depth:")
    qboost_accs_by_p = {}
    for p in sorted(qaoa_results.keys()):
        sel = qaoa_results[p]['selected']
        acc, _ = evaluate_ensemble(classifiers, sel, X_test, y_test)
        qboost_accs_by_p[p] = acc
        print(f"    p={p}: accuracy={acc:.4f}, "
              f"selected={list(np.where(sel == 1)[0])}")

    # Evaluate exact optimal selection
    exact_accuracy, _ = evaluate_ensemble(
        classifiers, best_selection, X_test, y_test
    )
    print(f"\n  Exact optimal ensemble accuracy: {exact_accuracy:.4f}")
    print(f"  Exact optimal selection: {list(np.where(best_selection == 1)[0])}")

    # =========================================================================
    # STEP 7: Compare with AdaBoost
    # =========================================================================

    print("\n--- Step 7: Compare with AdaBoost ---")

    adaboost_accuracy, adaboost_model = run_adaboost_comparison(
        X_train, y_train, X_test, y_test, n_estimators=N_CLASSIFIERS
    )

    print(f"AdaBoost (n_estimators={N_CLASSIFIERS}):")
    print(f"  Test accuracy: {adaboost_accuracy:.4f}")

    # All-classifiers majority vote
    all_selected = np.ones(N_CLASSIFIERS, dtype=int)
    all_accuracy, _ = evaluate_ensemble(classifiers, all_selected, X_test, y_test)
    print(f"\nAll classifiers (majority vote): {all_accuracy:.4f}")

    # Best single classifier
    best_single_acc = max(individual_test_accs)
    best_single_idx = np.argmax(individual_test_accs)
    print(f"Best single classifier (h_{best_single_idx}): {best_single_acc:.4f}")

    print(f"\nComparison summary:")
    print(f"  Best single classifier:  {best_single_acc:.4f}")
    print(f"  All classifiers vote:    {all_accuracy:.4f}")
    print(f"  AdaBoost:                {adaboost_accuracy:.4f}")
    print(f"  QBoost (QAOA p={best_p}):     {qboost_accuracy:.4f}")
    print(f"  QBoost (exact):          {exact_accuracy:.4f}")

    # =========================================================================
    # STEP 8: Visualization
    # =========================================================================

    print("\n--- Step 8: Visualization ---")

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # --- (0,0) Individual weak classifier accuracies ---
    ax = axes[0, 0]
    x_pos = np.arange(N_CLASSIFIERS)
    colors_bar = ['#2ecc71' if best_selected[i] == 1 else '#bdc3c7'
                  for i in range(N_CLASSIFIERS)]
    bars = ax.bar(x_pos, individual_test_accs, color=colors_bar, edgecolor='black',
                  linewidth=0.5)
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Random guess')
    ax.set_xlabel('Classifier index', fontsize=12)
    ax.set_ylabel('Test accuracy', fontsize=12)
    ax.set_title('Individual Weak Classifier Accuracies', fontsize=14)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'h_{i}' for i in range(N_CLASSIFIERS)])
    ax.set_ylim(0.3, 1.0)
    ax.legend(loc='lower right')
    # Add annotation for selected classifiers
    for i in range(N_CLASSIFIERS):
        if best_selected[i] == 1:
            ax.annotate('*', (x_pos[i], individual_test_accs[i] + 0.01),
                        ha='center', fontsize=16, color='green', fontweight='bold')

    # --- (0,1) QBoost vs AdaBoost accuracy comparison ---
    ax = axes[0, 1]
    methods = ['Best\nsingle', 'All vote', 'AdaBoost', f'QBoost\n(p={best_p})',
               'QBoost\n(exact)']
    accuracies = [best_single_acc, all_accuracy, adaboost_accuracy,
                  qboost_accuracy, exact_accuracy]
    bar_colors = ['#3498db', '#9b59b6', '#e74c3c', '#2ecc71', '#1abc9c']
    bars = ax.bar(methods, accuracies, color=bar_colors, edgecolor='black',
                  linewidth=0.5)
    ax.set_ylabel('Test accuracy', fontsize=12)
    ax.set_title('Classification Accuracy Comparison', fontsize=14)
    ax.set_ylim(0.4, 1.05)
    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f'{acc:.3f}', ha='center', fontsize=10, fontweight='bold')

    # --- (1,0) Decision boundary for QBoost ensemble ---
    ax = axes[1, 0]
    # Create meshgrid for decision boundary
    x_min, x_max = X_test[:, 0].min() - 0.5, X_test[:, 0].max() + 0.5
    y_min, y_max = X_test[:, 1].min() - 0.5, X_test[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200),
                         np.linspace(y_min, y_max, 200))
    grid_points = np.c_[xx.ravel(), yy.ravel()]

    # Compute QBoost ensemble predictions on grid
    selected_idx = np.where(best_selected == 1)[0]
    if len(selected_idx) > 0:
        grid_votes = np.zeros(len(grid_points))
        for idx in selected_idx:
            grid_votes += classifiers[idx].predict(grid_points)
        grid_predictions = np.sign(grid_votes)
        grid_predictions[grid_predictions == 0] = 1
        Z = grid_predictions.reshape(xx.shape)

        ax.contourf(xx, yy, Z, levels=[-2, 0, 2], colors=['#ffcccc', '#ccccff'],
                    alpha=0.5)
        ax.contour(xx, yy, Z, levels=[0], colors='black', linewidths=2)

    # Plot test points
    ax.scatter(X_test[y_test == 1, 0], X_test[y_test == 1, 1],
               c='blue', marker='o', edgecolors='black', s=40, label='y=+1')
    ax.scatter(X_test[y_test == -1, 0], X_test[y_test == -1, 1],
               c='red', marker='s', edgecolors='black', s=40, label='y=-1')
    ax.set_xlabel('Feature 1', fontsize=12)
    ax.set_ylabel('Feature 2', fontsize=12)
    ax.set_title(f'QBoost Decision Boundary (p={best_p})', fontsize=14)
    ax.legend(loc='upper right')

    # --- (1,1) QUBO matrix heatmap ---
    ax = axes[1, 1]
    im = ax.imshow(Q, cmap='RdBu_r', aspect='equal')
    ax.set_xlabel('Classifier j', fontsize=12)
    ax.set_ylabel('Classifier i', fontsize=12)
    ax.set_title(f'QUBO Matrix Q (lambda={REG_LAMBDA})', fontsize=14)
    ax.set_xticks(range(N_CLASSIFIERS))
    ax.set_yticks(range(N_CLASSIFIERS))
    ax.set_xticklabels([f'h_{i}' for i in range(N_CLASSIFIERS)])
    ax.set_yticklabels([f'h_{i}' for i in range(N_CLASSIFIERS)])
    plt.colorbar(im, ax=ax, label='Q_ij value')

    # Add value annotations on the heatmap
    for i in range(N_CLASSIFIERS):
        for j in range(N_CLASSIFIERS):
            ax.text(j, i, f'{Q[i,j]:.0f}', ha='center', va='center',
                    fontsize=7, color='white' if abs(Q[i, j]) > Q.max() * 0.6 else 'black')

    plt.suptitle('QBoost -- QUBO Ensemble Selection Results', fontsize=16,
                 fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig("quantum/algorithms/23_qboost_qubo/qboost_qubo_results.png",
                dpi=150, bbox_inches='tight')
    print("Plot saved to quantum/algorithms/23_qboost_qubo/qboost_qubo_results.png")

    # =========================================================================
    # STEP 9: Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    QBoost successfully selected an optimal ensemble of weak classifiers
    by solving a QUBO problem with QAOA.

    Dataset: make_moons (200 samples, noise=0.3)
    Weak classifiers: {N_CLASSIFIERS} decision stumps
    Regularization: lambda = {REG_LAMBDA}

    Results:
      Best single classifier:  {best_single_acc:.4f}
      All classifiers vote:    {all_accuracy:.4f}
      AdaBoost ({N_CLASSIFIERS} estimators):    {adaboost_accuracy:.4f}
      QBoost (QAOA p={best_p}):     {qboost_accuracy:.4f}
      QBoost (exact QUBO):     {exact_accuracy:.4f}

    QBoost selected {len(selected_idx)} / {N_CLASSIFIERS} classifiers: {list(selected_idx)}

    Key concepts demonstrated:
    1. Formulating ensemble selection as QUBO
    2. QUBO to Ising Hamiltonian conversion (w_i = (1-Z_i)/2)
    3. Solving with QAOA at multiple depths
    4. QBoost promotes classifier diversity via Q matrix
    5. Regularization controls ensemble size vs. accuracy tradeoff
    """)


if __name__ == "__main__":
    main()
