"""
Toric Codes - Local Simulator Implementation
=============================================

Builds a d=2 toric code with 8 data qubits on a 2x2 torus.
Demonstrates vertex and plaquette operators with periodic boundary
conditions, logical operators as non-contractible loops, and
the 4-fold ground state degeneracy (2 logical qubits).

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Toric code on L x L torus:
    - 2*L^2 data qubits (one per edge of the lattice)
    - L^2 vertex operators (A_v): product of X on edges meeting at vertex
    - L^2 plaquette operators (B_p): product of Z on edges around face
    - 2*L^2 - (L^2 + L^2 - 2) = 2 logical qubits (4-fold degeneracy)

For d=2 (L=2) toric code:
    - 8 data qubits (edges of 2x2 periodic lattice)
    - 4 vertex operators (X-type)
    - 4 plaquette operators (Z-type)
    - But only 3+3 = 6 independent (one of each is product of others)
    - 8 - 6 = 2 logical qubits

Lattice layout (2x2 torus, edges labeled 0-7):
    Horizontal edges: e0=(0,0)-(0,1), e1=(0,1)-(0,0) [wraps]
                      e2=(1,0)-(1,1), e3=(1,1)-(1,0) [wraps]
    Vertical edges:   e4=(0,0)-(1,0), e5=(0,1)-(1,1)
                      e6=(1,0)-(0,0) [wraps], e7=(1,1)-(0,1) [wraps]

Logical operators:
    Logical X1: X on horizontal non-contractible loop
    Logical Z1: Z on vertical non-contractible loop
    Logical X2: X on vertical non-contractible loop
    Logical Z2: Z on horizontal non-contractible loop

Code parameters: [[8, 2, 2]] (for L=2)
    General: [[2L^2, 2, L]]
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import SparsePauliOp, Statevector


# =============================================================================
# TORIC CODE LAYOUT (L=2)
# =============================================================================

# 2x2 torus with periodic boundary conditions
# Vertices: v(r,c) for r,c in {0,1}
# Edges: 4 horizontal + 4 vertical = 8 total
#
# Edge numbering:
#   Horizontal: h(r,c) = edge from v(r,c) to v(r, (c+1)%2)
#     h(0,0) = e0, h(0,1) = e1, h(1,0) = e2, h(1,1) = e3
#   Vertical:   v(r,c) = edge from v(r,c) to v((r+1)%2, c)
#     v(0,0) = e4, v(0,1) = e5, v(1,0) = e6, v(1,1) = e7

L = 2
N_QUBITS = 2 * L * L  # 8 data qubits


def edge_h(r, c):
    """Index of horizontal edge at (r,c)."""
    return r * L + c


def edge_v(r, c):
    """Index of vertical edge at (r,c)."""
    return L * L + r * L + c


# Vertex operators A_v: product of X on edges meeting at vertex v(r,c)
# Each vertex has 4 edges: up, down, left, right (with periodic BC)
def vertex_edges(r, c):
    """Edges meeting at vertex (r,c)."""
    return [
        edge_h(r, c),              # right horizontal
        edge_h(r, (c - 1) % L),    # left horizontal
        edge_v(r, c),              # down vertical
        edge_v((r - 1) % L, c),    # up vertical
    ]


# Plaquette operators B_p: product of Z on edges around face
# Face at (r,c) has 4 edges: top, bottom, left, right
def plaquette_edges(r, c):
    """Edges around plaquette (face) at (r,c)."""
    return [
        edge_h(r, c),              # top horizontal
        edge_h((r + 1) % L, c),    # bottom horizontal
        edge_v(r, c),              # left vertical
        edge_v(r, (c + 1) % L),    # right vertical
    ]


# Build all vertex and plaquette operators
VERTEX_OPS = {}
for r in range(L):
    for c in range(L):
        VERTEX_OPS[f'A({r},{c})'] = vertex_edges(r, c)

PLAQUETTE_OPS = {}
for r in range(L):
    for c in range(L):
        PLAQUETTE_OPS[f'B({r},{c})'] = plaquette_edges(r, c)


# =============================================================================
# STABILIZER CONSTRUCTION
# =============================================================================

def build_toric_stabilizers():
    """
    Build SparsePauliOp objects for all toric code stabilizers.

    Vertex operators: X on edges meeting at each vertex
    Plaquette operators: Z on edges around each face
    """
    stabilizers = {}

    for name, edges in VERTEX_OPS.items():
        label = ['I'] * N_QUBITS
        for e in edges:
            label[N_QUBITS - 1 - e] = 'X'
        stabilizers[name] = SparsePauliOp.from_list(
            [(''.join(label), 1.0)])

    for name, edges in PLAQUETTE_OPS.items():
        label = ['I'] * N_QUBITS
        for e in edges:
            label[N_QUBITS - 1 - e] = 'Z'
        stabilizers[name] = SparsePauliOp.from_list(
            [(''.join(label), 1.0)])

    return stabilizers


def build_logical_operators():
    """
    Build logical operators for d=2 toric code.

    2 logical qubits -> 2 pairs of (X_L, Z_L).

    Logical X1: X on horizontal non-contractible loop (row 0)
        = X on e0, e1 (all horizontal edges in row 0)
    Logical Z1: Z on vertical non-contractible loop (column 0)
        = Z on e4, e6 (all vertical edges in column 0)

    Logical X2: X on vertical non-contractible loop (column 0)
        = X on e4, e6
    Logical Z2: Z on horizontal non-contractible loop (row 0)
        = Z on e0, e1
    """
    # Logical pair 1: horizontal X loop, vertical Z loop
    x1_label = ['I'] * N_QUBITS
    for c in range(L):
        x1_label[N_QUBITS - 1 - edge_h(0, c)] = 'X'
    x1 = SparsePauliOp.from_list([(''.join(x1_label), 1.0)])

    z1_label = ['I'] * N_QUBITS
    for r in range(L):
        z1_label[N_QUBITS - 1 - edge_v(r, 0)] = 'Z'
    z1 = SparsePauliOp.from_list([(''.join(z1_label), 1.0)])

    # Logical pair 2: vertical X loop, horizontal Z loop
    x2_label = ['I'] * N_QUBITS
    for r in range(L):
        x2_label[N_QUBITS - 1 - edge_v(r, 0)] = 'X'
    x2 = SparsePauliOp.from_list([(''.join(x2_label), 1.0)])

    z2_label = ['I'] * N_QUBITS
    for c in range(L):
        z2_label[N_QUBITS - 1 - edge_h(0, c)] = 'Z'
    z2 = SparsePauliOp.from_list([(''.join(z2_label), 1.0)])

    return (x1, z1), (x2, z2)


# =============================================================================
# SYNDROME MEASUREMENT
# =============================================================================

def build_syndrome_circuit(error_type=None, error_qubit=None):
    """
    Build syndrome measurement circuit for d=2 toric code.

    4 vertex (X-type) ancillas + 4 plaquette (Z-type) ancillas.
    """
    data = QuantumRegister(N_QUBITS, 'q')
    v_anc = QuantumRegister(4, 'va')
    p_anc = QuantumRegister(4, 'pa')
    v_bits = ClassicalRegister(4, 'v_syn')
    p_bits = ClassicalRegister(4, 'p_syn')
    qc = QuantumCircuit(data, v_anc, p_anc, v_bits, p_bits)

    # Error injection
    if error_type is not None and error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
    qc.barrier()

    # Vertex syndrome (X-stabilizers detect Z errors)
    # Ancilla in |+>, CNOT to data edges
    v_list = list(VERTEX_OPS.values())
    for i, edges in enumerate(v_list):
        qc.h(v_anc[i])
        for e in edges:
            qc.cx(v_anc[i], data[e])
        qc.h(v_anc[i])
        qc.measure(v_anc[i], v_bits[i])
    qc.barrier()

    # Plaquette syndrome (Z-stabilizers detect X errors)
    # CNOT from data edges to ancilla
    p_list = list(PLAQUETTE_OPS.values())
    for i, edges in enumerate(p_list):
        for e in edges:
            qc.cx(data[e], p_anc[i])
        qc.measure(p_anc[i], p_bits[i])

    return qc


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_lattice_structure():
    """Display the toric code lattice structure."""
    print("\n" + "=" * 70)
    print("PART A: d=2 Toric Code Lattice Structure")
    print("=" * 70)

    print(f"\n  Torus: {L}x{L} periodic lattice")
    print(f"  Data qubits: {N_QUBITS} (one per edge)")

    print(f"\n  Edge numbering:")
    print(f"    Horizontal edges:")
    for r in range(L):
        for c in range(L):
            e = edge_h(r, c)
            c_next = (c + 1) % L
            print(f"      e{e}: v({r},{c}) -- v({r},{c_next})")

    print(f"    Vertical edges:")
    for r in range(L):
        for c in range(L):
            e = edge_v(r, c)
            r_next = (r + 1) % L
            print(f"      e{e}: v({r},{c}) -- v({r_next},{c})")

    print(f"\n  Vertex operators (X-type, detect Z errors):")
    for name, edges in VERTEX_OPS.items():
        print(f"    {name}: X on edges {edges}")

    print(f"\n  Plaquette operators (Z-type, detect X errors):")
    for name, edges in PLAQUETTE_OPS.items():
        print(f"    {name}: Z on edges {edges}")


def demo_stabilizer_properties():
    """Verify stabilizer properties."""
    print("\n" + "=" * 70)
    print("PART B: Stabilizer Properties")
    print("=" * 70)

    stabilizers = build_toric_stabilizers()

    # Check that product of all vertex operators = I
    print("\n  Product of all vertex operators:")
    v_names = [n for n in stabilizers if n.startswith('A')]
    product_label = ['I'] * N_QUBITS
    for name in v_names:
        for e in VERTEX_OPS[name]:
            if product_label[N_QUBITS - 1 - e] == 'I':
                product_label[N_QUBITS - 1 - e] = 'X'
            else:
                product_label[N_QUBITS - 1 - e] = 'I'  # X*X = I
    print(f"    Product = {''.join(product_label)}")
    print(f"    (Should be all I: each edge appears in exactly 2 vertices)")

    # Similarly for plaquette operators
    print("\n  Product of all plaquette operators:")
    p_names = [n for n in stabilizers if n.startswith('B')]
    product_label = ['I'] * N_QUBITS
    for name in p_names:
        for e in PLAQUETTE_OPS[name]:
            if product_label[N_QUBITS - 1 - e] == 'I':
                product_label[N_QUBITS - 1 - e] = 'Z'
            else:
                product_label[N_QUBITS - 1 - e] = 'I'
    print(f"    Product = {''.join(product_label)}")
    print(f"    (Should be all I: each edge borders exactly 2 faces)")

    # Independent generators
    n_v_ind = L * L - 1  # One vertex constraint
    n_p_ind = L * L - 1  # One plaquette constraint
    k = N_QUBITS - n_v_ind - n_p_ind
    print(f"\n  Independent generators: {n_v_ind} vertex + {n_p_ind} plaquette"
          f" = {n_v_ind + n_p_ind}")
    print(f"  Logical qubits: k = {N_QUBITS} - {n_v_ind + n_p_ind} = {k}")
    print(f"  Ground state degeneracy: 2^k = {2**k}")


def demo_logical_operators():
    """Display logical operators."""
    print("\n" + "=" * 70)
    print("PART C: Logical Operators (Non-Contractible Loops)")
    print("=" * 70)

    (x1, z1), (x2, z2) = build_logical_operators()

    print(f"\n  Logical qubit 1:")
    print(f"    X_L1 (horizontal loop): {x1}")
    print(f"    Z_L1 (vertical loop):   {z1}")

    print(f"\n  Logical qubit 2:")
    print(f"    X_L2 (vertical loop):   {x2}")
    print(f"    Z_L2 (horizontal loop): {z2}")

    print(f"\n  Topological protection:")
    print(f"    Logical operators are non-contractible loops on the torus")
    print(f"    Minimum weight of logical operator = L = {L} (code distance)")
    print(f"    Cannot be deformed to a point -> topologically protected")


def demo_syndrome_measurement():
    """Demonstrate syndrome measurement."""
    print("\n" + "=" * 70)
    print("PART D: Syndrome Measurement")
    print("=" * 70)

    sim = AerSimulator()

    test_cases = [
        (None, None, "No error"),
        ('X', 0, "X on e0 (horiz)"),
        ('X', 4, "X on e4 (vert)"),
        ('Z', 0, "Z on e0 (horiz)"),
        ('Z', 4, "Z on e4 (vert)"),
        ('Y', 2, "Y on e2"),
    ]

    for etype, qidx, label in test_cases:
        qc = build_syndrome_circuit(etype, qidx)
        counts = sim.run(qc, shots=2048).result().get_counts()
        dominant = max(counts, key=counts.get)
        print(f"\n  {label}:")
        print(f"    Dominant syndrome: {dominant}")
        print(f"    (format: plaquette_syn vertex_syn)")


def demo_degeneracy():
    """
    Demonstrate 4-fold ground state degeneracy (2 logical qubits).

    The ground space is spanned by 4 states corresponding to
    the 4 eigenvalue combinations of (Z_L1, Z_L2).
    """
    print("\n" + "=" * 70)
    print("PART E: Ground State Degeneracy")
    print("=" * 70)

    print(f"\n  For L={L} toric code:")
    print(f"    Number of data qubits: {N_QUBITS}")
    print(f"    Independent stabilizers: {2*(L*L - 1)} = {2*(L*L-1)}")
    print(f"    Logical qubits: k = {N_QUBITS} - {2*(L*L-1)} = 2")
    print(f"    Ground state degeneracy: 2^2 = 4")

    print(f"\n  The 4 ground states are labeled by (Z_L1, Z_L2):")
    print(f"    |00_L>: Z_L1 = +1, Z_L2 = +1")
    print(f"    |01_L>: Z_L1 = +1, Z_L2 = -1")
    print(f"    |10_L>: Z_L1 = -1, Z_L2 = +1")
    print(f"    |11_L>: Z_L1 = -1, Z_L2 = -1")

    print(f"\n  General L toric code: [[2L^2, 2, L]]")
    print(f"    L=2: [[8, 2, 2]]")
    print(f"    L=3: [[18, 2, 3]]")
    print(f"    L=4: [[32, 2, 4]]")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_toric_code():
    """Visualize the d=2 toric code on a torus (unfolded)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: lattice with edges labeled
    ax = axes[0]

    # Draw vertices (2x2 grid, shown as 3x3 with periodic wrapping)
    for r in range(3):
        for c in range(3):
            alpha = 1.0 if r < 2 and c < 2 else 0.3
            ax.plot(c, 2 - r, 'ko', markersize=15, alpha=alpha)
            if r < 2 and c < 2:
                ax.text(c - 0.15, 2 - r + 0.15, f'v({r},{c})',
                        fontsize=8, color='blue')

    # Draw horizontal edges
    h_colors = ['red', 'orange', 'green', 'purple']
    for r in range(2):
        for c in range(2):
            e = edge_h(r, c)
            c_next = c + 1
            ax.plot([c, c_next], [2 - r, 2 - r], '-',
                    color=h_colors[e], linewidth=3, alpha=0.8)
            ax.text((c + c_next) / 2, 2 - r + 0.1, f'e{e}',
                    ha='center', fontsize=9, fontweight='bold',
                    color=h_colors[e])

    # Draw vertical edges
    v_colors = ['blue', 'cyan', 'magenta', 'brown']
    for r in range(2):
        for c in range(2):
            e = edge_v(r, c)
            r_next = r + 1
            ax.plot([c, c], [2 - r, 2 - r_next], '-',
                    color=v_colors[e - 4], linewidth=3, alpha=0.8)
            ax.text(c + 0.1, (2 - r + 2 - r_next) / 2, f'e{e}',
                    fontsize=9, fontweight='bold',
                    color=v_colors[e - 4])

    # Indicate periodic boundaries
    ax.annotate('periodic', xy=(2.2, 1), fontsize=8, color='gray',
                fontstyle='italic')
    ax.annotate('periodic', xy=(0.5, -0.3), fontsize=8, color='gray',
                fontstyle='italic', ha='center')

    ax.set_xlim(-0.5, 2.8)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect('equal')
    ax.set_title(f'd={L} Toric Code Lattice (8 edges)', fontsize=13)

    # Right: stabilizer structure
    ax = axes[1]
    all_ops = {}
    all_ops.update(VERTEX_OPS)
    all_ops.update(PLAQUETTE_OPS)

    op_names = list(all_ops.keys())
    n_ops = len(op_names)
    membership = np.zeros((n_ops, N_QUBITS))
    for i, (name, edges) in enumerate(all_ops.items()):
        for e in edges:
            membership[i, e] = 1

    im = ax.imshow(membership, cmap='Blues', vmin=0, vmax=1, aspect='auto')
    ax.set_xticks(range(N_QUBITS))
    ax.set_xticklabels([f'e{i}' for i in range(N_QUBITS)], fontsize=8)
    ax.set_yticks(range(n_ops))
    ax.set_yticklabels(op_names, fontsize=8)
    ax.set_xlabel('Edge (data qubit)', fontsize=11)
    ax.set_ylabel('Stabilizer', fontsize=11)
    ax.set_title('Stabilizer-Edge Membership', fontsize=13)

    # Separator between vertex and plaquette operators
    ax.axhline(y=3.5, color='red', linewidth=2, linestyle='--')
    ax.text(N_QUBITS + 0.3, 1.5, 'Vertex\n(X-type)', fontsize=9,
            va='center', color='red')
    ax.text(N_QUBITS + 0.3, 5.5, 'Plaquette\n(Z-type)', fontsize=9,
            va='center', color='red')

    for i in range(n_ops):
        for j in range(N_QUBITS):
            if membership[i, j] > 0:
                ax.text(j, i, '1', ha='center', va='center',
                        fontsize=9, fontweight='bold')

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/10_toric_codes/toric_code_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("d=2 Toric Code - Local Simulator")
    print("=" * 70)

    demo_lattice_structure()
    demo_stabilizer_properties()
    demo_logical_operators()
    demo_syndrome_measurement()
    demo_degeneracy()
    plot_toric_code()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    d=2 Toric Code:
    - 8 data qubits on edges of 2x2 periodic lattice
    - 4 vertex operators (X-type) + 4 plaquette operators (Z-type)
    - 3+3 = 6 independent stabilizers
    - Code parameters: [[8, 2, 2]]
    - 2 logical qubits, 4-fold ground state degeneracy

    Topological properties:
    - Logical operators = non-contractible loops on torus
    - Topologically protected: local errors cannot create logical errors
    - Product of all vertex ops = I (constraint)
    - Product of all plaquette ops = I (constraint)

    General toric code: [[2L^2, 2, L]]
    - Distance L: corrects floor((L-1)/2) errors
    - Always encodes exactly 2 logical qubits (genus-1 surface)

    Key insight: topological order provides robust error protection.
    The code space depends only on the topology (genus), not details.
    """)


if __name__ == "__main__":
    main()
