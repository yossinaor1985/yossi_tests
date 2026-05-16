"""
Clifford Data Regression (CDR) - IBM Production-Ready Implementation
=====================================================================

Production workflow for CDR on IBM hardware.
Uses near-Clifford training circuits for learning the noise-induced
mapping, then applies linear correction to the target circuit.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
CDR: train on Clifford circuits (classically simulable via Gottesman-Knill)
to learn E_ideal = a * E_noisy + b. Apply to target circuit.
No noise model knowledge required.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/mitigation/08_CDR/production_results"


# =============================================================================
# TRAINING CIRCUIT GENERATION
# =============================================================================

def generate_training_circuits(
    target_thetas: List[float],
    n_qubits: int,
    n_training: int = 20,
    seed: int = 42
) -> List[Tuple[QuantumCircuit, List[float]]]:
    """
    Generate near-Clifford training circuits for CDR.

    Clifford substitution (see explanation_physicist.md, Section 3.1):
        Replace Ry(theta) with Ry(k*pi/2) for random k.
        Same circuit structure -> similar noise experience.

    Args:
        target_thetas: Original non-Clifford angles.
        n_qubits: Number of qubits.
        n_training: Number of training circuits.
        seed: Random seed.

    Returns:
        List of (circuit, clifford_angles) tuples.
    """
    rng = np.random.default_rng(seed)
    clifford_options = [0, np.pi / 2, np.pi, 3 * np.pi / 2]

    circuits = []
    for _ in range(n_training):
        cliff_angles = [rng.choice(clifford_options) for _ in target_thetas]

        qc = QuantumCircuit(n_qubits)
        for i in range(n_qubits):
            qc.h(i)
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)
        for i, theta in enumerate(cliff_angles):
            if i < n_qubits:
                qc.ry(theta, i)
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)

        circuits.append((qc, cliff_angles))

    return circuits


def build_target_circuit(thetas: List[float], n_qubits: int) -> QuantumCircuit:
    """Build target circuit with non-Clifford rotations."""
    qc = QuantumCircuit(n_qubits)
    for i in range(n_qubits):
        qc.h(i)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    for i, theta in enumerate(thetas):
        if i < n_qubits:
            qc.ry(theta, i)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    return qc


# =============================================================================
# EXPECTATION VALUE COMPUTATION
# =============================================================================

def exact_expectation(circuit: QuantumCircuit, obs_qubits: List[int]) -> float:
    """Compute exact <ZZ...Z> via statevector simulation."""
    sv = Statevector.from_instruction(circuit)
    probs = sv.probabilities_dict()
    n = circuit.num_qubits
    val = 0.0
    for bs, p in probs.items():
        parity = sum(int(bs.zfill(n)[n - 1 - q]) for q in obs_qubits) % 2
        val += (-1) ** parity * p
    return val


def noisy_expectation(circuit: QuantumCircuit, obs_qubits: List[int],
                      backend: AerSimulator, shots: int = 8192) -> float:
    """Compute noisy <ZZ...Z> from simulator."""
    n = circuit.num_qubits
    qc = circuit.copy()
    qc.measure_all()
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()
    total = sum(counts.values())
    val = 0.0
    for bs, c in counts.items():
        parity = sum(int(bs.zfill(n)[n - 1 - q]) for q in obs_qubits) % 2
        val += (-1) ** parity * c / total
    return val


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full CDR production workflow.

    Steps:
        1. Configure backend
        2. Build target circuit
        3. Generate training circuits
        4. Collect training data (exact + noisy)
        5. Fit linear regression
        6. Run target circuit (noisy)
        7. Apply CDR correction
        8. Save results

    Args:
        use_simulator: If True, use noisy AerSimulator.
    """
    print("=" * 70)
    print("Clifford Data Regression - Production Workflow")
    print("=" * 70)

    n_qubits = 2
    thetas = [0.9, 1.7]
    obs_qubits = [0, 1]
    n_training = 25
    shots = 8192

    # -----------------------------------------------------------------
    # Step 1: Backend
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        noise_model = NoiseModel()
        noise_model.add_all_qubit_quantum_error(
            depolarizing_error(0.005, 1), ['x', 'h', 'sx', 'ry', 'rz']
        )
        noise_model.add_all_qubit_quantum_error(
            depolarizing_error(0.02, 2), ['cx']
        )
        backend = AerSimulator(noise_model=noise_model)
        print("  AerSimulator with depolarizing noise")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        print("  IBM hardware (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Target circuit
    # -----------------------------------------------------------------
    print(f"\nStep 2: Target circuit (thetas = {thetas})")
    target_qc = build_target_circuit(thetas, n_qubits)
    ideal_value = exact_expectation(target_qc, obs_qubits)
    print(f"  Ideal <ZZ> = {ideal_value:.6f}")

    # -----------------------------------------------------------------
    # Step 3: Training circuits
    # -----------------------------------------------------------------
    print(f"\nStep 3: Generating {n_training} near-Clifford training circuits")
    training = generate_training_circuits(thetas, n_qubits, n_training, seed=42)

    # -----------------------------------------------------------------
    # Step 4: Collect training data
    # -----------------------------------------------------------------
    print("\nStep 4: Collecting training data")
    exact_vals = []
    noisy_vals = []
    for qc, angles in training:
        exact_vals.append(exact_expectation(qc, obs_qubits))
        noisy_vals.append(noisy_expectation(qc, obs_qubits, backend, shots))

    print(f"  Training exact range:  [{min(exact_vals):.4f}, {max(exact_vals):.4f}]")
    print(f"  Training noisy range:  [{min(noisy_vals):.4f}, {max(noisy_vals):.4f}]")

    # -----------------------------------------------------------------
    # Step 5: Fit regression
    # -----------------------------------------------------------------
    print("\nStep 5: Fitting linear regression")
    x = np.array(noisy_vals)
    y = np.array(exact_vals)
    coeffs = np.polyfit(x, y, 1)
    a, b = coeffs[0], coeffs[1]

    y_pred = a * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    print(f"  E_exact = {a:.4f} * E_noisy + {b:.4f}")
    print(f"  R-squared = {r2:.4f}")

    # -----------------------------------------------------------------
    # Step 6: Run target circuit
    # -----------------------------------------------------------------
    print(f"\nStep 6: Running target circuit ({shots} shots)")
    if not use_simulator:
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        target_qc_t = pm.run(target_qc.copy())
    noisy_target = noisy_expectation(target_qc, obs_qubits, backend, shots)
    print(f"  Noisy target <ZZ> = {noisy_target:.6f}")

    # -----------------------------------------------------------------
    # Step 7: CDR correction
    # -----------------------------------------------------------------
    print("\nStep 7: Applying CDR correction")
    corrected = a * noisy_target + b
    print(f"  CDR corrected <ZZ> = {corrected:.6f}")

    # Summary
    raw_error = abs(noisy_target - ideal_value)
    cdr_error = abs(corrected - ideal_value)
    print(f"\n  Summary:")
    print(f"    Ideal:       {ideal_value:.6f}")
    print(f"    Raw:         {noisy_target:.6f} (error: {raw_error:.6f})")
    print(f"    CDR:         {corrected:.6f} (error: {cdr_error:.6f})")
    if cdr_error > 1e-8:
        print(f"    Improvement: {raw_error / cdr_error:.1f}x")

    # -----------------------------------------------------------------
    # Step 8: Save
    # -----------------------------------------------------------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        "timestamp": datetime.now().isoformat(),
        "n_qubits": n_qubits,
        "target_thetas": thetas,
        "n_training": n_training,
        "shots": shots,
        "regression": {"a": a, "b": b, "r_squared": r2},
        "ideal_value": ideal_value,
        "noisy_target": noisy_target,
        "cdr_corrected": corrected,
    }

    filepath = os.path.join(RESULTS_DIR, "cdr_results.json")
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run CDR production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
