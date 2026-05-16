"""
Stabilizer Formalism - IBM Production-Ready Implementation
==========================================================

Production workflow demonstrating stabilizer formalism concepts
on IBM hardware (via AerSimulator).
Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Demonstrates syndrome extraction using stabilizer measurements
for the [[5,1,3]] perfect code and Steane code.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = ("quantum/error_correction/06_stabilizer_formalism/"
               "production_results")


def measure_stabilizer(qc, data, ancilla, c_bit, stabilizer_label):
    """
    Append stabilizer measurement circuit.

    For each qubit position in stabilizer_label:
        I -> do nothing
        X -> H-CNOT-H pattern (or: ancilla in |+>, CNOT, then H-measure)
        Y -> S^dag-H-CNOT-H-S pattern
        Z -> CNOT pattern

    Simplified approach: use ancilla in |+> for X, |0> for Z.
    """
    n = len(stabilizer_label)

    # Determine if stabilizer is all-X, all-Z, or mixed
    has_x = 'X' in stabilizer_label
    has_z = 'Z' in stabilizer_label

    if has_x and not has_z:
        # X-type stabilizer: ancilla in |+>, CNOT(ancilla, data), measure in X
        qc.h(ancilla)
        for i in range(n):
            if stabilizer_label[i] == 'X':
                qc.cx(ancilla, data[n - 1 - i])
        qc.h(ancilla)
        qc.measure(ancilla, c_bit)
    elif has_z and not has_x:
        # Z-type stabilizer: CNOT(data, ancilla), measure ancilla
        for i in range(n):
            if stabilizer_label[i] == 'Z':
                qc.cx(data[n - 1 - i], ancilla)
        qc.measure(ancilla, c_bit)
    else:
        # Mixed stabilizer: general approach
        qc.h(ancilla)
        for i in range(n):
            qubit_idx = n - 1 - i
            if stabilizer_label[i] == 'X':
                qc.cx(ancilla, data[qubit_idx])
            elif stabilizer_label[i] == 'Z':
                qc.cz(ancilla, data[qubit_idx])
            elif stabilizer_label[i] == 'Y':
                qc.sdg(data[qubit_idx])
                qc.cx(ancilla, data[qubit_idx])
                qc.s(data[qubit_idx])
        qc.h(ancilla)
        qc.measure(ancilla, c_bit)


def build_five_qubit_syndrome_circuit(error_type=None, error_qubit=None):
    """
    Build syndrome extraction circuit for [[5,1,3]] code.

    Stabilizer generators:
        g1 = XZZXI
        g2 = IXZZX
        g3 = XIXZZ
        g4 = ZXIXZ

    4 ancilla qubits for 4 generators.
    """
    generators = ['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ']

    data = QuantumRegister(5, 'd')
    anc = QuantumRegister(4, 'a')
    syn_bits = ClassicalRegister(4, 'syn')
    qc = QuantumCircuit(data, anc, syn_bits)

    # Prepare a state in the code space (simplified: just |00000>)
    # In practice, would use proper encoding circuit
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

    # Measure each stabilizer
    for i, gen in enumerate(generators):
        measure_stabilizer(qc, data, anc[i], syn_bits[i], gen)

    return qc


def build_steane_syndrome_circuit(error_type=None, error_qubit=None):
    """
    Build syndrome extraction for [[7,1,3]] Steane code.

    Uses CSS structure: separate X and Z syndrome extraction.
    X-stabilizers: XIXIXIX, IXXIIXX, IIIXXXX
    Z-stabilizers: ZIZIZIZ, IZZIIIZZ[:7], IIIZZZZ
    """
    data = QuantumRegister(7, 'd')
    x_anc = QuantumRegister(3, 'xa')
    z_anc = QuantumRegister(3, 'za')
    x_bits = ClassicalRegister(3, 'xsyn')
    z_bits = ClassicalRegister(3, 'zsyn')
    qc = QuantumCircuit(data, x_anc, z_anc, x_bits, z_bits)

    # Steane encoding (simplified for |0_L>)
    qc.h(data[0])
    qc.h(data[1])
    qc.h(data[3])
    qc.cx(data[0], data[2])
    qc.cx(data[0], data[4])
    qc.cx(data[0], data[6])
    qc.cx(data[1], data[2])
    qc.cx(data[1], data[5])
    qc.cx(data[1], data[6])
    qc.cx(data[3], data[4])
    qc.cx(data[3], data[5])
    qc.cx(data[3], data[6])
    qc.barrier()

    # Error injection
    if error_type is not None and error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
    qc.barrier()

    # Z-syndrome (detect X errors): CNOT from data to ancilla
    z_positions = [[0, 2, 4, 6], [1, 2, 5, 6], [3, 4, 5, 6]]
    for i, positions in enumerate(z_positions):
        for pos in positions:
            qc.cx(data[pos], z_anc[i])
    for i in range(3):
        qc.measure(z_anc[i], z_bits[i])
    qc.barrier()

    # X-syndrome (detect Z errors): ancilla in |+>, CNOT to data
    x_positions = [[0, 2, 4, 6], [1, 2, 5, 6], [3, 4, 5, 6]]
    for i in range(3):
        qc.h(x_anc[i])
    for i, positions in enumerate(x_positions):
        for pos in positions:
            qc.cx(x_anc[i], data[pos])
    for i in range(3):
        qc.h(x_anc[i])
    for i in range(3):
        qc.measure(x_anc[i], x_bits[i])

    return qc


def run_production():
    print("=" * 70)
    print("Stabilizer Formalism - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    sim = AerSimulator()
    shots = 8192

    # --- IBM Session Management (template) ---
    # service = QiskitRuntimeService(channel="ibm_quantum")
    # backend = service.least_busy(simulator=False, min_num_qubits=13)
    # session = Session(service=service, backend=backend)
    # sampler = SamplerV2(session=session)

    results = {}

    # Test [[5,1,3]] code syndrome extraction
    print("\n  [[5,1,3]] Perfect Code Syndromes:")
    five_qubit_results = {}
    test_errors = [
        (None, None, "No error"),
        ('X', 0, "X on q0"),
        ('X', 2, "X on q2"),
        ('Z', 1, "Z on q1"),
        ('Z', 4, "Z on q4"),
    ]

    for etype, qidx, label in test_errors:
        qc = build_five_qubit_syndrome_circuit(etype, qidx)
        counts = sim.run(qc, shots=shots).result().get_counts()
        dominant = max(counts, key=counts.get)
        five_qubit_results[label] = {
            "dominant_syndrome": dominant,
            "counts_sample": dict(list(counts.items())[:3]),
        }
        print(f"    {label}: syndrome = {dominant}")

    results["five_qubit_code"] = five_qubit_results

    # Test Steane code syndrome extraction
    print("\n  Steane [[7,1,3]] Code Syndromes:")
    steane_results = {}
    test_errors_steane = [
        (None, None, "No error"),
        ('X', 0, "X on q0"),
        ('X', 3, "X on q3"),
        ('Z', 1, "Z on q1"),
        ('Z', 6, "Z on q6"),
    ]

    for etype, qidx, label in test_errors_steane:
        qc = build_steane_syndrome_circuit(etype, qidx)
        counts = sim.run(qc, shots=shots).result().get_counts()
        dominant = max(counts, key=counts.get)
        steane_results[label] = {
            "dominant_syndrome": dominant,
            "counts_sample": dict(list(counts.items())[:3]),
        }
        print(f"    {label}: syndrome = {dominant}")

    results["steane_code"] = steane_results

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_data = {
        "timestamp": datetime.now().isoformat(),
        "topic": "stabilizer_formalism",
        "shots": shots,
        "results": results,
    }
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(out_data, f, indent=2, default=str)

    print(f"\n  Results saved to {RESULTS_DIR}")
    print(f"\n  Production notes:")
    print(f"    - [[5,1,3]] code: 5+4=9 qubits, mixed stabilizers")
    print(f"    - Steane code: 7+6=13 qubits, CSS stabilizers")
    print(f"    - General stabilizer measurement uses ancilla-based scheme")
    print(f"    - Mixed Paulis (e.g. XZZXI) require CZ and controlled-S gates")
    print(f"    - CSS codes simplify to only CNOT-based measurements")


if __name__ == "__main__":
    run_production()
