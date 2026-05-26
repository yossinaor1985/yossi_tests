"""
Federated Quantum Neural Network - Local Simulator
====================================================

This script demonstrates Federated Learning applied to a Parameterized
Quantum Circuit (PQC) for binary classification. Multiple simulated
clients each train a shared QNN architecture on their private local
data, then a central server aggregates the parameter updates via
Federated Averaging (FedAvg).

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Federated Learning (McMahan et al. 2017) enables collaborative model
training without sharing raw data. In the quantum setting (Chen et al.
2021), each client trains the same PQC architecture locally:

    |psi(x, theta)> = W(theta) S(x) |0>^n

where S(x) is a feature map encoding classical data and W(theta) is a
trainable ansatz. The model output is:

    f(x; theta) = <psi(x, theta)| Z_0 |psi(x, theta)>

The Federated Averaging protocol proceeds as:
    1. Server broadcasts global parameters theta^t to all N clients
    2. Each client trains locally for E epochs using parameter shift rule
    3. Clients send updated parameters to server
    4. Server averages: theta^{t+1} = (1/N) sum_i theta_i^{t+1}

Key insight: PQC parameters are classical floats, so aggregation is
identical to classical federated learning. Only parameters are shared;
raw data never leaves the client.

Problem: Binary classification on make_moons (sklearn)
    - 3 federated clients, each with a private data partition
    - 2-qubit PQC: ZZFeatureMap(2, reps=1) + RealAmplitudes(2, reps=1)
    - Observable: Z on qubit 0
    - Comparison with centralized training on the full dataset
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.quantum_info import SparsePauliOp, Statevector


# =============================================================================
# CONFIGURATION
# =============================================================================

np.random.seed(42)
SAVE_DIR = "quantum/algorithms/22_federated_qnn"


# =============================================================================
# DATA GENERATION
# =============================================================================

def create_federated_data(n_samples=150, n_clients=3, test_size=0.2,
                          noise=0.15):
    """
    Generate a binary classification dataset and partition it across clients.

    Creates a make_moons dataset, scales features to [0, pi] for quantum
    encoding, converts labels to {-1, +1}, and splits into N client
    partitions plus a shared test set.

    Args:
        n_samples: Total number of samples to generate.
        n_clients: Number of federated clients.
        test_size: Fraction of data to hold out for testing.
        noise: Noise parameter for make_moons.

    Returns:
        client_data: List of (X_train_i, y_train_i) tuples, one per client.
        X_test: Test features, shape (n_test, 2).
        y_test: Test labels in {-1, +1}, shape (n_test,).
        X_all_train: Combined training features (for centralized baseline).
        y_all_train: Combined training labels (for centralized baseline).
    """
    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=42)

    # Scale features to [0, pi] for quantum feature map encoding
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    # Convert labels: {0, 1} -> {-1, +1}
    y = 2 * y - 1

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    # Partition training data across clients (roughly equal sizes)
    indices = np.arange(len(X_train))
    np.random.shuffle(indices)
    client_indices = np.array_split(indices, n_clients)

    client_data = []
    for idx in client_indices:
        client_data.append((X_train[idx], y_train[idx]))

    return client_data, X_test, y_test, X_train, y_train


# =============================================================================
# QUANTUM CIRCUIT CONSTRUCTION
# =============================================================================

def build_qnn_circuit(num_qubits=2):
    """
    Build the PQC architecture: feature map + trainable ansatz.

    Circuit structure:
        |0>^n --[ZZFeatureMap(x)]--[RealAmplitudes(theta)]-- <Z_0>

    The ZZFeatureMap encodes 2D classical features into qubit rotations
    with entangling ZZ interactions. The RealAmplitudes ansatz provides
    trainable Ry rotations with CNOT entanglement.

    Args:
        num_qubits: Number of qubits (must match feature dimension).

    Returns:
        circuit: The full parameterized QuantumCircuit.
        feature_map: The ZZFeatureMap sub-circuit.
        ansatz: The RealAmplitudes sub-circuit.
        num_feature_params: Number of feature map parameters.
        num_ansatz_params: Number of trainable ansatz parameters.
    """
    feature_map = ZZFeatureMap(num_qubits, reps=1)
    ansatz = RealAmplitudes(num_qubits, reps=1, entanglement='linear')

    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    num_feature_params = feature_map.num_parameters
    num_ansatz_params = ansatz.num_parameters

    return circuit, feature_map, ansatz, num_feature_params, num_ansatz_params


# =============================================================================
# STATEVECTOR-BASED QNN EVALUATION
# =============================================================================

def evaluate_expectation(circuit, feature_params, ansatz_params, x,
                         num_feature_params):
    """
    Compute <Z_0> for a single input x using Statevector simulation.

    Binds feature map parameters to x and ansatz parameters to theta,
    then computes the expectation value of Z on qubit 0.

    Args:
        circuit: The parameterized QNN circuit.
        feature_params: List of Parameter objects for the feature map.
        ansatz_params: List of Parameter objects for the ansatz.
        x: Input feature vector, shape (2,).
        num_feature_params: Number of feature map parameters.

    Returns:
        float: The expectation value <Z_0> in [-1, 1].
    """
    # Build parameter binding dictionary
    param_dict = {}
    all_params = list(circuit.parameters)

    # Feature map parameters come first in the circuit
    feature_param_objs = all_params[:num_feature_params]
    ansatz_param_objs = all_params[num_feature_params:]

    for param, val in zip(feature_param_objs, x):
        param_dict[param] = float(val)
    for param, val in zip(ansatz_param_objs, ansatz_params):
        param_dict[param] = float(val)

    # Bind parameters and compute statevector
    bound_circuit = circuit.assign_parameters(param_dict)
    sv = Statevector(bound_circuit)

    # Observable: Z on qubit 0
    num_qubits = circuit.num_qubits
    z_label = "I" * (num_qubits - 1) + "Z"
    observable = SparsePauliOp.from_list([(z_label, 1.0)])

    expectation = sv.expectation_value(observable).real
    return expectation


def compute_gradient_parameter_shift(circuit, feature_params, ansatz_params,
                                      x, num_feature_params):
    """
    Compute the gradient of <Z_0> w.r.t. ansatz parameters using the
    parameter shift rule.

    For each ansatz parameter theta_k:
        d<Z_0>/d(theta_k) = [<Z_0>(theta_k + pi/2) - <Z_0>(theta_k - pi/2)] / 2

    This is exact (not an approximation) for gates of the form
    exp(-i theta G / 2) where G^2 = I.

    Args:
        circuit: The parameterized QNN circuit.
        feature_params: Feature map Parameter objects.
        ansatz_params: Current ansatz parameter values, shape (p,).
        x: Input feature vector, shape (2,).
        num_feature_params: Number of feature map parameters.

    Returns:
        np.array: Gradient vector, shape (p,).
    """
    num_params = len(ansatz_params)
    gradient = np.zeros(num_params)
    shift = np.pi / 2

    for k in range(num_params):
        # Forward shift: theta_k + pi/2
        params_plus = ansatz_params.copy()
        params_plus[k] += shift

        # Backward shift: theta_k - pi/2
        params_minus = ansatz_params.copy()
        params_minus[k] -= shift

        f_plus = evaluate_expectation(
            circuit, feature_params, params_plus, x, num_feature_params
        )
        f_minus = evaluate_expectation(
            circuit, feature_params, params_minus, x, num_feature_params
        )

        gradient[k] = (f_plus - f_minus) / 2.0

    return gradient


# =============================================================================
# LOCAL TRAINING
# =============================================================================

def train_local(params, X_local, y_local, circuit, num_feature_params,
                lr=0.1, epochs=5):
    """
    Train the QNN locally on one client's data for E epochs.

    Uses MSE loss: L = (1/|D|) sum_j (f(x_j; theta) - y_j)^2
    Gradient: dL/d(theta_k) = (2/|D|) sum_j (f - y) * df/d(theta_k)

    The parameter shift rule computes df/d(theta_k) exactly.

    Args:
        params: Current ansatz parameters, shape (p,). Modified in-place
            is avoided; a copy is returned.
        X_local: Local training features, shape (n_local, 2).
        y_local: Local training labels in {-1, +1}, shape (n_local,).
        circuit: The parameterized QNN circuit.
        num_feature_params: Number of feature map parameters.
        lr: Learning rate for gradient descent.
        epochs: Number of local training epochs.

    Returns:
        np.array: Updated parameter vector, shape (p,).
        list: Loss value at each epoch.
    """
    theta = params.copy()
    loss_history = []
    feature_params = list(circuit.parameters)[:num_feature_params]
    n_samples = len(X_local)

    for epoch in range(epochs):
        total_loss = 0.0
        grad_accumulator = np.zeros_like(theta)

        for j in range(n_samples):
            x_j = X_local[j]
            y_j = y_local[j]

            # Forward pass: compute prediction
            f_j = evaluate_expectation(
                circuit, feature_params, theta, x_j, num_feature_params
            )

            # MSE loss contribution
            residual = f_j - y_j
            total_loss += residual ** 2

            # Gradient via parameter shift rule
            grad_f = compute_gradient_parameter_shift(
                circuit, feature_params, theta, x_j, num_feature_params
            )

            # Chain rule: dL/dtheta = 2 * (f - y) * df/dtheta
            grad_accumulator += 2.0 * residual * grad_f

        # Average gradient over batch
        grad_accumulator /= n_samples
        total_loss /= n_samples

        # Gradient descent step
        theta -= lr * grad_accumulator
        loss_history.append(total_loss)

    return theta, loss_history


# =============================================================================
# FEDERATED AGGREGATION
# =============================================================================

def federated_average(client_params_list):
    """
    Compute the federated average of client parameter vectors.

    FedAvg: theta^{t+1} = (1/N) sum_{i=1}^{N} theta_i^{t+1}

    This is an element-wise arithmetic mean. Since PQC parameters are
    classical floats, this is identical to classical federated averaging.

    Args:
        client_params_list: List of N parameter arrays, each shape (p,).

    Returns:
        np.array: Averaged parameter vector, shape (p,).
    """
    stacked = np.stack(client_params_list, axis=0)
    return np.mean(stacked, axis=0)


# =============================================================================
# EVALUATION
# =============================================================================

def evaluate_qnn(params, X_test, y_test, circuit, num_feature_params):
    """
    Evaluate QNN accuracy on a test set.

    Prediction rule: y_hat = sign(f(x; theta))
    where f is the <Z_0> expectation value.

    Args:
        params: Ansatz parameter vector, shape (p,).
        X_test: Test features, shape (n_test, 2).
        y_test: Test labels in {-1, +1}, shape (n_test,).
        circuit: The parameterized QNN circuit.
        num_feature_params: Number of feature map parameters.

    Returns:
        float: Classification accuracy in [0, 1].
        np.array: Raw predictions (expectation values).
    """
    feature_params = list(circuit.parameters)[:num_feature_params]
    predictions = []

    for x in X_test:
        f = evaluate_expectation(
            circuit, feature_params, params, x, num_feature_params
        )
        predictions.append(f)

    predictions = np.array(predictions)
    y_pred = np.sign(predictions)
    # Handle exact zeros (unlikely but possible)
    y_pred[y_pred == 0] = 1.0

    accuracy = accuracy_score(y_test, y_pred)
    return accuracy, predictions


# =============================================================================
# CENTRALIZED TRAINING (BASELINE)
# =============================================================================

def train_centralized(X_all, y_all, circuit, num_feature_params,
                      lr=0.1, epochs=15):
    """
    Train the QNN on all data combined (centralized baseline).

    This represents the upper bound on accuracy: what you could achieve
    if all data were available in one place. The federated approach
    should ideally approach this accuracy.

    Args:
        X_all: All training features combined, shape (n_total, 2).
        y_all: All training labels combined, shape (n_total,).
        circuit: The parameterized QNN circuit.
        num_feature_params: Number of feature map parameters.
        lr: Learning rate.
        epochs: Total number of training epochs.

    Returns:
        np.array: Trained parameter vector.
        list: Loss at each epoch.
    """
    num_ansatz_params = len(list(circuit.parameters)) - num_feature_params
    theta = np.random.uniform(0, 2 * np.pi, num_ansatz_params)
    feature_params = list(circuit.parameters)[:num_feature_params]

    loss_history = []

    for epoch in range(epochs):
        total_loss = 0.0
        grad_accumulator = np.zeros_like(theta)

        for j in range(len(X_all)):
            x_j = X_all[j]
            y_j = y_all[j]

            f_j = evaluate_expectation(
                circuit, feature_params, theta, x_j, num_feature_params
            )

            residual = f_j - y_j
            total_loss += residual ** 2

            grad_f = compute_gradient_parameter_shift(
                circuit, feature_params, theta, x_j, num_feature_params
            )
            grad_accumulator += 2.0 * residual * grad_f

        grad_accumulator /= len(X_all)
        total_loss /= len(X_all)

        theta -= lr * grad_accumulator
        loss_history.append(total_loss)

        if (epoch + 1) % 5 == 0:
            print(f"    Centralized epoch {epoch + 1}/{epochs}: "
                  f"loss = {total_loss:.4f}")

    return theta, loss_history


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_decision_boundary(ax, params, circuit, num_feature_params, X, y,
                           title, resolution=30):
    """
    Plot the QNN decision boundary over a 2D feature space.

    Creates a mesh grid over [0, pi] x [0, pi], evaluates the QNN at
    each grid point, and plots the sign of the prediction as a filled
    contour with data points overlaid.

    Args:
        ax: Matplotlib axes object to plot on.
        params: Ansatz parameters.
        circuit: QNN circuit.
        num_feature_params: Number of feature map parameters.
        X: Data features, shape (n, 2).
        y: Data labels in {-1, +1}, shape (n,).
        title: Plot title string.
        resolution: Number of grid points per axis.
    """
    feature_params = list(circuit.parameters)[:num_feature_params]

    x_min, x_max = 0, np.pi
    y_min, y_max = 0, np.pi
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, resolution),
        np.linspace(y_min, y_max, resolution)
    )
    grid_points = np.c_[xx.ravel(), yy.ravel()]

    predictions = []
    for pt in grid_points:
        f = evaluate_expectation(
            circuit, feature_params, params, pt, num_feature_params
        )
        predictions.append(f)

    predictions = np.array(predictions).reshape(xx.shape)

    ax.contourf(xx, yy, predictions, levels=50, cmap='RdBu', alpha=0.7)
    ax.contour(xx, yy, predictions, levels=[0.0], colors='k', linewidths=2)

    mask_pos = (y == 1)
    mask_neg = (y == -1)
    ax.scatter(X[mask_pos, 0], X[mask_pos, 1], c='blue', marker='o',
               edgecolors='k', s=30, label='Class +1')
    ax.scatter(X[mask_neg, 0], X[mask_neg, 1], c='red', marker='s',
               edgecolors='k', s=30, label='Class -1')

    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')
    ax.set_title(title, fontsize=11)
    ax.legend(fontsize=8, loc='upper left')


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Federated Quantum Neural Network - Local Simulator")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Generate Federated Data
    # =========================================================================

    print("\n--- Step 1: Generate Federated Data (3 Clients) ---")

    N_CLIENTS = 3
    client_data, X_test, y_test, X_all_train, y_all_train = \
        create_federated_data(n_samples=150, n_clients=N_CLIENTS)

    print(f"Total training samples: {len(X_all_train)}")
    print(f"Test samples: {len(X_test)}")
    for i, (X_i, y_i) in enumerate(client_data):
        n_pos = np.sum(y_i == 1)
        n_neg = np.sum(y_i == -1)
        print(f"  Client {i+1}: {len(X_i)} samples "
              f"(+1: {n_pos}, -1: {n_neg})")

    # =========================================================================
    # STEP 2: Build Shared PQC Architecture
    # =========================================================================

    print("\n--- Step 2: Build Shared PQC Architecture ---")

    circuit, feature_map, ansatz, num_feat_params, num_ansatz_params = \
        build_qnn_circuit(num_qubits=2)

    print(f"Feature map: ZZFeatureMap(2, reps=1)")
    print(f"  Parameters: {num_feat_params}")
    print(f"Ansatz: RealAmplitudes(2, reps=1, entanglement='linear')")
    print(f"  Parameters: {num_ansatz_params}")
    print(f"Total circuit parameters: {circuit.num_parameters}")
    print(f"Observable: Z on qubit 0")
    print(f"\nCircuit structure:")
    print(circuit.draw(output="text", fold=100))

    # =========================================================================
    # STEP 3: Federated Training (FedAvg)
    # =========================================================================

    print("\n--- Step 3: Federated Training (FedAvg) ---")

    COMM_ROUNDS = 5
    LOCAL_EPOCHS = 5
    LEARNING_RATE = 0.1

    print(f"Communication rounds: {COMM_ROUNDS}")
    print(f"Local epochs per round: {LOCAL_EPOCHS}")
    print(f"Learning rate: {LEARNING_RATE}")
    print(f"Clients: {N_CLIENTS}")

    # Initialize global parameters randomly
    global_params = np.random.uniform(0, 2 * np.pi, num_ansatz_params)
    print(f"\nInitial global parameters: {global_params}")

    federated_accuracy_history = []
    federated_loss_history = []

    for round_t in range(COMM_ROUNDS):
        print(f"\n  === Communication Round {round_t + 1}/{COMM_ROUNDS} ===")

        client_updated_params = []

        for i, (X_i, y_i) in enumerate(client_data):
            # Each client starts from the current global parameters
            updated_params_i, loss_i = train_local(
                params=global_params,
                X_local=X_i,
                y_local=y_i,
                circuit=circuit,
                num_feature_params=num_feat_params,
                lr=LEARNING_RATE,
                epochs=LOCAL_EPOCHS
            )
            client_updated_params.append(updated_params_i)
            print(f"    Client {i+1}: local loss after {LOCAL_EPOCHS} "
                  f"epochs = {loss_i[-1]:.4f}")

        # Server aggregation: federated averaging
        global_params = federated_average(client_updated_params)
        print(f"    Server: aggregated {N_CLIENTS} client updates "
              f"(FedAvg)")

        # Evaluate global model on test set
        acc, _ = evaluate_qnn(
            global_params, X_test, y_test, circuit, num_feat_params
        )
        federated_accuracy_history.append(acc)
        print(f"    Global model test accuracy: {acc:.4f} "
              f"({acc * 100:.1f}%)")

        # Track average client loss for this round
        avg_loss = np.mean([loss_i[-1] for loss_i
                            in [train_local(global_params, X_i, y_i,
                                            circuit, num_feat_params,
                                            lr=0, epochs=1)[1]
                                for X_i, y_i in client_data]])
        federated_loss_history.append(avg_loss)

    federated_final_params = global_params.copy()

    # =========================================================================
    # STEP 4: Centralized Training (Baseline)
    # =========================================================================

    print("\n--- Step 4: Centralized Training (Baseline) ---")
    print(f"Training on all {len(X_all_train)} samples combined...")

    centralized_params, centralized_loss = train_centralized(
        X_all_train, y_all_train, circuit, num_feat_params,
        lr=LEARNING_RATE,
        epochs=COMM_ROUNDS * LOCAL_EPOCHS  # Same total epochs
    )

    centralized_acc, _ = evaluate_qnn(
        centralized_params, X_test, y_test, circuit, num_feat_params
    )
    print(f"  Centralized test accuracy: {centralized_acc:.4f} "
          f"({centralized_acc * 100:.1f}%)")

    # =========================================================================
    # STEP 5: Comparison Table
    # =========================================================================

    print("\n--- Step 5: Comparison Table ---")
    federated_final_acc = federated_accuracy_history[-1]

    print(f"\n{'Metric':<30} | {'Federated':>12} | {'Centralized':>12}")
    print("-" * 60)
    print(f"{'Test accuracy':<30} | "
          f"{federated_final_acc:>11.4f} | "
          f"{centralized_acc:>11.4f}")
    print(f"{'Data shared?':<30} | {'No':>12} | {'Yes':>12}")
    print(f"{'Communication rounds':<30} | "
          f"{COMM_ROUNDS:>12} | {'0':>12}")
    print(f"{'Total local epochs':<30} | "
          f"{COMM_ROUNDS * LOCAL_EPOCHS:>12} | "
          f"{COMM_ROUNDS * LOCAL_EPOCHS:>12}")
    print(f"{'Clients':<30} | {N_CLIENTS:>12} | {'1':>12}")
    print(f"{'Parameters exchanged/round':<30} | "
          f"{num_ansatz_params:>12} | {'N/A':>12}")

    # =========================================================================
    # STEP 6: Visualization
    # =========================================================================

    print("\n--- Step 6: Visualization ---")
    print("Generating plots...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    # --- Plot (0,0): Decision boundary - Federated model ---
    plot_decision_boundary(
        axes[0, 0], federated_final_params, circuit, num_feat_params,
        X_test, y_test,
        f"Federated Model (acc={federated_final_acc:.2f})",
        resolution=25
    )

    # --- Plot (0,1): Decision boundary - Centralized model ---
    plot_decision_boundary(
        axes[0, 1], centralized_params, circuit, num_feat_params,
        X_test, y_test,
        f"Centralized Model (acc={centralized_acc:.2f})",
        resolution=25
    )

    # --- Plot (1,0): Accuracy per communication round ---
    rounds = list(range(1, COMM_ROUNDS + 1))
    axes[1, 0].plot(rounds, federated_accuracy_history, 'o-',
                    color='#2ecc71', linewidth=2, markersize=8,
                    label='Federated')
    axes[1, 0].axhline(y=centralized_acc, color='#3498db',
                       linestyle='--', linewidth=2,
                       label=f'Centralized ({centralized_acc:.2f})')
    axes[1, 0].set_xlabel('Communication Round', fontsize=12)
    axes[1, 0].set_ylabel('Test Accuracy', fontsize=12)
    axes[1, 0].set_title('Federated Convergence vs. Centralized Baseline',
                         fontsize=12)
    axes[1, 0].set_ylim(0, 1.05)
    axes[1, 0].set_xticks(rounds)
    axes[1, 0].legend(fontsize=10)
    axes[1, 0].grid(True, alpha=0.3)
    for r, acc in zip(rounds, federated_accuracy_history):
        axes[1, 0].annotate(f'{acc:.2f}', (r, acc),
                            textcoords="offset points",
                            xytext=(0, 10), ha='center', fontsize=9)

    # --- Plot (1,1): Client data distributions ---
    colors = ['#e74c3c', '#2ecc71', '#3498db']
    markers_pos = ['o', 's', '^']
    markers_neg = ['v', 'D', 'P']

    for i, (X_i, y_i) in enumerate(client_data):
        mask_pos = (y_i == 1)
        mask_neg = (y_i == -1)
        axes[1, 1].scatter(X_i[mask_pos, 0], X_i[mask_pos, 1],
                           c=colors[i], marker=markers_pos[i],
                           edgecolors='k', s=40,
                           label=f'Client {i+1} (+1)', alpha=0.8)
        axes[1, 1].scatter(X_i[mask_neg, 0], X_i[mask_neg, 1],
                           c=colors[i], marker=markers_neg[i],
                           edgecolors='k', s=40,
                           label=f'Client {i+1} (-1)', alpha=0.5)

    axes[1, 1].set_xlabel('Feature 1', fontsize=12)
    axes[1, 1].set_ylabel('Feature 2', fontsize=12)
    axes[1, 1].set_title('Client Data Distributions', fontsize=12)
    axes[1, 1].legend(fontsize=7, loc='upper left', ncol=2)
    axes[1, 1].set_xlim(0, np.pi)
    axes[1, 1].set_ylim(0, np.pi)
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    save_path = f"{SAVE_DIR}/federated_qnn_results.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Plot saved to {save_path}")

    # =========================================================================
    # STEP 7: Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    Federated Quantum Neural Network successfully trained a shared
    2-qubit PQC across {N_CLIENTS} clients without sharing any raw data.

    Architecture:
      Feature map: ZZFeatureMap(2, reps=1)
      Ansatz: RealAmplitudes(2, reps=1, entanglement='linear')
      Trainable parameters: {num_ansatz_params}
      Observable: Z on qubit 0

    Federated Training:
      Communication rounds: {COMM_ROUNDS}
      Local epochs per round: {LOCAL_EPOCHS}
      Final test accuracy: {federated_final_acc:.4f} ({federated_final_acc * 100:.1f}%)
      Accuracy progression: {[f'{a:.2f}' for a in federated_accuracy_history]}

    Centralized Baseline:
      Total epochs: {COMM_ROUNDS * LOCAL_EPOCHS}
      Final test accuracy: {centralized_acc:.4f} ({centralized_acc * 100:.1f}%)

    Key Concepts Demonstrated:
      1. FedAvg protocol: local training + parameter averaging
      2. PQC parameters are classical floats -> standard FL applies
      3. Parameter shift rule for gradient computation
      4. Privacy preservation: only {num_ansatz_params} floats shared per round
      5. Trade-off: privacy vs. convergence speed
      6. {N_CLIENTS} clients x {LOCAL_EPOCHS} local epochs x {COMM_ROUNDS} rounds
         = {N_CLIENTS * LOCAL_EPOCHS * COMM_ROUNDS} total client-epochs

    Data privacy: raw data NEVER left the clients. Only {num_ansatz_params}
    parameter values were shared per client per round.
    """)


if __name__ == "__main__":
    main()
