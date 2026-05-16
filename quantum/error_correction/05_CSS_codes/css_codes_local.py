"""
CSS Codes - Local Simulator Implementation
===========================================

General Calderbank-Shor-Steane (CSS) code construction demonstration.
Uses the Hamming [7,4,3] code as an example to build the Steane code.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
CSS code construction from two classical codes C1 and C2:
    - Require: C2 subset of C1 (equivalently, C1_perp subset of C2_perp)
    - Equivalently: H1 * H2^T = 0 (mod 2)
    - X-stabilizers from rows of H2 (detect Z errors)
    - Z-stabilizers from rows of H1 (detect X errors)

For self-dual CSS codes: C1 = C2, so H1 = H2 = H
    - Condition: H * H^T = 0 (mod 2) -- code is self-orthogonal

Example: Hamming [7,4,3] code
    - H * H^T = 0 (mod 2) -- verified below
    - Yields the [[7,1,3]] Steane code
    - k = k1 + k2 - n = 4 + 4 - 7 = 1 logical qubit

Parameters:
    n = block length of classical code
    k1 = dimension of C1
    k2 = dimension of C2
    k_quantum = k1 + k2 - n (logical qubits)
    d = min(d(C1\\C2), d(C2_perp\\C1_perp))
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, SparsePauliOp


# =============================================================================
# CLASSICAL CODE DEFINITIONS
# =============================================================================

def hamming_743_parity_check():
    """
    Parity check matrix for the classical Hamming [7,4,3] code.

    H has 3 rows and 7 columns. Each column is a distinct nonzero
    binary vector of length 3 (the binary representations of 1-7).
    """
    H = np.array([
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
    ], dtype=int)
    return H


def verify_css_condition(H1, H2):
    """
    Verify the CSS condition: H1 * H2^T = 0 (mod 2).

    This ensures that:
        - C2_perp subset of C1 (or equivalently C2 subset of C1)
        - X and Z stabilizers commute
        - The quantum code is well-defined
    """
    product = (H1 @ H2.T) % 2
    is_valid = np.all(product == 0)
    return is_valid, product


def classical_syndrome(H, error_vector):
    """
    Compute classical syndrome s = H * e (mod 2).

    The syndrome identifies which column of H matches the error pattern.
    For single-bit errors, the syndrome is the column of H.
    """
    s = (H @ error_vector) % 2
    return s


def classical_decode(H, syndrome):
    """
    Decode a Hamming syndrome to find the error position.

    The syndrome is the binary representation of the error column index.
    For Hamming codes, column j has value j+1 in binary.
    """
    s_val = syndrome[0] + 2 * syndrome[1] + 4 * syndrome[2]
    if s_val == 0:
        return None
    return s_val - 1


# =============================================================================
# CSS CODE CONSTRUCTION
# =============================================================================

def build_css_stabilizers(H1, H2, n):
    """
    Build X and Z stabilizers from parity check matrices.

    Z-stabilizers from rows of H1 (detect X errors):
        For each row r of H1, create Z_i where H1[r,i] = 1

    X-stabilizers from rows of H2 (detect Z errors):
        For each row r of H2, create X_i where H2[r,i] = 1
    """
    z_stabilizers = []
    for row_idx in range(H1.shape[0]):
        label = ['I'] * n
        for col in range(n):
            if H1[row_idx, col] == 1:
                label[n - 1 - col] = 'Z'  # Qiskit reverse ordering
        z_stabilizers.append(SparsePauliOp.from_list(
            [(''.join(label), 1.0)]))

    x_stabilizers = []
    for row_idx in range(H2.shape[0]):
        label = ['I'] * n
        for col in range(n):
            if H2[row_idx, col] == 1:
                label[n - 1 - col] = 'X'
        x_stabilizers.append(SparsePauliOp.from_list(
            [(''.join(label), 1.0)]))

    return x_stabilizers, z_stabilizers


def verify_stabilizer_commutation(x_stabs, z_stabs):
    """
    Verify that all X-stabilizers commute with all Z-stabilizers.

    Two Pauli operators commute iff they overlap on an even number
    of qubits where one is X and the other is Z (or vice versa).
    This is guaranteed by the CSS condition H1 * H2^T = 0.
    """
    results = []
    for i, sx in enumerate(x_stabs):
        for j, sz in enumerate(z_stabs):
            # Compute commutator via SparsePauliOp
            comm = (sx @ sz) - (sz @ sx)
            comm = comm.simplify()
            commutes = len(comm) == 0 or all(
                abs(c) < 1e-10 for c in comm.coeffs)
            results.append((i, j, commutes))
    return results


# =============================================================================
# CSS ENCODING AND SYNDROME
# =============================================================================

def build_css_encoding_circuit(H):
    """
    Build encoding circuit for a self-dual CSS code from parity check H.

    For the Hamming-based Steane code:
        1. H on parity-bit positions (positions 0, 1, 3 in 0-indexed)
        2. CNOT from parity bits to data bits according to H
    """
    n = H.shape[1]
    data = QuantumRegister(n, 'q')
    qc = QuantumCircuit(data, name='css_encode')

    # Identify parity bit positions (columns that are unit vectors)
    parity_positions = []
    for row_idx in range(H.shape[0]):
        for col in range(n):
            if H[row_idx, col] == 1:
                # Check if this column is a unit vector for this row
                is_unit = True
                for other_row in range(H.shape[0]):
                    if other_row != row_idx and H[other_row, col] == 1:
                        is_unit = False
                        break
                if is_unit and col not in parity_positions:
                    parity_positions.append(col)
                    break

    # H on parity positions
    for pos in parity_positions:
        qc.h(data[pos])

    # CNOT from each parity position to data positions in its row
    for row_idx, parity_pos in enumerate(parity_positions):
        for col in range(n):
            if H[row_idx, col] == 1 and col != parity_pos:
                qc.cx(data[parity_pos], data[col])

    return qc, parity_positions


def build_css_x_syndrome(H, n):
    """Build X-error syndrome circuit using Z-stabilizers from H."""
    n_stab = H.shape[0]
    data = QuantumRegister(n, 'q')
    anc = QuantumRegister(n_stab, 'xsyn')
    cbits = ClassicalRegister(n_stab, 'x_meas')
    qc = QuantumCircuit(data, anc, cbits, name='x_syndrome')

    for row in range(n_stab):
        for col in range(n):
            if H[row, col] == 1:
                qc.cx(data[col], anc[row])
    for i in range(n_stab):
        qc.measure(anc[i], cbits[i])

    return qc


def build_css_z_syndrome(H, n):
    """Build Z-error syndrome circuit using X-stabilizers from H."""
    n_stab = H.shape[0]
    data = QuantumRegister(n, 'q')
    anc = QuantumRegister(n_stab, 'zsyn')
    cbits = ClassicalRegister(n_stab, 'z_meas')
    qc = QuantumCircuit(data, anc, cbits, name='z_syndrome')

    for i in range(n_stab):
        qc.h(anc[i])
    for row in range(n_stab):
        for col in range(n):
            if H[row, col] == 1:
                qc.cx(anc[row], data[col])
    for i in range(n_stab):
        qc.h(anc[i])
    for i in range(n_stab):
        qc.measure(anc[i], cbits[i])

    return qc


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_css_condition():
    """Verify the CSS condition for the Hamming code."""
    print("\n" + "=" * 70)
    print("PART A: CSS Condition Verification")
    print("=" * 70)

    H = hamming_743_parity_check()

    print("\n  Hamming [7,4,3] parity check matrix H:")
    for i, row in enumerate(H):
        print(f"    Row {i}: {row}")

    # Self-dual CSS: H1 = H2 = H
    is_valid, product = verify_css_condition(H, H)
    print(f"\n  CSS condition: H * H^T (mod 2) =")
    for row in product:
        print(f"    {row}")
    print(f"  Is zero? {is_valid}")
    print(f"  -> CSS code is {'valid' if is_valid else 'INVALID'}")

    # Classical code parameters
    n = 7
    k_classical = 4
    d_classical = 3
    k_quantum = 2 * k_classical - n
    print(f"\n  Classical code: [{n},{k_classical},{d_classical}]")
    print(f"  Quantum code: [[{n},{k_quantum},{d_classical}]]")
    print(f"  k_quantum = 2*k_classical - n = 2*{k_classical} - {n} = "
          f"{k_quantum}")


def demo_stabilizer_construction():
    """Build and display CSS stabilizers."""
    print("\n" + "=" * 70)
    print("PART B: CSS Stabilizer Construction")
    print("=" * 70)

    H = hamming_743_parity_check()
    x_stabs, z_stabs = build_css_stabilizers(H, H, 7)

    print("\n  Z-stabilizers (from H1, detect X errors):")
    for i, s in enumerate(z_stabs):
        print(f"    Sz{i+1}: {s}")

    print("\n  X-stabilizers (from H2, detect Z errors):")
    for i, s in enumerate(x_stabs):
        print(f"    Sx{i+1}: {s}")

    # Verify commutation
    comm_results = verify_stabilizer_commutation(x_stabs, z_stabs)
    all_commute = all(c for _, _, c in comm_results)
    print(f"\n  All X-Z stabilizer pairs commute: {all_commute}")
    if not all_commute:
        for i, j, c in comm_results:
            if not c:
                print(f"    WARNING: Sx{i+1} and Sz{j+1} do NOT commute!")


def demo_encoding():
    """Demonstrate CSS encoding and verify codewords."""
    print("\n" + "=" * 70)
    print("PART C: CSS Encoding (Hamming -> Steane)")
    print("=" * 70)

    H = hamming_743_parity_check()
    enc_circuit, parity_pos = build_css_encoding_circuit(H)

    print(f"\n  Parity bit positions: {parity_pos}")
    print(f"  Encoding circuit depth: {enc_circuit.depth()}")

    # Verify encoded state
    qc0 = QuantumCircuit(7)
    qc0 = qc0.compose(enc_circuit)
    sv0 = Statevector(qc0)

    n_nonzero = len([a for a in sv0.data if abs(a) > 1e-10])
    print(f"\n  |0_L> has {n_nonzero} nonzero amplitudes")

    print(f"  Codeword basis states:")
    for i, a in enumerate(sv0.data):
        if abs(a) > 1e-10:
            bits = format(i, '07b')
            weight = bits.count('1')
            print(f"    |{bits}> (weight {weight}): {a.real:+.6f}")


def demo_independent_correction():
    """Demonstrate independent X and Z error correction."""
    print("\n" + "=" * 70)
    print("PART D: Independent Error Correction (CSS Property)")
    print("=" * 70)

    H = hamming_743_parity_check()
    sim = AerSimulator()

    # X errors detected by Z-syndrome
    print("\n  X errors (Z-syndrome from H1):")
    for q in range(7):
        data_reg = QuantumRegister(7, 'q')
        anc = QuantumRegister(3, 'syn')
        cbits = ClassicalRegister(3, 'meas')
        qc = QuantumCircuit(data_reg, anc, cbits)

        enc, _ = build_css_encoding_circuit(H)
        qc = qc.compose(enc, qubits=range(7))
        qc.x(data_reg[q])

        for row in range(3):
            for col in range(7):
                if H[row, col] == 1:
                    qc.cx(data_reg[col], anc[row])
        for i in range(3):
            qc.measure(anc[i], cbits[i])

        counts = sim.run(qc, shots=1024).result().get_counts()
        syndrome = max(counts, key=counts.get)
        s_bits = [int(b) for b in reversed(syndrome)]
        decoded = classical_decode(H, s_bits)
        status = "CORRECT" if decoded == q else "WRONG"
        print(f"    X on q{q}: syndrome={syndrome}, "
              f"decoded=q{decoded} [{status}]")

    # Z errors detected by X-syndrome
    print("\n  Z errors (X-syndrome from H2):")
    for q in range(7):
        data_reg = QuantumRegister(7, 'q')
        anc = QuantumRegister(3, 'syn')
        cbits = ClassicalRegister(3, 'meas')
        qc = QuantumCircuit(data_reg, anc, cbits)

        enc, _ = build_css_encoding_circuit(H)
        qc = qc.compose(enc, qubits=range(7))
        qc.z(data_reg[q])

        for i in range(3):
            qc.h(anc[i])
        for row in range(3):
            for col in range(7):
                if H[row, col] == 1:
                    qc.cx(anc[row], data_reg[col])
        for i in range(3):
            qc.h(anc[i])
        for i in range(3):
            qc.measure(anc[i], cbits[i])

        counts = sim.run(qc, shots=1024).result().get_counts()
        syndrome = max(counts, key=counts.get)
        s_bits = [int(b) for b in reversed(syndrome)]
        decoded = classical_decode(H, s_bits)
        status = "CORRECT" if decoded == q else "WRONG"
        print(f"    Z on q{q}: syndrome={syndrome}, "
              f"decoded=q{decoded} [{status}]")


def demo_css_vs_general():
    """Compare CSS construction parameters."""
    print("\n" + "=" * 70)
    print("PART E: CSS Code Parameter Summary")
    print("=" * 70)

    codes = [
        ("Steane", 7, 4, 4, 3),
        ("Shor (as CSS)", 9, 8, 2, 3),
    ]

    print(f"\n  {'Code':<20} {'n':>3} {'k1':>3} {'k2':>3} "
          f"{'k_q':>3} {'d':>3} {'Notation':<15}")
    print(f"  {'-'*55}")
    for name, n, k1, k2, d in codes:
        k_q = k1 + k2 - n
        notation = f"[[{n},{k_q},{d}]]"
        print(f"  {name:<20} {n:>3} {k1:>3} {k2:>3} "
              f"{k_q:>3} {d:>3} {notation:<15}")

    print(f"\n  CSS advantages:")
    print(f"    1. X and Z errors corrected independently")
    print(f"    2. Transversal CNOT gate")
    print(f"    3. Classical decoding for each error type")
    print(f"    4. Simpler syndrome extraction circuits")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_css_structure():
    """Visualize the CSS code structure."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    H = hamming_743_parity_check()

    # Parity check matrix
    ax = axes[0]
    im = ax.imshow(H, cmap='Blues', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(7))
    ax.set_xticklabels([f'q{i}' for i in range(7)])
    ax.set_yticks(range(3))
    ax.set_yticklabels(['Row 0', 'Row 1', 'Row 2'])
    ax.set_title('Hamming [7,4,3] Parity Check Matrix H', fontsize=13)
    ax.set_xlabel('Qubit Position', fontsize=11)
    for i in range(3):
        for j in range(7):
            ax.text(j, i, str(H[i, j]), ha='center', va='center',
                    fontsize=12, fontweight='bold')

    # CSS condition verification
    ax = axes[1]
    product = (H @ H.T) % 2
    im2 = ax.imshow(product, cmap='RdYlGn_r', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(3))
    ax.set_xticklabels(['Row 0', 'Row 1', 'Row 2'])
    ax.set_yticks(range(3))
    ax.set_yticklabels(['Row 0', 'Row 1', 'Row 2'])
    ax.set_title('H * H^T (mod 2) = 0  [CSS Condition]', fontsize=13)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, str(product[i, j]), ha='center', va='center',
                    fontsize=14, fontweight='bold')
    plt.colorbar(im2, ax=ax)

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/05_CSS_codes/css_codes_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("CSS Codes - Local Simulator")
    print("=" * 70)

    demo_css_condition()
    demo_stabilizer_construction()
    demo_encoding()
    demo_independent_correction()
    demo_css_vs_general()
    plot_css_structure()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    CSS (Calderbank-Shor-Steane) Code Construction:
    - Built from two classical codes C1, C2 with C2 subset C1
    - CSS condition: H1 * H2^T = 0 (mod 2)
    - X-stabilizers from H2 -> detect Z errors
    - Z-stabilizers from H1 -> detect X errors
    - Independent X and Z correction (key CSS property!)

    Example: Hamming [7,4,3] -> Steane [[7,1,3]]
    - Self-dual: H1 = H2 = H
    - H * H^T = 0 (mod 2) verified
    - 3 X-stabilizers + 3 Z-stabilizers = 6 total
    - k_quantum = 2*4 - 7 = 1 logical qubit

    Next: Stabilizer formalism provides a general framework
    that encompasses CSS and non-CSS codes.
    """)


if __name__ == "__main__":
    main()
