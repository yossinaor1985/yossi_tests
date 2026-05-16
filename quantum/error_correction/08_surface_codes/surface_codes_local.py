"""
Surface Codes - Local Simulator Implementation
===============================================

Builds a d=3 surface code conceptually with 9 data qubits on a 3x3 grid.
Defines vertex operators (Z-type) and plaquette operators (X-type),
demonstrates error injection and syndrome measurement.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Surface code (d=3):
    - 9 data qubits on a 3x3 grid
    - Vertex operators (Z-type): product of Z on edges meeting at vertex
    - Plaquette operators (X-type): product of X on edges around a face

Grid layout (data qubits numbered 0-8):
    0 - 1 - 2
    |   |   |
    3 - 4 - 5
    |   |   |
    6 - 7 - 8

For the rotated surface code:
    - 4 X-stabilizers (plaquettes)
    - 4 Z-stabilizers (vertices)
    - 8 stabilizers, 9 qubits -> 1 logical qubit

Code parameters: [[9,1,3]] (or [[d^2, 1, d]] in general)
    - Distance d=3: corrects 1 error
    - Logical X: chain across the lattice (horizontal)
    - Logical Z: chain across the lattice (vertical)

Advantages:
    - Local stabilizers (at most weight 4)
    - Threshold ~1% for circuit-level noise
    - Leading candidate for fault-tolerant quantum computing
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp, Statevector


# =============================================================================
# SURFACE CODE LAYOUT (d=3)
# =============================================================================

# Data qubit positions on 3x3 grid
# Row 0: q0, q1, q2
# Row 1: q3, q4, q5
# Row 2: q6, q7, q8

def get_qubit_position(qubit_idx):
    """Get (row, col) position of a data qubit."""
    return (qubit_idx // 3, qubit_idx % 3)


# Plaquette (X-type) stabilizers for d=3 rotated surface code
# Each plaquette is a face of the grid
PLAQUETTE_STABILIZERS = {
    'P1': [0, 1, 3, 4],  # Top-left face
    'P2': [1, 2, 4, 5],  # Top-right face
    'P3': [3, 4, 6, 7],  # Bottom-left face
    'P4': [4, 5, 7, 8],  # Bottom-right face
}

# Vertex (Z-type) stabilizers for d=3 rotated surface code
# Vertices are at the centers of the dual lattice
VERTEX_STABILIZERS = {
    'V1': [0, 1],         # Top boundary
    'V2': [0, 3],         # Left boundary
    'V3': [2, 5],         # Right boundary
    'V4': [6, 7],         # Bottom boundary (partial)
    'V5': [1, 2, 4, 5],   # Internal vertex
    'V6': [3, 4, 6, 7],   # Internal vertex
    'V7': [5, 8],         # Right boundary
    'V8': [7, 8],         # Bottom boundary
}

# Simplified: use 4 X-stabilizers and 4 Z-stabilizers
X_STABILIZERS = {
    'X1': [0, 1, 3, 4],
    'X2': [1, 2, 4, 5],
    'X3': [3, 4, 6, 7],
    'X4': [4, 5, 7, 8],
}

Z_STABILIZERS = {
    'Z1': [0, 1],
    'Z2': [2, 5],
    'Z3': [3, 6],
    'Z4': [7, 8],
}


# =============================================================================
# STABILIZER CONSTRUCTION
# =============================================================================

def build_surface_stabilizers():
    """
    Build SparsePauliOp objects for all surface code stabilizers.

    X-stabilizers: X on qubits around each plaquette
    Z-stabilizers: Z on qubits at each vertex
    """
    stabilizers = {}
    n = 9

    for name, qubits in X_STABILIZERS.items():
        label = ['I'] * n
        for q in qubits:
            label[n - 1 - q] = 'X'
        stabilizers[name] = SparsePauliOp.from_list(
            [(''.join(label), 1.0)])

    for name, qubits in Z_STABILIZERS.items():
        label = ['I'] * n
        for q in qubits:
            label[n - 1 - q] = 'Z'
        stabilizers[name] = SparsePauliOp.from_list(
            [(''.join(label), 1.0)])

    return stabilizers


def build_logical_operators():
    """
    Build logical operators for d=3 surface code.

    Logical X: horizontal chain (e.g., X0 X1 X2)
    Logical Z: vertical chain (e.g., Z0 Z3 Z6)
    """
    n = 9
    # Logical X: top row
    x_label = ['I'] * n
    for q in [0, 1, 2]:
        x_label[n - 1 - q] = 'X'
    x_logical = SparsePauliOp.from_list([(''.join(x_label), 1.0)])

    # Logical Z: left column
    z_label = ['I'] * n
    for q in [0, 3, 6]:
        z_label[n - 1 - q] = 'Z'
    z_logical = SparsePauliOp.from_list([(''.join(z_label), 1.0)])

    return x_logical, z_logical


# =============================================================================
# SYNDROME MEASUREMENT
# =============================================================================

def build_syndrome_circuit(error_type=None, error_qubit=None):
    """
    Build syndrome extraction circuit for d=3 surface code.

    4 X-syndrome ancillas + 4 Z-syndrome ancillas.
    """
    data = QuantumRegister(9, 'q')
    x_anc = QuantumRegister(4, 'xa')
    z_anc = QuantumRegister(4, 'za')
    x_bits = ClassicalRegister(4, 'x_syn')
    z_bits = ClassicalRegister(4, 'z_syn')
    qc = QuantumCircuit(data, x_anc, z_anc, x_bits, z_bits)

    # Inject error
    if error_type is not None and error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
    qc.barrier()

    # X-syndrome measurement (plaquette operators)
    # X-stabilizers measured via ancilla in |+>, CNOT to data
    x_stab_list = list(X_STABILIZERS.values())
    for i, qubits in enumerate(x_stab_list):
        qc.h(x_anc[i])
        for q in qubits:
            qc.cx(x_anc[i], data[q])
        qc.h(x_anc[i])
        qc.measure(x_anc[i], x_bits[i])
    qc.barrier()

    # Z-syndrome measurement (vertex operators)
    # Z-stabilizers measured via CNOT from data to ancilla
    z_stab_list = list(Z_STABILIZERS.values())
    for i, qubits in enumerate(z_stab_list):
        for q in qubits:
            qc.cx(data[q], z_anc[i])
        qc.measure(z_anc[i], z_bits[i])

    return qc


# =============================================================================
# SIMPLE LOOKUP DECODER (d=3)
# =============================================================================

def build_x_error_lookup():
    """
    Build lookup table: Z-syndrome -> X correction for d=3.

    Z-stabilizers detect X errors.
    4-bit Z-syndrome maps to error location.
    """
    table = {}
    # No error
    table[(0, 0, 0, 0)] = None

    # Single X errors: compute their Z-syndrome
    for q in range(9):
        syndrome = []
        for z_name, z_qubits in Z_STABILIZERS.items():
            # X on qubit q anticommutes with Z on qubit q
            anticommutes = q in z_qubits
            syndrome.append(1 if anticommutes else 0)
        s = tuple(syndrome)
        if s not in table:
            table[s] = q

    return table


def build_z_error_lookup():
    """
    Build lookup table: X-syndrome -> Z correction for d=3.

    X-stabilizers detect Z errors.
    4-bit X-syndrome maps to error location.
    """
    table = {}
    table[(0, 0, 0, 0)] = None

    for q in range(9):
        syndrome = []
        for x_name, x_qubits in X_STABILIZERS.items():
            anticommutes = q in x_qubits
            syndrome.append(1 if anticommutes else 0)
        s = tuple(syndrome)
        if s not in table:
            table[s] = q

    return table


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_stabilizers():
    """Display surface code stabilizers."""
    print("\n" + "=" * 70)
    print("PART A: d=3 Surface Code Stabilizers")
    print("=" * 70)

    stabilizers = build_surface_stabilizers()

    print("\n  Grid layout:")
    print("    q0 - q1 - q2")
    print("     |    |    |")
    print("    q3 - q4 - q5")
    print("     |    |    |")
    print("    q6 - q7 - q8")

    print("\n  X-stabilizers (plaquette operators):")
    for name, qubits in X_STABILIZERS.items():
        print(f"    {name}: X on qubits {qubits}")

    print("\n  Z-stabilizers (vertex operators):")
    for name, qubits in Z_STABILIZERS.items():
        print(f"    {name}: Z on qubits {qubits}")

    x_l, z_l = build_logical_operators()
    print(f"\n  Logical X: X on [0,1,2] (top row)")
    print(f"  Logical Z: Z on [0,3,6] (left column)")
    print(f"  Code parameters: [[9, 1, 3]]")


def demo_syndrome_measurement():
    """Demonstrate syndrome measurement for various errors."""
    print("\n" + "=" * 70)
    print("PART B: Syndrome Measurement")
    print("=" * 70)

    sim = AerSimulator()

    test_cases = [
        (None, None, "No error"),
        ('X', 0, "X on q0"),
        ('X', 4, "X on q4 (center)"),
        ('X', 8, "X on q8"),
        ('Z', 0, "Z on q0"),
        ('Z', 4, "Z on q4 (center)"),
        ('Z', 8, "Z on q8"),
    ]

    for etype, qidx, label in test_cases:
        qc = build_syndrome_circuit(etype, qidx)
        counts = sim.run(qc, shots=2048).result().get_counts()
        dominant = max(counts, key=counts.get)
        print(f"\n  {label}:")
        print(f"    Dominant syndrome: {dominant}")
        print(f"    (format: z_syn x_syn)")


def demo_lookup_decoder():
    """Demonstrate the lookup decoder for d=3."""
    print("\n" + "=" * 70)
    print("PART C: Lookup Decoder (d=3)")
    print("=" * 70)

    x_lookup = build_x_error_lookup()
    z_lookup = build_z_error_lookup()

    print("\n  X-error lookup (Z-syndrome -> correction):")
    for syndrome, correction in sorted(x_lookup.items()):
        if correction is not None:
            r, c = get_qubit_position(correction)
            print(f"    Z-syndrome {syndrome} -> X on q{correction} "
                  f"(row {r}, col {c})")
        else:
            print(f"    Z-syndrome {syndrome} -> no error")

    print("\n  Z-error lookup (X-syndrome -> correction):")
    for syndrome, correction in sorted(z_lookup.items()):
        if correction is not None:
            r, c = get_qubit_position(correction)
            print(f"    X-syndrome {syndrome} -> Z on q{correction} "
                  f"(row {r}, col {c})")
        else:
            print(f"    X-syndrome {syndrome} -> no error")

    # Coverage
    x_covered = sum(1 for v in x_lookup.values() if v is not None)
    z_covered = sum(1 for v in z_lookup.values() if v is not None)
    print(f"\n  X-error patterns with unique syndrome: {x_covered}/9")
    print(f"  Z-error patterns with unique syndrome: {z_covered}/9")


def demo_error_correction_cycle():
    """Demonstrate full error correction with statevector."""
    print("\n" + "=" * 70)
    print("PART D: Error Correction Verification")
    print("=" * 70)

    # Use lookup tables to verify correction
    x_lookup = build_x_error_lookup()
    z_lookup = build_z_error_lookup()

    print("\n  Single X errors:")
    for q in range(9):
        # Compute Z-syndrome
        z_syn = []
        for z_qubits in Z_STABILIZERS.values():
            z_syn.append(1 if q in z_qubits else 0)
        correction = x_lookup.get(tuple(z_syn))
        status = "CORRECTED" if correction == q else "AMBIGUOUS"
        print(f"    X on q{q}: Z-syndrome={tuple(z_syn)}, "
              f"correction=q{correction} [{status}]")

    print("\n  Single Z errors:")
    for q in range(9):
        x_syn = []
        for x_qubits in X_STABILIZERS.values():
            x_syn.append(1 if q in x_qubits else 0)
        correction = z_lookup.get(tuple(x_syn))
        status = "CORRECTED" if correction == q else "AMBIGUOUS"
        print(f"    Z on q{q}: X-syndrome={tuple(x_syn)}, "
              f"correction=q{correction} [{status}]")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_surface_code():
    """Visualize the d=3 surface code lattice and stabilizers."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: lattice structure
    ax = axes[0]
    # Draw grid
    for i in range(3):
        for j in range(3):
            q = i * 3 + j
            ax.plot(j, 2 - i, 'ko', markersize=20)
            ax.text(j, 2 - i, f'q{q}', ha='center', va='center',
                    color='white', fontsize=9, fontweight='bold')

    # Draw edges
    for i in range(3):
        for j in range(2):
            ax.plot([j, j + 1], [2 - i, 2 - i], 'k-', linewidth=1)
    for i in range(2):
        for j in range(3):
            ax.plot([j, j], [2 - i, 2 - i - 1], 'k-', linewidth=1)

    # Draw plaquettes (X-stabilizers) as colored faces
    colors = ['#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA']
    for idx, (name, qubits) in enumerate(X_STABILIZERS.items()):
        positions = [get_qubit_position(q) for q in qubits]
        rows = [2 - p[0] for p in positions]
        cols = [p[1] for p in positions]
        center_r = np.mean(rows)
        center_c = np.mean(cols)
        rect = mpatches.FancyBboxPatch(
            (center_c - 0.4, center_r - 0.4), 0.8, 0.8,
            boxstyle="round,pad=0.05", alpha=0.3,
            facecolor=colors[idx], edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        ax.text(center_c, center_r, name, ha='center', va='center',
                fontsize=8, color='red')

    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title('d=3 Surface Code Lattice', fontsize=13)
    ax.set_xlabel('Column', fontsize=11)
    ax.set_ylabel('Row', fontsize=11)

    # Right: syndrome pattern for X error on q4
    ax = axes[1]
    for i in range(3):
        for j in range(3):
            q = i * 3 + j
            color = 'red' if q == 4 else 'black'
            size = 25 if q == 4 else 20
            ax.plot(j, 2 - i, 'o', color=color, markersize=size)
            ax.text(j, 2 - i, f'q{q}', ha='center', va='center',
                    color='white', fontsize=9, fontweight='bold')

    for i in range(3):
        for j in range(2):
            ax.plot([j, j + 1], [2 - i, 2 - i], 'k-', linewidth=1)
    for i in range(2):
        for j in range(3):
            ax.plot([j, j], [2 - i, 2 - i - 1], 'k-', linewidth=1)

    # Highlight triggered Z-stabilizers for X on q4
    for name, qubits in Z_STABILIZERS.items():
        triggered = 4 in qubits
        if triggered:
            positions = [get_qubit_position(q) for q in qubits]
            for p in positions:
                ax.plot(p[1], 2 - p[0], 'o', color='orange',
                        markersize=30, alpha=0.3)

    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title('X Error on q4: Triggered Z-Stabilizers', fontsize=13)
    ax.set_xlabel('Column', fontsize=11)
    ax.set_ylabel('Row', fontsize=11)

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/08_surface_codes/surface_code_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("d=3 Surface Code - Local Simulator")
    print("=" * 70)

    demo_stabilizers()
    demo_syndrome_measurement()
    demo_lookup_decoder()
    demo_error_correction_cycle()
    plot_surface_code()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    d=3 Surface Code:
    - 9 data qubits on 3x3 grid
    - 4 X-stabilizers (plaquette) + 4 Z-stabilizers (vertex)
    - Code parameters: [[9, 1, 3]]
    - Distance 3: corrects any single-qubit error

    Key properties:
    - Local stabilizers (weight 2 or 4 only)
    - Threshold ~1% for circuit-level noise
    - Only nearest-neighbor interactions needed
    - Scalable: [[d^2, 1, d]] for general distance d

    Logical operators:
    - Logical X: horizontal chain (top row)
    - Logical Z: vertical chain (left column)

    This is the leading candidate for practical fault-tolerant QC.
    Next: Color codes offer richer transversal gate sets.
    """)


if __name__ == "__main__":
    main()
