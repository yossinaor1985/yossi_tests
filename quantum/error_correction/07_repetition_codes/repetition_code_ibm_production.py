"""
Repetition Codes - IBM Production-Ready Implementation
======================================================

Production workflow for repetition code error correction on IBM hardware.
Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Implements d-qubit repetition codes with syndrome extraction
and majority vote decoding for d=3,5,7.
"""

import json
import os
from datetime import datetime

import numpy as np
from scipy.special import comb
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session

RESULTS_DIR = "quantum/error_correction/07_repetition_codes/production_results"


def build_repetition_circuit(d, error_qubits=None):
    """
    Build full repetition code circuit: encode -> error -> syndrome -> measure.

    d data qubits, d-1 syndrome ancillas.
    Encoding: CNOT chain from q0 to q1, ..., q_{d-1}.
    Syndrome: nearest-neighbor Z-parity checks.
    """
    data = QuantumRegister(d, 'd')
    n_syn = d - 1
    syn = QuantumRegister(n_syn, 's')
    syn_bits = ClassicalRegister(n_syn, 'syn')
    out = ClassicalRegister(d, 'out')
    qc = QuantumCircuit(data, syn, syn_bits, out)

    # Encode
    for i in range(1, d):
        qc.cx(data[0], data[i])
    qc.barrier()

    # Error injection
    if error_qubits is not None:
        for eq in error_qubits:
            qc.x(data[eq])
    qc.barrier()

    # Syndrome measurement
    for i in range(n_syn):
        qc.cx(data[i], syn[i])
        qc.cx(data[i + 1], syn[i])
    for i in range(n_syn):
        qc.measure(syn[i], syn_bits[i])
    qc.barrier()

    # Measure all data qubits (for post-processing)
    for i in range(d):
        qc.measure(data[i], out[i])

    return qc


def majority_vote_decode(data_bits_str, d):
    """Decode by majority vote on measured data qubits."""
    n_ones = sum(int(b) for b in data_bits_str)
    return 1 if n_ones > d / 2 else 0


def theoretical_error_rate(d, p):
    """Theoretical logical error rate for d-qubit repetition code."""
    t = d // 2
    p_l = 0.0
    for j in range(t + 1, d + 1):
        p_l += comb(d, j, exact=True) * (p ** j) * ((1 - p) ** (d - j))
    return p_l


def run_production():
    print("=" * 70)
    print("Repetition Codes - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    sim = AerSimulator()
    shots = 8192

    # --- IBM Session Management (template) ---
    # service = QiskitRuntimeService(channel="ibm_quantum")
    # backend = service.least_busy(simulator=False, min_num_qubits=15)
    # session = Session(service=service, backend=backend)
    # sampler = SamplerV2(session=session)

    results = {}

    for d in [3, 5, 7]:
        print(f"\n  --- d={d} Repetition Code ---")
        d_results = {}

        test_cases = [
            (None, "No error"),
            ([0], "X on q0"),
            ([d // 2], f"X on q{d // 2}"),
        ]
        # Add multi-error test within correction capacity
        if d >= 5:
            test_cases.append(([0, d - 1], f"X on q0,q{d-1}"))

        for err_qubits, label in test_cases:
            qc = build_repetition_circuit(d, err_qubits)
            counts = sim.run(qc, shots=shots).result().get_counts()

            # Majority vote decoding on data bits
            correct = 0
            total = 0
            for bitstring, count in counts.items():
                parts = bitstring.split()
                data_bits = parts[0]  # Data qubits (leftmost register)
                decoded = majority_vote_decode(data_bits, d)
                if decoded == 0:  # We encoded |0>
                    correct += count
                total += count

            acc = correct / total if total > 0 else 0
            d_results[label] = {
                "accuracy": acc,
                "counts_sample": dict(list(counts.items())[:3]),
            }
            print(f"    {label}: accuracy = {acc:.4f}")

        # Theoretical error rates at sample p values
        d_results["theoretical"] = {
            f"p={p:.2f}": theoretical_error_rate(d, p)
            for p in [0.01, 0.05, 0.1, 0.2]
        }

        results[f"d={d}"] = d_results

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_data = {
        "timestamp": datetime.now().isoformat(),
        "code": "repetition codes",
        "distances": [3, 5, 7],
        "shots": shots,
        "results": results,
    }
    with open(os.path.join(RESULTS_DIR, "results.json"), 'w') as f:
        json.dump(out_data, f, indent=2, default=str)

    print(f"\n  Results saved to {RESULTS_DIR}")
    print(f"\n  Production notes:")
    print(f"    - d=3: 3+2=5 qubits, d=5: 5+4=9 qubits, d=7: 7+6=13 qubits")
    print(f"    - Linear connectivity sufficient (nearest-neighbor)")
    print(f"    - Majority vote decoding is O(d)")
    print(f"    - Good benchmark for hardware noise characterization")
    print(f"    - Only corrects bit-flip errors (not phase-flip)")


if __name__ == "__main__":
    run_production()
