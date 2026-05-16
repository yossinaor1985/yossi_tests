"""
Quantum Boltzmann Machine - IBM Production-Ready Implementation
================================================================

Production QBM workflow using variational circuit to approximate
thermal states on IBM hardware.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED - uses AerSimulator.
"""

import json
import os
from datetime import datetime

import numpy as np
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer.primitives import SamplerV2 as AerSampler

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/algorithms/16_quantum_boltzmann/production_results"
NUM_QUBITS = 3
NUM_LAYERS = 4
MAX_ITER = 200
SHOTS = 8192


def build_circuit(n_qubits, n_layers):
    """Build variational thermal state circuit."""
    n_params = n_qubits * 2 * n_layers
    params = ParameterVector('theta', n_params)
    qc = QuantumCircuit(n_qubits)
    idx = 0
    for layer in range(n_layers):
        for q in range(n_qubits):
            qc.ry(params[idx], q)
            idx += 1
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
        for q in range(n_qubits):
            qc.rz(params[idx], q)
            idx += 1
    return qc, params


def get_probs(circuit, values):
    """Get probability distribution from circuit."""
    bound = circuit.assign_parameters(dict(zip(circuit.parameters, values)))
    return Statevector(bound).probabilities()


def create_target(n_qubits):
    """Target distribution."""
    n = 2 ** n_qubits
    target = np.zeros(n)
    if n_qubits == 3:
        target[0] = 0.25
        target[1] = 0.08
        target[2] = 0.02
        target[3] = 0.05
        target[4] = 0.05
        target[5] = 0.03
        target[6] = 0.07
        target[7] = 0.45
    target /= target.sum()
    return target


def kl_div(p, q, eps=1e-10):
    """KL divergence."""
    q = np.clip(q, eps, 1.0)
    p = np.clip(p, eps, 1.0)
    return np.sum(p * np.log(p / q))


def run_production():
    print("=" * 70)
    print("QBM - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    target = create_target(NUM_QUBITS)
    circuit, params = build_circuit(NUM_QUBITS, NUM_LAYERS)
    n_params = len(params)

    print(f"\n  Qubits: {NUM_QUBITS}, Layers: {NUM_LAYERS}, Params: {n_params}")

    # For real hardware:
    # with Session(service=service, backend=backend) as session:
    #     sampler = SamplerV2(session=session)
    #     sampler.options.default_shots = SHOTS

    loss_history = []
    best = {"loss": float('inf'), "params": None}

    def objective(values):
        probs = get_probs(circuit, values)
        kl = kl_div(target, probs)
        loss_history.append(kl)
        if kl < best["loss"]:
            best["loss"] = kl
            best["params"] = values.copy()
        if len(loss_history) % 50 == 0:
            print(f"  Iter {len(loss_history):4d}: KL = {kl:.6f}")
        return kl

    rng = np.random.default_rng(42)
    x0 = rng.uniform(-np.pi, np.pi, n_params)

    print(f"\n  Training (COBYLA, {MAX_ITER} iters)...")
    minimize(objective, x0, method='COBYLA', options={'maxiter': MAX_ITER})

    learned = get_probs(circuit, best["params"])
    final_kl = kl_div(target, learned)
    tv = 0.5 * np.sum(np.abs(target - learned))

    print(f"\n  Final KL: {final_kl:.6f}, TV: {tv:.4f}")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "config": {"qubits": NUM_QUBITS, "layers": NUM_LAYERS, "max_iter": MAX_ITER},
        "metrics": {"kl_divergence": float(final_kl), "total_variation": float(tv)},
        "distributions": {
            "target": target.tolist(),
            "learned": learned.tolist(),
        },
    }
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n  Results saved to {RESULTS_DIR}/results.json")
    print(f"\n{'='*70}")
    print("PRODUCTION SUMMARY")
    print(f"{'='*70}")
    print(f"""
    QBM trained: {NUM_QUBITS} qubits, {NUM_LAYERS} layers
    Final KL divergence: {final_kl:.6f}
    Total variation: {tv:.4f}

    Production notes:
        - Variational circuit approximates Gibbs state
        - Use Session for batched sampling on IBM hardware
        - Higher shots improve gradient estimates
        - Consider Trotterized Gibbs preparation for deeper models
    """)


if __name__ == "__main__":
    run_production()