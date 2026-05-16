"""
Variational Quantum Regressor (VQR) - IBM Production-Ready Implementation
===========================================================================

Production VQR workflow for IBM hardware.

Qiskit Version: 2.4.1

Production considerations:
    - VQR is more shot-hungry than VQC (continuous output needs precision)
    - Use higher shot counts (8192+) for smoother gradients
    - SPSA is preferred on noisy hardware
    - Target scaling to [-1, 1] is critical (expectation value bounds)

NOT ACTUALLY DEPLOYED - uses AerSimulator for demonstration.
"""

import json
import os
from datetime import datetime

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

from qiskit.circuit.library import ZFeatureMap, RealAmplitudes
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_machine_learning.algorithms import VQR
from qiskit_algorithms.optimizers import COBYLA, SPSA

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Session


RESULTS_DIR = "quantum/algorithms/14_VQR/production_results"
NUM_QUBITS = 1
ANSATZ_REPS = 2
MAX_ITERATIONS = 80
SHOTS = 8192
RANDOM_SEED = 42


def prepare_data(n_samples=60):
    """Prepare sine regression dataset."""
    rng = np.random.default_rng(RANDOM_SEED)
    X = rng.uniform(0, 1, (n_samples, 1))
    y = np.sin(2 * np.pi * X[:, 0]) + rng.normal(0, 0.05, n_samples)

    X_scaler = MinMaxScaler(feature_range=(0, np.pi))
    X_scaled = X_scaler.fit_transform(X)

    y_scaler = MinMaxScaler(feature_range=(-0.9, 0.9))
    y_scaled = y_scaler.fit_transform(y.reshape(-1, 1)).flatten()

    n_train = int(0.7 * n_samples)
    idx = rng.permutation(n_samples)

    X_train, X_test = X_scaled[idx[:n_train]], X_scaled[idx[n_train:]]
    y_train, y_test = y_scaled[idx[:n_train]], y_scaled[idx[n_train:]]

    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"  Target range: [{y_scaled.min():.2f}, {y_scaled.max():.2f}]")
    return X_train, X_test, y_train, y_test, X_scaler, y_scaler


def save_checkpoint(params, iteration, loss, path):
    """Save training checkpoint."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "params": params.tolist() if isinstance(params, np.ndarray) else list(params),
        "iteration": iteration,
        "loss": float(loss) if loss is not None else None,
        "timestamp": datetime.now().isoformat(),
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def run_production():
    print("=" * 70)
    print("VQR - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Data
    print(f"\n--- Data ---")
    X_train, X_test, y_train, y_test, X_sc, y_sc = prepare_data(60)

    # Circuit
    print(f"\n--- Circuit ---")
    feature_map = ZFeatureMap(feature_dimension=NUM_QUBITS, reps=1)
    ansatz = RealAmplitudes(num_qubits=NUM_QUBITS, reps=ANSATZ_REPS, entanglement='linear')
    print(f"  ZFeatureMap({NUM_QUBITS}q) + RealAmplitudes(reps={ANSATZ_REPS})")
    print(f"  Trainable params: {ansatz.num_parameters}")

    # Training
    print(f"\n--- Training ---")
    loss_history = []
    iter_count = [0]
    checkpoint_path = os.path.join(RESULTS_DIR, "checkpoint.json")

    def callback(weights, loss):
        iter_count[0] += 1
        loss_history.append(float(loss))
        if iter_count[0] % 20 == 0:
            save_checkpoint(weights, iter_count[0], loss, checkpoint_path)
            print(f"  Iter {iter_count[0]:3d}: MSE = {loss:.6f} [saved]")

    # Small random init near zero (barren plateau mitigation)
    rng = np.random.default_rng(RANDOM_SEED)
    initial_point = rng.uniform(-0.1, 0.1, ansatz.num_parameters)

    optimizer = SPSA(maxiter=MAX_ITERATIONS)
    estimator = AerEstimator()

    # For real hardware:
    # with Session(service=service, backend=backend) as session:
    #     estimator = EstimatorV2(session=session)
    #     estimator.options.default_shots = SHOTS

    vqr = VQR(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=optimizer,
        estimator=estimator,
        initial_point=initial_point,
        callback=callback,
    )

    print(f"  Optimizer: SPSA ({MAX_ITERATIONS} iterations)")
    vqr.fit(X_train, y_train)

    # Evaluation
    print(f"\n--- Evaluation ---")
    y_pred_train = vqr.predict(X_train)
    y_pred_test = vqr.predict(X_test)

    mse_train = mean_squared_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_test, y_pred_test)
    r2_test = r2_score(y_test, y_pred_test)

    print(f"  Train MSE: {mse_train:.6f}")
    print(f"  Test MSE:  {mse_test:.6f}")
    print(f"  Test R^2:  {r2_test:.4f}")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "config": {"num_qubits": NUM_QUBITS, "ansatz_reps": ANSATZ_REPS,
                    "max_iter": MAX_ITERATIONS, "shots": SHOTS},
        "metrics": {"mse_train": float(mse_train), "mse_test": float(mse_test),
                     "r2_test": float(r2_test)},
    }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*70}")
    print("PRODUCTION SUMMARY")
    print(f"{'='*70}")
    print(f"""
    VQR Production:
        Circuit: ZFeatureMap + RealAmplitudes(reps={ANSATZ_REPS})
        Optimizer: SPSA ({MAX_ITERATIONS} iters)
        Test MSE: {mse_test:.6f}, R^2: {r2_test:.4f}

    Notes:
        - Higher shots (8192+) needed for smooth expectation values
        - SPSA preferred for noisy gradients on hardware
        - Target scaling to [-0.9, 0.9] critical (leave margin from [-1,1] bounds)
        - Checkpoint/resume enabled for long training runs
    """)


if __name__ == "__main__":
    run_production()