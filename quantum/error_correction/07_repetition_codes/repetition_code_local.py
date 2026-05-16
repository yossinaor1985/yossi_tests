"""
Repetition Codes - Local Simulator Implementation
==================================================

Generalization of the 3-qubit bit-flip code to d-qubit repetition codes
for d = 3, 5, 7. Demonstrates how increasing code distance suppresses
logical error rates.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
d-qubit repetition code:
    Encoding: |0> -> |00...0> (d zeros), |1> -> |11...1> (d ones)
    Stabilizers: Z_i Z_{i+1} for i = 0, ..., d-2 (nearest-neighbor parity)
    Distance: d (minimum weight of a logical operator)
    Corrects: floor((d-1)/2) bit-flip errors

Majority vote correction:
    After measuring all qubits, take majority vote.
    Error occurs when > d/2 qubits flip.

Logical error rate for physical error rate p:
    p_L = sum_{j=ceil(d/2)}^{d} C(d,j) * p^j * (1-p)^(d-j)

    For d=3: p_L = 3p^2 - 2p^3
    For d=5: p_L = 10p^3 - 15p^4 + 6p^5
    For d=7: p_L = 35p^4 - 84p^5 + 70p^6 - 20p^7

Threshold: p < 0.5 (code always helps when p < 0.5)

Limitation: only corrects bit-flip (X) errors, not phase (Z) errors.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import comb

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


# =============================================================================
# REPETITION CODE CONSTRUCTION
# =============================================================================

def build_repetition_encoding(d):
    """
    Build d-qubit repetition code encoding circuit.

    Encoding: CNOT chain from qubit 0 to all others.
        |psi>|0>...|0> -> CNOT(0,1), CNOT(0,2), ..., CNOT(0,d-1)

    Result: |0> -> |00...0>, |1> -> |11...1>
    """
    data = QuantumRegister(d, 'q')
    qc = QuantumCircuit(data, name=f'rep_{d}_encode')

    for i in range(1, d):
        qc.cx(data[0], data[i])

    return qc


def build_repetition_syndrome(d):
    """
    Build syndrome measurement circuit for d-qubit repetition code.

    d-1 syndrome bits from nearest-neighbor Z-parity checks:
        s_i = Z_i * Z_{i+1} for i = 0, ..., d-2

    Each syndrome bit detects if adjacent qubits disagree.
    """
    n_syn = d - 1
    data = QuantumRegister(d, 'q')
    anc = QuantumRegister(n_syn, 'syn')
    cbits = ClassicalRegister(n_syn, 'syn_meas')
    qc = QuantumCircuit(data, anc, cbits, name=f'rep_{d}_syndrome')

    for i in range(n_syn):
        qc.cx(data[i], anc[i])
        qc.cx(data[i + 1], anc[i])

    for i in range(n_syn):
        qc.measure(anc[i], cbits[i])

    return qc


def decode_repetition_syndrome(syndrome_bits, d):
    """
    Decode repetition code syndrome using minimum-weight correction.

    The syndrome identifies boundaries between regions of 0s and 1s.
    The correction flips the minimum number of qubits to restore uniformity.

    For simple implementation: use majority vote on the implied qubit values.
    """
    # Reconstruct qubit values from syndrome
    # syndrome[i] = 1 means qubit[i] != qubit[i+1]
    qubit_values = [0]  # Assume qubit 0 is 0
    for i in range(len(syndrome_bits)):
        if syndrome_bits[i] == 1:
            qubit_values.append(1 - qubit_values[-1])
        else:
            qubit_values.append(qubit_values[-1])

    # Majority vote
    n_ones = sum(qubit_values)
    n_zeros = d - n_ones
    if n_ones > n_zeros:
        # Flip all zeros to ones
        correction = [i for i in range(d) if qubit_values[i] == 0]
        decoded_value = 1
    else:
        # Flip all ones to zeros
        correction = [i for i in range(d) if qubit_values[i] == 1]
        decoded_value = 0

    return correction, decoded_value


# =============================================================================
# ERROR SIMULATION
# =============================================================================

def simulate_bit_flip_errors(d, p, n_trials=10000, rng=None):
    """
    Simulate repetition code under random bit-flip errors.

    For each trial:
        1. Start with encoded |0> = |00...0>
        2. Each qubit flips independently with probability p
        3. Apply majority vote correction
        4. Check if logical qubit is correct

    Returns: logical error rate
    """
    if rng is None:
        rng = np.random.default_rng(42)

    errors = 0
    for _ in range(n_trials):
        # Random bit-flip errors on each qubit
        flips = rng.random(d) < p
        n_flips = flips.sum()

        # Majority vote: error if more than d/2 qubits flipped
        if n_flips > d / 2:
            errors += 1
        elif n_flips == d / 2 and d % 2 == 0:
            # Tie-break: randomly choose (counts as error half the time)
            errors += rng.random() < 0.5

    return errors / n_trials


def theoretical_logical_error_rate(d, p):
    """
    Compute theoretical logical error rate for d-qubit repetition code.

    p_L = sum_{j=ceil(d/2)}^{d} C(d,j) * p^j * (1-p)^(d-j)
    """
    t = d // 2  # Number of correctable errors
    p_L = 0.0
    for j in range(t + 1, d + 1):
        p_L += comb(d, j, exact=True) * (p ** j) * ((1 - p) ** (d - j))
    return p_L


# =============================================================================
# QISKIT CIRCUIT SIMULATION
# =============================================================================

def run_qiskit_repetition(d, error_qubits=None):
    """
    Run repetition code cycle using Qiskit AerSimulator.

    Steps: encode -> inject errors -> syndrome -> decode
    """
    data = QuantumRegister(d, 'q')
    n_syn = d - 1
    anc = QuantumRegister(n_syn, 'syn')
    syn_bits = ClassicalRegister(n_syn, 'syn_meas')
    out = ClassicalRegister(d, 'out')
    qc = QuantumCircuit(data, anc, syn_bits, out)

    # Encode
    for i in range(1, d):
        qc.cx(data[0], data[i])
    qc.barrier()

    # Inject errors
    if error_qubits is not None:
        for eq in error_qubits:
            qc.x(data[eq])
    qc.barrier()

    # Syndrome measurement
    for i in range(n_syn):
        qc.cx(data[i], anc[i])
        qc.cx(data[i + 1], anc[i])
    for i in range(n_syn):
        qc.measure(anc[i], syn_bits[i])
    qc.barrier()

    # Measure all data qubits
    for i in range(d):
        qc.measure(data[i], out[i])

    sim = AerSimulator()
    counts = sim.run(qc, shots=4096).result().get_counts()

    return counts


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_encoding():
    """Demonstrate repetition code encoding for d=3,5,7."""
    print("\n" + "=" * 70)
    print("PART A: Repetition Code Encoding")
    print("=" * 70)

    for d in [3, 5, 7]:
        # Encode |0>
        qc0 = QuantumCircuit(d)
        enc = build_repetition_encoding(d)
        qc0 = qc0.compose(enc)
        sv0 = Statevector(qc0)

        # Encode |1>
        qc1 = QuantumCircuit(d)
        qc1.x(0)
        qc1 = qc1.compose(enc)
        sv1 = Statevector(qc1)

        print(f"\n  d={d} repetition code:")
        print(f"    |0_L> = |{'0'*d}>")
        print(f"    |1_L> = |{'1'*d}>")
        print(f"    Corrects up to {(d-1)//2} bit-flip errors")
        print(f"    Stabilizers: {d-1} nearest-neighbor Z-parities")
        print(f"    <0_L|1_L> = {abs(sv0.inner(sv1))**2:.10f}")


def demo_syndrome():
    """Demonstrate syndrome measurement for various error patterns."""
    print("\n" + "=" * 70)
    print("PART B: Syndrome Measurement")
    print("=" * 70)

    for d in [3, 5]:
        print(f"\n  d={d} code:")

        test_cases = [
            ([], "No error"),
            ([0], "X on q0"),
            ([d-1], f"X on q{d-1}"),
            ([d//2], f"X on q{d//2}"),
        ]
        if d >= 5:
            test_cases.append(([0, 1], "X on q0,q1"))

        for error_qubits, name in test_cases:
            counts = run_qiskit_repetition(d, error_qubits if error_qubits else None)
            print(f"    {name}: {dict(list(counts.items())[:3])}")


def demo_error_rate_comparison():
    """Compare error rates for different code distances."""
    print("\n" + "=" * 70)
    print("PART C: Error Rate Comparison (d=3, 5, 7)")
    print("=" * 70)

    p_values = np.linspace(0.001, 0.49, 40)
    distances = [3, 5, 7]
    n_trials = 50000
    rng = np.random.default_rng(42)

    results = {}
    for d in distances:
        simulated = []
        theoretical = []
        for p in p_values:
            sim_rate = simulate_bit_flip_errors(d, p, n_trials, rng)
            theo_rate = theoretical_logical_error_rate(d, p)
            simulated.append(sim_rate)
            theoretical.append(theo_rate)
        results[d] = {
            'simulated': np.array(simulated),
            'theoretical': np.array(theoretical),
        }

    # Print sample values
    print(f"\n  {'p':>6} | {'d=3 (sim)':>10} | {'d=5 (sim)':>10} | "
          f"{'d=7 (sim)':>10} | {'d=3 (thy)':>10} | {'d=5 (thy)':>10} | "
          f"{'d=7 (thy)':>10}")
    print(f"  {'-'*80}")
    for idx in range(0, len(p_values), 8):
        p = p_values[idx]
        vals = [f"{results[d]['simulated'][idx]:.5f}" for d in distances]
        thys = [f"{results[d]['theoretical'][idx]:.5f}" for d in distances]
        print(f"  {p:>6.3f} | {vals[0]:>10} | {vals[1]:>10} | "
              f"{vals[2]:>10} | {thys[0]:>10} | {thys[1]:>10} | "
              f"{thys[2]:>10}")

    return p_values, results


def demo_majority_vote():
    """Demonstrate majority vote correction step by step."""
    print("\n" + "=" * 70)
    print("PART D: Majority Vote Correction")
    print("=" * 70)

    d = 5
    test_syndromes = [
        ([0, 0, 0, 0], "No errors"),
        ([1, 0, 0, 0], "Error between q0-q1 (q0 flipped)"),
        ([0, 1, 0, 0], "Error between q1-q2 (q1 flipped)"),
        ([1, 1, 0, 0], "Errors at boundary of q0,q1 (q0,q1 flipped)"),
    ]

    for syndrome, description in test_syndromes:
        correction, decoded = decode_repetition_syndrome(syndrome, d)
        print(f"\n  Syndrome: {syndrome}")
        print(f"    Description: {description}")
        print(f"    Correction qubits: {correction}")
        print(f"    Decoded logical value: {decoded}")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_error_rates(p_values, results):
    """Plot error rate curves for different code distances."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    colors = {3: 'blue', 5: 'green', 7: 'red'}

    # Linear scale
    ax = axes[0]
    ax.plot(p_values, p_values, 'k--', linewidth=1, label='Uncoded (p)')
    for d in [3, 5, 7]:
        ax.plot(p_values, results[d]['simulated'], 'o',
                color=colors[d], markersize=2, alpha=0.4,
                label=f'd={d} (simulated)')
        ax.plot(p_values, results[d]['theoretical'], '-',
                color=colors[d], linewidth=2,
                label=f'd={d} (theoretical)')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Logical Error Rate', fontsize=12)
    ax.set_title('Repetition Code: Error Suppression', fontsize=13)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # Log scale
    ax = axes[1]
    ax.semilogy(p_values, p_values, 'k--', linewidth=1, label='Uncoded')
    for d in [3, 5, 7]:
        theo = results[d]['theoretical']
        valid = theo > 0
        ax.semilogy(p_values[valid], theo[valid], '-',
                     color=colors[d], linewidth=2, label=f'd={d}')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Logical Error Rate (log scale)', fontsize=12)
    ax.set_title('Repetition Code: Log-Scale Comparison', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, which='both')
    ax.set_ylim(1e-8, 1)

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/07_repetition_codes/"
        "repetition_code_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Repetition Codes (d=3,5,7) - Local Simulator")
    print("=" * 70)

    demo_encoding()
    demo_syndrome()
    p_values, results = demo_error_rate_comparison()
    demo_majority_vote()
    plot_error_rates(p_values, results)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    d-Qubit Repetition Code:
    - Encodes |0> -> |0...0>, |1> -> |1...1> (d copies)
    - Distance d: corrects floor((d-1)/2) bit-flip errors
    - Stabilizers: d-1 nearest-neighbor Z-parities
    - Majority vote decoding

    Error rates:
    - d=3: p_L = 3p^2 - 2p^3 (corrects 1 error)
    - d=5: p_L = 10p^3 - 15p^4 + 6p^5 (corrects 2 errors)
    - d=7: p_L = 35p^4 - ... (corrects 3 errors)
    - Threshold: p < 0.5

    Key insight: increasing d provides exponential suppression of p_L
    when p < threshold. This is the foundation of fault-tolerant QC.

    Limitation: only corrects X errors, not Z errors.
    Next: Surface codes protect against both X and Z errors.
    """)


if __name__ == "__main__":
    main()
