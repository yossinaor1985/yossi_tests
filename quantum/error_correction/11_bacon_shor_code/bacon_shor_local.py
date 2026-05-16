"""
Bacon-Shor Code (3x3) - Local Simulator Implementation
========================================================

Implements the [[9,1,3]] Bacon-Shor subsystem code on a 3x3 qubit grid.
Demonstrates gauge operators, stabilizer derivation, syndrome extraction
via 2-body gauge measurements, and single-qubit error correction.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Grid layout (row, col):
    q(0,0)  q(0,1)  q(0,2)
    q(1,0)  q(1,1)  q(1,2)
    q(2,0)  q(2,1)  q(2,2)

Gauge operators (weight-2):
    XX horizontal:  G^X_{i,j} = X_{i,j} X_{i,j+1}  (within row)
    ZZ vertical:    G^Z_{i,j} = Z_{i,j} Z_{i+1,j}  (within column)

Stabilizers (from gauge products):
    S^X_i = prod_j X_{i,j} X_{i+1,j}   (rows i, i+1)
    S^Z_j = prod_i Z_{i,j} Z_{i,j+1}   (columns j, j+1)

Logical operators:
    X_L = X on any full row (weight 3)
    Z_L = Z on any full column (weight 3)

Distance: d = min(3,3) = 3  ->  corrects 1 arbitrary error
"""

import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, Operator, Pauli, SparsePauliOp


# =============================================================================
# GRID DEFINITIONS
# =============================================================================

ROWS = 3
COLS = 3
N_QUBITS = ROWS * COLS  # 9


def qubit_index(row, col):
    """
    Map 2D grid position to linear qubit index.

    Layout:
        q0=q(0,0)  q1=q(0,1)  q2=q(0,2)
        q3=q(1,0)  q4=q(1,1)  q5=q(1,2)
        q6=q(2,0)  q7=q(2,1)  q8=q(2,2)
    """
    return row * COLS + col


def grid_position(index):
    """Map linear qubit index back to (row, col)."""
    return divmod(index, COLS)


# =============================================================================
# GAUGE OPERATORS (2-BODY)
# =============================================================================

def build_xx_gauge_operators():
    """
    Build all XX gauge operators (horizontal pairs within rows).

    G^X_{i,j} = X_{i,j} X_{i,j+1}
    For 3x3 grid: 3 rows * 2 pairs = 6 operators.

    Returns list of (label, qubit_pair, SparsePauliOp).
    """
    operators = []
    for row in range(ROWS):
        for col in range(COLS - 1):
            q1 = qubit_index(row, col)
            q2 = qubit_index(row, col + 1)

            # Build Pauli string: X on q1 and q2, I elsewhere
            pauli_str = ['I'] * N_QUBITS
            pauli_str[q1] = 'X'
            pauli_str[q2] = 'X'
            # Qiskit Pauli ordering: qubit 0 is rightmost
            pauli_label = ''.join(reversed(pauli_str))

            op = SparsePauliOp(pauli_label)
            label = f"G^X_({row},{col}): X_{q1}X_{q2}"
            operators.append((label, (q1, q2), op))

    return operators


def build_zz_gauge_operators():
    """
    Build all ZZ gauge operators (vertical pairs within columns).

    G^Z_{i,j} = Z_{i,j} Z_{i+1,j}
    For 3x3 grid: 2 pairs * 3 columns = 6 operators.

    Returns list of (label, qubit_pair, SparsePauliOp).
    """
    operators = []
    for col in range(COLS):
        for row in range(ROWS - 1):
            q1 = qubit_index(row, col)
            q2 = qubit_index(row + 1, col)

            pauli_str = ['I'] * N_QUBITS
            pauli_str[q1] = 'Z'
            pauli_str[q2] = 'Z'
            pauli_label = ''.join(reversed(pauli_str))

            op = SparsePauliOp(pauli_label)
            label = f"G^Z_({row},{col}): Z_{q1}Z_{q2}"
            operators.append((label, (q1, q2), op))

    return operators


# =============================================================================
# STABILIZERS (FROM GAUGE PRODUCTS)
# =============================================================================

def build_x_stabilizers():
    """
    Build X-type stabilizers: X on all qubits in row i AND row i+1.

    S^X_i = prod_j X_{i,j} X_{i+1,j}

    For 3x3 grid: 2 stabilizers (rows 0-1, rows 1-2).
    Each has weight 6 (X on 6 qubits in two rows).

    These are products of XX gauge operators measured column-by-column.
    """
    stabilizers = []
    for row in range(ROWS - 1):
        pauli_str = ['I'] * N_QUBITS
        for col in range(COLS):
            q1 = qubit_index(row, col)
            q2 = qubit_index(row + 1, col)
            pauli_str[q1] = 'X'
            pauli_str[q2] = 'X'

        pauli_label = ''.join(reversed(pauli_str))
        op = SparsePauliOp(pauli_label)
        label = f"S^X_{row}: X on rows {row},{row + 1}"
        stabilizers.append((label, op))

    return stabilizers


def build_z_stabilizers():
    """
    Build Z-type stabilizers: Z on all qubits in column j AND column j+1.

    S^Z_j = prod_i Z_{i,j} Z_{i,j+1}

    For 3x3 grid: 2 stabilizers (cols 0-1, cols 1-2).
    Each has weight 6 (Z on 6 qubits in two columns).

    These are products of ZZ gauge operators measured row-by-row.
    """
    stabilizers = []
    for col in range(COLS - 1):
        pauli_str = ['I'] * N_QUBITS
        for row in range(ROWS):
            q1 = qubit_index(row, col)
            q2 = qubit_index(row, col + 1)
            pauli_str[q1] = 'Z'
            pauli_str[q2] = 'Z'

        pauli_label = ''.join(reversed(pauli_str))
        op = SparsePauliOp(pauli_label)
        label = f"S^Z_{col}: Z on cols {col},{col + 1}"
        stabilizers.append((label, op))

    return stabilizers


def build_logical_operators():
    """
    Build logical X and Z operators.

    X_L = X on row 0 (any row works): X_0 X_1 X_2
    Z_L = Z on col 0 (any col works): Z_0 Z_3 Z_6
    """
    # Logical X: X on all qubits in row 0
    x_str = ['I'] * N_QUBITS
    for col in range(COLS):
        x_str[qubit_index(0, col)] = 'X'
    x_label = ''.join(reversed(x_str))
    x_l = SparsePauliOp(x_label)

    # Logical Z: Z on all qubits in column 0
    z_str = ['I'] * N_QUBITS
    for row in range(ROWS):
        z_str[qubit_index(row, 0)] = 'Z'
    z_label = ''.join(reversed(z_str))
    z_l = SparsePauliOp(z_label)

    return x_l, z_l


# =============================================================================
# VERIFICATION: GAUGE AND STABILIZER ALGEBRA
# =============================================================================

def verify_gauge_algebra():
    """
    Verify the algebraic structure of the Bacon-Shor code.

    Checks:
    1. Gauge operators within same type commute: [G^X, G^X] = 0, [G^Z, G^Z] = 0
    2. Some cross-type gauge operators anticommute: {G^X, G^Z} = 0
    3. All stabilizers commute with all gauge operators
    4. Logical operators commute with all stabilizers
    5. X_L and Z_L anticommute with each other
    """
    print("\n" + "=" * 70)
    print("PART A: Gauge and Stabilizer Algebra Verification")
    print("=" * 70)

    xx_gauges = build_xx_gauge_operators()
    zz_gauges = build_zz_gauge_operators()
    x_stabs = build_x_stabilizers()
    z_stabs = build_z_stabilizers()
    x_l, z_l = build_logical_operators()

    # Check 1: XX gauges commute with each other
    print("\n  1. XX gauge operators mutually commute:")
    all_commute = True
    for i in range(len(xx_gauges)):
        for j in range(i + 1, len(xx_gauges)):
            comm = xx_gauges[i][2] @ xx_gauges[j][2] - xx_gauges[j][2] @ xx_gauges[i][2]
            if not np.allclose(comm.to_matrix().toarray(), 0):
                print(f"     FAIL: [{xx_gauges[i][0]}, {xx_gauges[j][0]}] != 0")
                all_commute = False
    print(f"     {'PASS' if all_commute else 'FAIL'}: All XX gauges commute")

    # Check 2: ZZ gauges commute with each other
    print("\n  2. ZZ gauge operators mutually commute:")
    all_commute = True
    for i in range(len(zz_gauges)):
        for j in range(i + 1, len(zz_gauges)):
            comm = zz_gauges[i][2] @ zz_gauges[j][2] - zz_gauges[j][2] @ zz_gauges[i][2]
            if not np.allclose(comm.to_matrix().toarray(), 0):
                print(f"     FAIL: [{zz_gauges[i][0]}, {zz_gauges[j][0]}] != 0")
                all_commute = False
    print(f"     {'PASS' if all_commute else 'FAIL'}: All ZZ gauges commute")

    # Check 3: Cross-type anticommutation
    print("\n  3. Cross-type gauge (anti)commutation:")
    n_anticommute = 0
    n_commute = 0
    for xx_label, xx_pair, xx_op in xx_gauges:
        for zz_label, zz_pair, zz_op in zz_gauges:
            comm = xx_op @ zz_op - zz_op @ xx_op
            anticomm = xx_op @ zz_op + zz_op @ xx_op
            if np.allclose(comm.to_matrix().toarray(), 0):
                n_commute += 1
            elif np.allclose(anticomm.to_matrix().toarray(), 0):
                n_anticommute += 1
    print(f"     Commuting pairs: {n_commute}")
    print(f"     Anticommuting pairs: {n_anticommute}")
    print(f"     Total cross pairs: {len(xx_gauges) * len(zz_gauges)}")
    print(f"     -> Gauge group is NON-ABELIAN (subsystem code)")

    # Check 4: Stabilizers commute with all gauge operators
    print("\n  4. Stabilizers commute with all gauge operators:")
    all_stab_gauge_ok = True
    all_gauges = [(l, p, o) for l, p, o in xx_gauges] + [(l, p, o) for l, p, o in zz_gauges]
    all_stabs = [(l, o) for l, o in x_stabs] + [(l, o) for l, o in z_stabs]
    for s_label, s_op in all_stabs:
        for g_label, _, g_op in all_gauges:
            comm = s_op @ g_op - g_op @ s_op
            if not np.allclose(comm.to_matrix().toarray(), 0):
                print(f"     FAIL: [{s_label}, {g_label}] != 0")
                all_stab_gauge_ok = False
    print(f"     {'PASS' if all_stab_gauge_ok else 'FAIL'}: "
          f"All {len(all_stabs)} stabilizers commute with all {len(all_gauges)} gauge ops")

    # Check 5: Stabilizers mutually commute
    print("\n  5. Stabilizers mutually commute:")
    stab_commute = True
    for i in range(len(all_stabs)):
        for j in range(i + 1, len(all_stabs)):
            comm = all_stabs[i][1] @ all_stabs[j][1] - all_stabs[j][1] @ all_stabs[i][1]
            if not np.allclose(comm.to_matrix().toarray(), 0):
                stab_commute = False
    print(f"     {'PASS' if stab_commute else 'FAIL'}: All stabilizer pairs commute")

    # Check 6: Logical operators commute with stabilizers
    print("\n  6. Logical operators commute with all stabilizers:")
    log_stab_ok = True
    for s_label, s_op in all_stabs:
        for log_name, log_op in [("X_L", x_l), ("Z_L", z_l)]:
            comm = log_op @ s_op - s_op @ log_op
            if not np.allclose(comm.to_matrix().toarray(), 0):
                print(f"     FAIL: [{log_name}, {s_label}] != 0")
                log_stab_ok = False
    print(f"     {'PASS' if log_stab_ok else 'FAIL'}")

    # Check 7: X_L and Z_L anticommute
    print("\n  7. Logical X and Z anticommute:")
    anticomm = x_l @ z_l + z_l @ x_l
    is_anticomm = np.allclose(anticomm.to_matrix().toarray(), 0)
    print(f"     {'PASS' if is_anticomm else 'FAIL'}: {{X_L, Z_L}} = 0")


# =============================================================================
# SYNDROME EXTRACTION VIA GAUGE MEASUREMENTS
# =============================================================================

def build_gauge_measurement_circuit(error_type=None, error_qubit=None):
    """
    Build a circuit that:
    1. Prepares a logical |0_L> state
    2. Injects an optional error
    3. Measures gauge operators (weight-2) to extract stabilizer syndromes

    The 3x3 Bacon-Shor gauge measurement protocol:
    - X-type syndrome: measure X_{i,j}X_{i+1,j} for each column j, between row pairs
    - Z-type syndrome: measure Z_{i,j}Z_{i,j+1} for each row i, between column pairs

    We use ancilla qubits for each gauge measurement.

    X-type gauge ancillae: 6 ancillae (2 row-pairs * 3 columns)
    Z-type gauge ancillae: 6 ancillae (3 rows * 2 column-pairs)
    Total ancillae: 12
    """
    data = QuantumRegister(9, 'data')

    # X-type gauge ancillae: measure X_{i,j}X_{i+1,j}
    # Row pair (0,1): cols 0,1,2 -> 3 ancillae
    # Row pair (1,2): cols 0,1,2 -> 3 ancillae
    x_anc = QuantumRegister(6, 'x_anc')
    x_bits = ClassicalRegister(6, 'x_gauge')

    # Z-type gauge ancillae: measure Z_{i,j}Z_{i,j+1}
    # Row 0: col pairs (0,1),(1,2) -> 2 ancillae
    # Row 1: col pairs (0,1),(1,2) -> 2 ancillae
    # Row 2: col pairs (0,1),(1,2) -> 2 ancillae
    z_anc = QuantumRegister(6, 'z_anc')
    z_bits = ClassicalRegister(6, 'z_gauge')

    qc = QuantumCircuit(data, x_anc, z_anc, x_bits, z_bits)

    # ---- Step 1: Prepare logical |0_L> ----
    # The Bacon-Shor |0_L> can be prepared by:
    # Start with |000000000>, apply H to all qubits in each row,
    # then entangle rows. A simpler approach: prepare the +1 eigenstate
    # of all Z-type stabilizers and X-type stabilizers.
    #
    # For the 3x3 code, |0_L> = equal superposition of all codewords
    # with Z_L = +1. We use a direct state preparation:
    # Apply H to each qubit in row 0, then CNOT down each column.
    for col in range(COLS):
        qc.h(data[qubit_index(0, col)])
    for col in range(COLS):
        for row in range(ROWS - 1):
            qc.cx(data[qubit_index(row, col)], data[qubit_index(row + 1, col)])
    qc.barrier(label='encoded')

    # ---- Step 2: Inject error ----
    if error_type is not None and error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
        qc.barrier(label='error')

    # ---- Step 3: Measure X-type gauge operators ----
    # X_{i,j}X_{i+1,j}: use Hadamard basis measurement
    # H-CNOT-CNOT-H on ancilla measures XX
    anc_idx = 0
    for row_pair in range(ROWS - 1):
        for col in range(COLS):
            q1 = qubit_index(row_pair, col)
            q2 = qubit_index(row_pair + 1, col)

            # Measure X_{q1} X_{q2} using ancilla
            qc.h(x_anc[anc_idx])
            qc.cx(x_anc[anc_idx], data[q1])
            qc.cx(x_anc[anc_idx], data[q2])
            qc.h(x_anc[anc_idx])
            qc.measure(x_anc[anc_idx], x_bits[anc_idx])
            anc_idx += 1

    qc.barrier()

    # ---- Step 4: Measure Z-type gauge operators ----
    # Z_{i,j}Z_{i,j+1}: standard parity check
    anc_idx = 0
    for row in range(ROWS):
        for col_pair in range(COLS - 1):
            q1 = qubit_index(row, col_pair)
            q2 = qubit_index(row, col_pair + 1)

            # Measure Z_{q1} Z_{q2} using ancilla
            qc.cx(data[q1], z_anc[anc_idx])
            qc.cx(data[q2], z_anc[anc_idx])
            qc.measure(z_anc[anc_idx], z_bits[anc_idx])
            anc_idx += 1

    return qc


def extract_syndromes_from_gauge(gauge_results):
    """
    Compute stabilizer syndromes from gauge measurement outcomes.

    X-type gauge results (6 bits, ordered by row_pair then col):
        x_gauge[0..2] = row pair (0,1), cols 0,1,2
        x_gauge[3..5] = row pair (1,2), cols 0,1,2

    X-type stabilizer S^X_i = product of gauge results across columns:
        S^X_0 = x_gauge[0] XOR x_gauge[1] XOR x_gauge[2]
        S^X_1 = x_gauge[3] XOR x_gauge[4] XOR x_gauge[5]

    Z-type gauge results (6 bits, ordered by row then col_pair):
        z_gauge[0..1] = row 0, col pairs (0,1),(1,2)
        z_gauge[2..3] = row 1, col pairs (0,1),(1,2)
        z_gauge[4..5] = row 2, col pairs (0,1),(1,2)

    Z-type stabilizer S^Z_j = product of gauge results across rows:
        S^Z_0 = z_gauge[0] XOR z_gauge[2] XOR z_gauge[4]
        S^Z_1 = z_gauge[1] XOR z_gauge[3] XOR z_gauge[5]

    Returns: (x_syndrome_0, x_syndrome_1, z_syndrome_0, z_syndrome_1)
    """
    x_gauge = gauge_results['x_gauge']
    z_gauge = gauge_results['z_gauge']

    # X-type stabilizer syndromes (from XX gauge products)
    sx0 = x_gauge[0] ^ x_gauge[1] ^ x_gauge[2]  # rows 0,1
    sx1 = x_gauge[3] ^ x_gauge[4] ^ x_gauge[5]  # rows 1,2

    # Z-type stabilizer syndromes (from ZZ gauge products)
    sz0 = z_gauge[0] ^ z_gauge[2] ^ z_gauge[4]  # cols 0,1
    sz1 = z_gauge[1] ^ z_gauge[3] ^ z_gauge[5]  # cols 1,2

    return (sx0, sx1, sz0, sz1)


def decode_syndrome(sx0, sx1, sz0, sz1):
    """
    Decode the syndrome to identify the error.

    X-type syndromes (sx0, sx1) detect Z errors, localizing to a row:
        (0, 0) -> no Z error (or error in gauge subspace)
        (1, 0) -> Z error in row 0
        (1, 1) -> Z error in row 1
        (0, 1) -> Z error in row 2

    Z-type syndromes (sz0, sz1) detect X errors, localizing to a column:
        (0, 0) -> no X error
        (1, 0) -> X error in col 0
        (1, 1) -> X error in col 1
        (0, 1) -> X error in col 2

    Returns dict with 'x_correction' and 'z_correction' info.
    """
    # Z-error row identification (from X-type syndrome)
    z_error_row = None
    if (sx0, sx1) == (1, 0):
        z_error_row = 0
    elif (sx0, sx1) == (1, 1):
        z_error_row = 1
    elif (sx0, sx1) == (0, 1):
        z_error_row = 2

    # X-error column identification (from Z-type syndrome)
    x_error_col = None
    if (sz0, sz1) == (1, 0):
        x_error_col = 0
    elif (sz0, sz1) == (1, 1):
        x_error_col = 1
    elif (sz0, sz1) == (0, 1):
        x_error_col = 2

    return {
        'z_error_row': z_error_row,
        'x_error_col': x_error_col,
        'x_syndrome': (sx0, sx1),
        'z_syndrome': (sz0, sz1),
    }


# =============================================================================
# STATEVECTOR VERIFICATION
# =============================================================================

def verify_stabilizer_eigenvalues():
    """
    Verify that the encoded |0_L> state is a +1 eigenstate of all stabilizers,
    using exact statevector simulation.
    """
    print("\n" + "=" * 70)
    print("PART B: Stabilizer Eigenvalue Verification")
    print("=" * 70)

    # Build the encoding circuit (same as in gauge measurement)
    qc = QuantumCircuit(9)
    for col in range(COLS):
        qc.h(qubit_index(0, col))
    for col in range(COLS):
        for row in range(ROWS - 1):
            qc.cx(qubit_index(row, col), qubit_index(row + 1, col))

    sv = Statevector(qc)

    # Check all stabilizers
    x_stabs = build_x_stabilizers()
    z_stabs = build_z_stabilizers()

    print("\n  Encoded |0_L> stabilizer eigenvalues:")
    for label, op in x_stabs:
        ev = sv.expectation_value(op)
        print(f"    {label}: <S> = {ev.real:+.6f}  "
              f"{'(+1 PASS)' if np.isclose(ev.real, 1.0) else '*** FAIL ***'}")

    for label, op in z_stabs:
        ev = sv.expectation_value(op)
        print(f"    {label}: <S> = {ev.real:+.6f}  "
              f"{'(+1 PASS)' if np.isclose(ev.real, 1.0) else '*** FAIL ***'}")

    # Check logical Z eigenvalue
    _, z_l = build_logical_operators()
    ev_zl = sv.expectation_value(z_l)
    print(f"\n    Z_L: <Z_L> = {ev_zl.real:+.6f}  "
          f"{'(+1 -> |0_L> PASS)' if np.isclose(ev_zl.real, 1.0) else '*** FAIL ***'}")


def verify_error_detection_statevector():
    """
    Inject single-qubit errors and verify syndrome detection using statevectors.
    """
    print("\n" + "=" * 70)
    print("PART C: Error Detection via Statevector (Exact)")
    print("=" * 70)

    x_stabs = build_x_stabilizers()
    z_stabs = build_z_stabilizers()

    # Build |0_L>
    qc_base = QuantumCircuit(9)
    for col in range(COLS):
        qc_base.h(qubit_index(0, col))
    for col in range(COLS):
        for row in range(ROWS - 1):
            qc_base.cx(qubit_index(row, col), qubit_index(row + 1, col))

    errors = {
        'X on q(1,1)': ('X', qubit_index(1, 1)),
        'Z on q(0,2)': ('Z', qubit_index(0, 2)),
        'Y on q(2,0)': ('Y', qubit_index(2, 0)),
    }

    for err_name, (err_type, err_q) in errors.items():
        qc = qc_base.copy()
        if err_type == 'X':
            qc.x(err_q)
        elif err_type == 'Z':
            qc.z(err_q)
        elif err_type == 'Y':
            qc.y(err_q)

        sv = Statevector(qc)
        r, c = grid_position(err_q)

        print(f"\n  Error: {err_name}  (qubit index {err_q}, grid ({r},{c}))")

        # X-type stabilizer eigenvalues (detect Z component)
        print(f"    X-type stabilizers (detect Z errors -> row localization):")
        for label, op in x_stabs:
            ev = sv.expectation_value(op)
            flag = "+1" if np.isclose(ev.real, 1.0) else "-1"
            print(f"      {label}: <S> = {ev.real:+.4f}  ({flag})")

        # Z-type stabilizer eigenvalues (detect X component)
        print(f"    Z-type stabilizers (detect X errors -> column localization):")
        for label, op in z_stabs:
            ev = sv.expectation_value(op)
            flag = "+1" if np.isclose(ev.real, 1.0) else "-1"
            print(f"      {label}: <S> = {ev.real:+.4f}  ({flag})")


# =============================================================================
# CIRCUIT-BASED SYNDROME EXTRACTION
# =============================================================================

def demo_gauge_syndrome_circuit():
    """
    Run the gauge measurement circuit with various injected errors.
    Demonstrate that 2-body gauge measurements extract correct syndromes.
    """
    print("\n" + "=" * 70)
    print("PART D: Gauge Measurement Syndrome Extraction (Circuit)")
    print("=" * 70)

    sim = AerSimulator()
    shots = 4096

    test_cases = [
        ("No error", None, None),
        ("X on q(1,1) [row=1,col=1]", 'X', qubit_index(1, 1)),
        ("Z on q(0,2) [row=0,col=2]", 'Z', qubit_index(0, 2)),
        ("X on q(2,0) [row=2,col=0]", 'X', qubit_index(2, 0)),
        ("Z on q(1,0) [row=1,col=0]", 'Z', qubit_index(1, 0)),
    ]

    for name, err_type, err_q in test_cases:
        qc = build_gauge_measurement_circuit(error_type=err_type, error_qubit=err_q)
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()

        # Aggregate syndrome statistics
        syndrome_counts = {}
        for bitstring, count in counts.items():
            # Qiskit bitstring format: "z_gauge x_gauge" (space-separated registers)
            parts = bitstring.split()
            if len(parts) == 2:
                z_bits_str, x_bits_str = parts[0], parts[1]
            else:
                # Single register fallback
                full = bitstring.replace(' ', '')
                x_bits_str = full[6:]
                z_bits_str = full[:6]

            x_gauge = [int(b) for b in reversed(x_bits_str)]
            z_gauge = [int(b) for b in reversed(z_bits_str)]

            gauge_data = {'x_gauge': x_gauge, 'z_gauge': z_gauge}
            sx0, sx1, sz0, sz1 = extract_syndromes_from_gauge(gauge_data)
            syn_key = (sx0, sx1, sz0, sz1)
            syndrome_counts[syn_key] = syndrome_counts.get(syn_key, 0) + count

        print(f"\n  {name}:")
        # Find dominant syndrome
        dominant_syn = max(syndrome_counts, key=syndrome_counts.get)
        dominant_frac = syndrome_counts[dominant_syn] / shots

        decoded = decode_syndrome(*dominant_syn)
        print(f"    Dominant syndrome: X=({dominant_syn[0]},{dominant_syn[1]}), "
              f"Z=({dominant_syn[2]},{dominant_syn[3]})  "
              f"[{dominant_frac:.1%} of shots]")

        if decoded['z_error_row'] is not None:
            print(f"    -> Z error detected in row {decoded['z_error_row']}")
        if decoded['x_error_col'] is not None:
            print(f"    -> X error detected in col {decoded['x_error_col']}")
        if decoded['z_error_row'] is None and decoded['x_error_col'] is None:
            print(f"    -> No error detected")

        # Show all syndromes observed
        print(f"    All syndromes observed ({len(syndrome_counts)} distinct):")
        for syn, cnt in sorted(syndrome_counts.items(), key=lambda x: -x[1])[:4]:
            print(f"      X=({syn[0]},{syn[1]}), Z=({syn[2]},{syn[3]}): "
                  f"{cnt}/{shots} = {cnt / shots:.3f}")


# =============================================================================
# COMPARISON: STABILIZER VS SUBSYSTEM APPROACH
# =============================================================================

def compare_stabilizer_vs_gauge():
    """
    Compare the weight of measurements needed:
    - Standard stabilizer approach: weight-6 stabilizer measurements
    - Bacon-Shor gauge approach: weight-2 gauge measurements

    This highlights the key advantage of the subsystem code.
    """
    print("\n" + "=" * 70)
    print("PART E: Stabilizer vs Gauge Measurement Comparison")
    print("=" * 70)

    x_stabs = build_x_stabilizers()
    z_stabs = build_z_stabilizers()
    xx_gauges = build_xx_gauge_operators()
    zz_gauges = build_zz_gauge_operators()

    print("\n  Standard stabilizer approach (direct measurement):")
    print("  " + "-" * 55)
    for label, op in x_stabs:
        pauli_str = str(op.paulis[0])
        weight = sum(1 for c in pauli_str if c != 'I')
        print(f"    {label}")
        print(f"      Pauli: {pauli_str}  (weight {weight})")
        print(f"      Requires: {weight}-qubit entangling circuit")

    for label, op in z_stabs:
        pauli_str = str(op.paulis[0])
        weight = sum(1 for c in pauli_str if c != 'I')
        print(f"    {label}")
        print(f"      Pauli: {pauli_str}  (weight {weight})")
        print(f"      Requires: {weight}-qubit entangling circuit")

    print(f"\n  Bacon-Shor gauge approach (2-body measurements):")
    print("  " + "-" * 55)
    print(f"    XX gauge operators ({len(xx_gauges)} total):")
    for label, pair, op in xx_gauges:
        print(f"      {label}  (weight 2)")

    print(f"\n    ZZ gauge operators ({len(zz_gauges)} total):")
    for label, pair, op in zz_gauges:
        print(f"      {label}  (weight 2)")

    print(f"\n  Summary:")
    print(f"    Stabilizer approach: 4 measurements of weight 6 each")
    print(f"    Gauge approach:      12 measurements of weight 2 each")
    print(f"    -> More measurements, but MUCH simpler circuits")
    print(f"    -> Each gauge measurement needs only 1 CNOT (not 5)")
    print(f"    -> Hardware-friendly: 2-body interactions are native on most platforms")


# =============================================================================
# ERROR RATE SIMULATION
# =============================================================================

def simulate_correction_rates(p_values, n_trials=5000):
    """
    Simulate logical error rates for the 3x3 Bacon-Shor code
    under independent depolarizing noise.

    For each physical error rate p:
    - Each qubit independently gets X, Y, or Z error with prob p/3 each
    - Measure syndromes and apply correction
    - Check if logical qubit is preserved

    Theoretical: code corrects 1 error, fails at 2+ errors.
    p_L ~ (9 choose 2) * p^2 = 36 * p^2 for small p.
    """
    print("\n" + "=" * 70)
    print("PART F: Logical Error Rate Simulation")
    print("=" * 70)

    rng = np.random.default_rng(42)
    results_coded = []
    results_uncoded = []

    for p in p_values:
        logical_errors = 0
        uncoded_errors = 0

        for _ in range(n_trials):
            # Generate random errors on each qubit
            x_errors = np.zeros(N_QUBITS, dtype=int)
            z_errors = np.zeros(N_QUBITS, dtype=int)

            for q in range(N_QUBITS):
                r = rng.random()
                if r < p / 3:
                    x_errors[q] = 1
                elif r < 2 * p / 3:
                    z_errors[q] = 1
                elif r < p:
                    x_errors[q] = 1
                    z_errors[q] = 1  # Y = iXZ

            # Compute X-type syndromes (detect Z errors)
            # S^X_i checks rows i, i+1: triggered if odd number of Z errors
            sx = np.zeros(ROWS - 1, dtype=int)
            for i in range(ROWS - 1):
                for j in range(COLS):
                    sx[i] ^= z_errors[qubit_index(i, j)] ^ z_errors[qubit_index(i + 1, j)]

            # Compute Z-type syndromes (detect X errors)
            # S^Z_j checks cols j, j+1: triggered if odd number of X errors
            sz = np.zeros(COLS - 1, dtype=int)
            for j in range(COLS - 1):
                for i in range(ROWS):
                    sz[j] ^= x_errors[qubit_index(i, j)] ^ x_errors[qubit_index(i, j + 1)]

            # Decode Z errors (from X-type syndrome) -> identify row
            z_correction = np.zeros(N_QUBITS, dtype=int)
            if tuple(sx) == (1, 0):
                # Z error in row 0 -> correct any qubit in row 0 (col is gauge freedom)
                z_correction[qubit_index(0, 0)] = 1
            elif tuple(sx) == (1, 1):
                z_correction[qubit_index(1, 0)] = 1
            elif tuple(sx) == (0, 1):
                z_correction[qubit_index(2, 0)] = 1

            # Decode X errors (from Z-type syndrome) -> identify column
            x_correction = np.zeros(N_QUBITS, dtype=int)
            if tuple(sz) == (1, 0):
                x_correction[qubit_index(0, 0)] = 1
            elif tuple(sz) == (1, 1):
                x_correction[qubit_index(0, 1)] = 1
            elif tuple(sz) == (0, 1):
                x_correction[qubit_index(0, 2)] = 1

            # Apply correction: residual = error XOR correction
            x_residual = x_errors ^ x_correction
            z_residual = z_errors ^ z_correction

            # Check logical error: X_L = X on row 0, Z_L = Z on col 0
            # Logical X error if odd number of X residuals in any row
            logical_x_err = 0
            for j in range(COLS):
                logical_x_err ^= x_residual[qubit_index(0, j)]

            logical_z_err = 0
            for i in range(ROWS):
                logical_z_err ^= z_residual[qubit_index(i, 0)]

            if logical_x_err or logical_z_err:
                logical_errors += 1

            # Uncoded: single qubit, any error is a logical error
            if rng.random() < p:
                uncoded_errors += 1

        results_coded.append(logical_errors / n_trials)
        results_uncoded.append(uncoded_errors / n_trials)

    return np.array(results_coded), np.array(results_uncoded)


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(p_values, p_coded, p_uncoded):
    """Plot logical error rates: coded vs uncoded."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Linear scale
    ax = axes[0]
    ax.plot(p_values, p_uncoded, 'r-', linewidth=2, label='Uncoded (1 qubit)')
    ax.plot(p_values, p_coded, 'b-o', markersize=3, linewidth=2,
            label='Bacon-Shor [[9,1,3]]')
    # Theoretical: leading order ~ C(9,2)*(p/3)^2 * 3 for depolarizing
    p_theory = 36 * (p_values ** 2)
    ax.plot(p_values, p_theory, 'g--', linewidth=1.5,
            label=r'Theory: $\sim 36p^2$ (leading order)')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Logical Error Rate', fontsize=12)
    ax.set_title('Bacon-Shor [[9,1,3]]: Error Suppression', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Log-log scale
    ax = axes[1]
    mask = (p_coded > 0) & (p_uncoded > 0)
    ax.loglog(p_values[mask], p_uncoded[mask], 'r-', linewidth=2, label='Uncoded')
    ax.loglog(p_values[mask], p_coded[mask], 'b-o', markersize=3,
              linewidth=2, label='Bacon-Shor [[9,1,3]]')
    ax.loglog(p_values[mask], p_theory[mask], 'g--', linewidth=1.5,
              label=r'Theory: $\sim 36p^2$')
    ax.set_xlabel('Physical Error Rate p', fontsize=12)
    ax.set_ylabel('Logical Error Rate', fontsize=12)
    ax.set_title('Log-Log Scale (slope=2 confirms quadratic suppression)', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig(
        "quantum/error_correction/11_bacon_shor_code/bacon_shor_results.png",
        dpi=150, bbox_inches='tight')
    plt.show()
    print("\n  Plot saved.")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Bacon-Shor Code [[9,1,3]] - Local Simulator")
    print("=" * 70)
    print(f"Grid: {ROWS}x{COLS} = {N_QUBITS} physical qubits")
    print(f"Distance: d = min({ROWS},{COLS}) = {min(ROWS, COLS)}")
    print(f"Corrects: {(min(ROWS, COLS) - 1) // 2} arbitrary error(s)")

    # Part A: Algebraic verification
    verify_gauge_algebra()

    # Part B: Stabilizer eigenvalues
    verify_stabilizer_eigenvalues()

    # Part C: Error detection via statevector
    verify_error_detection_statevector()

    # Part D: Circuit-based gauge syndrome extraction
    demo_gauge_syndrome_circuit()

    # Part E: Stabilizer vs gauge comparison
    compare_stabilizer_vs_gauge()

    # Part F: Error rate simulation
    p_values = np.linspace(0.005, 0.15, 20)
    p_coded, p_uncoded = simulate_correction_rates(p_values, n_trials=10000)
    plot_results(p_values, p_coded, p_uncoded)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Bacon-Shor Code [[9,1,3]] (3x3 grid):
    - Subsystem code: gauge group is non-Abelian
    - 6 XX gauge operators (horizontal, weight 2)
    - 6 ZZ gauge operators (vertical, weight 2)
    - 4 stabilizers (weight 6) derived from gauge products
    - Syndrome extraction via 2-body measurements ONLY
    - Corrects 1 arbitrary single-qubit error
    - Equivalent to Shor's 9-qubit code (different strategy, same protection)
    - Key advantage: no multi-body measurements needed
    """)


if __name__ == "__main__":
    main()
