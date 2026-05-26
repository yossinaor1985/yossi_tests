"""
Federated Quantum Neural Network - IBM Production-Ready Implementation
=======================================================================

Production pipeline for Federated QML using Parameterized Quantum Circuits:
    1. Configurable federated data generation (N clients, IID/non-IID)
    2. Shared PQC architecture: ZZFeatureMap + RealAmplitudes
    3. Local training via parameter shift rule (Statevector simulation)
    4. Federated Averaging (FedAvg) with configurable aggregation
    5. Centralized baseline for comparison
    6. Result persistence to JSON
    7. Warm-start support for multi-stage training

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Key production features:
    - Full configuration section for reproducibility
    - Warm-start from previous training checkpoints
    - Per-round metric logging (accuracy, loss, parameter norms)
    - JSON result persistence with timestamps and full metadata
    - Commented IBM hardware sections ready for real backend execution

References:
    - McMahan et al. (2017): FedAvg algorithm
    - Chen et al. (2021): Federated Quantum ML
    - Li et al. (2021): Non-IID analysis for quantum FL
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

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# IBM Runtime imports (uncomment for real hardware deployment)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, SamplerV2, Session


# =============================================================================
# CONFIGURATION
# =============================================================================

# --- Federated Learning ---
N_CLIENTS = 3                # Number of federated clients
COMM_ROUNDS = 5              # Number of server-client communication rounds
LOCAL_EPOCHS = 5             # Local training epochs per client per round
LEARNING_RATE = 0.1          # Client-side learning rate
AGGREGATION = "uniform"      # "uniform" (1/N) or "weighted" (|D_i|/|D|)

# --- PQC Architecture ---
NUM_QUBITS = 2               # Number of qubits
FEATURE_MAP_REPS = 1         # ZZFeatureMap repetitions
ANSATZ_REPS = 1              # RealAmplitudes repetitions
ANSATZ_ENTANGLEMENT = "linear"  # Entanglement pattern

# --- Data ---
N_SAMPLES = 150              # Total dataset size
TEST_SIZE = 0.2              # Fraction held out for testing
NOISE = 0.15                 # make_moons noise level
RANDOM_SEED = 42             # Reproducibility seed

# --- Warm-start ---
USE_WARM_START = False        # If True, load initial params from file
WARM_START_PATH = None        # Path to JSON with previous results

# --- Output ---
RESULTS_DIR = "quantum/algorithms/22_federated_qnn/results"

# --- Hardware ---
SHOTS = 8192                  # Shots for hardware/shot-based simulation


# =============================================================================
# IBM QUANTUM SERVICE (uncomment for real hardware)
# =============================================================================
# service = QiskitRuntimeService(
#     channel="ibm_quantum",
#     token="YOUR_IBM_QUANTUM_TOKEN"
# )
# backend = service.least_busy(
#     simulator=False,
#     min_num_qubits=NUM_QUBITS,
#     operational=True
# )
# print(f"Selected backend: {backend.name}")


# =============================================================================
# DATA GENERATION
# =============================================================================

def create_federated_dataset(n_samples=N_SAMPLES, n_clients=N_CLIENTS,
                              test_size=TEST_SIZE, noise=NOISE,
                              seed=RANDOM_SEED):
    """
    Generate and partition a classification dataset for federated learning.

    Creates a make_moons dataset, scales to [0, pi], converts labels to
    {-1, +1}, splits into train/test, then partitions training data
    across N clients.

    Parameters
    ----------
    n_samples : int
        Total number of samples.
    n_clients : int
        Number of federated clients.
    test_size : float
        Fraction held out for testing.
    noise : float
        Noise parameter for make_moons.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    client_data : list of (ndarray, ndarray)
        Each entry is (X_i, y_i) for client i.
    X_test : ndarray, shape (n_test, 2)
        Test features.
    y_test : ndarray, shape (n_test,)
        Test labels in {-1, +1}.
    X_train : ndarray, shape (n_train, 2)
        All training features combined.
    y_train : ndarray, shape (n_train,)
        All training labels combined.
    """
    np.random.seed(seed)

    X, y = make_moons(n_samples=n_samples, noise=noise, random_state=seed)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    y = 2 * y - 1  # {0, 1} -> {-1, +1}

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed, stratify=y
    )

    indices = np.arange(len(X_train))
    np.random.shuffle(indices)
    client_indices = np.array_split(indices, n_clients)

    client_data = []
    for idx in client_indices:
        client_data.append((X_train[idx], y_train[idx]))

    return client_data, X_test, y_test, X_train, y_train


# =============================================================================
# PQC CONSTRUCTION
# =============================================================================

def build_pqc(num_qubits=NUM_QUBITS, fm_reps=FEATURE_MAP_REPS,
              ansatz_reps=ANSATZ_REPS, entanglement=ANSATZ_ENTANGLEMENT):
    """
    Build the shared PQC architecture.

    Circuit: |0>^n --[ZZFeatureMap(x)]--[RealAmplitudes(theta)]-- <Z_0>

    Parameters
    ----------
    num_qubits : int
        Number of qubits.
    fm_reps : int
        ZZFeatureMap repetition count.
    ansatz_reps : int
        RealAmplitudes repetition count.
    entanglement : str
        Entanglement pattern for ansatz ('linear', 'full', 'circular').

    Returns
    -------
    circuit : QuantumCircuit
        The full parameterized circuit.
    num_feature_params : int
        Number of feature map parameters.
    num_ansatz_params : int
        Number of trainable ansatz parameters.
    """
    feature_map = ZZFeatureMap(num_qubits, reps=fm_reps)
    ansatz = RealAmplitudes(num_qubits, reps=ansatz_reps,
                            entanglement=entanglement)

    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    return circuit, feature_map.num_parameters, ansatz.num_parameters


# =============================================================================
# STATEVECTOR QNN ENGINE
# =============================================================================

def qnn_forward(circuit, ansatz_params, x, num_feature_params):
    """
    Compute <Z_0> for input x with given ansatz parameters.

    Uses Statevector simulation (exact, noiseless).

    Parameters
    ----------
    circuit : QuantumCircuit
        The parameterized PQC.
    ansatz_params : ndarray, shape (p,)
        Current trainable parameters.
    x : ndarray, shape (d,)
        Input feature vector.
    num_feature_params : int
        Number of feature map parameters.

    Returns
    -------
    float
        Expectation value <Z_0> in [-1, 1].
    """
    all_params = list(circuit.parameters)
    param_dict = {}

    for param, val in zip(all_params[:num_feature_params], x):
        param_dict[param] = float(val)
    for param, val in zip(all_params[num_feature_params:], ansatz_params):
        param_dict[param] = float(val)

    bound = circuit.assign_parameters(param_dict)
    sv = Statevector(bound)

    num_q = circuit.num_qubits
    z_label = "I" * (num_q - 1) + "Z"
    obs = SparsePauliOp.from_list([(z_label, 1.0)])

    return sv.expectation_value(obs).real


def qnn_gradient(circuit, ansatz_params, x, num_feature_params):
    """
    Gradient of <Z_0> w.r.t. ansatz parameters via parameter shift rule.

    d<Z_0>/d(theta_k) = [<Z_0>(theta_k + pi/2) - <Z_0>(theta_k - pi/2)] / 2

    Parameters
    ----------
    circuit : QuantumCircuit
        The parameterized PQC.
    ansatz_params : ndarray, shape (p,)
        Current trainable parameters.
    x : ndarray, shape (d,)
        Input feature vector.
    num_feature_params : int
        Number of feature map parameters.

    Returns
    -------
    ndarray, shape (p,)
        Gradient vector.
    """
    p = len(ansatz_params)
    grad = np.zeros(p)
    shift = np.pi / 2

    for k in range(p):
        params_plus = ansatz_params.copy()
        params_plus[k] += shift
        params_minus = ansatz_params.copy()
        params_minus[k] -= shift

        f_plus = qnn_forward(circuit, params_plus, x, num_feature_params)
        f_minus = qnn_forward(circuit, params_minus, x, num_feature_params)
        grad[k] = (f_plus - f_minus) / 2.0

    return grad


# =============================================================================
# LOCAL TRAINING ENGINE
# =============================================================================

def local_train(circuit, params, X_local, y_local, num_feature_params,
                lr=LEARNING_RATE, epochs=LOCAL_EPOCHS):
    """
    Perform local SGD training on one client's data.

    MSE loss: L = (1/|D|) sum (f(x; theta) - y)^2
    Gradient: dL/dtheta = (2/|D|) sum (f - y) * df/dtheta

    Parameters
    ----------
    circuit : QuantumCircuit
        Shared PQC architecture.
    params : ndarray, shape (p,)
        Starting parameters (from global model).
    X_local : ndarray, shape (n_i, d)
        Client's local features.
    y_local : ndarray, shape (n_i,)
        Client's local labels.
    num_feature_params : int
        Number of feature map parameters.
    lr : float
        Learning rate.
    epochs : int
        Number of local epochs.

    Returns
    -------
    ndarray, shape (p,)
        Updated parameters after local training.
    list of float
        Loss at each epoch.
    """
    theta = params.copy()
    n = len(X_local)
    loss_hist = []

    for ep in range(epochs):
        total_loss = 0.0
        grad_acc = np.zeros_like(theta)

        for j in range(n):
            f_j = qnn_forward(circuit, theta, X_local[j], num_feature_params)
            res = f_j - y_local[j]
            total_loss += res ** 2
            g = qnn_gradient(circuit, theta, X_local[j], num_feature_params)
            grad_acc += 2.0 * res * g

        grad_acc /= n
        total_loss /= n
        theta -= lr * grad_acc
        loss_hist.append(total_loss)

    return theta, loss_hist


# =============================================================================
# FEDERATED AGGREGATION
# =============================================================================

def federated_aggregate(client_params_list, client_sizes=None,
                         mode=AGGREGATION):
    """
    Aggregate client parameters via federated averaging.

    Supports:
    - "uniform": theta^{t+1} = (1/N) sum_i theta_i
    - "weighted": theta^{t+1} = sum_i (|D_i|/|D|) theta_i

    Parameters
    ----------
    client_params_list : list of ndarray
        Each entry is shape (p,).
    client_sizes : list of int or None
        Dataset size per client (required for weighted mode).
    mode : str
        "uniform" or "weighted".

    Returns
    -------
    ndarray, shape (p,)
        Aggregated parameter vector.
    """
    if mode == "uniform":
        return np.mean(np.stack(client_params_list), axis=0)
    elif mode == "weighted":
        if client_sizes is None:
            raise ValueError("client_sizes required for weighted aggregation")
        total = sum(client_sizes)
        weights = np.array([s / total for s in client_sizes])
        stacked = np.stack(client_params_list)
        return np.sum(stacked * weights[:, None], axis=0)
    else:
        raise ValueError(f"Unknown aggregation mode: {mode}")


# =============================================================================
# EVALUATION
# =============================================================================

def evaluate_model(circuit, params, X, y, num_feature_params):
    """
    Evaluate QNN accuracy on a dataset.

    Prediction: y_hat = sign(<Z_0>).

    Parameters
    ----------
    circuit : QuantumCircuit
        The PQC.
    params : ndarray, shape (p,)
        Ansatz parameters.
    X : ndarray, shape (n, d)
        Features.
    y : ndarray, shape (n,)
        True labels in {-1, +1}.
    num_feature_params : int
        Number of feature map parameters.

    Returns
    -------
    float
        Accuracy in [0, 1].
    float
        Mean loss (MSE).
    ndarray
        Raw predictions.
    """
    preds = np.array([
        qnn_forward(circuit, params, x, num_feature_params) for x in X
    ])
    y_hat = np.sign(preds)
    y_hat[y_hat == 0] = 1.0

    acc = accuracy_score(y, y_hat)
    mse = np.mean((preds - y) ** 2)
    return acc, mse, preds


# =============================================================================
# CENTRALIZED BASELINE
# =============================================================================

def train_centralized_baseline(circuit, X, y, num_feature_params,
                                num_ansatz_params, lr=LEARNING_RATE,
                                total_epochs=None):
    """
    Centralized training on all data combined.

    This is the accuracy upper bound: what you could achieve if all
    data were available in one place.

    Parameters
    ----------
    circuit : QuantumCircuit
        The PQC.
    X : ndarray, shape (n, d)
        All training features.
    y : ndarray, shape (n,)
        All training labels.
    num_feature_params : int
        Number of feature map parameters.
    num_ansatz_params : int
        Number of ansatz parameters.
    lr : float
        Learning rate.
    total_epochs : int or None
        Total epochs (defaults to COMM_ROUNDS * LOCAL_EPOCHS).

    Returns
    -------
    ndarray, shape (p,)
        Trained parameters.
    list of float
        Loss at each epoch.
    """
    if total_epochs is None:
        total_epochs = COMM_ROUNDS * LOCAL_EPOCHS

    np.random.seed(RANDOM_SEED + 1000)  # Different seed from federated init
    theta = np.random.uniform(0, 2 * np.pi, num_ansatz_params)
    loss_hist = []

    for ep in range(total_epochs):
        total_loss = 0.0
        grad_acc = np.zeros_like(theta)

        for j in range(len(X)):
            f_j = qnn_forward(circuit, theta, X[j], num_feature_params)
            res = f_j - y[j]
            total_loss += res ** 2
            g = qnn_gradient(circuit, theta, X[j], num_feature_params)
            grad_acc += 2.0 * res * g

        grad_acc /= len(X)
        total_loss /= len(X)
        theta -= lr * grad_acc
        loss_hist.append(total_loss)

        if (ep + 1) % 5 == 0:
            print(f"    Centralized epoch {ep + 1}/{total_epochs}: "
                  f"loss = {total_loss:.4f}")

    return theta, loss_hist


# =============================================================================
# WARM-START SUPPORT
# =============================================================================

def load_warm_start(filepath):
    """
    Load initial parameters from a previous training result.

    Parameters
    ----------
    filepath : str
        Path to JSON results file from a previous run.

    Returns
    -------
    ndarray
        Parameter vector to use as initialization.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    params = np.array(data["results"]["federated"]["final_parameters"])
    print(f"  Warm-start loaded from {filepath}")
    print(f"  Parameters: {params}")
    return params


# =============================================================================
# MAIN PRODUCTION PIPELINE
# =============================================================================

def run_federated_qnn_production():
    """
    Full production pipeline for Federated Quantum Neural Network.
    """
    print("=" * 70)
    print("Federated QNN - Production IBM Quantum Implementation")
    print("=" * 70)

    # Print configuration
    print(f"\nConfiguration:")
    print(f"  Clients: {N_CLIENTS}")
    print(f"  Communication rounds: {COMM_ROUNDS}")
    print(f"  Local epochs: {LOCAL_EPOCHS}")
    print(f"  Learning rate: {LEARNING_RATE}")
    print(f"  Aggregation: {AGGREGATION}")
    print(f"  Qubits: {NUM_QUBITS}")
    print(f"  Feature map reps: {FEATURE_MAP_REPS}")
    print(f"  Ansatz reps: {ANSATZ_REPS}")
    print(f"  Entanglement: {ANSATZ_ENTANGLEMENT}")
    print(f"  Samples: {N_SAMPLES}")
    print(f"  Test fraction: {TEST_SIZE}")
    print(f"  Warm-start: {USE_WARM_START}")

    # =========================================================================
    # STEP 1: Backend Selection
    # =========================================================================

    print("\n--- Step 1: Backend Selection ---")
    print("Using local Aer simulator for demonstration.")

    # -----------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # service = QiskitRuntimeService(
    #     channel="ibm_quantum",
    #     token="YOUR_TOKEN"
    # )
    # backend = service.least_busy(
    #     simulator=False,
    #     min_num_qubits=NUM_QUBITS,
    #     operational=True
    # )
    # print(f"Backend: {backend.name}")
    #
    # # Transpile the circuit for the target backend
    # pm = generate_preset_pass_manager(optimization_level=3,
    #                                   backend=backend)
    # -----------------------------------------------------------------

    # =========================================================================
    # STEP 2: Data Setup
    # =========================================================================

    print("\n--- Step 2: Federated Data Generation ---")

    client_data, X_test, y_test, X_train, y_train = \
        create_federated_dataset()

    client_sizes = [len(X_i) for X_i, _ in client_data]

    print(f"Total training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    for i, (X_i, y_i) in enumerate(client_data):
        n_pos = np.sum(y_i == 1)
        n_neg = np.sum(y_i == -1)
        print(f"  Client {i+1}: {len(X_i)} samples "
              f"(+1: {n_pos}, -1: {n_neg})")

    # =========================================================================
    # STEP 3: Build Shared PQC
    # =========================================================================

    print("\n--- Step 3: Shared PQC Architecture ---")

    circuit, num_feat_params, num_ansatz_params = build_pqc()

    print(f"Feature map: ZZFeatureMap({NUM_QUBITS}, reps={FEATURE_MAP_REPS})")
    print(f"Ansatz: RealAmplitudes({NUM_QUBITS}, reps={ANSATZ_REPS}, "
          f"entanglement='{ANSATZ_ENTANGLEMENT}')")
    print(f"Feature map parameters: {num_feat_params}")
    print(f"Ansatz (trainable) parameters: {num_ansatz_params}")
    print(f"Total circuit depth: {circuit.depth()}")

    # -----------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # transpiled = pm.run(circuit)
    # print(f"Transpiled depth: {transpiled.depth()}")
    # print(f"CX count: {transpiled.count_ops().get('cx', 0)}")
    # -----------------------------------------------------------------

    # =========================================================================
    # STEP 4: Initialize Parameters
    # =========================================================================

    print("\n--- Step 4: Parameter Initialization ---")

    if USE_WARM_START and WARM_START_PATH is not None:
        global_params = load_warm_start(WARM_START_PATH)
    else:
        np.random.seed(RANDOM_SEED)
        global_params = np.random.uniform(0, 2 * np.pi, num_ansatz_params)
        print(f"Random initialization: {global_params}")

    # =========================================================================
    # STEP 5: Federated Training
    # =========================================================================

    print("\n--- Step 5: Federated Training (FedAvg) ---")

    round_metrics = []

    for round_t in range(COMM_ROUNDS):
        print(f"\n  === Communication Round {round_t + 1}/{COMM_ROUNDS} ===")

        client_updated_params = []
        client_losses = []

        for i, (X_i, y_i) in enumerate(client_data):
            updated_i, loss_i = local_train(
                circuit, global_params, X_i, y_i, num_feat_params,
                lr=LEARNING_RATE, epochs=LOCAL_EPOCHS
            )
            client_updated_params.append(updated_i)
            client_losses.append(loss_i[-1])
            print(f"    Client {i+1}: final local loss = {loss_i[-1]:.4f}")

        # Federated aggregation
        global_params = federated_aggregate(
            client_updated_params, client_sizes, mode=AGGREGATION
        )

        # Evaluate global model
        acc, mse, _ = evaluate_model(
            circuit, global_params, X_test, y_test, num_feat_params
        )

        param_norm = np.linalg.norm(global_params)
        avg_client_loss = np.mean(client_losses)

        print(f"    Server: aggregated {N_CLIENTS} clients ({AGGREGATION})")
        print(f"    Global test accuracy: {acc:.4f} ({acc * 100:.1f}%)")
        print(f"    Average client loss: {avg_client_loss:.4f}")
        print(f"    Parameter norm: {param_norm:.4f}")

        round_metrics.append({
            "round": round_t + 1,
            "test_accuracy": float(acc),
            "test_mse": float(mse),
            "avg_client_loss": float(avg_client_loss),
            "param_norm": float(param_norm),
            "parameters": global_params.tolist(),
        })

    federated_params = global_params.copy()
    federated_acc = round_metrics[-1]["test_accuracy"]

    # =========================================================================
    # STEP 6: Centralized Baseline
    # =========================================================================

    print("\n--- Step 6: Centralized Baseline ---")

    total_epochs = COMM_ROUNDS * LOCAL_EPOCHS
    print(f"Training centralized model for {total_epochs} epochs "
          f"on {len(X_train)} samples...")

    centralized_params, centralized_loss = train_centralized_baseline(
        circuit, X_train, y_train, num_feat_params, num_ansatz_params,
        lr=LEARNING_RATE, total_epochs=total_epochs
    )

    centralized_acc, centralized_mse, _ = evaluate_model(
        circuit, centralized_params, X_test, y_test, num_feat_params
    )
    print(f"  Centralized test accuracy: {centralized_acc:.4f}")

    # =========================================================================
    # STEP 7: Results Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION RESULTS")
    print("=" * 70)

    print(f"\n  Federated Model:")
    print(f"    Final accuracy: {federated_acc:.4f} "
          f"({federated_acc * 100:.1f}%)")
    print(f"    Communication rounds: {COMM_ROUNDS}")
    print(f"    Parameters per exchange: {num_ansatz_params}")
    print(f"    Total floats communicated: "
          f"{COMM_ROUNDS * N_CLIENTS * num_ansatz_params}")

    print(f"\n  Centralized Model:")
    print(f"    Final accuracy: {centralized_acc:.4f} "
          f"({centralized_acc * 100:.1f}%)")
    print(f"    Total epochs: {total_epochs}")

    print(f"\n  Accuracy gap: "
          f"{abs(federated_acc - centralized_acc):.4f}")

    # =========================================================================
    # STEP 8: Save Results to JSON
    # =========================================================================

    print("\n--- Step 8: Saving Results ---")

    os.makedirs(RESULTS_DIR, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "Federated_QNN",
        "qiskit_version": "2.4.1",
        "configuration": {
            "n_clients": N_CLIENTS,
            "comm_rounds": COMM_ROUNDS,
            "local_epochs": LOCAL_EPOCHS,
            "learning_rate": LEARNING_RATE,
            "aggregation_mode": AGGREGATION,
            "num_qubits": NUM_QUBITS,
            "feature_map": f"ZZFeatureMap({NUM_QUBITS}, reps={FEATURE_MAP_REPS})",
            "ansatz": f"RealAmplitudes({NUM_QUBITS}, reps={ANSATZ_REPS}, "
                      f"entanglement='{ANSATZ_ENTANGLEMENT}')",
            "num_feature_params": num_feat_params,
            "num_ansatz_params": num_ansatz_params,
            "observable": "Z_0",
            "n_samples": N_SAMPLES,
            "test_size": TEST_SIZE,
            "noise": NOISE,
            "random_seed": RANDOM_SEED,
            "warm_start": USE_WARM_START,
            "backend": "aer_simulator (demo)",
            "shots": SHOTS,
        },
        "data": {
            "total_train_samples": len(X_train),
            "test_samples": len(X_test),
            "client_sizes": client_sizes,
            "client_label_counts": [
                {"+1": int(np.sum(y_i == 1)),
                 "-1": int(np.sum(y_i == -1))}
                for _, y_i in client_data
            ],
        },
        "results": {
            "federated": {
                "final_accuracy": float(federated_acc),
                "final_parameters": federated_params.tolist(),
                "round_metrics": round_metrics,
                "total_floats_communicated":
                    COMM_ROUNDS * N_CLIENTS * num_ansatz_params,
            },
            "centralized": {
                "final_accuracy": float(centralized_acc),
                "final_mse": float(centralized_mse),
                "final_parameters": centralized_params.tolist(),
                "total_epochs": total_epochs,
                "loss_history": [float(l) for l in centralized_loss],
            },
            "accuracy_gap": float(abs(federated_acc - centralized_acc)),
        },
    }

    filepath = os.path.join(RESULTS_DIR, "federated_qnn_results.json")
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
    Federated QNN - Production Considerations:

    1. Communication Overhead:
       - Each round: N clients send p floats each to the server,
         server sends p floats back to each client.
       - Total per round: 2 * N * p * sizeof(float64) bytes.
       - For our setup: 2 * 3 * 4 * 8 = 192 bytes/round (negligible).
       - For production (50 clients, 100 params): 80 KB/round.
       - Communication is NOT the bottleneck; local circuit evaluation is.
       - Compression: quantize parameters to float16 or send only deltas.

    2. Differential Privacy:
       - Add Gaussian noise to parameter updates before sharing:
         theta_i^noisy = theta_i + N(0, sigma^2 * I)
       - Calibrate sigma for (epsilon, delta)-DP guarantee.
       - Trade-off: sigma too large -> convergence degradation.
       - For PQCs with few parameters (p ~ 10), DP noise has
         outsized impact compared to classical DNNs with millions of params.
       - Consider secure aggregation as a noise-free alternative.

    3. Non-IID Data Challenges:
       - If clients have biased label distributions, FedAvg suffers
         from "client drift" (local optima diverge).
       - Symptoms: oscillating global accuracy, never reaching
         centralized baseline.
       - Mitigations:
         (a) FedProx: add proximal term mu/2 ||theta - theta_global||^2
         (b) Increase comm_rounds, decrease local_epochs
         (c) Share a small public dataset across clients
         (d) Use momentum-based aggregation (FedAdam, FedYogi)
       - Detection: monitor per-client loss variance across rounds.

    4. Hardware Heterogeneity:
       - In a real deployment, different clients may have access to
         different quantum hardware (different gate sets, noise levels).
       - Transpilation must be done per-client to match their backend.
       - Noisy clients produce noisier gradient estimates, biasing
         the federated average.
       - Mitigation: weight aggregation by inverse noise level or
         use robust aggregation (trimmed mean, median).
       - Stragglers: set a timeout per round; if a client doesn't
         report in time, proceed with the others (partial aggregation).

    5. Scaling to More Qubits:
       - Ansatz parameter count scales as O(n * reps) for
         RealAmplitudes with linear entanglement.
       - More parameters -> more communication, more gradient evals.
       - For n > 10 qubits, consider:
         (a) Mini-batch local training (not full-batch)
         (b) SPSA optimizer instead of parameter shift (fewer evals)
         (c) Layer-wise federated training (federate only some layers)
       - Circuit depth increases linearly with reps; transpiled depth
         grows with backend connectivity constraints.

    6. Warm-Start Strategy:
       - Set USE_WARM_START = True and provide WARM_START_PATH to
         resume from a previous checkpoint.
       - Useful for: incremental learning (new data arrives),
         hyperparameter tuning (try different learning rates from
         the same starting point), hardware migration (start on
         simulator, fine-tune on hardware).

    7. Security Threats:
       - Model poisoning: a malicious client sends adversarial
         parameter updates to degrade the global model.
       - Mitigation: Byzantine-robust aggregation (Krum, multi-Krum,
         coordinate-wise median).
       - Free-riding: a client sends back unchanged parameters to
         benefit from others' training without contributing.
       - Detection: monitor parameter delta norms per client.
    """)


if __name__ == "__main__":
    run_federated_qnn_production()
