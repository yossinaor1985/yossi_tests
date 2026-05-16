"""
Hybrid Quantum-Classical Neural Networks (TorchConnector) - Local Simulator
============================================================================

Demonstrates combining classical PyTorch layers with quantum circuit layers
using qiskit_machine_learning's TorchConnector.

Qiskit Version: 2.4.1

Architecture (see explanation_physicist.md, Section 2):
    x -> [Classical Linear layers] -> x' -> [Quantum QNN] -> q -> [Classical Linear] -> y

Gradient flow is end-to-end:
    - Classical layers: standard PyTorch backpropagation
    - Quantum layer: parameter shift rule (handled by TorchConnector)
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_machine_learning.neural_networks import EstimatorQNN
from qiskit_machine_learning.connectors import TorchConnector


# =============================================================================
# DATA
# =============================================================================

def create_dataset(n_samples=200):
    """Create make_moons dataset."""
    X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=42)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    return X_train, X_test, y_train, y_test


def to_tensors(X_train, X_test, y_train, y_test):
    """Convert numpy arrays to PyTorch tensors."""
    X_tr = torch.tensor(X_train, dtype=torch.float32)
    X_te = torch.tensor(X_test, dtype=torch.float32)
    y_tr = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    y_te = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)
    return X_tr, X_te, y_tr, y_te


# =============================================================================
# HYBRID MODEL
# =============================================================================

class HybridQNN(nn.Module):
    """
    Hybrid Quantum-Classical Neural Network.

    Architecture (see explanation_physicist.md, Section 3):
        1. Classical preprocessing: Linear(2, 4) -> ReLU -> Linear(4, 2)
           Maps input features to 2 values suitable for 2-qubit encoding
        2. Quantum layer: EstimatorQNN via TorchConnector
           ZZFeatureMap + RealAmplitudes -> <Z> expectation value
        3. Classical postprocessing: Linear(1, 1) -> Sigmoid
           Maps quantum output to classification probability

    The TorchConnector (Section 2.3) enables:
        - Automatic gradient computation (parameter shift for quantum, backprop for classical)
        - Standard PyTorch training loop compatibility
        - Batch processing of inputs
    """

    def __init__(self, qnn_module):
        super().__init__()

        # Classical preprocessing (Section 3.1):
        # Reduces/transforms features for quantum encoding
        self.pre = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 2),
            nn.Tanh(),  # Output in [-1, 1]
        )
        # Scale to [0, pi] for quantum encoding
        self.scale = np.pi

        # Quantum layer (Section 3.2):
        # TorchConnector wraps EstimatorQNN as nn.Module
        self.qnn = qnn_module

        # Classical postprocessing (Section 3.3):
        # Maps quantum expectation value to class probability
        self.post = nn.Sequential(
            nn.Linear(1, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        # Step 1: Classical preprocessing
        x = self.pre(x)
        x = (x + 1) * self.scale / 2  # Rescale [-1,1] -> [0, pi]

        # Step 2: Quantum layer
        x = self.qnn(x)

        # Step 3: Classical postprocessing
        x = self.post(x)
        return x


class PureClassicalNN(nn.Module):
    """Classical baseline with comparable parameter count."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)


# =============================================================================
# BUILD QNN LAYER
# =============================================================================

def build_qnn_layer(num_qubits=2, ansatz_reps=1):
    """
    Build the quantum layer as a TorchConnector module.

    Returns an nn.Module that:
        Input: 2D tensor of shape (batch_size, num_qubits)
        Output: 2D tensor of shape (batch_size, 1)
    """
    feature_map = ZZFeatureMap(feature_dimension=num_qubits, reps=1)
    ansatz = RealAmplitudes(num_qubits=num_qubits, reps=ansatz_reps, entanglement='linear')

    # Combine into one circuit
    circuit = QuantumCircuit(num_qubits)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    # Observable: Z on qubit 0
    observable = SparsePauliOp.from_list([("ZI", 1.0)])

    estimator = AerEstimator()

    qnn = EstimatorQNN(
        circuit=circuit,
        estimator=estimator,
        observables=[observable],
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
    )

    # Wrap as PyTorch module
    initial_weights = torch.tensor(
        np.random.default_rng(42).uniform(-0.1, 0.1, qnn.num_weights),
        dtype=torch.float64,
    )
    qnn_module = TorchConnector(qnn, initial_weights=initial_weights)

    return qnn_module, qnn.num_weights


# =============================================================================
# TRAINING
# =============================================================================

def train_model(model, X_train, y_train, epochs=30, lr=0.01):
    """
    Standard PyTorch training loop.

    The hybrid model is trained with:
        - Adam optimizer for all parameters (classical + quantum)
        - BCE loss for binary classification
        - Gradient flow: backprop -> parameter shift -> backprop
          (see explanation_physicist.md, Section 2.2)
    """
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.BCELoss()

    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=16, shuffle=True)

    loss_history = []
    model.train()

    for epoch in range(epochs):
        epoch_loss = 0.0
        n_batches = 0

        for X_batch, y_batch in loader:
            optimizer.zero_grad()
            y_pred = model(X_batch)
            loss = criterion(y_pred, y_batch)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            n_batches += 1

        avg_loss = epoch_loss / n_batches
        loss_history.append(avg_loss)

        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch+1:3d}/{epochs}: loss = {avg_loss:.4f}")

    return loss_history


def evaluate_model(model, X_test, y_test):
    """Evaluate model accuracy."""
    model.eval()
    with torch.no_grad():
        y_pred = model(X_test)
        y_pred_class = (y_pred >= 0.5).float()
        acc = (y_pred_class == y_test).float().mean().item()
    return acc


# =============================================================================
# MAIN DEMOS
# =============================================================================

def demo_hybrid():
    """Demonstrate the hybrid quantum-classical model."""
    print("\n" + "=" * 70)
    print("PART A: Hybrid Quantum-Classical Neural Network")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_dataset(n_samples=150)
    X_tr, X_te, y_tr, y_te = to_tensors(X_train, X_test, y_train, y_test)

    print(f"Dataset: {len(X_train)} train / {len(X_test)} test")

    # Build hybrid model
    qnn_module, n_qweights = build_qnn_layer(num_qubits=2, ansatz_reps=1)
    model = HybridQNN(qnn_module)

    n_classical = sum(p.numel() for p in model.pre.parameters()) + \
                  sum(p.numel() for p in model.post.parameters())
    print(f"\nHybrid model:")
    print(f"  Classical params: {n_classical}")
    print(f"  Quantum params:   {n_qweights}")
    print(f"  Total params:     {n_classical + n_qweights}")

    # Train
    print(f"\nTraining (30 epochs, Adam lr=0.01)...")
    loss_history = train_model(model, X_tr, y_tr, epochs=30, lr=0.01)

    # Evaluate
    acc = evaluate_model(model, X_te, y_te)
    print(f"\n  Test accuracy: {acc:.4f}")

    return model, X_tr, X_te, y_tr, y_te, loss_history, acc


def demo_classical_baseline():
    """Train a pure classical baseline for comparison."""
    print("\n" + "=" * 70)
    print("PART B: Pure Classical Baseline")
    print("=" * 70)

    X_train, X_test, y_train, y_test = create_dataset(n_samples=150)
    X_tr, X_te, y_tr, y_te = to_tensors(X_train, X_test, y_train, y_test)

    model = PureClassicalNN()
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  Classical NN params: {n_params}")

    print(f"\nTraining (30 epochs, Adam lr=0.01)...")
    loss_history = train_model(model, X_tr, y_tr, epochs=30, lr=0.01)

    acc = evaluate_model(model, X_te, y_te)
    print(f"\n  Test accuracy: {acc:.4f}")

    return loss_history, acc


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(hybrid_loss, hybrid_acc, classical_loss, classical_acc,
                 model, X_te, y_te):
    """Visualize hybrid vs classical comparison."""
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))

    # Loss curves
    ax = axes[0]
    ax.plot(hybrid_loss, 'b-', linewidth=2, label=f'Hybrid (acc={hybrid_acc:.3f})')
    ax.plot(classical_loss, 'r--', linewidth=2, label=f'Classical (acc={classical_acc:.3f})')
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('BCE Loss', fontsize=12)
    ax.set_title('Training Loss Comparison', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Decision boundary (hybrid)
    ax = axes[1]
    X_np = X_te.numpy()
    y_np = y_te.numpy().flatten()
    h = 0.1
    x_min, x_max = X_np[:, 0].min() - 0.3, X_np[:, 0].max() + 0.3
    y_min, y_max = X_np[:, 1].min() - 0.3, X_np[:, 1].max() + 0.3
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    grid = torch.tensor(np.c_[xx.ravel(), yy.ravel()], dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        Z = model(grid).numpy().reshape(xx.shape)
    ax.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu', levels=20)
    ax.scatter(X_np[:, 0], X_np[:, 1], c=y_np, cmap='RdBu', edgecolors='k', s=30)
    ax.set_title('Hybrid QNN Decision Boundary', fontsize=13)
    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')

    # Architecture comparison
    ax = axes[2]
    methods = ['Hybrid\nQC-NN', 'Pure\nClassical']
    accs = [hybrid_acc, classical_acc]
    colors = ['#9b59b6', '#3498db']
    bars = ax.bar(methods, accs, color=colors, width=0.5)
    ax.set_ylabel('Test Accuracy', fontsize=12)
    ax.set_title('Architecture Comparison', fontsize=13)
    ax.set_ylim(0, 1.1)
    for bar, acc in zip(bars, accs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{acc:.3f}', ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig("quantum/algorithms/15_hybrid_torch_qnn/hybrid_results.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/15_hybrid_torch_qnn/hybrid_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Hybrid Quantum-Classical Neural Networks - Local Simulator")
    print("=" * 70)
    print("Qiskit 2.4.1 | PyTorch | AerSimulator")

    # Hybrid model
    model, X_tr, X_te, y_tr, y_te, hybrid_loss, hybrid_acc = demo_hybrid()

    # Classical baseline
    classical_loss, classical_acc = demo_classical_baseline()

    # Visualization
    plot_results(hybrid_loss, hybrid_acc, classical_loss, classical_acc,
                 model, X_te, y_te)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Hybrid QC-NN demonstrated:

    Architecture: Classical(2->8->2) -> Quantum(2q, ZZFeatureMap+RealAmplitudes) -> Classical(1->1)

    Key points:
    - TorchConnector bridges Qiskit QNN to PyTorch nn.Module
    - End-to-end gradient flow: backprop + parameter shift rule
    - Classical layers handle dimensionality reduction
    - Quantum layer provides exponential feature space
    - Standard PyTorch training loop works unchanged

    When to use hybrid:
    - High-dimensional input data (classical layers reduce to qubit count)
    - Need quantum expressivity but few qubits available
    - Transfer learning from pretrained classical models
    """)


if __name__ == "__main__":
    main()