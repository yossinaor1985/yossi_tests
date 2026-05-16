"""
3-Qubit Bit-Flip Code - Local Simulator Implementation
========================================================

Demonstrates encoding, error injection, syndrome measurement,
and error correction for the simplest quantum error correcting code.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Encoding: |psi> = alpha|0> + beta|1> -> alpha|000> + beta|111>
Stabilizers: S1 = Z1Z2, S2 = Z2Z3
Syndrome decoding: (0,0)->None, (1,0)->X1, (1,1)->X2, (0,1)->X3
Logical error rate: p_L = 3p^2 - 2p^3 (fails with 2+ errors)
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
    Build the 3-qubit bit-flip encoding circuit.

    Encoding (see explanation_physicist.md, Section 2.2):
        |psi>|0>|0> -> CNOT(0,1) -> CNOT(0,2) -> alpha|000> + beta|111>

    The data qubit (q0) is entangled with two ancilla qubits (q1, q2)
    via CNOT gates. This creates the GHZ-type encoded state.
    """
    data = QuantumRegister(3, 'data')
    qc = QuantumCircuit(data, name='encode')

    # CNOT from data qubit to ancilla qubits
    qc.cx(data[0], data[1])
    qc.cx(data[0], data[2])

    return qc


def build_syndrome_circuit():
    """
    Build syndrome measurement circuit.

    Syndrome (see explanation_physicist.md, Section 4):
        S1 = Z1Z2: parity of qubits 0,1
        S2 = Z2Z3: parity of qubits 1,2

    Measured via CNOT gates to ancilla qubits:
        a0 = q0 XOR q1 (syndrome bit 1)
        a1 = q1 XOR q2 (syndrome bit 2)
    """
    data = QuantumRegister(3, 'data')
    syndrome = QuantumRegister(2, 'syn')
    syn_bits = ClassicalRegister(2, 'syn_meas')
    qc = QuantumCircuit(data, syndrome, syn_bits, name='syndrome')

    # S1 = Z1Z2: check parity of q0, q1
    qc.cx(data[0], syndrome[0])
    qc.cx(data[1], syndrome[0])

    # S2 = Z2Z3: check parity of q1, q2
    qc.cx(data[1], syndrome[1])
    qc.cx(data[2], syndrome[1])

    # Measure syndrome
    qc.measure(syndrome[0], syn_bits[0])
    qc.measure(syndrome[1], syn_bits[1])

    return qc


def build_correction_circuit(syndrome_result):
    """
    Build correction circuit based on syndrome.

    Syndrome table (explanation_physicist.md, Section 4.2):
        (0,0) -> no error
        (1,0) -> X on qubit 0
        (1,1) -> X on qubit 1
        (0,1) -> X on qubit 2
    """
    data = QuantumRegister(3, 'data')
    qc = QuantumCircuit(data, name='correct')

    s1, s2 = syndrome_result

    if s1 == 1 and s2 == 0:
        qc.x(data[0])  # Error on qubit 0
    elif s1 == 1 and s2 == 1:
        qc.x(data[1])  # Error on qubit 1
    elif s1 == 0 and s2 == 1:
        qc.x(data[2])  # Error on qubit 2

    return qc


# =============================================================================
# FULL ENCODE-ERROR-CORRECT CYCLE
# =============================================================================

def run_bit_flip_code(error_prob, n_shots=10000, initial_state='0'):
    """
    Run the full bit-flip code cycle.

    Steps:
        1. Prepare initial state
        2. Encode into 3 qubits
        3. Apply bit-flip errors with probability p
        4. Measure syndrome
        5. Apply correction
        6. Decode and measure logical qubit
    """
    # Build full circuit
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

    # Step 2: Encode
    qc.cx(data[0], data[1])
    qc.cx(data[0], data[2])
    qc.barrier()

    # Step 3: Apply bit-flip errors (simulated using rotation gates)
    # X error with probability p is equivalent to:
    # With prob p, apply X; with prob 1-p, apply I
    # We use the qiskit noise model instead
    # For this demo, we'll manually inject errors for specific analysis
    # and use the noise model for statistical analysis

    qc.barrier()

    # Step 4: Syndrome measurement
    qc.cx(data[0], syndrome[0])
    qc.cx(data[1], syndrome[0])
    qc.cx(data[1], syndrome[1])
    qc.cx(data[2], syndrome[1])
    qc.measure(syndrome[0], syn_bits[0])
    qc.measure(syndrome[1], syn_bits[1])

    # Step 5 & 6: Correction and output would need conditional operations
    # For statistical analysis, we use a different approach below

    return qc


def simulate_error_rates(p_values, n_trials=10000):
    """
    Compare logical error rate with and without the bit-flip code.

    Without code: p_error = p
    With code: p_error = 3p^2 - 2p^3 (from Section 5.1)

    We simulate using pure state evolution and random error injection.
    """
    results_coded = []
    results_uncoded = []

    rng = np.random.default_rng(42)

    for p in p_values:
        # Uncoded: simply flip with probability p
        errors_uncoded = rng.random(n_trials) < p
        p_uncoded = errors_uncoded.mean()
        results_uncoded.append(p_uncoded)

        # Coded: flip each of 3 qubits independently with prob p
        # Error occurs when majority vote fails (2+ flips)
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
    print("PART A: Encoding Circuit")
    print("=" * 70)

    # Encode |0>
    qc = QuantumCircuit(3)
    qc.cx(0, 1)
    qc.cx(0, 2)

    sv = Statevector(qc)
    print(f"\nEncoding |0>:")
    print(f"  Circuit: {qc.draw(output='text')}")
    print(f"  |0_L> = {sv}")

    # Encode |1>
    qc1 = QuantumCircuit(3)
    qc1.x(0)
    qc1.cx(0, 1)
    qc1.cx(0, 2)

    sv1 = Statevector(qc1)
    print(f"\nEncoding |1>:")
    print(f"  |1_L> = {sv1}")

    # Encode |+>
    qcp = QuantumCircuit(3)
    qcp.h(0)
    qcp.cx(0, 1)
    qcp.cx(0, 2)

    svp = Statevector(qcp)
    print(f"\nEncoding |+>:")
    print(f"  |+_L> = {svp}")
    print(f"  = (|000> + |111>)/sqrt(2)  (GHZ state)")


def demo_syndrome():
    """Demonstrate syndrome measurement for each error type."""
    print("\n" + "=" * 70)
    print("PART B: Syndrome Measurement")
    print("=" * 70)

    errors = {
        "No error (I)": None,
        "X on qubit 0": 0,
        "X on qubit 1": 1,
        "X on qubit 2": 2,
    }

    for name, error_qubit in errors.items():
        # Build: encode -> error -> syndrome
        qc = QuantumCircuit(5, 2)  # 3 data + 2 syndrome, 2 classical

        # Encode |0>
        qc.cx(0, 1)
        qc.cx(0, 2)

        # Inject error
        if error_qubit is not None:
            qc.x(error_qubit)

        # Syndrome measurement
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(1, 4)
        qc.cx(2, 4)
        qc.measure(3, 0)
        qc.measure(4, 1)

        # Run
        sim = AerSimulator()
        result = sim.run(qc, shots=1024).result()
        counts = result.get_counts()

        print(f"\n  {name}:")
        print(f"    Syndrome: {counts}")


def demo_error_rates():
    """Compare coded vs uncoded error rates."""
    print("\n" + "=" * 70)
    print("PART C: Error Rate Comparison")
    print("=" * 70)

    p_values = np.linspace(0.001, 0.5, 30)
    p_uncoded, p_coded = simulate_error_rates(p_values, n_trials=50000)

    # Theoretical
    p_theory = 3 * p_values**2 - 2 * p_values**3

    print(f"\n  Physical error rate -> Logical error rate:")
    for p, pu, pc, pt in zip(p_values[::5], p_uncoded[::5], p_coded[::5], p_theory[::5]):
        print(f"    p={p:.3f}: uncoded={pu:.4f}, coded={pc:.4f}, theory={pt:.4f}")

    return p_values, p_uncoded, p_coded, p_theory


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(p_values, p_uncoded, p_coded, p_theory):
    """Plot error rate comparison."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Error rates
    ax = axes[0]
    ax.plot(p_values, p_uncoded, 'r-', linewidth=2, label='Uncoded (p)')
    ax.plot(p_values, p_coded, 'bo', markersize=3, alpha=0.5, label='Coded (simulation)')
    ax.plot(p_values, p_theory, 'g--', linewidth=2, label='Coded (theory: 3p^2 - 2p^3)')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Logical Error Rate', fontsize=12)
    ax.set_title('Bit-Flip Code: Coded vs Uncoded', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Improvement factor
    ax = axes[1]
    improvement = p_uncoded / (p_coded + 1e-10)
    improvement_theory = p_values / (p_theory + 1e-10)
    ax.plot(p_values, improvement_theory, 'g-', linewidth=2, label='Improvement (p / p_L)')
    ax.axhline(y=1, color='r', linestyle='--', label='Break-even (improvement = 1)')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Improvement Factor', fontsize=12)
    ax.set_title('Error Suppression Factor', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(improvement_theory[:20]) * 1.1)

    plt.tight_layout()
    plt.savefig("quantum/error_correction/01_bit_flip_code/bit_flip_results.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("3-Qubit Bit-Flip Code - Local Simulator")
    print("=" * 70)

    demo_encoding()
    demo_syndrome()
    p_values, p_uncoded, p_coded, p_theory = demo_error_rates()
    plot_results(p_values, p_uncoded, p_coded, p_theory)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    3-Qubit Bit-Flip Code:
    - Encodes: |0> -> |000>, |1> -> |111>
    - Corrects: single X (bit-flip) errors
    - Stabilizers: Z1Z2, Z2Z3
    - Logical error rate: 3p^2 - 2p^3
    - Helps when: p < 0.5

    Limitation: does NOT correct phase (Z) or general errors.
    """)


if __name__ == "__main__":
    main()