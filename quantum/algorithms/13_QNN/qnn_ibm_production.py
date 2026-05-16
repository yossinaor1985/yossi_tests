"""
Quantum Neural Networks (QNN) - IBM Production-Ready Implementation
=====================================================================

Production QNN workflow for IBM hardware with error mitigation
and session management.

Qiskit Version: 2.4.1

Production considerations:
    - QNNs require many circuit evaluations (forward + backward passes)
    - Sessions are critical for batching these evaluations efficiently
    - Error mitigation is important for gradient quality
    - Consider shot budget: more shots = better gradients but slower
"""

import json
import os
from datetime import datetime

import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_machine_learning.neural_networks import EstimatorQNN
from qiskit_machine_learning.algorithms import NeuralNetworkClassifier
from qiskit_algorithms.optimizers import COBYLA, SPSA

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Session


def create_production_dataset(n_samples=100):
    """Create and preprocess dataset for QNN training."""
    X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=42)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    y = 2 * y - 1  # Convert to {-1, +1}

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


def build_production_qnn(num_qubits=2, reps=1):
    """
    Build a production QNN with conservative architecture.

    For production:
        - Use fewer reps (1-2) to keep circuit shallow
        - Linear entanglement to match hardware topology
        - ZZFeatureMap for data encoding (captures pairwise correlations)
    """
    from qiskit import QuantumCircuit

    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=1)
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=reps, entanglement='linear')

    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    observable = SparsePauliOp.from_list([("ZI", 1.0)])

    return circuit, feature_map, ansatz, observable


def run_production():
    print("=" * 70)
    print("QNN - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # Configuration
    # =========================================================================

    NUM_QUBITS = 2
    ANSATZ_REPS = 1  # Keep shallow for NISQ
    MAX_ITER = 100
    N_SAMPLES = 80

    # =========================================================================
    # STEP 1: Data Preparation
    # =========================================================================

    print("\n--- Step 1: Data ---")

    X_train, X_test, y_train, y_test = create_production_dataset(N_SAMPLES)
    print(f"Train: {len(X_train)}, Test: {len(X_test)}")

    # =========================================================================
    # STEP 2: Build QNN
    # =========================================================================

    print("\n--- Step 2: QNN Architecture ---")

    circuit, feature_map, ansatz, observable = build_production_qnn(
        NUM_QUBITS, ANSATZ_REPS
    )

    print(f"Circuit depth: {circuit.depth()}")
    print(f"Input params: {feature_map.num_parameters}")
    print(f"Weight params: {ansatz.num_parameters}")

    # =========================================================================
    # STEP 3: Create and Train QNN Classifier
    # =========================================================================

    print("\n--- Step 3: Training ---")

    estimator = AerEstimator()

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_TOKEN")
    # backend = service.least_busy(simulator=False, min_num_qubits=NUM_QUBITS)
    #
    # with Session(service=service, backend=backend) as session:
    #     estimator = EstimatorV2(session=session)
    #     estimator.options.resilience_level = 1
    #     estimator.options.default_shots = 4096
    #     estimator.options.dynamical_decoupling.enable = True
    # -------------------------------------------------------------------------

    qnn = EstimatorQNN(
        circuit=circuit,
        estimator=estimator,
        observables=[observable],
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
    )

    # Use NeuralNetworkClassifier for automated training
    classifier = NeuralNetworkClassifier(
        neural_network=qnn,
        optimizer=COBYLA(maxiter=MAX_ITER),
    )

    # Training callback
    loss_history = []

    print(f"Training with COBYLA (max {MAX_ITER} iterations)...")
    classifier.fit(X_train, y_train)

    # =========================================================================
    # STEP 4: Evaluate
    # =========================================================================

    print("\n--- Step 4: Evaluation ---")

    y_pred_train = classifier.predict(X_train)
    y_pred_test = classifier.predict(X_test)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    print(f"Training accuracy: {train_acc:.4f}")
    print(f"Test accuracy: {test_acc:.4f}")

    # =========================================================================
    # STEP 5: Save Results
    # =========================================================================

    print("\n--- Step 5: Saving ---")

    output_dir = "quantum/algorithms/13_QNN/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "EstimatorQNN Classifier",
        "qiskit_version": "2.4.1",
        "config": {
            "num_qubits": NUM_QUBITS,
            "ansatz_reps": ANSATZ_REPS,
            "feature_map": "ZZFeatureMap",
            "ansatz": "RealAmplitudes",
            "optimizer": "COBYLA",
            "max_iterations": MAX_ITER,
        },
        "results": {
            "train_accuracy": float(train_acc),
            "test_accuracy": float(test_acc),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
        },
    }

    filepath = os.path.join(output_dir, "qnn_results.json")
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
    QNN on IBM Hardware:

    1. Shot Budget Planning:
       - Each forward pass: ~N_train circuit evaluations
       - Each backward pass: ~2 * N_weights * N_train evaluations
       - Total per epoch: ~(1 + 2*N_weights) * N_train circuits
       - Plan for 100+ epochs -> thousands of circuits

    2. Session Management:
       - Use Sessions to batch circuit evaluations
       - Sessions keep your QPU reservation active
       - Reduces queue wait times between evaluations

    3. Error Mitigation:
       - resilience_level=1 (TREX) for gradient quality
       - Dynamical decoupling for idle qubits
       - Consider PEC for high-fidelity gradient estimation

    4. Architecture for NISQ:
       - reps=1 for <10 qubits on current hardware
       - reps=2 maximum for utility-scale experiments
       - Linear entanglement to minimize SWAP overhead

    5. Practical Tips:
       - Start with COBYLA (gradient-free, robust)
       - Switch to SPSA for larger problems
       - Monitor both train and test accuracy
       - Use early stopping to prevent overfitting
    """)


if __name__ == "__main__":
    run_production()
