"""
Quantum Neural Networks (QNN) - Local Simulator Implementation
================================================================

This script demonstrates both EstimatorQNN and SamplerQNN from
qiskit_machine_learning for classification and regression tasks.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
QNNs implement: f(x; theta) = <0| U^dag(x,theta) O U(x,theta) |0>

Two types:
    - EstimatorQNN: output = <O> (expectation value)
    - SamplerQNN: output = P(z) (probability distribution)

Architecture: Feature map W(x) + Ansatz V(theta) + Measurement O
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_circles
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes, EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import EstimatorV2 as AerEstimator, SamplerV2 as AerSampler
from qiskit_machine_learning.neural_networks import EstimatorQNN, SamplerQNN
from qiskit_machine_learning.connectors import TorchConnector
from qiskit_algorithms.optimizers import COBYLA, L_BFGS_B


def create_dataset(n_samples=200, dataset_type="moons"):
    """
    Create a synthetic binary classification dataset.

    Args:
        n_samples: Number of data points
        dataset_type: "moons" or "circles"

    Returns:
        X_train, X_test, y_train, y_test: Split dataset
    """
    if dataset_type == "moons":
        X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=42)
    else:
        X, y = make_circles(n_samples=n_samples, noise=0.1, factor=0.5, random_state=42)

    # Scale features to [0, pi] for quantum encoding
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    return X_train, X_test, y_train, y_test


def build_qnn_circuit(num_qubits=2, reps=1):
    """
    Build a QNN circuit with feature map + ansatz.

    Architecture (see explanation_physicist.md, Section 2.1):
        |psi(x, theta)> = V(theta) W(x) |0>

    Feature map W(x): ZZFeatureMap encodes data x into the quantum state
        using Z and ZZ rotations.
    Ansatz V(theta): RealAmplitudes with trainable R_Y rotations.

    Returns:
        circuit: Combined feature map + ansatz circuit
        feature_map: The data encoding circuit
        ansatz: The trainable circuit
    """
    # Feature map: encodes 2D data into 2 qubits
    # See PQC_ansatz_design/explanation_physicist.md, Section 8
    feature_map = ZZFeatureMap(
        feature_dimension=num_qubits,
        reps=1,
    )

    # Ansatz: trainable variational circuit
    ansatz = RealAmplitudes(
        num_qubits=num_qubits,
        reps=reps,
        entanglement='linear',
    )

    # Combine: feature_map + ansatz
    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    return circuit, feature_map, ansatz


def demo_estimator_qnn():
    """
    Demonstrate EstimatorQNN for binary classification.

    EstimatorQNN outputs: <psi(x, theta)| O |psi(x, theta)>
    where O is a Pauli observable (e.g., Z on qubit 0).

    Output range: [-1, 1]
    Classification: sign(output) determines the class

    See explanation_physicist.md, Section 2.2.
    """
    print("\n" + "=" * 70)
    print("PART A: EstimatorQNN for Classification")
    print("=" * 70)

    # Dataset
    X_train, X_test, y_train, y_test = create_dataset(n_samples=100, dataset_type="moons")
    # Convert labels from {0, 1} to {-1, +1} for EstimatorQNN
    y_train_est = 2 * y_train - 1
    y_test_est = 2 * y_test - 1

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Build QNN circuit
    num_qubits = 2
    circuit, feature_map, ansatz = build_qnn_circuit(num_qubits, reps=2)

    print(f"\nQNN Circuit:")
    print(f"  Feature map: ZZFeatureMap ({feature_map.num_parameters} input params)")
    print(f"  Ansatz: RealAmplitudes ({ansatz.num_parameters} trainable params)")
    print(f"  Total circuit depth: {circuit.depth()}")
    print(f"\n{circuit.draw(output='text', fold=80)}")

    # Create EstimatorQNN
    # Observable: Z on qubit 0 (binary output)
    observable = SparsePauliOp.from_list([("ZI", 1.0)])

    estimator = AerEstimator()

    qnn = EstimatorQNN(
        circuit=circuit,
        estimator=estimator,
        observables=[observable],
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
    )

    print(f"\nEstimatorQNN created:")
    print(f"  Input features: {qnn.num_inputs}")
    print(f"  Trainable weights: {qnn.num_weights}")
    print(f"  Output dimension: {qnn.output_shape}")

    # Forward pass with random weights
    initial_weights = np.random.default_rng(42).uniform(
        -np.pi, np.pi, qnn.num_weights
    )

    # Test forward pass
    sample_output = qnn.forward(X_train[:5], initial_weights)
    print(f"\nSample forward pass (5 points):")
    print(f"  Outputs: {sample_output.flatten()}")
    print(f"  Expected: {y_train_est[:5]}")

    # Test backward pass (gradients)
    input_grad, weight_grad = qnn.backward(X_train[:1], initial_weights)
    print(f"\nBackward pass (gradients):")
    print(f"  Weight gradient shape: {weight_grad.shape}")
    print(f"  Weight gradient sample: {weight_grad[0, 0, :3]}...")

    return qnn, X_train, X_test, y_train_est, y_test_est, initial_weights


def demo_sampler_qnn():
    """
    Demonstrate SamplerQNN for binary classification.

    SamplerQNN outputs: P(z | x, theta) for each measurement outcome z.
    With an interpret function, we map bitstrings to class labels.

    See explanation_physicist.md, Section 2.3.
    """
    print("\n" + "=" * 70)
    print("PART B: SamplerQNN for Classification")
    print("=" * 70)

    # Dataset
    X_train, X_test, y_train, y_test = create_dataset(n_samples=100, dataset_type="circles")

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Build circuit with measurements
    num_qubits = 2
    circuit, feature_map, ansatz = build_qnn_circuit(num_qubits, reps=2)

    # Define interpret function: maps bitstrings to class labels
    # Parity function: XOR of all bits
    def parity(x):
        """Map bitstring integer to binary class via parity."""
        return x % 2  # Even -> 0, Odd -> 1

    sampler = AerSampler()

    qnn = SamplerQNN(
        circuit=circuit,
        sampler=sampler,
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
        interpret=parity,
        output_shape=2,  # 2 classes
    )

    print(f"\nSamplerQNN created:")
    print(f"  Input features: {qnn.num_inputs}")
    print(f"  Trainable weights: {qnn.num_weights}")
    print(f"  Output dimension: {qnn.output_shape}")

    # Forward pass
    initial_weights = np.random.default_rng(42).uniform(
        -np.pi, np.pi, qnn.num_weights
    )

    sample_output = qnn.forward(X_train[:5], initial_weights)
    print(f"\nSample forward pass (5 points):")
    print(f"  P(class=0), P(class=1):")
    for i in range(5):
        print(f"    Point {i}: [{sample_output[i, 0]:.4f}, {sample_output[i, 1]:.4f}] "
              f"-> predicted class {np.argmax(sample_output[i])}, actual {y_train[i]}")

    return qnn, X_train, X_test, y_train, y_test, initial_weights


def build_data_reuploading_qnn(num_qubits=1, num_layers=3):
    """
    Build a data re-uploading QNN (universal quantum classifier).

    Architecture (see explanation_physicist.md, Section 3.1):
        U(x, theta) = V_L(theta_L) W(x) ... V_1(theta_1) W(x)

    Data x is encoded multiple times, interleaved with trainable rotations.
    This is provably universal for function approximation.

    Args:
        num_qubits: Number of qubits
        num_layers: Number of data re-uploading layers

    Returns:
        QuantumCircuit: The re-uploading QNN circuit
    """
    input_params = ParameterVector('x', 2)  # 2D input
    weight_params = ParameterVector('w', 3 * num_layers)  # 3 rotations per layer

    qc = QuantumCircuit(num_qubits)

    for l in range(num_layers):
        # Data encoding (re-uploaded each layer)
        qc.ry(input_params[0], 0)
        qc.rz(input_params[1], 0)

        # Trainable rotation
        qc.ry(weight_params[3 * l], 0)
        qc.rz(weight_params[3 * l + 1], 0)
        qc.rx(weight_params[3 * l + 2], 0)

    return qc, list(input_params), list(weight_params)


def main():
    print("=" * 70)
    print("Quantum Neural Networks (QNN) - Local Simulator")
    print("=" * 70)

    # =========================================================================
    # PART A: EstimatorQNN
    # =========================================================================

    est_qnn, X_train_e, X_test_e, y_train_e, y_test_e, weights_e = demo_estimator_qnn()

    # =========================================================================
    # PART B: SamplerQNN
    # =========================================================================

    samp_qnn, X_train_s, X_test_s, y_train_s, y_test_s, weights_s = demo_sampler_qnn()

    # =========================================================================
    # PART C: Data Re-uploading QNN
    # =========================================================================

    print("\n" + "=" * 70)
    print("PART C: Data Re-uploading QNN (Universal Classifier)")
    print("=" * 70)

    qc_reup, input_p, weight_p = build_data_reuploading_qnn(num_qubits=1, num_layers=3)
    print(f"\nRe-uploading QNN circuit:")
    print(f"  Qubits: 1")
    print(f"  Layers: 3")
    print(f"  Input params: {len(input_p)}")
    print(f"  Weight params: {len(weight_p)}")
    print(f"\n{qc_reup.draw(output='text')}")

    print("\n  This single-qubit QNN with 3 re-uploading layers can approximate")
    print("  any function f:[0,2pi]->[−1,1] using a 3-term Fourier series.")
    print("  See explanation_physicist.md, Section 5.1 for the universality theorem.")

    # =========================================================================
    # PART D: Visualization
    # =========================================================================

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: Training data (moons)
    scatter1 = axes[0].scatter(X_train_e[:, 0], X_train_e[:, 1],
                               c=y_train_e, cmap='RdBu', edgecolors='k', s=40)
    axes[0].set_xlabel('Feature 1', fontsize=12)
    axes[0].set_ylabel('Feature 2', fontsize=12)
    axes[0].set_title('EstimatorQNN Data (Moons)', fontsize=13)
    plt.colorbar(scatter1, ax=axes[0], label='Class')

    # Plot 2: Training data (circles)
    scatter2 = axes[1].scatter(X_train_s[:, 0], X_train_s[:, 1],
                               c=y_train_s, cmap='RdBu', edgecolors='k', s=40)
    axes[1].set_xlabel('Feature 1', fontsize=12)
    axes[1].set_ylabel('Feature 2', fontsize=12)
    axes[1].set_title('SamplerQNN Data (Circles)', fontsize=13)
    plt.colorbar(scatter2, ax=axes[1], label='Class')

    # Plot 3: QNN architecture comparison
    architectures = ['EstimatorQNN\n(expectation)', 'SamplerQNN\n(probability)',
                     'Re-uploading\n(universal)']
    params = [est_qnn.num_weights, samp_qnn.num_weights, len(weight_p)]
    colors = ['#3498db', '#2ecc71', '#e74c3c']

    bars = axes[2].bar(architectures, params, color=colors)
    axes[2].set_ylabel('Trainable Parameters', fontsize=12)
    axes[2].set_title('QNN Architecture Comparison', fontsize=13)
    for bar, p in zip(bars, params):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    str(p), ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig("quantum/algorithms/13_QNN/qnn_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/13_QNN/qnn_results.png")

    # =========================================================================
    # Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Quantum Neural Networks demonstrated:

    A. EstimatorQNN:
       - Output: <psi|O|psi> in [-1, 1]
       - Best for: regression, binary classification
       - Gradient: parameter shift rule

    B. SamplerQNN:
       - Output: P(class | x, theta)
       - Best for: multi-class classification
       - Uses interpret function to map bitstrings to classes

    C. Data Re-uploading QNN:
       - Encodes data multiple times (interleaved with trainable layers)
       - Provably universal for function approximation
       - Output is a truncated Fourier series

    Key design choices:
    - Feature map: how data enters the circuit
    - Ansatz: trainable variational structure
    - Observable: what we measure at the end
    - These choices determine the model's expressiveness
    """)


if __name__ == "__main__":
    main()
