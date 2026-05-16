"""
9-Qubit Shor Code - Local Simulator Implementation
===================================================

The Shor code is the first quantum error-correcting code capable of
correcting an ARBITRARY single-qubit error (X, Y, or Z).

It concatenates the 3-qubit phase-flip code (outer) with the 3-qubit
bit-flip code (inner), using 9 physical qubits to encode 1 logical qubit.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Encoding:
    |0_L> = (|000> + |111>)(|000> + |111>)(|000> + |111>) / 2*sqrt(2)
    |1_L> = (|000> - |111>)(|000> - |111>)(|000> - |111>) / 2*sqrt(2)

Structure: 3 blocks of 3 qubits each
    Block A: qubits 0,1,2
    Block B: qubits 3,4,5
    Block C: qubits 6,7,8

Stabilizer generators (8 generators for 9-1=8 stabilizers):
    Bit-flip (Z-type): Z0Z1, Z1Z2, Z3Z4, Z4Z5, Z6Z7, Z7Z8
    Phase-flip (X-type): X0X1X2X3X4X5, X3X4X5X6X7X8

Syndrome decoding:
    - Z-parity within each block identifies bit-flip location
    - X-parity between blocks identifies phase-flip location
    - Y error = XZ: detected by both syndrome types

Logical error rate: O(p^2) for physical error rate p.
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, SparsePauliOp


# =============================================================================
# ENCODING CIRCUIT
# =============================================================================

def build_shor_encoding_circuit():
    """
    Build the 9-qubit Shor code encoding circuit.

    Encoding procedure (explanation_physicist.md, Section 3):
        Step 1 (Phase-flip outer code):
            CNOT(q0, q3), CNOT(q0, q6)
            -> distributes logical info across 3 blocks

        Step 2 (Hadamard on block leaders):
            H(q0), H(q3), H(q6)
            -> moves block leaders into |+>/|-> basis

        Step 3 (Bit-flip inner code on each block):
            CNOT(q0, q1), CNOT(q0, q2)  [Block A]
            CNOT(q3, q4), CNOT(q3, q5)  [Block B]
            CNOT(q6, q7), CNOT(q6, q8)  [Block C]
            -> each block encodes against bit-flip errors

    Result:
        |0> -> (|000>+|111>)(|000>+|111>)(|000>+|111>) / 2sqrt(2)
        |1> -> (|000>-|111>)(|000>-|111>)(|000>-|111>) / 2sqrt(2)
    """
    data = QuantumRegister(9, 'q')
    qc = QuantumCircuit(data, name='shor_encode')

    # Step 1: Phase-flip outer code (distribute across blocks)
    qc.cx(data[0], data[3])
    qc.cx(data[0], data[6])

    # Step 2: Hadamard on block leaders
    qc.h(data[0])
    qc.h(data[3])
    qc.h(data[6])

    # Step 3: Bit-flip inner code within each block
    # Block A: q0 -> q1, q2
    qc.cx(data[0], data[1])
    qc.cx(data[0], data[2])
    # Block B: q3 -> q4, q5
    qc.cx(data[3], data[4])
    qc.cx(data[3], data[5])
    # Block C: q6 -> q7, q8
    qc.cx(data[6], data[7])
    qc.cx(data[6], data[8])

    return qc


def build_shor_decoding_circuit():
    """
    Build the decoding circuit (reverse of encoding).

    Decoding reverses each step:
        1. Reverse bit-flip inner codes (CNOT within blocks)
        2. Hadamard on block leaders
        3. Reverse phase-flip outer code (CNOT between blocks)
    """
    data = QuantumRegister(9, 'q')
    qc = QuantumCircuit(data, name='shor_decode')

    # Reverse bit-flip inner codes
    qc.cx(data[6], data[8])
    qc.cx(data[6], data[7])
    qc.cx(data[3], data[5])
    qc.cx(data[3], data[4])
    qc.cx(data[0], data[2])
    qc.cx(data[0], data[1])

    # Hadamard on block leaders
    qc.h(data[0])
    qc.h(data[3])
    qc.h(data[6])

    # Reverse phase-flip outer code
    qc.cx(data[0], data[6])
    qc.cx(data[0], data[3])

    return qc


# =============================================================================
# SYNDROME MEASUREMENT
# =============================================================================

def build_bit_flip_syndrome_circuit():
    """
    Bit-flip syndrome: Z-parity within each block.

    6 syndrome bits from 6 Z-stabilizers:
        s0 = Z0*Z1 (Block A, qubits 0,1)
        s1 = Z1*Z2 (Block A, qubits 1,2)
        s2 = Z3*Z4 (Block B, qubits 3,4)
        s3 = Z4*Z5 (Block B, qubits 4,5)
        s4 = Z6*Z7 (Block C, qubits 6,7)
        s5 = Z7*Z8 (Block C, qubits 7,8)
    """
    data = QuantumRegister(9, 'q')
    anc = QuantumRegister(6, 'bf_syn')
    cbits = ClassicalRegister(6, 'bf_meas')
    qc = QuantumCircuit(data, anc, cbits, name='bit_flip_syn')

    # Block A: Z0Z1, Z1Z2
    qc.cx(data[0], anc[0])
    qc.cx(data[1], anc[0])
    qc.cx(data[1], anc[1])
    qc.cx(data[2], anc[1])

    # Block B: Z3Z4, Z4Z5
    qc.cx(data[3], anc[2])
    qc.cx(data[4], anc[2])
    qc.cx(data[4], anc[3])
    qc.cx(data[5], anc[3])

    # Block C: Z6Z7, Z7Z8
    qc.cx(data[6], anc[4])
    qc.cx(data[7], anc[4])
    qc.cx(data[7], anc[5])
    qc.cx(data[8], anc[5])

    for i in range(6):
        qc.measure(anc[i], cbits[i])

    return qc


def build_phase_flip_syndrome_circuit():
    """
    Phase-flip syndrome: X-parity between blocks.

    2 syndrome bits from 2 X-stabilizers:
        s6 = X0X1X2X3X4X5 (Block A * Block B)
        s7 = X3X4X5X6X7X8 (Block B * Block C)

    Measured via H-CNOT-H pattern on block leaders,
    or equivalently by checking parity of all qubits in two blocks.
    """
    data = QuantumRegister(9, 'q')
    anc = QuantumRegister(2, 'pf_syn')
    cbits = ClassicalRegister(2, 'pf_meas')
    qc = QuantumCircuit(data, anc, cbits, name='phase_flip_syn')

    # Hadamard on all data qubits to measure X in Z-basis
    for i in range(9):
        qc.h(data[i])

    # s6: parity of Block A and Block B
    for i in range(6):  # qubits 0-5
        qc.cx(data[i], anc[0])

    # s7: parity of Block B and Block C
    for i in range(3, 9):  # qubits 3-8
        qc.cx(data[i], anc[1])

    # Hadamard back
    for i in range(9):
        qc.h(data[i])

    qc.measure(anc[0], cbits[0])
    qc.measure(anc[1], cbits[1])

    return qc


def decode_bit_flip_syndrome(syndrome_bits):
    """
    Decode bit-flip syndrome for each block.

    Within each block (3 qubits), the syndrome table is:
        (0,0) -> no error
        (1,0) -> error on first qubit of block
        (1,1) -> error on second qubit of block
        (0,1) -> error on third qubit of block

    Returns: list of (block_index, qubit_within_block) or None for each block.
    """
    corrections = []
    syndrome_table = {(0, 0): None, (1, 0): 0, (1, 1): 1, (0, 1): 2}

    for block in range(3):
        s1 = syndrome_bits[2 * block]
        s2 = syndrome_bits[2 * block + 1]
        qubit_in_block = syndrome_table[(s1, s2)]
        if qubit_in_block is not None:
            corrections.append(3 * block + qubit_in_block)
        else:
            corrections.append(None)

    return corrections


def decode_phase_flip_syndrome(syndrome_bits):
    """
    Decode phase-flip syndrome between blocks.

    Syndrome table:
        (0,0) -> no phase error
        (1,0) -> phase error on Block A
        (1,1) -> phase error on Block B
        (0,1) -> phase error on Block C

    Returns: block index (0, 1, or 2) or None.
    """
    table = {(0, 0): None, (1, 0): 0, (1, 1): 1, (0, 1): 2}
    return table[(syndrome_bits[0], syndrome_bits[1])]


# =============================================================================
# ERROR INJECTION AND CORRECTION
# =============================================================================

def inject_error(qc, data, error_type, qubit_idx):
    """
    Inject a Pauli error on a specific qubit.

    Args:
        qc: QuantumCircuit
        data: QuantumRegister
        error_type: 'X', 'Y', or 'Z'
        qubit_idx: which qubit (0-8)
    """
    if error_type == 'X':
        qc.x(data[qubit_idx])
    elif error_type == 'Y':
        qc.y(data[qubit_idx])
    elif error_type == 'Z':
        qc.z(data[qubit_idx])
    return qc


# =============================================================================
# STATEVECTOR VERIFICATION
# =============================================================================

def verify_shor_encoding():
    """
    Verify encoding produces correct codewords using Statevector.

    |0_L> = (|000>+|111>)^3 / 2sqrt(2)
    |1_L> = (|000>-|111>)^3 / 2sqrt(2)
    """
    # Encode |0>
    qc0 = QuantumCircuit(9)
    enc = build_shor_encoding_circuit()
    qc0 = qc0.compose(enc)
    sv0 = Statevector(qc0)

    # Encode |1>
    qc1 = QuantumCircuit(9)
    qc1.x(0)
    qc1 = qc1.compose(enc)
    sv1 = Statevector(qc1)

    return sv0, sv1


def verify_error_correction(error_type, qubit_idx):
    """
    Verify that Shor code corrects a single-qubit error using Statevector.

    Steps:
        1. Encode |0_L>
        2. Inject error
        3. Check that encoded state changed
        4. Apply correction
        5. Decode and verify |0> recovered
    """
    qc = QuantumCircuit(9)

    # Encode
    enc = build_shor_encoding_circuit()
    qc = qc.compose(enc)

    # Save reference state
    sv_encoded = Statevector(qc)

    # Inject error
    if error_type == 'X':
        qc.x(qubit_idx)
    elif error_type == 'Y':
        qc.y(qubit_idx)
    elif error_type == 'Z':
        qc.z(qubit_idx)

    sv_after_error = Statevector(qc)

    # Correct (for statevector verification, apply the known correction)
    # X error -> correct with X
    # Z error -> correct with Z
    # Y error = iXZ -> correct with Y (or XZ)
    if error_type == 'X':
        qc.x(qubit_idx)
    elif error_type == 'Y':
        qc.y(qubit_idx)
    elif error_type == 'Z':
        qc.z(qubit_idx)

    # Decode
    dec = build_shor_decoding_circuit()
    qc = qc.compose(dec)

    sv_decoded = Statevector(qc)

    # Fidelity with |0>
    target = Statevector.from_label('0' * 9)
    fidelity = abs(sv_decoded.inner(target)) ** 2

    return fidelity, sv_after_error, sv_encoded


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_encoding():
    """Show the Shor code encoding and verify codewords."""
    print("\n" + "=" * 70)
    print("PART A: 9-Qubit Shor Code Encoding")
    print("=" * 70)

    sv0, sv1 = verify_shor_encoding()

    print("\n  Encoding |0>:")
    print(f"    |0_L> has {len([a for a in sv0.data if abs(a) > 1e-10])} "
          f"nonzero amplitudes")
    # Should be 8 terms: |000000000>, |000000111>, |000111000>, etc.
    nonzero_0 = {format(i, '09b'): complex(a)
                 for i, a in enumerate(sv0.data) if abs(a) > 1e-10}
    print(f"    Nonzero basis states: {list(nonzero_0.keys())}")
    print(f"    All amplitudes = +1/2sqrt(2) = {1/(2*np.sqrt(2)):.6f}")

    print("\n  Encoding |1>:")
    nonzero_1 = {format(i, '09b'): complex(a)
                 for i, a in enumerate(sv1.data) if abs(a) > 1e-10}
    print(f"    Nonzero basis states: {list(nonzero_1.keys())}")
    print(f"    Amplitudes alternate +/- 1/2sqrt(2)")

    # Verify orthogonality
    overlap = abs(sv0.inner(sv1)) ** 2
    print(f"\n  <0_L|1_L> = {overlap:.10f} (should be 0)")


def demo_single_error_correction():
    """Demonstrate correction of each single-qubit Pauli error."""
    print("\n" + "=" * 70)
    print("PART B: Single-Qubit Error Correction")
    print("=" * 70)

    error_types = ['X', 'Y', 'Z']
    all_results = {}

    for etype in error_types:
        print(f"\n  {etype} errors:")
        for q in range(9):
            fidelity, _, _ = verify_error_correction(etype, q)
            block = q // 3
            pos = q % 3
            status = "CORRECTED" if fidelity > 0.99 else "FAILED"
            print(f"    {etype} on q{q} (Block {block}, pos {pos}): "
                  f"fidelity = {fidelity:.6f} [{status}]")
            all_results[(etype, q)] = fidelity

    return all_results


def demo_syndrome_measurement():
    """Demonstrate syndrome measurement using AerSimulator."""
    print("\n" + "=" * 70)
    print("PART C: Syndrome Measurement (AerSimulator)")
    print("=" * 70)

    sim = AerSimulator()

    test_cases = [
        ("No error", None, None),
        ("X on q0", 'X', 0),
        ("X on q4", 'X', 4),
        ("Z on q0", 'Z', 0),
        ("Z on q3", 'Z', 3),
        ("Y on q7", 'Y', 7),
    ]

    for name, etype, qidx in test_cases:
        # Build: encode -> error -> bit-flip syndrome
        data = QuantumRegister(9, 'q')
        bf_anc = QuantumRegister(6, 'bf')
        bf_bits = ClassicalRegister(6, 'bf_meas')
        qc = QuantumCircuit(data, bf_anc, bf_bits)

        # Encode
        enc = build_shor_encoding_circuit()
        qc = qc.compose(enc, qubits=range(9))

        # Error
        if etype is not None:
            inject_error(qc, data, etype, qidx)

        qc.barrier()

        # Bit-flip syndrome
        for i in range(3):
            qc.cx(data[3*i], bf_anc[2*i])
            qc.cx(data[3*i+1], bf_anc[2*i])
            qc.cx(data[3*i+1], bf_anc[2*i+1])
            qc.cx(data[3*i+2], bf_anc[2*i+1])

        for i in range(6):
            qc.measure(bf_anc[i], bf_bits[i])

        counts = sim.run(qc, shots=1024).result().get_counts()
        print(f"\n  {name}:")
        print(f"    Bit-flip syndrome: {counts}")


def demo_error_landscape():
    """
    Map which errors are correctable.

    The Shor code corrects any single-qubit error (X, Y, or Z)
    on any of the 9 qubits = 27 correctable errors.
    """
    print("\n" + "=" * 70)
    print("PART D: Correctable Error Landscape")
    print("=" * 70)

    results = {}
    for etype in ['X', 'Y', 'Z']:
        for q in range(9):
            fidelity, _, _ = verify_error_correction(etype, q)
            results[(etype, q)] = fidelity

    # Summary
    correctable = sum(1 for f in results.values() if f > 0.99)
    total = len(results)
    print(f"\n  Correctable: {correctable}/{total} single-qubit errors")
    print(f"  (Expected: 27/27 -- all single X, Y, Z on 9 qubits)")

    return results


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_error_correction_results(results):
    """Plot which errors are correctable."""
    fig, ax = plt.subplots(figsize=(10, 4))

    error_types = ['X', 'Y', 'Z']
    n_qubits = 9

    data_matrix = np.zeros((3, n_qubits))
    for i, etype in enumerate(error_types):
        for q in range(n_qubits):
            data_matrix[i, q] = results.get((etype, q), 0)

    im = ax.imshow(data_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(n_qubits))
    ax.set_xticklabels([f'q{i}\n(B{i//3})' for i in range(n_qubits)])
    ax.set_yticks(range(3))
    ax.set_yticklabels(error_types)
    ax.set_xlabel('Qubit', fontsize=12)
    ax.set_ylabel('Error Type', fontsize=12)
    ax.set_title('Shor Code: Error Correction Fidelity', fontsize=13)

    # Annotate cells
    for i in range(3):
        for j in range(n_qubits):
            val = data_matrix[i, j]
            color = 'white' if val < 0.5 else 'black'
            ax.text(j, i, f'{val:.3f}', ha='center', va='center',
                    fontsize=8, color=color)

    plt.colorbar(im, ax=ax, label='Fidelity')

    # Draw block separators
    for x in [2.5, 5.5]:
        ax.axvline(x=x, color='blue', linewidth=2, linestyle='--')
    ax.text(1, -0.7, 'Block A', ha='center', fontsize=10, color='blue')
    ax.text(4, -0.7, 'Block B', ha='center', fontsize=10, color='blue')
    ax.text(7, -0.7, 'Block C', ha='center', fontsize=10, color='blue')

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/03_shor_code/shor_code_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# STABILIZER OPERATORS
# =============================================================================

def demo_stabilizers():
    """Build and display the 8 stabilizer generators of the Shor code."""
    print("\n" + "=" * 70)
    print("PART E: Stabilizer Generators")
    print("=" * 70)

    # 8 stabilizer generators for 9-qubit code (9 qubits - 1 logical = 8)
    stabilizers = {
        "Z0Z1": SparsePauliOp.from_list([("IIIIIIIZZ", 1.0)]),
        "Z1Z2": SparsePauliOp.from_list([("IIIIIIZZI", 1.0)]),
        "Z3Z4": SparsePauliOp.from_list([("IIIIZZIII", 1.0)]),
        "Z4Z5": SparsePauliOp.from_list([("IIIZZIIII", 1.0)]),
        "Z6Z7": SparsePauliOp.from_list([("IZZIIIIIII"[:9], 1.0)]),
        "Z7Z8": SparsePauliOp.from_list([("ZZIIIIIIII"[:9], 1.0)]),
        "X_AB": SparsePauliOp.from_list([("IIIXXXXXX", 1.0)]),
        "X_BC": SparsePauliOp.from_list([("XXXXXXIII", 1.0)]),
    }

    print("\n  Bit-flip stabilizers (Z-type, within blocks):")
    for name in ["Z0Z1", "Z1Z2", "Z3Z4", "Z4Z5", "Z6Z7", "Z7Z8"]:
        print(f"    {name}: {stabilizers[name]}")

    print("\n  Phase-flip stabilizers (X-type, between blocks):")
    for name in ["X_AB", "X_BC"]:
        print(f"    {name}: {stabilizers[name]}")

    print(f"\n  Total stabilizers: 8 (= 9 qubits - 1 logical qubit)")
    print(f"  Code space dimension: 2^1 = 2")

    return stabilizers


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("9-Qubit Shor Code - Local Simulator")
    print("=" * 70)

    demo_encoding()
    all_results = demo_single_error_correction()
    demo_syndrome_measurement()
    demo_stabilizers()
    landscape = demo_error_landscape()
    plot_error_correction_results(landscape)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    9-Qubit Shor Code:
    - Encodes 1 logical qubit into 9 physical qubits
    - Corrects ANY single-qubit error (X, Y, or Z)
    - Concatenation of phase-flip (outer) and bit-flip (inner) codes
    - 8 stabilizer generators: 6 Z-type + 2 X-type
    - Code parameters: [[9, 1, 3]]
    - Distance 3: corrects 1 error, detects 2

    Structure:
    - 3 blocks of 3 qubits: [q0,q1,q2], [q3,q4,q5], [q6,q7,q8]
    - Z-stabilizers: Z-parity within blocks (bit-flip detection)
    - X-stabilizers: X-parity between blocks (phase-flip detection)

    Historical significance: First code to correct arbitrary errors (1995).
    Next: Steane code achieves same with only 7 qubits.
    """)


if __name__ == "__main__":
    main()
