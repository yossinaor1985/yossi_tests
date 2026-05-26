"""
Fully Quantum Boosting via Amplitude Amplification - IBM Production-Ready
===========================================================================

This script demonstrates a production-quality amplitude amplification
workflow for boosting quantum classifier accuracy, designed for execution
on IBM Quantum hardware.

Qiskit Version: 2.4.1

Key production features:
    1. Configurable classifier and amplification parameters
    2. Backend-aware circuit transpilation
    3. Comprehensive Grover oscillation analysis
    4. Result persistence in JSON format
    5. Comparison of actual vs theoretical success curves
    6. Gate count and depth analysis per iteration count k

NOTE: Execution on real hardware is commented out. Set your IBM token
and uncomment the relevant sections to run on a real backend.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

# IBM Runtime imports (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session


# =============================================================================
# Configuration
# =============================================================================

# Classifier parameters
BASE_CLASSIFIER_ANGLE = 1.2    # RY angle for the data qubit (controls base accuracy)
TARGET_LABEL = 1               # Correct classification label (0 or 1)

# Amplitude amplification parameters
MAX_ITERATIONS = 8             # Maximum number of Grover iterations to test
SHOTS = 8192                   # Shots per circuit for sampling

# Output
OUTPUT_DIR = "quantum/algorithms/25_quantum_amplitude_boosting/results"


# =============================================================================
# Circuit Construction Functions
# =============================================================================

def build_simple_classifier(theta):
    """
    Build a 2-qubit classifier circuit with tunable base accuracy.

    Circuit:
        |0>_0 --[RY(theta)]--*--------
                              |
        |0>_1 ----------------X--[RY(pi/4)]--

    The parameter theta controls the base accuracy. For theta ~ 1.2,
    the probability of measuring |1> on qubit 1 is approximately 65%.

    Args:
        theta: Classifier angle parameter

    Returns:
        QuantumCircuit: The 2-qubit classifier circuit
    """
    qc = QuantumCircuit(2, name="Classifier_A")
    qc.ry(theta, 0)
    qc.cx(0, 1)
    qc.ry(np.pi / 4, 1)
    return qc


def build_classification_oracle(target_state):
    """
    Build oracle that marks the correct classification state.

    For target_state = 1: applies Z on qubit 1 (flips phase of |1>).
    For target_state = 0: applies X-Z-X on qubit 1 (flips phase of |0>).

    Args:
        target_state: Integer (0 or 1) representing the correct label

    Returns:
        QuantumCircuit: Oracle circuit
    """
    qc = QuantumCircuit(2, name="S_good")
    if target_state == 0:
        qc.x(1)
        qc.z(1)
        qc.x(1)
    else:
        qc.z(1)
    return qc


def build_zero_reflection(num_qubits):
    """
    Build the zero-state reflection: S_0 = 2|0><0| - I.

    Flips the phase of every basis state except |0...0>.

    Implementation: X on all qubits, multi-controlled Z, X on all qubits.

    Args:
        num_qubits: Number of qubits

    Returns:
        QuantumCircuit: Zero-state reflection circuit
    """
    qc = QuantumCircuit(num_qubits, name="S_0")
    for q in range(num_qubits):
        qc.x(q)
    if num_qubits == 2:
        qc.h(1)
        qc.cx(0, 1)
        qc.h(1)
    else:
        qc.h(num_qubits - 1)
        qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
        qc.h(num_qubits - 1)
    for q in range(num_qubits):
        qc.x(q)
    return qc


def build_grover_iterate(classifier_circuit, oracle):
    """
    Construct one Grover iterate: Q = A S_0^{dagger} A^{dagger} S_good.

    Args:
        classifier_circuit: The classifier circuit A
        oracle: The classification oracle S_good

    Returns:
        QuantumCircuit: One Grover iterate Q
    """
    num_qubits = classifier_circuit.num_qubits
    qc = QuantumCircuit(num_qubits, name="Q_iterate")
    qc.compose(oracle, inplace=True)
    qc.compose(classifier_circuit.inverse(), inplace=True)
    zero_ref = build_zero_reflection(num_qubits)
    qc.compose(zero_ref, inplace=True)
    qc.compose(classifier_circuit, inplace=True)
    return qc


def apply_amplitude_amplification(classifier_circuit, oracle, num_iterations):
    """
    Apply amplitude amplification: A followed by k Grover iterates.

    The full circuit computes Q^k A |0>.

    Args:
        classifier_circuit: The classifier circuit A
        oracle: The classification oracle S_good
        num_iterations: Number of Grover iterations k

    Returns:
        QuantumCircuit: The boosted circuit
    """
    num_qubits = classifier_circuit.num_qubits
    qc = QuantumCircuit(num_qubits, name=f"AA_k{num_iterations}")
    qc.compose(classifier_circuit, inplace=True)
    if num_iterations > 0:
        grover_iter = build_grover_iterate(classifier_circuit, oracle)
        for _ in range(num_iterations):
            qc.compose(grover_iter, inplace=True)
    return qc


def compute_success_probability(circuit, target_state):
    """
    Compute success probability via exact Statevector simulation.

    Args:
        circuit: QuantumCircuit to evaluate
        target_state: Target value (0 or 1) for the classification qubit

    Returns:
        float: Probability of correct classification
    """
    sv = Statevector(circuit)
    probs = sv.probabilities_dict()
    success_prob = 0.0
    for bitstring, prob in probs.items():
        label_bit = int(bitstring[0])
        if label_bit == target_state:
            success_prob += prob
    return success_prob


def theoretical_success_probability(p_base, k):
    """
    Compute theoretical success probability: p(k) = sin^2((2k+1) * theta_a).

    Args:
        p_base: Base success probability
        k: Number of Grover iterations

    Returns:
        float: Theoretical success probability
    """
    theta_a = np.arcsin(np.sqrt(p_base))
    return np.sin((2 * k + 1) * theta_a) ** 2


def run_amplitude_amplification_production():
    """
    Full production amplitude amplification pipeline.
    """
    print("=" * 70)
    print("Amplitude Amplification - Production IBM Quantum Implementation")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Configuration Summary
    # =========================================================================

    print(f"\nConfiguration:")
    print(f"  Classifier angle: {BASE_CLASSIFIER_ANGLE:.4f} rad")
    print(f"  Target label: |{TARGET_LABEL}>")
    print(f"  Max Grover iterations: {MAX_ITERATIONS}")
    print(f"  Shots per circuit: {SHOTS}")
    print(f"  Output directory: {OUTPUT_DIR}")

    # =========================================================================
    # STEP 2: IBM Quantum Service
    # =========================================================================

    print("\n--- Step 2: Backend Selection ---")
    print("Using local Aer simulator for demonstration.")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # service = QiskitRuntimeService(
    #     channel="ibm_quantum",
    #     token="YOUR_TOKEN"
    # )
    # backend = service.least_busy(
    #     simulator=False,
    #     min_num_qubits=2,
    #     operational=True
    # )
    # print(f"Backend: {backend.name}")
    # -------------------------------------------------------------------------

    # =========================================================================
    # STEP 3: Build Classifier and Verify Base Accuracy
    # =========================================================================

    print("\n--- Step 3: Classifier Construction ---")

    classifier = build_simple_classifier(BASE_CLASSIFIER_ANGLE)
    oracle = build_classification_oracle(TARGET_LABEL)

    p_base = compute_success_probability(classifier, TARGET_LABEL)
    theta_a = np.arcsin(np.sqrt(p_base))
    k_opt_exact = (np.pi / (4 * theta_a)) - 0.5

    print(f"Base success probability: p_base = {p_base:.6f}")
    print(f"theta_a = {theta_a:.6f} rad ({theta_a * 180 / np.pi:.2f} deg)")
    print(f"Optimal k (continuous): {k_opt_exact:.4f}")
    print(f"Oscillation period: ~{np.pi / theta_a:.2f} iterations")

    # =========================================================================
    # STEP 4: Transpilation Analysis
    # =========================================================================

    print("\n--- Step 4: Transpilation Analysis ---")

    for k in [0, 1, 2, 3]:
        boosted = apply_amplitude_amplification(classifier, oracle, k)
        decomposed = boosted.decompose()
        gate_counts = decomposed.count_ops()
        cx_count = gate_counts.get('cx', 0)
        depth = decomposed.depth()
        print(f"  k={k}: depth={depth:>4}, "
              f"gates={sum(gate_counts.values()):>4}, "
              f"CX={cx_count:>3}")

    print("\nKey insight: each Grover iterate adds ~2*depth(A) + depth(oracle)")
    print("Circuit depth grows linearly with k.")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
    # for k in [0, 1, 2, 3]:
    #     boosted = apply_amplitude_amplification(classifier, oracle, k)
    #     boosted.measure_all()
    #     transpiled = pm.run(boosted)
    #     print(f"  k={k}: transpiled depth={transpiled.depth()}, "
    #           f"CX={transpiled.count_ops().get('cx', 0)}")
    # -------------------------------------------------------------------------

    # =========================================================================
    # STEP 5: Run Amplitude Amplification (Statevector + Sampling)
    # =========================================================================

    print("\n--- Step 5: Amplitude Amplification Results ---")

    k_values = list(range(MAX_ITERATIONS + 1))
    results_per_k = {}

    print(f"\n{'k':>3} | {'p_actual':>10} | {'p_theory':>10} | "
          f"{'delta':>10} | {'Depth':>6} | {'Status':>12}")
    print("-" * 65)

    for k in k_values:
        # Build boosted circuit
        boosted = apply_amplitude_amplification(classifier, oracle, k)

        # Exact probability via Statevector
        p_actual = compute_success_probability(boosted, TARGET_LABEL)
        p_theory = theoretical_success_probability(p_base, k)
        delta = abs(p_actual - p_theory)

        # Circuit metrics
        decomposed = boosted.decompose()
        depth = decomposed.depth()
        gate_counts = decomposed.count_ops()

        # Sampling via AerSimulator
        boosted_meas = boosted.copy()
        boosted_meas.measure_all()

        backend_sim = AerSimulator()
        sampler = AerSampler(backend=backend_sim)
        job = sampler.run([boosted_meas], shots=SHOTS)
        result = job.result()
        counts = result[0].data.meas.get_counts()

        # Compute sampled success probability
        total_shots = sum(counts.values())
        sampled_success = sum(
            count for bs, count in counts.items()
            if int(bs[0]) == TARGET_LABEL
        ) / total_shots

        # Status
        if p_actual > 0.95:
            status = "EXCELLENT"
        elif p_actual > p_base:
            status = "IMPROVED"
        elif abs(p_actual - p_base) < 0.05:
            status = "NEUTRAL"
        else:
            status = "OVERSHOOT"

        print(f"{k:>3} | {p_actual:>10.6f} | {p_theory:>10.6f} | "
              f"{delta:>10.2e} | {depth:>6} | {status:>12}")

        results_per_k[k] = {
            "p_actual_statevector": float(p_actual),
            "p_theoretical": float(p_theory),
            "p_sampled": float(sampled_success),
            "deviation": float(delta),
            "circuit_depth": int(depth),
            "gate_counts": {str(g): int(c) for g, c in gate_counts.items()},
            "cx_count": int(gate_counts.get('cx', 0)),
            "status": status,
            "top_counts": dict(
                sorted(counts.items(), key=lambda x: x[1], reverse=True)[:8]
            ),
        }

    # =========================================================================
    # STEP 6: Find Optimal k and Analyze Oscillation
    # =========================================================================

    print("\n--- Step 6: Oscillation Analysis ---")

    best_k = max(results_per_k.keys(),
                 key=lambda k: results_per_k[k]["p_actual_statevector"])
    best_prob = results_per_k[best_k]["p_actual_statevector"]

    overshoot_ks = [k for k, r in results_per_k.items()
                    if r["p_actual_statevector"] < p_base and k > 0]

    print(f"\nBest iteration count: k = {best_k}")
    print(f"Best success probability: {best_prob:.6f}")
    print(f"Improvement: {p_base:.4f} -> {best_prob:.4f} "
          f"({best_prob / p_base:.2f}x)")
    print(f"Overshooting at k = {overshoot_ks}")
    print(f"Oscillation period: ~{np.pi / theta_a:.1f} iterations")

    # Maximum validation error
    max_deviation = max(r["deviation"] for r in results_per_k.values())
    print(f"Max |actual - theory| deviation: {max_deviation:.2e}")
    print(f"Theory validation: {'PASS' if max_deviation < 0.02 else 'FAIL'}")

    # =========================================================================
    # STEP 7: Save Results
    # =========================================================================

    print("\n--- Step 7: Saving Results ---")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "Amplitude_Amplification_Boosting",
        "qiskit_version": "2.4.1",
        "classifier": {
            "type": "2_qubit_RY_CNOT_RY",
            "angle_theta": float(BASE_CLASSIFIER_ANGLE),
            "target_label": int(TARGET_LABEL),
            "num_qubits": 2,
            "base_success_probability": float(p_base),
            "theta_a_rad": float(theta_a),
            "theta_a_deg": float(theta_a * 180 / np.pi),
            "optimal_k_continuous": float(k_opt_exact),
            "oscillation_period": float(np.pi / theta_a),
        },
        "config": {
            "max_iterations": MAX_ITERATIONS,
            "shots": SHOTS,
            "backend": "aer_simulator (demo)",
        },
        "results": {
            "best_k": int(best_k),
            "best_success_probability": float(best_prob),
            "improvement_factor": float(best_prob / p_base),
            "overshoot_iterations": overshoot_ks,
            "max_theory_deviation": float(max_deviation),
            "per_iteration": {
                str(k): r for k, r in results_per_k.items()
            },
        },
        "theoretical_formula": (
            "p(k) = sin^2((2k+1) * arcsin(sqrt(p_base)))"
        ),
    }

    filepath = os.path.join(OUTPUT_DIR,
                            "quantum_amplitude_boosting_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"Results saved to {filepath}")

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print(f"""
    Amplitude Amplification Boosting - Production Considerations:

    1. Circuit Depth Growth:
       - Each Grover iterate adds 2*depth(A) + depth(oracle) gates
       - For the 2-qubit classifier: ~12 gates per iterate
       - For k iterations: total depth ~ (2k+1) * depth_A + k * depth_oracle
       - NISQ feasibility: k = 1-3 is practical; k > 3 likely too deep
       - At k={best_k}, the decomposed circuit depth is
         {results_per_k[best_k]['circuit_depth']}

    2. Grover's Oscillation:
       - Success probability oscillates: p(k) = sin^2((2k+1) * theta_a)
       - Overshooting occurs when (2k+1)*theta_a > pi/2
       - Must estimate p_base to choose optimal k
       - Quantum counting (phase estimation on Q) can estimate theta_a
         but adds significant circuit depth

    3. Relationship to Grover Search:
       - Grover search is the special case where A = H^n (uniform
         superposition) and p_base = M/N (M marked items out of N)
       - Amplitude amplification generalizes to ANY state preparation A
       - The quadratic speedup O(1/sqrt(epsilon)) is tight (BBBV lower bound)

    4. Oblivious Amplitude Amplification (OAA):
       - Standard AA requires an oracle S_good that marks correct states
       - OAA removes this requirement when the "good" subspace is
         defined by an ancilla register being in state |0>
       - More practical for inference (no labels needed at prediction time)
       - Requires the classifier to use an ancilla-flagged architecture

    5. Classical vs Quantum Error Reduction:
       - Classical repetition: O(1/epsilon) independent classifier runs
         to reduce error probability to epsilon (by majority vote)
       - Quantum amplitude amplification: O(1/sqrt(epsilon)) coherent
         iterations (quadratic speedup)
       - BUT: quantum requires coherent reversible classifier
       - Classical can use non-reversible, noisy classifiers
       - Break-even point depends on classifier depth and hardware noise

    6. NISQ Hardware Limitations:
       - Each Grover iterate doubles the effective classifier depth
       - Gate errors accumulate: fidelity ~ (1-e)^(num_2q_gates)
       - For current error rates (~0.5-1% per CX), the boosted circuit
         at k=2 has ~{results_per_k[min(2, MAX_ITERATIONS)]['cx_count']} CX gates
       - Error mitigation (TREX, ZNE) can help but adds overhead
       - Practical recommendation: use k=1 on NISQ, verify improvement

    7. Extensions:
       - Fixed-point amplitude amplification (Yoder, Low, Chuang 2014):
         converges monotonically (no oscillation) but slower
       - Variable-time amplitude amplification: adaptively choose k
       - Quantum signal processing: unified framework for amplitude
         manipulation with optimal query complexity
    """)


if __name__ == "__main__":
    run_amplitude_amplification_production()
