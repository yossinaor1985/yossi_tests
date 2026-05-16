"""
Hybrid Quantum-Classical NN - IBM Production-Ready Implementation
==================================================================

Production hybrid model workflow with session management and checkpointing.

Qiskit Version: 2.4.1

NOT ACTUALLY DEPLOYED - uses AerSimulator for demonstration.
"""

import json
import os
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_machine_learning.neural_networks import EstimatorQNN
from qiskit_machine_learning.connectors import TorchConnector

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Session

RESULTS_DIR = "quantum/algorithms/15_hybrid_torch_qnn/production_results"
NUM_QUBITS = 2
ANSATZ_REPS = 1
EPOCHS = 25
LEARNING_RATE = 0.01
BATCH_SIZE = 16
SHOTS = 4096


class ProductionHybridQNN(nn.Module):
    """Production hybrid model with conservative architecture."""

    def __init__(self, qnn_module):
        super().__init__()
        self.pre = nn.Sequential(
            nn.Linear(2, 8), nn.ReLU(), nn.Linear(8, 2), nn.Tanh()
        )
        self.scale = np.pi
        self.qnn = qnn_module
        self.post = nn.Sequential(nn.Linear(1, 1), nn.Sigmoid())

    def forward(self, x):
        x = self.pre(x)
        x = (x + 1) * self.scale / 2
        x = self.qnn(x)
        x = self.post(x)
        return x


def build_production_qnn():
    """Build quantum layer with production settings."""
    feature_map = ZZFeatureMap(feature_dimension=NUM_QUBITS, reps=1)
    ansatz = RealAmplitudes(num_qubits=NUM_QUBITS, reps=ANSATZ_REPS, entanglement='linear')

    circuit = QuantumCircuit(NUM_QUBITS)
    circuit.compose(feature_map, inplace=True)
    circuit.compose(ansatz, inplace=True)

    observable = SparsePauliOp.from_list([("ZI", 1.0)])
    estimator = AerEstimator()

    # For real hardware:
    # with Session(service=service, backend=backend) as session:
    #     estimator = EstimatorV2(session=session)
    #     estimator.options.default_shots = SHOTS

    qnn = EstimatorQNN(
        circuit=circuit, estimator=estimator,
        observables=[observable],
        input_params=feature_map.parameters,
        weight_params=ansatz.parameters,
    )

    init_w = torch.tensor(
        np.random.default_rng(42).uniform(-0.1, 0.1, qnn.num_weights),
        dtype=torch.float64,
    )
    return TorchConnector(qnn, initial_weights=init_w), qnn.num_weights


def save_model_checkpoint(model, epoch, loss, path):
    """Save full model checkpoint."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'loss': loss,
        'timestamp': datetime.now().isoformat(),
    }, path)


def run_production():
    print("=" * 70)
    print("Hybrid QC-NN - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Data
    print(f"\n--- Data ---")
    X, y = make_moons(n_samples=150, noise=0.15, random_state=42)
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

    X_tr = torch.tensor(X_train, dtype=torch.float32)
    X_te = torch.tensor(X_test, dtype=torch.float32)
    y_tr = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
    y_te = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    # Model
    print(f"\n--- Model ---")
    qnn_module, n_qw = build_production_qnn()
    model = ProductionHybridQNN(qnn_module)
    n_cp = sum(p.numel() for p in model.pre.parameters()) + sum(p.numel() for p in model.post.parameters())
    print(f"  Classical params: {n_cp}")
    print(f"  Quantum params:   {n_qw}")

    # Training
    print(f"\n--- Training ---")
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.BCELoss()
    loader = DataLoader(TensorDataset(X_tr, y_tr), batch_size=BATCH_SIZE, shuffle=True)

    loss_history = []
    checkpoint_path = os.path.join(RESULTS_DIR, "model_checkpoint.pt")

    for epoch in range(EPOCHS):
        model.train()
        epoch_loss, n_batch = 0.0, 0
        for X_b, y_b in loader:
            optimizer.zero_grad()
            loss = criterion(model(X_b), y_b)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
            n_batch += 1

        avg = epoch_loss / n_batch
        loss_history.append(avg)

        if (epoch + 1) % 5 == 0:
            save_model_checkpoint(model, epoch, avg, checkpoint_path)
            print(f"  Epoch {epoch+1:3d}/{EPOCHS}: loss={avg:.4f} [saved]")

    # Evaluation
    print(f"\n--- Evaluation ---")
    model.eval()
    with torch.no_grad():
        y_pred = (model(X_te) >= 0.5).float()
        acc = (y_pred == y_te).float().mean().item()
    print(f"  Test accuracy: {acc:.4f}")

    # Save
    results = {
        "timestamp": datetime.now().isoformat(),
        "config": {"qubits": NUM_QUBITS, "ansatz_reps": ANSATZ_REPS,
                    "epochs": EPOCHS, "lr": LEARNING_RATE},
        "metrics": {"test_accuracy": float(acc), "final_loss": loss_history[-1]},
    }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*70}")
    print("PRODUCTION SUMMARY")
    print(f"{'='*70}")
    print(f"""
    Hybrid QC-NN: Classical(2->8->2) -> QNN(2q) -> Classical(1->1)
    Test accuracy: {acc:.4f}

    Production notes:
        - Model checkpointing enables resume after failures
        - Classical layers handle feature preprocessing (GPU-accelerable)
        - Quantum layer uses shallow circuit (reps=1) for hardware reliability
        - For real hardware: wrap estimator in Session for efficiency
    """)


if __name__ == "__main__":
    run_production()