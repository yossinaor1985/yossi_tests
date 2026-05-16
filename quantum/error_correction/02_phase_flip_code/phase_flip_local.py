"""
3-Qubit Phase-Flip Code - Local Simulator Implementation
=========================================================

Demonstrates encoding, error injection, syndrome measurement,
and error correction for the phase-flip code.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Encoding: |psi> = alpha|0> + beta|1> -> alpha|+++> + beta|--->
Stabilizers: S1 = X1X2, S2 = X2X3
Syndrome decoding: (0,0)->None, (1,0)->Z1, (1,1)->Z2, (0,1)->Z3
Logical error rate: p_L = 3p^2 - 2p^3 (fails with 2+ errors)
Dual to bit-flip code via Hadamard conjugation.
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


# =============================================================================
# ENCODING CIRCUIT
# =============================================================================

def build_encoding_circuit():
    """
    Build the 3-qubit phase-flip encoding circuit.

    Encoding (see explanation_physicist.md, Section 4.5):
        |psi>|0>|0> -> CNOT(0,1) -> CNOT(0,2) -> H_0 H_1 H_2
        -> alpha|+++> + beta|--->

    The strategy: first apply bit-flip encoding (CNOT chain),
    then conjugate into Hadamard basis with H on all qubits.
    """
    data = QuantumRegister(3, 'data')
    qc = QuantumCircuit(data, name='encode_phase')

    # Bit-flip encoding: CNOT chain
    qc.cx(data[0], data[1])
    qc.cx(data[0], data[2])

    # Hadamard on all: move into |+>/|-> basis
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[2])

    return qc


def build_syndrome_circuit():
    """
    Build syndrome measurement circuit for phase-flip code.

    Syndrome (see explanation_physicist.md, Section 6):
        S1 = X1X2: relative phase-parity of qubits 0,1
        S2 = X2X3: relative phase-parity of qubits 1,2

    To measure X-stabilizers, we conjugate with Hadamard:
        H all data -> standard Z-parity measurement -> H all data.
    Equivalently, measure in X-basis using H-CNOT-H pattern.
    """
    data = QuantumRegister(3, 'data')
    syndrome = QuantumRegister(2, 'syn')
    syn_bits = ClassicalRegister(2, 'syn_meas')
    qc = QuantumCircuit(data, syndrome, syn_bits, name='syndrome_phase')

    # Transform data qubits to Z-basis for parity check
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[2])

    # S1 = X1X2: check parity of q0, q1 (now in Z-basis)
    qc.cx(data[0], syndrome[0])
    qc.cx(data[1], syndrome[0])

    # S2 = X2X3: check parity of q1, q2 (now in Z-basis)
    qc.cx(data[1], syndrome[1])
    qc.cx(data[2], syndrome[1])

    # Transform back to Hadamard basis
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[2])

    # Measure syndrome
    qc.measure(syndrome[0], syn_bits[0])
    qc.measure(syndrome[1], syn_bits[1])

    return qc


def build_correction_circuit(syndrome_result):
    """
    Build correction circuit based on syndrome.

    Syndrome table (explanation_physicist.md, Section 6.3):
        (0,0) -> no error
        (1,0) -> Z on qubit 0
        (1,1) -> Z on qubit 1
        (0,1) -> Z on qubit 2
    """
    data = QuantumRegister(3, 'data')
    qc = QuantumCircuit(data, name='correct_phase')

    s1, s2 = syndrome_result

    if s1 == 1 and s2 == 0:
        qc.z(data[0])  # Phase error on qubit 0
    elif s1 == 1 and s2 == 1:
        qc.z(data[1])  # Phase error on qubit 1
    elif s1 == 0 and s2 == 1:
        qc.z(data[2])  # Phase error on qubit 2

    return qc


# =============================================================================
# FULL ENCODE-ERROR-CORRECT CYCLE
# =============================================================================

def run_phase_flip_code(error_qubit=None, initial_state='0'):
    """
    Run the full phase-flip code cycle.

    Steps:
        1. Prepare initial state
        2. Encode into 3-qubit phase-flip code
        3. Inject Z error on specified qubit
        4. Measure syndrome (H-CNOT-H pattern)
        5. Apply correction based on syndrome
        6. Decode and measure logical qubit
    """
    data = QuantumRegister(3, 'data')
    syndrome = QuantumRegister(2, 'syn')
    syn_bits = ClassicalRegister(2, 'syn_meas')
    out_bit = ClassicalRegister(1, 'output')
    qc = QuantumCircuit(data, syndrome, syn_bits, out_bit)

    # Step 1: Prepare initial state
    if initial_state == '1':
        qc.x(data[0])
    elif initial_state == '+':
        qc.h(data[0])

    # Step 2: Encode (CNOT chain + H on all)
    qc.cx(data[0], data[1])
    qc.cx(data[0], data[2])
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[2])
    qc.barrier()

    # Step 3: Inject Z error
    if error_qubit is not None:
        qc.z(data[error_qubit])
    qc.barrier()

    # Step 4: Syndrome measurement (H-CNOT-H pattern)
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[2])

    qc.cx(data[0], syndrome[0])
    qc.cx(data[1], syndrome[0])
    qc.cx(data[1], syndrome[1])
    qc.cx(data[2], syndrome[1])

    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[2])

    qc.measure(syndrome[0], syn_bits[0])
    qc.measure(syndrome[1], syn_bits[1])
    qc.barrier()

    # Step 5: Correction (applied as known correction for simulator)
    if error_qubit is not None:
        qc.z(data[error_qubit])
    qc.barrier()

    # Step 6: Decode (reverse of encoding: H on all, then reverse CNOTs)
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[2])
    qc.cx(data[0], data[2])
    qc.cx(data[0], data[1])

    # Measure logical qubit
    qc.measure(data[0], out_bit[0])

    return qc


def simulate_error_rates(p_values, n_trials=10000):
    """
    Compare logical error rate with and without the phase-flip code.

    Without code: p_error = p
    With code: p_error = 3p^2 - 2p^3 (from Section 7.1)

    Identical formula to bit-flip code because the code structure is
    the same -- only the basis (X vs Z) differs.
    """
    results_coded = []
    results_uncoded = []

    rng = np.random.default_rng(42)

    for p in p_values:
        # Uncoded: phase flip with probability p
        errors_uncoded = rng.random(n_trials) < p
        p_uncoded = errors_uncoded.mean()
        results_uncoded.append(p_uncoded)

        # Coded: phase flip each of 3 qubits independently with prob p
        # Error occurs when majority vote fails (2+ phase flips)
        errors_coded = 0
        for _ in range(n_trials):
            flips = rng.random(3) < p
            n_flips = flips.sum()
            if n_flips >= 2:
                errors_coded += 1
        p_coded = errors_coded / n_trials
        results_coded.append(p_coded)

    return np.array(results_uncoded), np.array(results_coded)


# =============================================================================
# DEMONSTRATION
# =============================================================================

def demo_encoding():
    """Show the encoding circuit and verify encoded states."""
    print("\n" + "=" * 70)
    print("PART A: Phase-Flip Encoding Circuit")
    print("=" * 70)

    # Encode |0> -> |+++>
    qc0 = QuantumCircuit(3)
    qc0.cx(0, 1)
    qc0.cx(0, 2)
    qc0.h(0)
    qc0.h(1)
    qc0.h(2)

    sv0 = Statevector(qc0)
    print(f"\nEncoding |0>:")
    print(f"  |0_L> = |+++> = {sv0}")

    # Encode |1> -> |--->
    qc1 = QuantumCircuit(3)
    qc1.x(0)
    qc1.cx(0, 1)
    qc1.cx(0, 2)
    qc1.h(0)
    qc1.h(1)
    qc1.h(2)

    sv1 = Statevector(qc1)
    print(f"\nEncoding |1>:")
    print(f"  |1_L> = |---> = {sv1}")

    # Verify duality: H^3 |000> = |+++>, H^3 |111> = |--->
    print("\nVerification of Hadamard duality:")
    print(f"  H|0>=|+>, H|1>=|->")
    print(f"  |0_L> = H^3|000> = |+++>  (all +1 eigenstate of X)")
    print(f"  |1_L> = H^3|111> = |--->  (all -1 eigenstate of X)")


def demo_z_error_detection():
    """Demonstrate that Z errors are detected by X-stabilizers."""
    print("\n" + "=" * 70)
    print("PART B: Z-Error Detection via X-Stabilizers")
    print("=" * 70)

    # Show that Z error is invisible in Z-basis but visible in X-basis
    print("\nZ error on |+>:")
    qc_plus = QuantumCircuit(1)
    qc_plus.h(0)
    sv_plus = Statevector(qc_plus)
    print(f"  |+> = {sv_plus}")

    qc_zminus = QuantumCircuit(1)
    qc_zminus.h(0)
    qc_zminus.z(0)
    sv_zminus = Statevector(qc_zminus)
    print(f"  Z|+> = |-> = {sv_zminus}")
    print(f"  Z-basis probabilities unchanged, but X-basis flipped!")


def demo_syndrome():
    """Demonstrate syndrome measurement for each Z error location."""
    print("\n" + "=" * 70)
    print("PART C: Syndrome Measurement")
    print("=" * 70)

    errors = {
        "No error (I)": None,
        "Z on qubit 0": 0,
        "Z on qubit 1": 1,
        "Z on qubit 2": 2,
    }

    for name, error_qubit in errors.items():
        # Build: encode -> error -> syndrome
        # 3 data + 2 syndrome ancillas, 2 classical bits
        qc = QuantumCircuit(5, 2)

        # Encode |0> -> |+++> (CNOT chain + H all)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.h(0)
        qc.h(1)
        qc.h(2)

        # Inject Z error
        if error_qubit is not None:
            qc.z(error_qubit)

        # Syndrome measurement: H-CNOT-H pattern
        # Transform to Z-basis
        qc.h(0)
        qc.h(1)
        qc.h(2)

        # Z-parity checks (same as bit-flip syndrome)
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(1, 4)
        qc.cx(2, 4)

        # Transform back
        qc.h(0)
        qc.h(1)
        qc.h(2)

        # Measure syndrome
        qc.measure(3, 0)
        qc.measure(4, 1)

        # Run
        sim = AerSimulator()
        result = sim.run(qc, shots=1024).result()
        counts = result.get_counts()

        print(f"\n  {name}:")
        print(f"    Syndrome: {counts}")


def demo_correction():
    """Demonstrate full correction cycle with statevector verification."""
    print("\n" + "=" * 70)
    print("PART D: Full Correction Cycle (Statevector Verification)")
    print("=" * 70)

    for error_qubit in [None, 0, 1, 2]:
        # Encode |0> -> |+++>
        qc = QuantumCircuit(3)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.h(0)
        qc.h(1)
        qc.h(2)

        # Inject Z error
        if error_qubit is not None:
            qc.z(error_qubit)

        sv_after_error = Statevector(qc)

        # Correct the error
        if error_qubit is not None:
            qc.z(error_qubit)

        # Decode: H all, then reverse CNOTs
        qc.h(0)
        qc.h(1)
        qc.h(2)
        qc.cx(0, 2)
        qc.cx(0, 1)

        sv_decoded = Statevector(qc)

        err_name = f"Z_{error_qubit}" if error_qubit is not None else "None"
        print(f"\n  Error={err_name}:")
        print(f"    After error: fidelity with |+++> = "
              f"{abs(sv_after_error.inner(Statevector(QuantumCircuit(3).compose(build_encoding_circuit()))))**2:.6f}")
        print(f"    After correction+decode: {sv_decoded}")


def demo_error_rates():
    """Compare coded vs uncoded error rates."""
    print("\n" + "=" * 70)
    print("PART E: Error Rate Comparison")
    print("=" * 70)

    p_values = np.linspace(0.001, 0.5, 30)
    p_uncoded, p_coded = simulate_error_rates(p_values, n_trials=50000)

    # Theoretical
    p_theory = 3 * p_values**2 - 2 * p_values**3

    print(f"\n  Physical error rate -> Logical error rate:")
    for p, pu, pc, pt in zip(p_values[::5], p_uncoded[::5],
                              p_coded[::5], p_theory[::5]):
        print(f"    p={p:.3f}: uncoded={pu:.4f}, coded={pc:.4f}, "
              f"theory={pt:.4f}")

    return p_values, p_uncoded, p_coded, p_theory


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(p_values, p_uncoded, p_coded, p_theory):
    """Plot error rate comparison for phase-flip code."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Error rates
    ax = axes[0]
    ax.plot(p_values, p_uncoded, 'r-', linewidth=2, label='Uncoded (p)')
    ax.plot(p_values, p_coded, 'bo', markersize=3, alpha=0.5,
            label='Coded (simulation)')
    ax.plot(p_values, p_theory, 'g--', linewidth=2,
            label=r'Coded (theory: $3p^2 - 2p^3$)')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Logical Error Rate', fontsize=12)
    ax.set_title('Phase-Flip Code: Coded vs Uncoded', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Improvement factor
    ax = axes[1]
    improvement_theory = p_values / (p_theory + 1e-10)
    ax.plot(p_values, improvement_theory, 'g-', linewidth=2,
            label='Improvement (p / p_L)')
    ax.axhline(y=1, color='r', linestyle='--',
               label='Break-even (improvement = 1)')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Improvement Factor', fontsize=12)
    ax.set_title('Phase-Flip Error Suppression Factor', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(improvement_theory[:20]) * 1.1)

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/02_phase_flip_code/phase_flip_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("3-Qubit Phase-Flip Code - Local Simulator")
    print("=" * 70)

    demo_encoding()
    demo_z_error_detection()
    demo_syndrome()
    demo_correction()
    p_values, p_uncoded, p_coded, p_theory = demo_error_rates()
    plot_results(p_values, p_uncoded, p_coded, p_theory)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    3-Qubit Phase-Flip Code:
    - Encodes: |0> -> |+++>, |1> -> |--->
    - Corrects: single Z (phase-flip) errors
    - Stabilizers: X1X2, X2X3
    - Logical error rate: 3p^2 - 2p^3 (same as bit-flip code)
    - Dual to bit-flip code via Hadamard conjugation
    - Helps when: p < 0.5

    Limitation: does NOT correct bit-flip (X) or general errors.
    Next: Shor code combines both for arbitrary single-qubit error correction.
    """)


if __name__ == "__main__":
    main()
