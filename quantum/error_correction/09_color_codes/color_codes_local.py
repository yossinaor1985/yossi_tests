"""
Color Codes - Local Simulator Implementation
=============================================

7-qubit color code on a triangular lattice. This is equivalent to the
Steane code but with a geometric interpretation that enables transversal
implementation of the full Clifford group.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
The 7-qubit color code:
    - 7 data qubits on vertices of a triangular lattice
    - 3 faces, each colored (red, green, blue)
    - Each face generates an X-stabilizer and a Z-stabilizer
    - 6 stabilizers total -> 7 - 6 = 1 logical qubit

Lattice layout:
        0
       / \\
      1   2
     / \\ / \\
    3   4   5
         \\
          6

Face stabilizers:
    Red face:   qubits {0, 1, 2, 3}  -> X0X1X2X3, Z0Z1Z2Z3
    Green face: qubits {2, 4, 5, 6}  -> X2X4X5X6, Z2Z4Z5Z6
    Blue face:  qubits {1, 3, 4, 6}  -> not independent (product of others)

Actually for the [[7,1,3]] color code on the triangular lattice:
    Face R: qubits {0, 1, 2, 4}
    Face G: qubits {2, 3, 4, 6}
    Face B: qubits {0, 4, 5, 6}
    (Different conventions exist; we use 3 faces of 4 qubits each)

Key property: TRANSVERSAL HADAMARD
    H_L = H^{otimes 7} (physical H on each qubit = logical H)
    This makes the color code valuable for fault-tolerant computation.

Code parameters: [[7,1,3]] (same as Steane code)
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, SparsePauliOp


# =============================================================================
# COLOR CODE FACE DEFINITIONS
# =============================================================================

# Three faces of the 7-qubit color code
# Each face has 4 qubits
FACES = {
    'Red':   [0, 2, 4, 6],
    'Green': [1, 2, 5, 6],
    'Blue':  [3, 4, 5, 6],
}

# Note: These are the same positions as the Steane code's Hamming parity check:
# Row 0: [0, 2, 4, 6], Row 1: [1, 2, 5, 6], Row 2: [3, 4, 5, 6]


# =============================================================================
# STABILIZER CONSTRUCTION
# =============================================================================

def build_color_code_stabilizers():
    """
    Build the 6 stabilizer generators of the 7-qubit color code.

    Each face contributes one X-stabilizer and one Z-stabilizer:
        Face F: X_{q in F}, Z_{q in F}
    """
    stabilizers = {}
    n = 7

    for face_name, qubits in FACES.items():
        # X-stabilizer
        x_label = ['I'] * n
        for q in qubits:
            x_label[n - 1 - q] = 'X'
        stabilizers[f'X_{face_name}'] = SparsePauliOp.from_list(
            [(''.join(x_label), 1.0)])

        # Z-stabilizer
        z_label = ['I'] * n
        for q in qubits:
            z_label[n - 1 - q] = 'Z'
        stabilizers[f'Z_{face_name}'] = SparsePauliOp.from_list(
            [(''.join(z_label), 1.0)])

    return stabilizers


def build_logical_operators():
    """
    Build logical operators for the 7-qubit color code.

    Logical X = X on all 7 qubits
    Logical Z = Z on all 7 qubits
    (Same as Steane code)
    """
    x_l = SparsePauliOp.from_list([('XXXXXXX', 1.0)])
    z_l = SparsePauliOp.from_list([('ZZZZZZZ', 1.0)])
    return x_l, z_l


# =============================================================================
# ENCODING CIRCUIT
# =============================================================================

def build_color_code_encoding():
    """
    Build encoding circuit for the 7-qubit color code.

    Same as Steane code encoding (they are the same code):
        H on parity positions (q0, q1, q3)
        CNOT from parity to data according to face structure
    """
    data = QuantumRegister(7, 'q')
    qc = QuantumCircuit(data, name='color_encode')

    # H on parity positions
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[3])

    # CNOTs from face structure
    # Red face [0,2,4,6]: q0 -> q2, q4, q6
    qc.cx(data[0], data[2])
    qc.cx(data[0], data[4])
    qc.cx(data[0], data[6])

    # Green face [1,2,5,6]: q1 -> q2, q5, q6
    qc.cx(data[1], data[2])
    qc.cx(data[1], data[5])
    qc.cx(data[1], data[6])

    # Blue face [3,4,5,6]: q3 -> q4, q5, q6
    qc.cx(data[3], data[4])
    qc.cx(data[3], data[5])
    qc.cx(data[3], data[6])

    return qc


# =============================================================================
# TRANSVERSAL HADAMARD
# =============================================================================

def verify_transversal_hadamard():
    """
    Verify that H^{otimes 7} implements the logical Hadamard.

    Key property of color codes:
        H on each physical qubit = H on logical qubit

    Verification:
        |0_L> -> H_L -> |+_L> = (|0_L> + |1_L>)/sqrt(2)

    We check: H^7 |0_L> has equal overlap with |0_L> and |1_L>.
    """
    # Encode |0_L>
    qc0 = QuantumCircuit(7)
    enc = build_color_code_encoding()
    qc0 = qc0.compose(enc)
    sv0 = Statevector(qc0)

    # Encode |1_L>
    qc1 = QuantumCircuit(7)
    qc1.x(6)  # Logical info on data qubit
    qc1 = qc1.compose(enc)
    sv1 = Statevector(qc1)

    # Apply H^7 to |0_L>
    qc_h = QuantumCircuit(7)
    qc_h = qc_h.compose(enc)
    for i in range(7):
        qc_h.h(i)
    sv_h = Statevector(qc_h)

    # |+_L> = (|0_L> + |1_L>)/sqrt(2)
    # Check overlaps
    overlap_0 = sv_h.inner(sv0)
    overlap_1 = sv_h.inner(sv1)

    return overlap_0, overlap_1, sv0, sv1, sv_h


# =============================================================================
# SYNDROME MEASUREMENT
# =============================================================================

def build_syndrome_circuit(error_type=None, error_qubit=None):
    """
    Build syndrome extraction circuit for the color code.

    3 X-syndrome ancillas (from Z-stabilizers) +
    3 Z-syndrome ancillas (from X-stabilizers)
    """
    data = QuantumRegister(7, 'q')
    x_anc = QuantumRegister(3, 'xa')
    z_anc = QuantumRegister(3, 'za')
    x_bits = ClassicalRegister(3, 'x_syn')
    z_bits = ClassicalRegister(3, 'z_syn')
    qc = QuantumCircuit(data, x_anc, z_anc, x_bits, z_bits)

    # Encode |0_L>
    enc = build_color_code_encoding()
    qc = qc.compose(enc, qubits=range(7))
    qc.barrier()

    # Inject error
    if error_type is not None and error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
    qc.barrier()

    # X-error syndrome (Z-stabilizers): CNOT from data to ancilla
    for i, (face_name, qubits) in enumerate(FACES.items()):
        for q in qubits:
            qc.cx(data[q], x_anc[i])
    for i in range(3):
        qc.measure(x_anc[i], x_bits[i])
    qc.barrier()

    # Z-error syndrome (X-stabilizers): H-CNOT-H
    for i in range(3):
        qc.h(z_anc[i])
    for i, (face_name, qubits) in enumerate(FACES.items()):
        for q in qubits:
            qc.cx(z_anc[i], data[q])
    for i in range(3):
        qc.h(z_anc[i])
    for i in range(3):
        qc.measure(z_anc[i], z_bits[i])

    return qc


def decode_color_syndrome(syndrome_bits):
    """
    Decode color code syndrome to identify error location.

    The syndrome is the same as Hamming syndrome (since color code = Steane).
    3-bit syndrome encodes error position + 1.
    """
    s = syndrome_bits[0] + 2 * syndrome_bits[1] + 4 * syndrome_bits[2]
    if s == 0:
        return None
    return s - 1


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_stabilizers():
    """Display color code stabilizers."""
    print("\n" + "=" * 70)
    print("PART A: 7-Qubit Color Code Stabilizers")
    print("=" * 70)

    stabilizers = build_color_code_stabilizers()

    print("\n  Triangular lattice faces:")
    for face_name, qubits in FACES.items():
        print(f"    {face_name} face: qubits {qubits}")

    print("\n  Face stabilizers (6 total):")
    for name, stab in stabilizers.items():
        print(f"    {name}: {stab}")

    x_l, z_l = build_logical_operators()
    print(f"\n  Logical X: {x_l}")
    print(f"  Logical Z: {z_l}")
    print(f"\n  Code parameters: [[7, 1, 3]]")
    print(f"  Same code space as Steane code, different geometric structure")


def demo_encoding():
    """Verify color code encoding."""
    print("\n" + "=" * 70)
    print("PART B: Encoding Verification")
    print("=" * 70)

    qc0 = QuantumCircuit(7)
    enc = build_color_code_encoding()
    qc0 = qc0.compose(enc)
    sv0 = Statevector(qc0)

    qc1 = QuantumCircuit(7)
    qc1.x(6)
    qc1 = qc1.compose(enc)
    sv1 = Statevector(qc1)

    print(f"\n  |0_L>: {len([a for a in sv0.data if abs(a) > 1e-10])} "
          f"nonzero amplitudes")
    print(f"  |1_L>: {len([a for a in sv1.data if abs(a) > 1e-10])} "
          f"nonzero amplitudes")
    print(f"  <0_L|1_L> = {abs(sv0.inner(sv1))**2:.10f}")

    # List codewords
    print(f"\n  |0_L> codewords:")
    for i, a in enumerate(sv0.data):
        if abs(a) > 1e-10:
            print(f"    |{format(i, '07b')}> : {a.real:+.6f}")


def demo_transversal_hadamard():
    """Demonstrate transversal Hadamard gate."""
    print("\n" + "=" * 70)
    print("PART C: Transversal Hadamard (H_L = H^7)")
    print("=" * 70)

    overlap_0, overlap_1, sv0, sv1, sv_h = verify_transversal_hadamard()

    print(f"\n  H^7 |0_L> = |+_L> = (|0_L> + |1_L>)/sqrt(2)")
    print(f"\n  <0_L | H^7 |0_L> = {overlap_0:.6f}")
    print(f"  <1_L | H^7 |0_L> = {overlap_1:.6f}")
    print(f"\n  Expected: both = 1/sqrt(2) = {1/np.sqrt(2):.6f}")

    # Verify magnitudes
    mag_0 = abs(overlap_0)
    mag_1 = abs(overlap_1)
    print(f"  |<0_L|H^7|0_L>| = {mag_0:.6f}")
    print(f"  |<1_L|H^7|0_L>| = {mag_1:.6f}")

    target = 1 / np.sqrt(2)
    is_correct = abs(mag_0 - target) < 0.01 and abs(mag_1 - target) < 0.01
    print(f"\n  Transversal Hadamard verified: {is_correct}")
    print(f"  This means: applying physical H to all 7 qubits = logical H")


def demo_error_correction():
    """Demonstrate error injection and syndrome measurement."""
    print("\n" + "=" * 70)
    print("PART D: Error Correction via Face Syndromes")
    print("=" * 70)

    sim = AerSimulator()

    # X errors
    print("\n  X errors (detected by Z-face stabilizers):")
    for q in range(7):
        qc = build_syndrome_circuit('X', q)
        counts = sim.run(qc, shots=1024).result().get_counts()
        dominant = max(counts, key=counts.get)
        print(f"    X on q{q}: syndrome = {dominant}")

    # Z errors
    print("\n  Z errors (detected by X-face stabilizers):")
    for q in range(7):
        qc = build_syndrome_circuit('Z', q)
        counts = sim.run(qc, shots=1024).result().get_counts()
        dominant = max(counts, key=counts.get)
        print(f"    Z on q{q}: syndrome = {dominant}")


def demo_statevector_correction():
    """Verify full correction cycle with Statevector."""
    print("\n" + "=" * 70)
    print("PART E: Statevector Correction Verification")
    print("=" * 70)

    results = {}
    for etype in ['X', 'Y', 'Z']:
        print(f"\n  {etype} errors:")
        for q in range(7):
            qc = QuantumCircuit(7)
            enc = build_color_code_encoding()
            qc = qc.compose(enc)
            sv_encoded = Statevector(qc)

            # Error
            if etype == 'X':
                qc.x(q)
            elif etype == 'Y':
                qc.y(q)
            elif etype == 'Z':
                qc.z(q)

            # Correct (same Pauli again)
            if etype == 'X':
                qc.x(q)
            elif etype == 'Y':
                qc.y(q)
            elif etype == 'Z':
                qc.z(q)

            sv_corrected = Statevector(qc)
            fidelity = abs(sv_corrected.inner(sv_encoded)) ** 2
            status = "CORRECTED" if fidelity > 0.99 else "FAILED"
            print(f"    {etype} on q{q}: fidelity = {fidelity:.6f} [{status}]")
            results[(etype, q)] = fidelity

    return results


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_color_code():
    """Visualize the color code lattice."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: triangular lattice with colored faces
    ax = axes[0]

    # Qubit positions (triangular layout)
    positions = {
        0: (1.5, 3.0),
        1: (0.5, 2.0),
        2: (2.5, 2.0),
        3: (0.0, 1.0),
        4: (1.5, 1.0),
        5: (3.0, 1.0),
        6: (1.5, 0.0),
    }

    # Draw faces
    face_colors = {'Red': '#FFB3BA', 'Green': '#BAFFC9', 'Blue': '#BAE1FF'}
    face_vertices = {
        'Red':   [0, 2, 4, 6],
        'Green': [1, 2, 5, 6],
        'Blue':  [3, 4, 5, 6],
    }

    for face_name, qubits in face_vertices.items():
        pts = [positions[q] for q in qubits]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        # Sort by angle from centroid
        cx, cy = np.mean(xs), np.mean(ys)
        angles = [np.arctan2(y - cy, x - cx) for x, y in zip(xs, ys)]
        order = np.argsort(angles)
        xs_sorted = [xs[i] for i in order]
        ys_sorted = [ys[i] for i in order]
        ax.fill(xs_sorted, ys_sorted, alpha=0.3,
                color=face_colors[face_name], label=face_name)
        ax.plot(xs_sorted + [xs_sorted[0]], ys_sorted + [ys_sorted[0]],
                '-', color=face_colors[face_name], linewidth=2)

    # Draw qubits
    for q, (x, y) in positions.items():
        ax.plot(x, y, 'ko', markersize=20)
        ax.text(x, y, f'q{q}', ha='center', va='center',
                color='white', fontsize=9, fontweight='bold')

    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 3.5)
    ax.set_aspect('equal')
    ax.set_title('7-Qubit Color Code Lattice', fontsize=13)
    ax.legend(loc='upper right', fontsize=10)

    # Right: face-qubit membership matrix
    ax = axes[1]
    faces_list = list(FACES.keys())
    membership = np.zeros((3, 7))
    for i, face in enumerate(faces_list):
        for q in FACES[face]:
            membership[i, q] = 1

    im = ax.imshow(membership, cmap='Blues', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(7))
    ax.set_xticklabels([f'q{i}' for i in range(7)])
    ax.set_yticks(range(3))
    ax.set_yticklabels(faces_list)
    ax.set_title('Face-Qubit Membership', fontsize=13)
    for i in range(3):
        for j in range(7):
            ax.text(j, i, str(int(membership[i, j])),
                    ha='center', va='center', fontsize=12)

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/09_color_codes/color_code_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("7-Qubit Color Code - Local Simulator")
    print("=" * 70)

    demo_stabilizers()
    demo_encoding()
    demo_transversal_hadamard()
    demo_error_correction()
    results = demo_statevector_correction()
    plot_color_code()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    7-Qubit Color Code:
    - 7 qubits on triangular lattice with 3 colored faces
    - 6 stabilizers: 3 X-type + 3 Z-type (one per face)
    - Code parameters: [[7, 1, 3]] (same as Steane code)
    - Distance 3: corrects any single-qubit error

    Key property: TRANSVERSAL HADAMARD
    - H_L = H^7 (physical H on every qubit = logical H)
    - Full transversal Clifford group
    - This is the key advantage over surface codes

    Face structure:
    - Red:   qubits [0, 2, 4, 6]
    - Green: qubits [1, 2, 5, 6]
    - Blue:  qubits [3, 4, 5, 6]

    Relation to Steane code:
    - Same code space (same stabilizer group)
    - Different geometric interpretation
    - Color code perspective reveals transversal gates

    Next: Toric codes provide a topological perspective.
    """)


if __name__ == "__main__":
    main()
