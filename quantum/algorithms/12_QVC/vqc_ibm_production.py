"""
Variational Quantum Classifier (VQC) - IBM Production-Ready Implementation
============================================================================

Production VQC workflow for IBM hardware with error mitigation,
session management, and checkpoint/resume capabilities.

Qiskit Version: 2.4.1

Production considerations:
    - VQC requires many circuit evaluations (one per training sample per iteration)
    - SPSA optimizer is preferred for noisy hardware (2 evaluations per step)
    - Sessions batch circuit executions for efficiency
    - Warm-starting from pretrained parameters reduces iterations needed
    - Checkpointing enables resume after job failures

NOT ACTUALLY DEPLOYED - uses AerSimulator for demonstration.
Uncomment IBM Runtime sections for real hardware execution.
"""

import json
import os
from datetime import datetime

import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report

from qiskit import QuantumCircuit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer.primitives import SamplerV2 as AerSampler
from qiskit_machine_learning.algorithms import VQC
from qiskit_algorithms.optimizers import COBYLA, SPSA

# =============================================================================
# IBM RUNTIME SETUP (uncomment for real hardware)
# =============================================================================
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session
#
# # Initialize service (requires IBM Quantum account)
# # service = QiskitRuntimeService(channel="ibm_quantum")
# # or for IBM Cloud:
# # service = QiskitRuntimeService(channel="ibm_cloud", instance="your/instance")
#
# def get_backend(service, min_qubits=2):
#     """Select the least busy backend with sufficient qubits."""
#     backends = service.backends(
#         filters=lambda b: (
#             b.configuration().n_qubits >= min_qubits
#             and b.status().operational
#             and not b.configuration().simulator
#         )
#     )
#     if not backends:
#         raise RuntimeError(f"No backends with >= {min_qubits} qubits available")
#     # Sort by pending jobs
#     backend = min(backends, key=lambda b: b.status().pending_jobs)
#     print(f"Selected backend: {backend.name} ({backend.status().pending_jobs} pending jobs)")
#     return backend


# =============================================================================
# CONFIGURATION
# =============================================================================

RESULTS_DIR = "quantum/algorithms/12_QVC/production_results"
NUM_QUBITS = 2
FEATURE_MAP_REPS = 1      # Shallow for hardware (reduces gate errors)
ANSATZ_REPS = 1            # Shallow for hardware
MAX_ITERATIONS = 60        # SPSA iterations
SPSA_LEARNING_RATE = 0.05
SPSA_PERTURBATION = 0.1
SHOTS = 4096               # Higher shots for production accuracy
RANDOM_SEED = 42


# =============================================================================
# DATA PREPARATION
# =============================================================================

def prepare_production_data(n_samples=100):
    """
    Prepare dataset with production-grade preprocessing.

    For production:
        - Larger dataset for better generalization
        - Careful feature scaling to [0, pi]
        - Stratified split to maintain class balance
    """
    X, y = make_moons(n_samples=n_samples, noise=0.15, random_state=RANDOM_SEED)

    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y
    )

    print(f"Dataset prepared:")
    print(f"  Train: {len(X_train)} samples (class 0: {sum(y_train==0)}, class 1: {sum(y_train==1)})")
    print(f"  Test:  {len(X_test)} samples (class 0: {sum(y_test==0)}, class 1: {sum(y_test==1)})")

    return X_train, X_test, y_train, y_test, scaler


# =============================================================================
# CIRCUIT CONSTRUCTION
# =============================================================================

def build_production_vqc_circuit():
    """
    Build a hardware-efficient VQC circuit.

    Production guidelines:
        - Use shallow circuits (reps=1) to minimize gate errors
        - Linear entanglement matches heavy-hex topology
        - ZZFeatureMap reps=1 still captures pairwise correlations
        - RealAmplitudes is sufficient (fewer parameters = faster convergence)

    See explanation_physicist.md, Sections 2.2 and 2.3.
    """
    feature_map = ZZFeatureMap(
        feature_dimension=NUM_QUBITS,
        reps=FEATURE_MAP_REPS,
    )

    ansatz = RealAmplitudes(
        num_qubits=NUM_QUBITS,
        reps=ANSATZ_REPS,
        entanglement='linear',
    )

    # Display circuit info
    qc = QuantumCircuit(NUM_QUBITS)
    qc.compose(feature_map, inplace=True)
    qc.compose(ansatz, inplace=True)

    print(f"\nProduction VQC circuit:")
    print(f"  Qubits: {NUM_QUBITS}")
    print(f"  Feature map: ZZFeatureMap (reps={FEATURE_MAP_REPS})")
    print(f"  Ansatz: RealAmplitudes (reps={ANSATZ_REPS})")
    print(f"  Trainable parameters: {ansatz.num_parameters}")
    print(f"  Circuit depth (pre-transpilation): {qc.depth()}")

    return feature_map, ansatz


# =============================================================================
# TRANSPILATION (for real hardware)
# =============================================================================

def transpile_for_hardware(circuit, backend=None):
    """
    Transpile circuit for target backend topology.

    For IBM hardware:
        - optimization_level=2 or 3 for production
        - Respects coupling map (which qubits are connected)
        - Inserts SWAP gates where needed
        - Decomposes to backend basis gates (CX, ID, RZ, SX, X)
    """
    if backend is not None:
        pm = generate_preset_pass_manager(
            optimization_level=2,
            backend=backend,
        )
        transpiled = pm.run(circuit)
        print(f"  Transpiled depth: {transpiled.depth()}")
        print(f"  Transpiled gate count: {dict(transpiled.count_ops())}")
        return transpiled
    else:
        print("  (No backend specified, skipping transpilation)")
        return circuit


# =============================================================================
# CHECKPOINTING
# =============================================================================

def save_checkpoint(params, iteration, loss, filepath):
    """Save training checkpoint for resume capability."""
    checkpoint = {
        "params": params.tolist() if isinstance(params, np.ndarray) else list(params),
        "iteration": iteration,
        "loss": float(loss) if loss is not None else None,
        "timestamp": datetime.now().isoformat(),
    }
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(checkpoint, f, indent=2)


def load_checkpoint(filepath):
    """Load training checkpoint."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            checkpoint = json.load(f)
        print(f"  Loaded checkpoint from iteration {checkpoint['iteration']}")
        return np.array(checkpoint["params"]), checkpoint["iteration"]
    return None, 0


# =============================================================================
# PRODUCTION TRAINING
# =============================================================================

def train_production_vqc(X_train, y_train, feature_map, ansatz, initial_point=None):
    """
    Train VQC with production settings.

    Uses SPSA optimizer (see explanation_physicist.md, Section 6.2):
        - Only 2 circuit evaluations per iteration (not 2p like parameter shift)
        - Robust to shot noise and hardware errors
        - Stochastic gradient approximation:
            grad_approx = [L(theta + c*delta) - L(theta - c*delta)] / (2c) * delta

    SPSA is the recommended optimizer for real quantum hardware because:
        1. Cost per iteration is independent of parameter count
        2. Naturally handles noisy objective functions
        3. Can escape local minima due to stochastic perturbations
    """
    print(f"\n{'='*50}")
    print("PRODUCTION TRAINING")
    print(f"{'='*50}")

    checkpoint_path = os.path.join(RESULTS_DIR, "checkpoint.json")
    loaded_params, start_iter = load_checkpoint(checkpoint_path)

    if loaded_params is not None and initial_point is None:
        initial_point = loaded_params
        print(f"  Resuming from checkpoint (iteration {start_iter})")
    elif initial_point is None:
        # Random initialization near zero (helps avoid barren plateaus)
        # See explanation_physicist.md, Section 5.3
        rng = np.random.default_rng(RANDOM_SEED)
        initial_point = rng.uniform(-0.1, 0.1, ansatz.num_parameters)
        print(f"  Initializing near zero (barren plateau mitigation)")

    # SPSA optimizer configuration
    optimizer = SPSA(
        maxiter=MAX_ITERATIONS,
        learning_rate=SPSA_LEARNING_RATE,
        perturbation=SPSA_PERTURBATION,
    )

    # Training callback with checkpointing
    loss_history = []
    iteration_count = [0]

    def production_callback(weights, loss):
        iteration_count[0] += 1
        loss_history.append(float(loss))

        # Checkpoint every 10 iterations
        if iteration_count[0] % 10 == 0:
            save_checkpoint(weights, iteration_count[0], loss, checkpoint_path)
            print(f"  Iter {iteration_count[0]:3d}: loss={loss:.4f} [checkpoint saved]")

    # Create sampler
    sampler = AerSampler()

    # For real hardware:
    # with Session(service=service, backend=backend) as session:
    #     sampler = SamplerV2(session=session)
    #     sampler.options.default_shots = SHOTS
    #     sampler.options.dynamical_decoupling.enable = True  # error mitigation
    #     vqc = VQC(...)

    vqc = VQC(
        feature_map=feature_map,
        ansatz=ansatz,
        optimizer=optimizer,
        sampler=sampler,
        initial_point=initial_point,
        callback=production_callback,
    )

    print(f"  Optimizer: SPSA (lr={SPSA_LEARNING_RATE}, pert={SPSA_PERTURBATION})")
    print(f"  Max iterations: {MAX_ITERATIONS}")
    print(f"  Training...\n")

    vqc.fit(X_train, y_train)

    # Final checkpoint
    save_checkpoint(
        vqc._fit_result.x if hasattr(vqc, '_fit_result') else initial_point,
        iteration_count[0], loss_history[-1] if loss_history else None,
        checkpoint_path
    )

    return vqc, loss_history


# =============================================================================
# PRODUCTION EVALUATION
# =============================================================================

def evaluate_production(vqc, X_train, X_test, y_train, y_test):
    """Comprehensive production evaluation with saved results."""
    print(f"\n{'='*50}")
    print("PRODUCTION EVALUATION")
    print(f"{'='*50}")

    y_pred_train = vqc.predict(X_train)
    y_pred_test = vqc.predict(X_test)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)

    print(f"\n  Train accuracy: {train_acc:.4f}")
    print(f"  Test accuracy:  {test_acc:.4f}")
    print(f"\n  Classification Report (Test):")
    print(classification_report(y_test, y_pred_test, target_names=["Class 0", "Class 1"]))

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "num_qubits": NUM_QUBITS,
            "feature_map_reps": FEATURE_MAP_REPS,
            "ansatz_reps": ANSATZ_REPS,
            "max_iterations": MAX_ITERATIONS,
            "shots": SHOTS,
            "optimizer": "SPSA",
        },
        "metrics": {
            "train_accuracy": float(train_acc),
            "test_accuracy": float(test_acc),
            "n_train": len(y_train),
            "n_test": len(y_test),
        },
        "predictions": {
            "y_test": y_test.tolist(),
            "y_pred_test": y_pred_test.tolist(),
        },
    }

    results_path = os.path.join(RESULTS_DIR, "evaluation_results.json")
    os.makedirs(os.path.dirname(results_path), exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"  Results saved to {results_path}")

    return results


# =============================================================================
# WARM-START STRATEGY
# =============================================================================

def warm_start_from_classical(X_train, y_train, ansatz):
    """
    Warm-start VQC parameters from a classical pre-training step.

    Strategy (see explanation_physicist.md, Section 5.3):
        1. Train a simple classical model
        2. Use classical decision boundary to initialize quantum parameters
        3. This places the optimization in a good region, avoiding barren plateaus

    A simpler approach: initialize near the identity (small random parameters)
    so the circuit starts close to |0>^n and gradually learns.
    """
    print(f"\n  Warm-start strategy: small random initialization")
    print(f"  (Parameters near zero -> circuit near identity -> gradients non-zero)")

    rng = np.random.default_rng(RANDOM_SEED)
    initial_params = rng.uniform(-0.05, 0.05, ansatz.num_parameters)

    print(f"  Initial parameter norm: {np.linalg.norm(initial_params):.4f}")
    return initial_params


# =============================================================================
# MAIN PRODUCTION PIPELINE
# =============================================================================

def run_production():
    print("=" * 70)
    print("VQC - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Qiskit 2.4.1 | Target: AerSimulator (swap for IBM backend)")

    # Step 1: Data preparation
    print(f"\n--- Step 1: Data Preparation ---")
    X_train, X_test, y_train, y_test, scaler = prepare_production_data(n_samples=120)

    # Step 2: Circuit construction
    print(f"\n--- Step 2: Circuit Construction ---")
    feature_map, ansatz = build_production_vqc_circuit()

    # Step 3: Transpilation
    print(f"\n--- Step 3: Transpilation ---")
    # For real hardware:
    # backend = get_backend(service, min_qubits=NUM_QUBITS)
    # transpile_for_hardware(circuit, backend)
    print("  Using AerSimulator (no transpilation needed)")

    # Step 4: Warm-start
    print(f"\n--- Step 4: Warm-Start ---")
    initial_point = warm_start_from_classical(X_train, y_train, ansatz)

    # Step 5: Training
    vqc, loss_history = train_production_vqc(
        X_train, y_train, feature_map, ansatz, initial_point
    )

    # Step 6: Evaluation
    results = evaluate_production(vqc, X_train, X_test, y_train, y_test)

    # Step 7: Summary
    print(f"\n{'='*70}")
    print("PRODUCTION SUMMARY")
    print(f"{'='*70}")
    print(f"""
    Configuration:
        Qubits: {NUM_QUBITS}
        Feature map: ZZFeatureMap (reps={FEATURE_MAP_REPS})
        Ansatz: RealAmplitudes (reps={ANSATZ_REPS})
        Optimizer: SPSA ({MAX_ITERATIONS} iterations)
        Shots: {SHOTS}

    Results:
        Train accuracy: {results['metrics']['train_accuracy']:.4f}
        Test accuracy:  {results['metrics']['test_accuracy']:.4f}

    Production notes:
        - For real IBM hardware, uncomment the QiskitRuntimeService sections
        - Use Session for batched circuit execution (reduces queue time)
        - Enable dynamical decoupling for error mitigation
        - SPSA is preferred over COBYLA for noisy backends
        - Checkpoint files enable resume after job failures
        - Monitor convergence: if loss plateaus, try different initial_point
    """)


if __name__ == "__main__":
    run_production()