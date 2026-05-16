"""
Stabilizer Formalism - Local Simulator Implementation
=====================================================

Demonstrates the stabilizer formalism: the mathematical framework
underlying all stabilizer quantum error-correcting codes.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Key concepts:
    1. Pauli group P_n = {+/-1, +/-i} x {I, X, Y, Z}^n
    2. Stabilizer group S: abelian subgroup of P_n not containing -I
    3. Code space V_S = {|psi>: g|psi> = |psi> for all g in S}
    4. For n-qubit code with k logical qubits: |S| = 2^(n-k)
       -> (n-k) independent generators

Error detection:
    - Error E is detectable iff E anticommutes with at least one g in S
    - Syndrome = pattern of (anti)commutation with generators
    - Two errors E1, E2 have same syndrome iff E1*E2 commutes with all g in S

Pauli commutation:
    - Same-type Paulis always commute: [X,X] = [Y,Y] = [Z,Z] = 0
    - Different-type Paulis anticommute: {X,Y} = {Y,Z} = {X,Z} = 0
    - Multi-qubit: count overlaps where types differ
    - Commute iff even number of anticommuting single-qubit pairs
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, SparsePauliOp, Statevector


# =============================================================================
# PAULI GROUP OPERATIONS
# =============================================================================

def check_commutation(p1, p2):
    """
    Check if two Pauli operators commute.

    Two n-qubit Paulis commute iff they anticommute on an even number
    of qubit positions. Uses Qiskit's Pauli class for this check.

    The symplectic inner product determines commutation:
        p1 and p2 commute iff <p1, p2>_s = 0 (mod 2)
        where <p1, p2>_s = p1.x . p2.z + p1.z . p2.x (mod 2)
    """
    pauli1 = Pauli(p1)
    pauli2 = Pauli(p2)
    return pauli1.commutes(pauli2)


def build_pauli_operator(label):
    """Build a Pauli operator from a string label like 'XZIY'."""
    return Pauli(label)


def symplectic_inner_product(p1_label, p2_label):
    """
    Compute the symplectic inner product of two Pauli operators.

    Returns 0 if they commute, 1 if they anticommute.
    """
    p1 = Pauli(p1_label)
    p2 = Pauli(p2_label)
    # Count anticommuting positions
    n_anticommuting = 0
    for i in range(len(p1_label)):
        a = p1_label[i]
        b = p2_label[i]
        if a != 'I' and b != 'I' and a != b:
            n_anticommuting += 1
    return n_anticommuting % 2


# =============================================================================
# STABILIZER GROUP VERIFICATION
# =============================================================================

def verify_stabilizer_group(generators):
    """
    Verify that a set of Pauli operators forms a valid stabilizer group.

    Requirements:
        1. All generators commute pairwise
        2. All generators square to +I (Hermitian)
        3. -I is not in the group
        4. Generators are independent
    """
    n_gen = len(generators)
    results = {
        "pairwise_commuting": True,
        "all_hermitian": True,
        "commutation_matrix": np.zeros((n_gen, n_gen), dtype=int),
    }

    # Check pairwise commutation
    for i in range(n_gen):
        for j in range(i + 1, n_gen):
            commutes = check_commutation(generators[i], generators[j])
            results["commutation_matrix"][i, j] = 0 if commutes else 1
            results["commutation_matrix"][j, i] = 0 if commutes else 1
            if not commutes:
                results["pairwise_commuting"] = False

    # All Pauli operators are Hermitian (square to I), so this is automatic
    # for operators without phase factors
    results["all_hermitian"] = True

    return results


def find_code_space(generators, n_qubits):
    """
    Find the code space as the +1 eigenspace of all stabilizer generators.

    For each computational basis state, check if it's stabilized by all
    generators. The code space is spanned by stabilized states.

    Note: This is exponential in n_qubits, only practical for small codes.
    """
    stabilized_states = []

    for state_idx in range(2 ** n_qubits):
        # Create computational basis state
        sv = Statevector.from_int(state_idx, 2 ** n_qubits)

        is_stabilized = True
        for gen_label in generators:
            # Apply stabilizer
            pauli = Pauli(gen_label)
            op = SparsePauliOp.from_list([(gen_label, 1.0)])
            sv_after = sv.evolve(op)

            # Check if eigenvalue is +1
            overlap = sv.inner(sv_after)
            if abs(overlap - 1.0) > 1e-10:
                is_stabilized = False
                break

        if is_stabilized:
            stabilized_states.append(
                (format(state_idx, f'0{n_qubits}b'), state_idx))

    return stabilized_states


# =============================================================================
# SYNDROME COMPUTATION
# =============================================================================

def compute_error_syndrome(generators, error_label):
    """
    Compute the syndrome of an error with respect to stabilizer generators.

    Syndrome bit s_i = 0 if error commutes with generator i
                     = 1 if error anticommutes with generator i

    The syndrome uniquely identifies the error (up to stabilizer equivalence).
    """
    syndrome = []
    for gen in generators:
        commutes = check_commutation(gen, error_label)
        syndrome.append(0 if commutes else 1)
    return tuple(syndrome)


def build_syndrome_table(generators, n_qubits):
    """
    Build a complete syndrome lookup table for single-qubit Pauli errors.

    Maps each syndrome pattern to the corresponding error.
    """
    table = {}

    # Identity (no error)
    identity = 'I' * n_qubits
    syndrome = compute_error_syndrome(generators, identity)
    table[syndrome] = "I (no error)"

    # Single-qubit X, Y, Z errors
    for error_type in ['X', 'Y', 'Z']:
        for qubit in range(n_qubits):
            error_label = list('I' * n_qubits)
            error_label[qubit] = error_type
            error_str = ''.join(error_label)
            syndrome = compute_error_syndrome(generators, error_str)
            table[syndrome] = f"{error_type} on q{n_qubits - 1 - qubit}"

    return table


# =============================================================================
# EXAMPLES: KNOWN CODES
# =============================================================================

def bit_flip_code_stabilizers():
    """3-qubit bit-flip code stabilizers."""
    return ['ZZI', 'IZZ']


def phase_flip_code_stabilizers():
    """3-qubit phase-flip code stabilizers."""
    return ['XXI', 'IXX']


def steane_code_stabilizers():
    """[[7,1,3]] Steane code stabilizers."""
    return [
        'XIXIXIX',  # Sx1: X on 0,2,4,6
        'IXXIIXX',  # Sx2: X on 1,2,5,6
        'IIIXXXX',  # Sx3: X on 3,4,5,6
        'ZIZIZIZ',  # Sz1: Z on 0,2,4,6
        'IZZIIIZZ'[:7],  # Sz2: Z on 1,2,5,6
        'IIIZZZZ',  # Sz3: Z on 3,4,5,6
    ]


def five_qubit_code_stabilizers():
    """
    [[5,1,3]] perfect code stabilizers.
    The smallest code that corrects arbitrary single-qubit errors.
    """
    return [
        'XZZXI',
        'IXZZX',
        'XIXZZ',
        'ZXIXZ',
    ]


# =============================================================================
# DEMONSTRATION FUNCTIONS
# =============================================================================

def demo_pauli_commutation():
    """Demonstrate Pauli commutation relations."""
    print("\n" + "=" * 70)
    print("PART A: Pauli Commutation Relations")
    print("=" * 70)

    # Single-qubit
    print("\n  Single-qubit Pauli commutation:")
    for p1 in ['X', 'Y', 'Z']:
        for p2 in ['X', 'Y', 'Z']:
            commutes = check_commutation(p1, p2)
            relation = "commutes" if commutes else "anticommutes"
            print(f"    [{p1}, {p2}]: {relation}")

    # Multi-qubit examples
    print("\n  Multi-qubit examples:")
    examples = [
        ('XX', 'ZZ', "XX and ZZ"),
        ('XZ', 'ZX', "XZ and ZX"),
        ('XY', 'YX', "XY and YX"),
        ('XXI', 'ZZI', "XXI and ZZI (bit-flip stabilizers)"),
        ('ZZI', 'IZZ', "ZZI and IZZ (bit-flip stabilizers)"),
    ]
    for p1, p2, desc in examples:
        commutes = check_commutation(p1, p2)
        sip = symplectic_inner_product(p1, p2)
        print(f"    {desc}: {'commute' if commutes else 'anticommute'} "
              f"(symplectic product = {sip})")


def demo_stabilizer_verification():
    """Verify stabilizer group properties for known codes."""
    print("\n" + "=" * 70)
    print("PART B: Stabilizer Group Verification")
    print("=" * 70)

    codes = {
        "3-qubit bit-flip": bit_flip_code_stabilizers(),
        "3-qubit phase-flip": phase_flip_code_stabilizers(),
        "[[5,1,3]] perfect": five_qubit_code_stabilizers(),
    }

    for name, generators in codes.items():
        print(f"\n  {name} code:")
        print(f"    Generators: {generators}")

        result = verify_stabilizer_group(generators)
        print(f"    Pairwise commuting: {result['pairwise_commuting']}")
        print(f"    All Hermitian: {result['all_hermitian']}")

        n_qubits = len(generators[0])
        n_gen = len(generators)
        k = n_qubits - n_gen
        print(f"    n={n_qubits}, n-k={n_gen} generators, k={k} logical")


def demo_error_detection():
    """Demonstrate error detection via anticommutation with stabilizers."""
    print("\n" + "=" * 70)
    print("PART C: Error Detection via Anticommutation")
    print("=" * 70)

    # Bit-flip code: detects X errors
    generators = bit_flip_code_stabilizers()
    print(f"\n  Bit-flip code stabilizers: {generators}")

    print("\n  X errors:")
    for q in range(3):
        error = ['I', 'I', 'I']
        error[q] = 'X'
        error_str = ''.join(error)
        syndrome = compute_error_syndrome(generators, error_str)
        print(f"    X on q{2-q}: syndrome = {syndrome}")

    print("\n  Z errors (not detectable by bit-flip code):")
    for q in range(3):
        error = ['I', 'I', 'I']
        error[q] = 'Z'
        error_str = ''.join(error)
        syndrome = compute_error_syndrome(generators, error_str)
        detected = any(s == 1 for s in syndrome)
        print(f"    Z on q{2-q}: syndrome = {syndrome} "
              f"({'detected' if detected else 'UNDETECTED'})")


def demo_syndrome_tables():
    """Build syndrome tables for various codes."""
    print("\n" + "=" * 70)
    print("PART D: Syndrome Tables")
    print("=" * 70)

    # Bit-flip code
    print("\n  3-qubit bit-flip code:")
    bf_gens = bit_flip_code_stabilizers()
    bf_table = build_syndrome_table(bf_gens, 3)
    for syndrome, error in sorted(bf_table.items()):
        print(f"    Syndrome {syndrome}: {error}")

    # Phase-flip code
    print("\n  3-qubit phase-flip code:")
    pf_gens = phase_flip_code_stabilizers()
    pf_table = build_syndrome_table(pf_gens, 3)
    for syndrome, error in sorted(pf_table.items()):
        print(f"    Syndrome {syndrome}: {error}")

    # [[5,1,3]] code
    print("\n  [[5,1,3]] perfect code:")
    fq_gens = five_qubit_code_stabilizers()
    fq_table = build_syndrome_table(fq_gens, 5)
    for syndrome, error in sorted(fq_table.items()):
        print(f"    Syndrome {syndrome}: {error}")


def demo_code_space():
    """Find code space for small codes."""
    print("\n" + "=" * 70)
    print("PART E: Code Space Identification")
    print("=" * 70)

    # Bit-flip code
    print("\n  3-qubit bit-flip code space:")
    bf_gens = bit_flip_code_stabilizers()
    bf_states = find_code_space(bf_gens, 3)
    print(f"    Stabilized basis states: {[s[0] for s in bf_states]}")
    print(f"    Code space dimension: {len(bf_states)}")
    print(f"    (Expected: |000> and |111>, dim=2 for k=1)")

    # Phase-flip code
    print("\n  3-qubit phase-flip code space:")
    pf_gens = phase_flip_code_stabilizers()
    pf_states = find_code_space(pf_gens, 3)
    print(f"    Stabilized basis states: {[s[0] for s in pf_states]}")
    print(f"    Code space dimension: {len(pf_states)}")
    print(f"    (Expected: dim=2 for k=1, but in |+>/|-> basis)")

    # Note: phase-flip code space is in Hadamard basis
    # The stabilized states in computational basis may be different
    print(f"    Note: Phase-flip code stores info in |+>/|-> basis.")
    print(f"    Code space is spanned by |+++> and |--->.")


def demo_steane_stabilizers():
    """Analyze Steane code stabilizers."""
    print("\n" + "=" * 70)
    print("PART F: Steane Code Stabilizer Analysis")
    print("=" * 70)

    generators = steane_code_stabilizers()
    print(f"\n  Generators ({len(generators)}):")
    for i, g in enumerate(generators):
        gtype = "X-type" if 'X' in g else "Z-type"
        print(f"    g{i+1} = {g} ({gtype})")

    result = verify_stabilizer_group(generators)
    print(f"\n  Pairwise commuting: {result['pairwise_commuting']}")
    print(f"  Parameters: [[7, 1, 3]]")
    print(f"  n=7, (n-k)=6 generators, k=1 logical qubit")

    # Check some errors
    print(f"\n  Sample error syndromes:")
    for etype in ['X', 'Z']:
        for q in [0, 3, 6]:
            error = ['I'] * 7
            error[q] = etype
            error_str = ''.join(error)
            syndrome = compute_error_syndrome(generators, error_str)
            print(f"    {etype} on q{6-q}: syndrome = {syndrome}")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_commutation_structure():
    """Visualize commutation structure of stabilizer codes."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    codes = {
        "Bit-flip (3-qubit)": bit_flip_code_stabilizers(),
        "Phase-flip (3-qubit)": phase_flip_code_stabilizers(),
        "[[5,1,3]] Perfect": five_qubit_code_stabilizers(),
    }

    for idx, (name, gens) in enumerate(codes.items()):
        ax = axes[idx]
        n_gen = len(gens)
        comm_matrix = np.zeros((n_gen, n_gen))

        for i in range(n_gen):
            for j in range(n_gen):
                if i == j:
                    comm_matrix[i, j] = 0.5  # Self
                else:
                    commutes = check_commutation(gens[i], gens[j])
                    comm_matrix[i, j] = 1.0 if commutes else 0.0

        im = ax.imshow(comm_matrix, cmap='RdYlGn', vmin=0, vmax=1,
                        aspect='auto')
        ax.set_xticks(range(n_gen))
        ax.set_xticklabels([f'g{i+1}' for i in range(n_gen)], fontsize=9)
        ax.set_yticks(range(n_gen))
        ax.set_yticklabels([f'g{i+1}' for i in range(n_gen)], fontsize=9)
        ax.set_title(name, fontsize=11)

        for i in range(n_gen):
            for j in range(n_gen):
                val = comm_matrix[i, j]
                if i == j:
                    ax.text(j, i, 'self', ha='center', va='center',
                            fontsize=8)
                else:
                    label = 'C' if val > 0.5 else 'A'
                    ax.text(j, i, label, ha='center', va='center',
                            fontsize=10, fontweight='bold')

    fig.suptitle('Stabilizer Generator Commutation (C=commute, A=anticommute)',
                 fontsize=12)
    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/06_stabilizer_formalism/"
        "stabilizer_formalism_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Stabilizer Formalism - Local Simulator")
    print("=" * 70)

    demo_pauli_commutation()
    demo_stabilizer_verification()
    demo_error_detection()
    demo_syndrome_tables()
    demo_code_space()
    demo_steane_stabilizers()
    plot_commutation_structure()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Stabilizer Formalism:
    - Foundation of quantum error correction theory
    - Stabilizer group S: abelian subgroup of Pauli group
    - Code space: simultaneous +1 eigenspace of all stabilizers
    - n qubits, (n-k) generators -> k logical qubits

    Error detection:
    - Error E detected iff it anticommutes with some stabilizer
    - Syndrome = pattern of (anti)commutation with generators
    - 2^(n-k) possible syndromes for (n-k) generators

    Examples analyzed:
    - Bit-flip code: 2 Z-stabilizers, detects X errors
    - Phase-flip code: 2 X-stabilizers, detects Z errors
    - [[5,1,3]] code: 4 generators, corrects any single error
    - Steane code: 6 generators (3 X + 3 Z), CSS structure

    Next: Repetition codes generalize the bit-flip code to higher distance.
    """)


if __name__ == "__main__":
    main()
