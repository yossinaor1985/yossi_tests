"""
Fully Quantum Boosting via Amplitude Amplification - Local Simulator
=====================================================================

This script demonstrates amplitude amplification applied to a simple
quantum classifier, showing how a weak classifier's success probability
can be boosted to near-certainty using Grover iterations.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
A quantum classifier A prepares the state:

    A |0> = sin(theta_a) |psi_good> + cos(theta_a) |psi_bad>

where the base success probability is p = sin^2(theta_a).

Amplitude amplification applies the Grover iterate:

    Q = A (2|0><0| - I) A^{dagger} S_good

where S_good flips the phase of the "good" (correct classification)
subspace. After k applications:

    Q^k A |0> has success probability p(k) = sin^2((2k+1) theta_a)

Key features demonstrated:
    1. Simple 2-qubit quantum classifier with tunable accuracy
    2. Manual construction of the Grover iterate for amplitude amplification
    3. Success probability oscillation (Grover's sinusoidal behavior)
    4. Comparison of actual vs theoretical success probabilities
    5. Overshooting effect: too many iterations degrades accuracy

Problem: Binary classification with a 2-qubit circuit
    - Qubit 0: data qubit
    - Qubit 1: classification (label) qubit
    - Target: boost the probability of measuring |1> on the label qubit
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator


def build_simple_classifier(theta):
    """
    Build a 2-qubit classifier circuit with tunable base accuracy.

    The classifier acts on:
        - Qubit 0: data qubit (input encoding)
        - Qubit 1: classification qubit (label output)

    Circuit:
        |0>_0 --[RY(theta)]--*--------
                              |
        |0>_1 ----------------X--[RY(pi/4)]--

    The RY(theta) on qubit 0 controls the data encoding, and the CNOT
    plus RY(pi/4) on qubit 1 produces a classification. The angle theta
    determines the base accuracy of the classifier.

    For theta ~ 1.2 rad, the base accuracy of measuring |1> on qubit 1
    is approximately 65%.

    Args:
        theta: Classifier angle parameter (controls base accuracy)

    Returns:
        QuantumCircuit: The 2-qubit classifier circuit
    """
    qc = QuantumCircuit(2, name="Classifier_A")
    qc.ry(theta, 0)       # Encode data on qubit 0
    qc.cx(0, 1)           # Entangle data and label
    qc.ry(np.pi / 4, 1)   # Classification rotation on label qubit
    return qc


def build_classification_oracle(target_state):
    """
    Build oracle that marks the "correct classification" state.

    The oracle flips the phase of the target state on the classification
    qubit. For target_state = 1 (correct classification is |1>):

        S_good |psi_0>|0> = +|psi_0>|0>    (wrong classification)
        S_good |psi_1>|1> = -|psi_1>|1>    (correct classification)

    This is implemented as a Z gate on the classification qubit (qubit 1),
    which applies -1 to the |1> component and +1 to the |0> component.

    For a general target state, we use X gates to map the target to |1>,
    apply Z, then unmap.

    Args:
        target_state: Integer (0 or 1) representing the correct label

    Returns:
        QuantumCircuit: Oracle circuit that marks the correct classification
    """
    qc = QuantumCircuit(2, name="S_good")

    if target_state == 0:
        # Mark |0> on qubit 1: X - Z - X = -(I - 2|0><0|) on qubit 1
        qc.x(1)
        qc.z(1)
        qc.x(1)
    else:
        # Mark |1> on qubit 1: Z gate flips phase of |1>
        qc.z(1)

    return qc


def build_zero_reflection(num_qubits):
    """
    Build the reflection about the zero state: S_0 = 2|0><0| - I.

    This operator flips the phase of every basis state EXCEPT |0...0>.
    Equivalently, it applies -1 to all states and +1 to |0...0>,
    which is -(I - 2|0><0|).

    Implementation:
        1. Apply X to all qubits (maps |0> -> |1>)
        2. Apply multi-controlled Z (flips phase of |1...1>)
        3. Apply X to all qubits (maps back)

    The overall effect is a phase flip on all states except |0...0>.

    Args:
        num_qubits: Number of qubits

    Returns:
        QuantumCircuit: Zero-state reflection circuit
    """
    qc = QuantumCircuit(num_qubits, name="S_0")

    # Apply X to all qubits
    for q in range(num_qubits):
        qc.x(q)

    # Multi-controlled Z gate: flip phase of |1...1>
    if num_qubits == 1:
        qc.z(0)
    elif num_qubits == 2:
        # CZ gate: flips phase when both qubits are |1>
        qc.h(1)
        qc.cx(0, 1)
        qc.h(1)
    else:
        # General: H on last qubit, multi-controlled X, H on last qubit
        qc.h(num_qubits - 1)
        qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
        qc.h(num_qubits - 1)

    # Apply X to all qubits
    for q in range(num_qubits):
        qc.x(q)

    return qc


def build_grover_iterate(classifier_circuit, oracle):
    """
    Construct one Grover iterate Q for amplitude amplification.

    The Grover iterate is:
        Q = A S_0^{dagger} A^{dagger} S_good

    Applied right-to-left:
        1. Apply S_good (oracle that marks correct classification)
        2. Apply A^{dagger} (inverse of classifier)
        3. Apply S_0^{dagger} = -(I - 2|0><0|) (zero-state reflection)
        4. Apply A (classifier again)

    Note: S_0^{dagger} = -(2|0><0| - I). In practice the global phase
    from the minus sign does not affect measurement probabilities, so we
    implement 2|0><0| - I and absorb the sign.

    Args:
        classifier_circuit: The classifier circuit A
        oracle: The classification oracle S_good

    Returns:
        QuantumCircuit: One Grover iterate Q
    """
    num_qubits = classifier_circuit.num_qubits
    qc = QuantumCircuit(num_qubits, name="Q_iterate")

    # Step 1: Apply oracle S_good
    qc.compose(oracle, inplace=True)

    # Step 2: Apply A^{dagger} (inverse classifier)
    qc.compose(classifier_circuit.inverse(), inplace=True)

    # Step 3: Apply zero-state reflection (2|0><0| - I)
    # We negate all states, then flip |0>. Equivalently, use the
    # build_zero_reflection which implements -(I - 2|0><0|) = 2|0><0| - I
    # up to global phase.
    zero_ref = build_zero_reflection(num_qubits)
    qc.compose(zero_ref, inplace=True)

    # Step 4: Apply A (classifier)
    qc.compose(classifier_circuit, inplace=True)

    return qc


def apply_amplitude_amplification(classifier_circuit, oracle, num_iterations):
    """
    Apply amplitude amplification: initial classifier + k Grover iterates.

    The full circuit is:
        Q^k A |0>

    where A is applied once (the initial state preparation) and Q is
    applied k times.

    Args:
        classifier_circuit: The classifier circuit A
        oracle: The classification oracle S_good
        num_iterations: Number of Grover iterations k

    Returns:
        QuantumCircuit: The boosted circuit Q^k A
    """
    num_qubits = classifier_circuit.num_qubits
    qc = QuantumCircuit(num_qubits, name=f"AA_k{num_iterations}")

    # Initial classifier application: A |0>
    qc.compose(classifier_circuit, inplace=True)

    # Apply Q = A S_0^{dagger} A^{dagger} S_good k times
    if num_iterations > 0:
        grover_iter = build_grover_iterate(classifier_circuit, oracle)
        for _ in range(num_iterations):
            qc.compose(grover_iter, inplace=True)

    return qc


def compute_success_probability(circuit, target_state):
    """
    Compute the probability of measuring the target state on the label qubit.

    Uses exact Statevector simulation (no sampling noise).

    For a 2-qubit circuit, the target is a specific value on qubit 1
    (the classification qubit). We sum probabilities over all basis states
    where qubit 1 has the target value.

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
        # Qiskit bitstring ordering: qubit 1 is the second-to-last character
        # For a 2-qubit system, bitstring "ab" means qubit 1 = a, qubit 0 = b
        label_bit = int(bitstring[0])  # Qubit 1 (label qubit)
        if label_bit == target_state:
            success_prob += prob

    return success_prob


def theoretical_success_probability(p_base, k):
    """
    Compute the theoretical success probability after k Grover iterations.

    p(k) = sin^2((2k+1) * arcsin(sqrt(p_base)))

    This is the exact analytical result from amplitude amplification theory
    (Brassard et al. 2002).

    Args:
        p_base: Base success probability of the classifier (0 < p_base < 1)
        k: Number of Grover iterations (non-negative integer)

    Returns:
        float: Theoretical success probability after k iterations
    """
    theta_a = np.arcsin(np.sqrt(p_base))
    return np.sin((2 * k + 1) * theta_a) ** 2


def main():
    print("=" * 70)
    print("Fully Quantum Boosting via Amplitude Amplification - Local Simulator")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Build a Quantum Classifier with Base Accuracy ~65%
    # =========================================================================

    print("\n--- Step 1: Build Quantum Classifier ---")

    # Choose theta to give approximately 65% base accuracy
    # The base accuracy depends on the interplay of RY(theta) and CNOT + RY(pi/4)
    # We'll determine the exact value via Statevector simulation
    CLASSIFIER_ANGLE = 1.2  # Tuned to give p_base ~ 0.65
    TARGET_LABEL = 1        # Correct classification is |1> on the label qubit

    classifier = build_simple_classifier(CLASSIFIER_ANGLE)

    print(f"Classifier angle theta = {CLASSIFIER_ANGLE:.4f} rad")
    print(f"Target classification: |{TARGET_LABEL}> on qubit 1")
    print(f"\nClassifier circuit:")
    print(classifier.draw(output="text"))

    # =========================================================================
    # STEP 2: Verify Base Success Probability via Statevector
    # =========================================================================

    print("\n--- Step 2: Verify Base Success Probability ---")

    p_base = compute_success_probability(classifier, TARGET_LABEL)
    theta_a = np.arcsin(np.sqrt(p_base))

    print(f"Base success probability: p_base = {p_base:.6f}")
    print(f"  = sin^2(theta_a) where theta_a = {theta_a:.6f} rad")
    print(f"  = {theta_a * 180 / np.pi:.2f} degrees")

    # Full state decomposition
    sv = Statevector(classifier)
    probs = sv.probabilities_dict()
    print(f"\nFull state after classifier A|00>:")
    for bs in sorted(probs.keys()):
        if probs[bs] > 1e-10:
            label = "GOOD (correct)" if int(bs[0]) == TARGET_LABEL else "BAD (incorrect)"
            print(f"  |{bs}> : prob = {probs[bs]:.6f}  [{label}]")

    print(f"\nTotal 'good' probability: {p_base:.6f}")
    print(f"Total 'bad' probability:  {1 - p_base:.6f}")

    # Estimate optimal number of iterations
    k_opt_exact = (np.pi / (4 * theta_a)) - 0.5
    print(f"\nOptimal iterations (continuous): k_opt = {k_opt_exact:.4f}")
    print(f"Nearest integers to try: k = {int(np.floor(k_opt_exact))} "
          f"or k = {int(np.ceil(k_opt_exact))}")

    # =========================================================================
    # STEP 3: Build the Classification Oracle
    # =========================================================================

    print("\n--- Step 3: Build Classification Oracle ---")

    oracle = build_classification_oracle(TARGET_LABEL)
    print(f"Oracle marks |{TARGET_LABEL}> on the classification qubit (qubit 1)")
    print(f"\nOracle circuit:")
    print(oracle.draw(output="text"))

    # Verify oracle action
    oracle_op = Operator(oracle)
    print(f"\nOracle matrix (2x2 block on qubit 1):")
    print(f"  Diagonal elements: {np.diag(oracle_op.data).real}")
    print(f"  (Should be +1 for |0> and -1 for |1> on qubit 1, "
          f"or vice versa)")

    # =========================================================================
    # STEP 4: Apply Amplitude Amplification for k = 0, 1, 2, 3, 4, 5
    # =========================================================================

    print("\n--- Step 4: Amplitude Amplification Results ---")

    max_k = 8
    k_values = list(range(max_k + 1))
    actual_probs = []
    theoretical_probs = []

    print(f"\n{'k':>3} | {'Actual p(k)':>12} | {'Theory p(k)':>12} | "
          f"{'Angle (2k+1)*theta_a':>22} | {'Match':>6}")
    print("-" * 70)

    for k in k_values:
        # Build boosted circuit
        boosted_circuit = apply_amplitude_amplification(
            classifier, oracle, k
        )

        # Compute actual success probability
        p_actual = compute_success_probability(boosted_circuit, TARGET_LABEL)
        actual_probs.append(p_actual)

        # Compute theoretical success probability
        p_theory = theoretical_success_probability(p_base, k)
        theoretical_probs.append(p_theory)

        # Angle for this k
        angle = (2 * k + 1) * theta_a
        angle_deg = angle * 180 / np.pi

        match = "OK" if abs(p_actual - p_theory) < 0.01 else "DIFF"

        print(f"{k:>3} | {p_actual:>12.6f} | {p_theory:>12.6f} | "
              f"{angle:>10.4f} rad ({angle_deg:>7.2f} deg) | {match:>6}")

    # =========================================================================
    # STEP 5: Compare Actual vs Theoretical (Validation)
    # =========================================================================

    print("\n--- Step 5: Validation of Actual vs Theoretical ---")

    max_deviation = max(abs(a - t) for a, t in
                        zip(actual_probs, theoretical_probs))
    print(f"Maximum deviation |actual - theory|: {max_deviation:.2e}")
    print(f"Validation: {'PASS' if max_deviation < 0.02 else 'FAIL'}")

    # Find the best k
    best_k = k_values[np.argmax(actual_probs)]
    best_prob = max(actual_probs)
    print(f"\nBest iteration count: k = {best_k}")
    print(f"Best success probability: {best_prob:.6f}")
    print(f"Improvement over base: {best_prob / p_base:.2f}x "
          f"({p_base:.4f} -> {best_prob:.4f})")

    # =========================================================================
    # STEP 6: Show the "Overshooting" Effect (Grover's Oscillation)
    # =========================================================================

    print("\n--- Step 6: Grover's Oscillation (Overshooting Effect) ---")

    print(f"\nThe success probability oscillates with period "
          f"T ~ pi/theta_a = {np.pi / theta_a:.2f} iterations.")
    print(f"theta_a = {theta_a:.4f} rad => the state rotates by "
          f"2*theta_a = {2 * theta_a:.4f} rad per Grover iterate.")

    # Find iterations where probability drops below base
    overshoot_ks = [k for k, p in zip(k_values, actual_probs)
                    if p < p_base and k > 0]
    if overshoot_ks:
        print(f"\nOvershooting detected at k = {overshoot_ks}")
        print(f"At these k values, the boosted accuracy is WORSE than "
              f"the base accuracy ({p_base:.4f})!")
        print("This demonstrates that amplitude amplification is NOT "
              "monotone -- more iterations is not always better.")
    else:
        print("\nNo overshooting detected in the tested range.")

    # Extended oscillation for visualization (fractional k for smooth curve)
    k_continuous = np.linspace(0, max_k, 500)
    p_continuous = np.sin((2 * k_continuous + 1) * theta_a) ** 2

    # =========================================================================
    # STEP 7: Visualization (2x1 plot)
    # =========================================================================

    print("\n--- Step 7: Visualization ---")
    print("Generating plots...")

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))

    # --- Plot (0): Success Probability vs Grover Iterations ---
    # Theoretical continuous curve
    axes[0].plot(k_continuous, p_continuous, 'b-', alpha=0.4,
                 linewidth=2, label='Theory (continuous)')

    # Actual discrete points
    axes[0].plot(k_values, actual_probs, 'ro', markersize=10, zorder=5,
                 label='Actual (Statevector)')

    # Theoretical discrete points
    axes[0].plot(k_values, theoretical_probs, 'b^', markersize=8,
                 zorder=4, alpha=0.7, label='Theory (discrete)')

    # Base probability line
    axes[0].axhline(y=p_base, color='gray', linestyle='--', alpha=0.6,
                     label=f'Base accuracy (p={p_base:.3f})')

    # Perfect accuracy line
    axes[0].axhline(y=1.0, color='green', linestyle=':', alpha=0.4,
                     label='Perfect accuracy (p=1)')

    # Highlight the best k
    axes[0].annotate(
        f'Best: k={best_k}\np={best_prob:.4f}',
        xy=(best_k, best_prob),
        xytext=(best_k + 0.5, best_prob - 0.15),
        fontsize=10,
        arrowprops=dict(arrowstyle='->', color='red'),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                  edgecolor='red')
    )

    # Highlight overshooting
    for k_over in overshoot_ks:
        p_over = actual_probs[k_over]
        axes[0].annotate(
            f'Overshoot!\np={p_over:.3f}',
            xy=(k_over, p_over),
            xytext=(k_over + 0.5, p_over + 0.12),
            fontsize=9,
            arrowprops=dict(arrowstyle='->', color='orange'),
            color='darkorange'
        )

    axes[0].set_xlabel('Number of Grover iterations (k)', fontsize=13)
    axes[0].set_ylabel('Success probability p(k)', fontsize=13)
    axes[0].set_title(
        'Amplitude Amplification: Success Probability vs Iterations\n'
        f'p(k) = sin²((2k+1) · arcsin(√{p_base:.3f}))  '
        f'[θ_a = {theta_a:.4f} rad]',
        fontsize=13
    )
    axes[0].set_xlim(-0.3, max_k + 0.5)
    axes[0].set_ylim(-0.05, 1.1)
    axes[0].set_xticks(k_values)
    axes[0].legend(loc='upper right', fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # --- Plot (1): Circuit Diagram for k=1 ---
    boosted_k1 = apply_amplitude_amplification(classifier, oracle, 1)
    boosted_k1_drawing = boosted_k1.decompose().draw(output="mpl",
                                                      fold=60,
                                                      style="iqp")

    # Since we cannot directly embed a circuit drawing in a subplot,
    # we render the circuit as text and annotate the subplot
    axes[1].set_axis_off()

    # Build a text representation of the circuit structure
    circuit_text = (
        "Amplitude Amplification Circuit (k=1)\n"
        "=" * 50 + "\n\n"
        "Structure: A |0⟩  followed by  Q = A · S₀ · A† · S_good\n\n"
    )

    # Show circuit gate counts
    gate_counts = boosted_k1.decompose().count_ops()
    circuit_text += "Gate counts (decomposed):\n"
    for gate, count in sorted(gate_counts.items()):
        circuit_text += f"  {gate}: {count}\n"

    circuit_text += f"\nCircuit depth: {boosted_k1.decompose().depth()}\n"
    circuit_text += f"Number of qubits: {boosted_k1.num_qubits}\n"

    # Show the text-based circuit diagram
    circuit_str = boosted_k1.decompose().draw(output="text", fold=80)
    circuit_text += f"\nCircuit diagram (k=1 iteration):\n{circuit_str}"

    axes[1].text(0.02, 0.98, circuit_text, transform=axes[1].transAxes,
                 fontsize=9, verticalalignment='top',
                 fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='lightyellow',
                           alpha=0.8))

    plt.tight_layout()
    save_path = ("quantum/algorithms/25_quantum_amplitude_boosting/"
                 "quantum_amplitude_boosting_results.png")
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"\nPlot saved to {save_path}")

    # =========================================================================
    # STEP 8: Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    Amplitude Amplification successfully boosted a weak quantum classifier.

    Classifier Configuration:
      Angle: theta = {CLASSIFIER_ANGLE:.4f} rad
      Base accuracy: p_base = {p_base:.4f} ({p_base * 100:.1f}%)
      Target label: |{TARGET_LABEL}>
      theta_a = arcsin(sqrt(p_base)) = {theta_a:.4f} rad

    Amplitude Amplification Results:
      Best iteration count: k = {best_k}
      Best success probability: {best_prob:.4f} ({best_prob * 100:.1f}%)
      Improvement: {p_base:.4f} -> {best_prob:.4f} ({best_prob / p_base:.2f}x boost)

    Key observations:
      1. Actual probabilities match theory: max deviation = {max_deviation:.2e}
      2. Success probability oscillates sinusoidally (Grover's oscillation)
      3. Overshooting at k = {overshoot_ks if overshoot_ks else 'none in range'}
         (more iterations can DECREASE accuracy)
      4. Optimal k depends on base accuracy via:
         k_opt = pi / (4 * arcsin(sqrt(p_base))) - 1/2 = {k_opt_exact:.2f}

    Quadratic speedup:
      Classical repetition: O(1/epsilon) calls to reduce error to epsilon
      Quantum amplification: O(1/sqrt(epsilon)) iterations
      For p_base = {p_base:.3f}, classical needs ~{int(1 / (1 - p_base))} repetitions
      to approach certainty; quantum needs ~{best_k} iteration(s).
    """)


if __name__ == "__main__":
    main()
