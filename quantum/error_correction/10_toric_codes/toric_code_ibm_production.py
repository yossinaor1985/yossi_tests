"""
Toric Codes - IBM Production-Ready Implementation
==================================================

Production workflow for the d=2 toric code on IBM hardware.
Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

The toric code is a topological code on a periodic lattice (torus)
that encodes 2 logical qubits with topological protection.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/error_correction/10_toric_codes/production_results"

L = 2
N_QUBITS = 2 * L * L  # 8


def edge_h(r, c):
    """Horizontal edge index."""
    return r * L + c


def edge_v(r, c):
    """Vertical edge index."""
    return L * L + r * L + c


# Vertex operators: X on edges meeting at vertex
VERTEX_OPS = {}
for r in range(L):
    for c in range(L):
        VERTEX_OPS[f'A({r},{c})'] = [
            edge_h(r, c),
            edge_h(r, (c - 1) % L),
            edge_v(r, c),
            edge_v((r - 1) % L, c),
        ]

# Plaquette operators: Z on edges around face
PLAQUETTE_OPS = {}
for r in range(L):
    for c in range(L):
        PLAQUETTE_OPS[f'B({r},{c})'] = [
            edge_h(r, c),
            edge_h((r + 1) % L, c),
            edge_v(r, c),
            edge_v(r, (c + 1) % L),
        ]


def build_toric_syndrome_circuit(error_type=None, error_qubit=None):
    """
    Build syndrome extraction circuit for d=2 toric code.

    8 data qubits + 4 vertex ancillas + 4 plaquette ancillas = 16 qubits.
    """
    data = QuantumRegister(N_QUBITS, 'd')
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

    # Vertex syndrome (X-type, detect Z errors)
    v_list = list(VERTEX_OPS.values())
    for i, edges in enumerate(v_list):
        qc.h(v_anc[i])
        for e in edges:
            qc.cx(v_anc[i], data[e])
        qc.h(v_anc[i])
        qc.measure(v_anc[i], v_bits[i])
    qc.barrier()

    # Plaquette syndrome (Z-type, detect X errors)
    p_list = list(PLAQUETTE_OPS.values())
    for i, edges in enumerate(p_list):
        for e in edges:
            qc.cx(data[e], p_anc[i])
        qc.measure(p_anc[i], p_bits[i])

    return qc


def run_production():
    print("=" * 70)
    print("Toric Code (d=2) - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    sim = AerSimulator()
    shots = 8192

    # --- IBM Session Management (template) ---
    # service = QiskitRuntimeService(channel="ibm_quantum")
    # backend = service.least_busy(simulator=False, min_num_qubits=16)
    # session = Session(service=service, backend=backend)
    # sampler = SamplerV2(session=session)

    test_cases = [
        (None, None, "No error"),
        ('X', 0, "X on e0 (horiz edge)"),
        ('X', 4, "X on e4 (vert edge)"),
        ('Z', 0, "Z on e0 (horiz edge)"),
        ('Z', 5, "Z on e5 (vert edge)"),
        ('Y', 2, "Y on e2 (horiz edge)"),
    ]

    results = {}
    for etype, qidx, label in test_cases:
        qc = build_toric_syndrome_circuit(etype, qidx)
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

    # Code parameters summary
    print(f"\n  Code parameters: [[{N_QUBITS}, 2, {L}]]")
    print(f"  Logical qubits: 2 (4-fold degeneracy)")
    print(f"  Distance: {L} (corrects {(L-1)//2} errors)")

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_data = {
        "timestamp": datetime.now().isoformat(),
        "code": f"toric code d={L}",
        "parameters": {
            "n": N_QUBITS,
            "k": 2,
            "d": L,
            "total_qubits": N_QUBITS + 8,
        },
        "shots": shots,
        "results": results,
    }
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(out_data, f, indent=2, default=str)

    print(f"\n  Results saved to {RESULTS_DIR}")
    print(f"\n  Production notes:")
    print(f"    - 16 qubits: 8 data + 4 vertex ancilla + 4 plaquette ancilla")
    print(f"    - Periodic boundary conditions (torus topology)")
    print(f"    - Weight-4 stabilizers (local)")
    print(f"    - 2 logical qubits from topological degeneracy")
    print(f"    - Distance only 2 for L=2 (minimal, for demonstration)")
    print(f"    - L=3 gives distance 3: [[18, 2, 3]] with 26 total qubits")


if __name__ == "__main__":
    run_production()
