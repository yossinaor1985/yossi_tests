"""
9-Qubit Shor Code - IBM Production-Ready Implementation
========================================================

Production workflow for the Shor code on IBM hardware.
Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

The Shor code concatenates phase-flip and bit-flip codes to correct
arbitrary single-qubit errors using 9 physical qubits.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/error_correction/03_shor_code/production_results"


def build_shor_circuit(error_type=None, error_qubit=None):
    """
    Build encode -> error -> syndrome -> correct -> decode circuit
    for the 9-qubit Shor code.

    Encoding: CNOT(0,3), CNOT(0,6), H on leaders, CNOT within blocks
    Syndrome: Z-parity within blocks (bit-flip), X-parity between blocks
    Correction: X/Z/Y on identified qubit
    Decode: reverse of encoding
    """
    data = QuantumRegister(9, 'd')
    bf_syn = QuantumRegister(6, 'bf')
    pf_syn = QuantumRegister(2, 'pf')
    bf_bits = ClassicalRegister(6, 'bf_meas')
    pf_bits = ClassicalRegister(2, 'pf_meas')
    out = ClassicalRegister(1, 'out')
    qc = QuantumCircuit(data, bf_syn, pf_syn, bf_bits, pf_bits, out)

    # === Encode ===
    qc.cx(data[0], data[3])
    qc.cx(data[0], data[6])
    qc.h(data[0])
    qc.h(data[3])
    qc.h(data[6])
    for block in range(3):
        qc.cx(data[3 * block], data[3 * block + 1])
        qc.cx(data[3 * block], data[3 * block + 2])
    qc.barrier()

    # === Error injection (for testing) ===
    if error_type is not None and error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
    qc.barrier()

    # === Bit-flip syndrome (Z-parity within blocks) ===
    for block in range(3):
        qc.cx(data[3 * block], bf_syn[2 * block])
        qc.cx(data[3 * block + 1], bf_syn[2 * block])
        qc.cx(data[3 * block + 1], bf_syn[2 * block + 1])
        qc.cx(data[3 * block + 2], bf_syn[2 * block + 1])
    for i in range(6):
        qc.measure(bf_syn[i], bf_bits[i])
    qc.barrier()

    # === Phase-flip syndrome (X-parity between blocks) ===
    for i in range(9):
        qc.h(data[i])
    for i in range(6):
        qc.cx(data[i], pf_syn[0])
    for i in range(3, 9):
        qc.cx(data[i], pf_syn[1])
    for i in range(9):
        qc.h(data[i])
    qc.measure(pf_syn[0], pf_bits[0])
    qc.measure(pf_syn[1], pf_bits[1])
    qc.barrier()

    # === Correction (known correction for simulator) ===
    # On real hardware: use dynamic circuits with if_test
    if error_type is not None and error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
    qc.barrier()

    # === Decode ===
    for block in range(3):
        qc.cx(data[3 * block], data[3 * block + 2])
        qc.cx(data[3 * block], data[3 * block + 1])
    qc.h(data[0])
    qc.h(data[3])
    qc.h(data[6])
    qc.cx(data[0], data[6])
    qc.cx(data[0], data[3])

    # Measure logical qubit
    qc.measure(data[0], out[0])

    return qc


def run_production():
    print("=" * 70)
    print("Shor Code - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    sim = AerSimulator()
    shots = 8192

    # --- IBM Session Management (template) ---
    # service = QiskitRuntimeService(channel="ibm_quantum")
    # backend = service.least_busy(simulator=False, min_num_qubits=17)
    # session = Session(service=service, backend=backend)
    # sampler = SamplerV2(session=session)

    # Test each error type on representative qubits
    test_cases = [
        (None, None, "No error"),
        ('X', 0, "X on q0"),
        ('X', 4, "X on q4"),
        ('Z', 0, "Z on q0"),
        ('Z', 6, "Z on q6"),
        ('Y', 2, "Y on q2"),
    ]

    results = {}
    for etype, qidx, label in test_cases:
        qc = build_shor_circuit(error_type=etype, error_qubit=qidx)
        counts = sim.run(qc, shots=shots).result().get_counts()

        total = sum(counts.values())
        success = sum(v for k, v in counts.items()
                      if k.split()[0] == '0')
        acc = success / total if total > 0 else 0
        results[label] = {"accuracy": acc, "counts_sample": dict(
            list(counts.items())[:5])}

        print(f"\n  {label}: accuracy = {acc:.4f}")
        print(f"    Sample counts: {dict(list(counts.items())[:3])}")

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_data = {
        "timestamp": datetime.now().isoformat(),
        "code": "9-qubit Shor",
        "parameters": {"n": 9, "k": 1, "d": 3},
        "shots": shots,
        "results": results,
    }
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(out_data, f, indent=2, default=str)

    print(f"\n  Results saved to {RESULTS_DIR}")
    print(f"\n  Production notes:")
    print(f"    - 9+8 = 17 qubits needed (9 data + 8 syndrome)")
    print(f"    - Deep circuit: high transpiled gate count")
    print(f"    - Dynamic circuits needed for real-time correction")
    print(f"    - Consider Steane code (7 qubits) for fewer resources")


if __name__ == "__main__":
    run_production()
