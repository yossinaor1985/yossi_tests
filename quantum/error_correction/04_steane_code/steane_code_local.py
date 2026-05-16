"""
[[7,1,3]] Steane Code - Local Simulator Implementation
======================================================

The Steane code is a 7-qubit CSS code based on the classical Hamming [7,4,3]
code. It encodes 1 logical qubit and corrects any single-qubit error.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Parity check matrix (Hamming [7,4,3]):
    H = [[1,0,1,0,1,0,1],
         [0,1,1,0,0,1,1],
         [0,0,0,1,1,1,1]]

6 stabilizer generators (from H):
    X-stabilizers: X on positions where each row of H has 1
        Sx1 = X0 X2 X4 X6   (row 1: positions 0,2,4,6)
        Sx2 = X1 X2 X5 X6   (row 2: positions 1,2,5,6)
        Sx3 = X3 X4 X5 X6   (row 3: positions 3,4,5,6)

    Z-stabilizers: Z on same positions
        Sz1 = Z0 Z2 Z4 Z6
        Sz2 = Z1 Z2 Z5 Z6
        Sz3 = Z3 Z4 Z5 Z6

Code parameters: [[7,1,3]] - 7 physical, 1 logical, distance 3
    - Corrects any single X, Z, or Y error
    - X and Z errors corrected independently (CSS property!)
    - X-syndrome from Z-stabilizers identifies X error location
    - Z-syndrome from X-stabilizers identifies Z error location
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, SparsePauliOp, Pauli


# =============================================================================
# HAMMING PARITY CHECK MATRIX
# =============================================================================

# Classical Hamming [7,4,3] parity check matrix
H_MATRIX = np.array([
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
], dtype=int)

# Positions where each row has 1s
ROW_POSITIONS = {
    0: [0, 2, 4, 6],  # Row 1
    1: [1, 2, 5, 6],  # Row 2
    2: [3, 4, 5, 6],  # Row 3
}


# =============================================================================
# STABILIZER CONSTRUCTION
# =============================================================================

def build_steane_stabilizers():
    """
    Build the 6 stabilizer generators of the Steane code.

    From the Hamming parity check matrix H:
        X-stabilizers: X on positions in each row of H
        Z-stabilizers: Z on positions in each row of H

    Returns dict of SparsePauliOp objects.
    """
    stabilizers = {}

    for row_idx in range(3):
        positions = ROW_POSITIONS[row_idx]

        # X-stabilizer: Pauli string with X at specified positions
        x_label = ['I'] * 7
        for pos in positions:
            x_label[6 - pos] = 'X'  # Qiskit uses reverse ordering
        stabilizers[f'Sx{row_idx+1}'] = SparsePauliOp.from_list(
            [(''.join(x_label), 1.0)])

        # Z-stabilizer: Pauli string with Z at specified positions
        z_label = ['I'] * 7
        for pos in positions:
            z_label[6 - pos] = 'Z'
        stabilizers[f'Sz{row_idx+1}'] = SparsePauliOp.from_list(
            [(''.join(z_label), 1.0)])

    return stabilizers


def build_logical_operators():
    """
    Build logical X and Z operators for the Steane code.

    Logical X = X on all 7 qubits (X_L = X^7)
    Logical Z = Z on all 7 qubits (Z_L = Z^7)
    """
    x_logical = SparsePauliOp.from_list([('XXXXXXX', 1.0)])
    z_logical = SparsePauliOp.from_list([('ZZZZZZZ', 1.0)])
    return x_logical, z_logical


# =============================================================================
# ENCODING CIRCUIT
# =============================================================================

def build_steane_encoding_circuit():
    """
    Build the Steane code encoding circuit.

    Encoding circuit for |0_L>:
        1. Prepare ancilla qubits in |+> using Hadamard
        2. Apply CNOTs according to parity check matrix
        3. Result: |0_L> = equal superposition of all codewords

    The encoding maps:
        |0> -> |0_L> = (1/sqrt(8)) * sum of all even-weight codewords
        |1> -> |1_L> = (1/sqrt(8)) * sum of all odd-weight codewords
    """
    data = QuantumRegister(7, 'q')
    qc = QuantumCircuit(data, name='steane_encode')

    # Prepare |+> on parity qubits (q0, q1, q3 are parity positions)
    # In Hamming code, positions 1,2,4 (0-indexed: 0,1,3) are parity bits
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[3])

    # Apply CNOT gates based on parity check matrix
    # Row 0 (parity bit q0): q0 controls q2, q4, q6
    qc.cx(data[0], data[2])
    qc.cx(data[0], data[4])
    qc.cx(data[0], data[6])

    # Row 1 (parity bit q1): q1 controls q2, q5, q6
    qc.cx(data[1], data[2])
    qc.cx(data[1], data[5])
    qc.cx(data[1], data[6])

    # Row 2 (parity bit q3): q3 controls q4, q5, q6
    qc.cx(data[3], data[4])
    qc.cx(data[3], data[5])
    qc.cx(data[3], data[6])

    return qc


# =============================================================================
# SYNDROME MEASUREMENT
# =============================================================================

def build_x_syndrome_circuit():
    """
    Build X-error syndrome measurement using Z-stabilizers.

    Z-stabilizers detect X errors:
        Sz1 = Z0Z2Z4Z6 -> syndrome bit s0
        Sz2 = Z1Z2Z5Z6 -> syndrome bit s1
        Sz3 = Z3Z4Z5Z6 -> syndrome bit s2

    The 3-bit syndrome gives the binary representation of the
    error position (Hamming syndrome property).
    """
    data = QuantumRegister(7, 'q')
    anc = QuantumRegister(3, 'xsyn')
    cbits = ClassicalRegister(3, 'x_meas')
    qc = QuantumCircuit(data, anc, cbits, name='x_syndrome')

    # Sz1 = Z0Z2Z4Z6
    for pos in ROW_POSITIONS[0]:
        qc.cx(data[pos], anc[0])

    # Sz2 = Z1Z2Z5Z6
    for pos in ROW_POSITIONS[1]:
        qc.cx(data[pos], anc[1])

    # Sz3 = Z3Z4Z5Z6
    for pos in ROW_POSITIONS[2]:
        qc.cx(data[pos], anc[2])

    for i in range(3):
        qc.measure(anc[i], cbits[i])

    return qc


def build_z_syndrome_circuit():
    """
    Build Z-error syndrome measurement using X-stabilizers.

    X-stabilizers detect Z errors:
        Sx1 = X0X2X4X6 -> syndrome bit s0
        Sx2 = X1X2X5X6 -> syndrome bit s1
        Sx3 = X3X4X5X6 -> syndrome bit s2

    Use H-CNOT-H pattern to measure X-stabilizers.
    """
    data = QuantumRegister(7, 'q')
    anc = QuantumRegister(3, 'zsyn')
    cbits = ClassicalRegister(3, 'z_meas')
    qc = QuantumCircuit(data, anc, cbits, name='z_syndrome')

    # Prepare ancillas in |+>
    for i in range(3):
        qc.h(anc[i])

    # Sx1 = X0X2X4X6: ancilla[0] controls X on data qubits
    for pos in ROW_POSITIONS[0]:
        qc.cx(anc[0], data[pos])

    # Sx2 = X1X2X5X6
    for pos in ROW_POSITIONS[1]:
        qc.cx(anc[1], data[pos])

    # Sx3 = X3X4X5X6
    for pos in ROW_POSITIONS[2]:
        qc.cx(anc[2], data[pos])

    # Hadamard back on ancillas
    for i in range(3):
        qc.h(anc[i])

    for i in range(3):
        qc.measure(anc[i], cbits[i])

    return qc


def decode_syndrome(syndrome_bits):
    """
    Decode a 3-bit Hamming syndrome to find error position.

    The syndrome is the binary representation of the error position + 1:
        000 -> no error
        001 -> error on qubit 0 (position 1 in 1-indexed)
        010 -> error on qubit 1 (position 2)
        011 -> error on qubit 2 (position 3)
        100 -> error on qubit 3 (position 4)
        101 -> error on qubit 4 (position 5)
        110 -> error on qubit 5 (position 6)
        111 -> error on qubit 6 (position 7)
    """
    s = syndrome_bits[0] + 2 * syndrome_bits[1] + 4 * syndrome_bits[2]
    if s == 0:
        return None
    return s - 1  # Convert from 1-indexed to 0-indexed


# =============================================================================
# STATEVECTOR VERIFICATION
# =============================================================================

def verify_steane_encoding():
    """Verify encoding using Statevector."""
    # Encode |0>
    qc0 = QuantumCircuit(7)
    enc = build_steane_encoding_circuit()
    qc0 = qc0.compose(enc)
    sv0 = Statevector(qc0)

    # Encode |1> (apply X on logical qubit before encoding)
    qc1 = QuantumCircuit(7)
    qc1.x(6)  # Logical info on qubit 6 (data bit)
    qc1 = qc1.compose(enc)
    sv1 = Statevector(qc1)

    return sv0, sv1


def verify_error_correction(error_type, qubit_idx):
    """
    Verify single-qubit error correction with Statevector.

    CSS property: X and Z errors are corrected independently.
    """
    qc = QuantumCircuit(7)
    enc = build_steane_encoding_circuit()
    qc = qc.compose(enc)
    sv_encoded = Statevector(qc)

    # Inject error
    if error_type == 'X':
        qc.x(qubit_idx)
    elif error_type == 'Z':
        qc.z(qubit_idx)
    elif error_type == 'Y':
        qc.y(qubit_idx)

    sv_after_error = Statevector(qc)

    # Correct (apply same error again = identity for Pauli)
    if error_type == 'X':
        qc.x(qubit_idx)
    elif error_type == 'Z':
        qc.z(qubit_idx)
    elif error_type == 'Y':
        qc.y(qubit_idx)

    sv_corrected = Statevector(qc)

    # Check fidelity with original encoded state
    fidelity = abs(sv_corrected.inner(sv_encoded)) ** 2
    return fidelity


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_stabilizers():
    """Display stabilizer generators."""
    print("\n" + "=" * 70)
    print("PART A: Steane Code Stabilizers")
    print("=" * 70)

    stabilizers = build_steane_stabilizers()

    print("\n  Hamming parity check matrix H:")
    for i, row in enumerate(H_MATRIX):
        print(f"    Row {i}: {row}")

    print("\n  X-stabilizers (detect Z errors):")
    for i in range(3):
        name = f"Sx{i+1}"
        positions = ROW_POSITIONS[i]
        print(f"    {name} = X on qubits {positions}: {stabilizers[name]}")

    print("\n  Z-stabilizers (detect X errors):")
    for i in range(3):
        name = f"Sz{i+1}"
        positions = ROW_POSITIONS[i]
        print(f"    {name} = Z on qubits {positions}: {stabilizers[name]}")

    x_l, z_l = build_logical_operators()
    print(f"\n  Logical X: {x_l}")
    print(f"  Logical Z: {z_l}")


def demo_encoding():
    """Verify encoding produces correct codewords."""
    print("\n" + "=" * 70)
    print("PART B: Encoding Verification")
    print("=" * 70)

    sv0, sv1 = verify_steane_encoding()

    n_nonzero_0 = len([a for a in sv0.data if abs(a) > 1e-10])
    n_nonzero_1 = len([a for a in sv1.data if abs(a) > 1e-10])

    print(f"\n  |0_L>: {n_nonzero_0} nonzero amplitudes (expected 8)")
    print(f"  |1_L>: {n_nonzero_1} nonzero amplitudes (expected 8)")

    # List nonzero basis states
    for label, sv in [("0_L", sv0), ("1_L", sv1)]:
        print(f"\n  |{label}> basis states:")
        for i, a in enumerate(sv.data):
            if abs(a) > 1e-10:
                bits = format(i, '07b')
                weight = bits.count('1')
                print(f"    |{bits}> (weight {weight}): "
                      f"amplitude = {a.real:+.6f}")

    overlap = abs(sv0.inner(sv1)) ** 2
    print(f"\n  <0_L|1_L> = {overlap:.10f} (should be 0)")


def demo_independent_correction():
    """
    Demonstrate CSS property: X and Z errors corrected independently.

    This is the key advantage of CSS codes:
        - Z-stabilizers detect X errors -> X-syndrome
        - X-stabilizers detect Z errors -> Z-syndrome
        - The two syndromes are computed independently
    """
    print("\n" + "=" * 70)
    print("PART C: Independent X and Z Error Correction (CSS Property)")
    print("=" * 70)

    sim = AerSimulator()

    # Test X errors detected by Z-stabilizers
    print("\n  X errors (detected by Z-stabilizers):")
    for q in range(7):
        data = QuantumRegister(7, 'q')
        anc = QuantumRegister(3, 'syn')
        cbits = ClassicalRegister(3, 'meas')
        qc = QuantumCircuit(data, anc, cbits)

        # Encode
        enc = build_steane_encoding_circuit()
        qc = qc.compose(enc, qubits=range(7))

        # X error
        qc.x(data[q])

        # Z-syndrome
        for row in range(3):
            for pos in ROW_POSITIONS[row]:
                qc.cx(data[pos], anc[row])
        for i in range(3):
            qc.measure(anc[i], cbits[i])

        counts = sim.run(qc, shots=1024).result().get_counts()
        syndrome = max(counts, key=counts.get)
        s_bits = [int(b) for b in reversed(syndrome)]
        decoded_pos = decode_syndrome(s_bits)
        status = "CORRECT" if decoded_pos == q else "WRONG"
        print(f"    X on q{q}: syndrome={syndrome}, "
              f"decoded=q{decoded_pos} [{status}]")

    # Test Z errors detected by X-stabilizers
    print("\n  Z errors (detected by X-stabilizers):")
    for q in range(7):
        data = QuantumRegister(7, 'q')
        anc = QuantumRegister(3, 'syn')
        cbits = ClassicalRegister(3, 'meas')
        qc = QuantumCircuit(data, anc, cbits)

        enc = build_steane_encoding_circuit()
        qc = qc.compose(enc, qubits=range(7))

        # Z error
        qc.z(data[q])

        # X-syndrome: H-CNOT-H pattern
        for i in range(3):
            qc.h(anc[i])
        for row in range(3):
            for pos in ROW_POSITIONS[row]:
                qc.cx(anc[row], data[pos])
        for i in range(3):
            qc.h(anc[i])
        for i in range(3):
            qc.measure(anc[i], cbits[i])

        counts = sim.run(qc, shots=1024).result().get_counts()
        syndrome = max(counts, key=counts.get)
        s_bits = [int(b) for b in reversed(syndrome)]
        decoded_pos = decode_syndrome(s_bits)
        status = "CORRECT" if decoded_pos == q else "WRONG"
        print(f"    Z on q{q}: syndrome={syndrome}, "
              f"decoded=q{decoded_pos} [{status}]")


def demo_all_errors():
    """Verify all single-qubit errors are correctable."""
    print("\n" + "=" * 70)
    print("PART D: Complete Error Correction Verification")
    print("=" * 70)

    results = {}
    for etype in ['X', 'Y', 'Z']:
        print(f"\n  {etype} errors:")
        for q in range(7):
            fidelity = verify_error_correction(etype, q)
            status = "CORRECTED" if fidelity > 0.99 else "FAILED"
            print(f"    {etype} on q{q}: fidelity = {fidelity:.6f} [{status}]")
            results[(etype, q)] = fidelity

    correctable = sum(1 for f in results.values() if f > 0.99)
    print(f"\n  Total correctable: {correctable}/21 single-qubit errors")

    return results


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(results):
    """Plot error correction results for the Steane code."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Fidelity heatmap
    ax = axes[0]
    error_types = ['X', 'Y', 'Z']
    data_matrix = np.zeros((3, 7))
    for i, etype in enumerate(error_types):
        for q in range(7):
            data_matrix[i, q] = results.get((etype, q), 0)

    im = ax.imshow(data_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(7))
    ax.set_xticklabels([f'q{i}' for i in range(7)])
    ax.set_yticks(range(3))
    ax.set_yticklabels(error_types)
    ax.set_xlabel('Qubit', fontsize=12)
    ax.set_ylabel('Error Type', fontsize=12)
    ax.set_title('Steane Code: Correction Fidelity', fontsize=13)
    for i in range(3):
        for j in range(7):
            val = data_matrix[i, j]
            ax.text(j, i, f'{val:.3f}', ha='center', va='center',
                    fontsize=9)
    plt.colorbar(im, ax=ax, label='Fidelity')

    # Stabilizer structure
    ax = axes[1]
    # Visualize which qubits each stabilizer acts on
    stab_matrix = np.zeros((6, 7))
    for row in range(3):
        for pos in ROW_POSITIONS[row]:
            stab_matrix[row, pos] = 1      # X-stabilizers
            stab_matrix[row + 3, pos] = 1  # Z-stabilizers

    im2 = ax.imshow(stab_matrix, cmap='Blues', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(7))
    ax.set_xticklabels([f'q{i}' for i in range(7)])
    ax.set_yticks(range(6))
    ax.set_yticklabels(['Sx1', 'Sx2', 'Sx3', 'Sz1', 'Sz2', 'Sz3'])
    ax.set_xlabel('Qubit', fontsize=12)
    ax.set_title('Steane Code: Stabilizer Structure', fontsize=13)
    ax.axhline(y=2.5, color='red', linewidth=2, linestyle='--')
    ax.text(7.5, 1, 'X-type', fontsize=10, va='center', color='blue')
    ax.text(7.5, 4, 'Z-type', fontsize=10, va='center', color='blue')

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/04_steane_code/steane_code_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("[[7,1,3]] Steane Code - Local Simulator")
    print("=" * 70)

    demo_stabilizers()
    demo_encoding()
    demo_independent_correction()
    results = demo_all_errors()
    plot_results(results)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    [[7,1,3]] Steane Code:
    - Encodes 1 logical qubit into 7 physical qubits
    - Based on classical Hamming [7,4,3] code
    - 6 stabilizer generators: 3 X-type + 3 Z-type
    - CSS code: X and Z errors corrected INDEPENDENTLY
    - Distance 3: corrects any single-qubit error

    Key advantage over Shor code:
    - Only 7 qubits (vs 9 for Shor)
    - CSS structure enables transversal CNOT gate
    - Syndrome is standard Hamming decoding

    CSS property: H1 * H2^T = 0 (self-dual code, H1 = H2 = H)
    Next: General CSS code construction.
    """)


if __name__ == "__main__":
    main()
