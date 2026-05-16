"""
Surface Codes - IBM Production-Ready Implementation
====================================================

Production workflow for d=3 surface code on IBM hardware.
Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Implements syndrome extraction for the d=3 rotated surface code
with 9 data qubits and 8 syndrome ancillas.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/error_correction/08_surface_codes/production_results"

# Surface code stabilizer definitions
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


def build_surface_code_circuit(error_type=None, error_qubit=None):
    """
    Build syndrome extraction circuit for d=3 surface code.

    9 data qubits + 4 X-ancillas + 4 Z-ancillas = 17 qubits.
    X-stabilizers: ancilla in |+>, CNOT to data, measure in X-basis.
    Z-stabilizers: CNOT from data to ancilla, measure in Z-basis.
    """
    data = QuantumRegister(9, 'd')
    x_anc = QuantumRegister(4, 'xa')
    z_anc = QuantumRegister(4, 'za')
    x_bits = ClassicalRegister(4, 'x_syn')
    z_bits = ClassicalRegister(4, 'z_syn')
    qc = QuantumCircuit(data, x_anc, z_anc, x_bits, z_bits)

    # Initialize in |0_L> (all zeros for simplicity)
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

    # X-stabilizer measurement
    x_stab_list = list(X_STABILIZERS.values())
    for i, qubits in enumerate(x_stab_list):
        qc.h(x_anc[i])
        for q in qubits:
            qc.cx(x_anc[i], data[q])
        qc.h(x_anc[i])
        qc.measure(x_anc[i], x_bits[i])
    qc.barrier()

    # Z-stabilizer measurement
    z_stab_list = list(Z_STABILIZERS.values())
    for i, qubits in enumerate(z_stab_list):
        for q in qubits:
            qc.cx(data[q], z_anc[i])
        qc.measure(z_anc[i], z_bits[i])

    return qc


def lookup_decode(x_syndrome, z_syndrome):
    """
    Simple lookup decoder for d=3 surface code.

    X-syndrome identifies Z error location.
    Z-syndrome identifies X error location.
    """
    # X-error lookup from Z-syndrome
    x_correction = None
    for q in range(9):
        z_syn = tuple(1 if q in qubits else 0
                      for qubits in Z_STABILIZERS.values())
        if z_syn == z_syndrome:
            x_correction = q
            break

    # Z-error lookup from X-syndrome
    z_correction = None
    for q in range(9):
        x_syn = tuple(1 if q in qubits else 0
                      for qubits in X_STABILIZERS.values())
        if x_syn == x_syndrome:
            z_correction = q
            break

    return x_correction, z_correction


def run_production():
    print("=" * 70)
    print("Surface Code (d=3) - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    sim = AerSimulator()
    shots = 8192

    # --- IBM Session Management (template) ---
    # service = QiskitRuntimeService(channel="ibm_quantum")
    # backend = service.least_busy(simulator=False, min_num_qubits=17)
    # session = Session(service=service, backend=backend)
    # sampler = SamplerV2(session=session)

    test_cases = [
        (None, None, "No error"),
        ('X', 0, "X on q0 (corner)"),
        ('X', 4, "X on q4 (center)"),
        ('X', 8, "X on q8 (corner)"),
        ('Z', 1, "Z on q1 (edge)"),
        ('Z', 4, "Z on q4 (center)"),
        ('Y', 4, "Y on q4 (center)"),
    ]

    results = {}
    for etype, qidx, label in test_cases:
        qc = build_surface_code_circuit(etype, qidx)
        counts = sim.run(qc, shots=shots).result().get_counts()

        dominant = max(counts, key=counts.get)
        fraction = counts[dominant] / shots

        results[label] = {
            "dominant_syndrome": dominant,
            "dominant_fraction": fraction,
            "counts_sample": dict(list(counts.items())[:3]),
        }
        print(f"\n  {label}:")
        print(f"    Dominant syndrome: {dominant} ({fraction:.3f})")

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_data = {
        "timestamp": datetime.now().isoformat(),
        "code": "surface code d=3",
        "parameters": {"n": 9, "k": 1, "d": 3, "total_qubits": 17},
        "shots": shots,
        "results": results,
    }
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(out_data, f, indent=2, default=str)

    print(f"\n  Results saved to {RESULTS_DIR}")
    print(f"\n  Production notes:")
    print(f"    - 17 qubits: 9 data + 4 X-ancilla + 4 Z-ancilla")
    print(f"    - Only nearest-neighbor connectivity needed")
    print(f"    - Weight-4 stabilizers (local measurements)")
    print(f"    - Threshold ~1% for circuit-level noise")
    print(f"    - Real-time decoding needed for repeated rounds")
    print(f"    - Consider MWPM decoder for production use")


if __name__ == "__main__":
    run_production()
