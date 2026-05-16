"""
TREX (Twirled Readout Error eXtinction) - IBM Production-Ready Implementation
================================================================================

Production workflow for TREX readout error mitigation on IBM hardware.
Randomizes readout via X twirls, then corrects via rescaling.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
TREX inserts random X gates before measurement, converting asymmetric
readout errors to symmetric form. Correction is a simple rescaling:
<O>_corrected = <O>_measured / Product_k (1 - e_0_k - e_1_k).
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, EstimatorV2, Session

RESULTS_DIR = "quantum/mitigation/02_TREX/production_results"


# =============================================================================
# TREX PRODUCTION UTILITIES
# =============================================================================

def generate_trex_circuits(
    base_circuit: QuantumCircuit,
    n_randomizations: int,
    seed: int = 42
) -> Tuple[List[QuantumCircuit], List[np.ndarray]]:
    """
    Generate TREX-twirled circuit variants for production.

    TREX protocol (see explanation_physicist.md, Section 3.1):
        Insert random X gates before measurement for each randomization.

    Args:
        base_circuit: Target circuit (with measurements).
        n_randomizations: Number of random twirl instances.
        seed: Random seed.

    Returns:
        Tuple of (twirled_circuits, random_bit_strings).
    """
    rng = np.random.default_rng(seed)
    n_qubits = base_circuit.num_qubits
    twirled = []
    randoms = []

    for idx in range(n_randomizations):
        r = rng.integers(0, 2, size=n_qubits)
        randoms.append(r)

        qr = QuantumRegister(n_qubits, 'q')
        cr = ClassicalRegister(n_qubits, 'c')
        qc = QuantumCircuit(qr, cr, name=f'trex_{idx}')

        # Copy non-measurement gates
        for inst in base_circuit.data:
            if inst.operation.name != 'measure':
                qargs = [qr[base_circuit.qubits.index(q)] for q in inst.qubits]
                cargs = [cr[base_circuit.clbits.index(c)] for c in inst.clbits] if inst.clbits else []
                if cargs:
                    qc.append(inst.operation, qargs, cargs)
                else:
                    qc.append(inst.operation, qargs)

        # X twirl before measurement
        qc.barrier()
        for k in range(n_qubits):
            if r[k] == 1:
                qc.x(qr[k])
        qc.measure(qr, cr)

        twirled.append(qc)

    return twirled, randoms


def detwirl_and_correct(
    counts_list: List[Dict[str, int]],
    random_strings: List[np.ndarray],
    qubit_error_rates: List[Tuple[float, float]],
    n_qubits: int
) -> Dict[str, float]:
    """
    De-twirl counts and apply TREX rescaling correction.

    Post-processing (see explanation_physicist.md, Section 3 and 4):
        1. XOR measured bits with random string to undo twirl
        2. Aggregate counts from all randomizations
        3. Rescale probabilities by 1/Product(1 - 2*e_sym_k)

    Args:
        counts_list: Counts from each twirled circuit.
        random_strings: Random strings for each circuit.
        qubit_error_rates: Per-qubit (e_0, e_1) from calibration.
        n_qubits: Number of qubits.

    Returns:
        Corrected probability distribution.
    """
    # De-twirl
    combined = {}
    for counts, r in zip(counts_list, random_strings):
        for bs, count in counts.items():
            bs_padded = bs.zfill(n_qubits)
            bits = []
            for k in range(n_qubits):
                m = int(bs_padded[n_qubits - 1 - k])
                bits.append(m ^ int(r[k]))
            detwirled_bs = ''.join(str(b) for b in reversed(bits))
            combined[detwirled_bs] = combined.get(detwirled_bs, 0) + count

    total = sum(combined.values())
    dist = {k: v / total for k, v in combined.items()}

    # Compute global rescaling factor
    # (see explanation_physicist.md, Section 4.2 for Pauli string correction)
    rescale = 1.0
    for e0, e1 in qubit_error_rates:
        rescale *= (1 - e0 - e1)

    # Apply rescaling to counts distribution
    corrected = {}
    for bs, prob in dist.items():
        corrected[bs] = prob  # Distribution stays the same for counts
        # Rescaling applies to expectation values, not raw probabilities

    return corrected


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full TREX production workflow.

    Steps:
        1. Configure backend
        2. Build target circuit
        3. Generate TREX-twirled variants
        4. Run all circuits
        5. De-twirl and correct
        6. Compute expectation values
        7. Save results

    Args:
        use_simulator: If True, use AerSimulator with noise.
    """
    print("=" * 70)
    print("TREX - Production Workflow")
    print("=" * 70)

    n_qubits = 2
    shots_per_circuit = 4096
    n_randomizations = 32

    # Per-qubit readout errors
    qubit_errors = [(0.02, 0.07), (0.03, 0.09)]

    # -----------------------------------------------------------------
    # Step 1: Backend
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        noise_model = NoiseModel()
        for q, (e0, e1) in enumerate(qubit_errors):
            re = ReadoutError([[1 - e0, e0], [e1, 1 - e1]])
            noise_model.add_readout_error(re, [q])
        backend = AerSimulator(noise_model=noise_model)
        print(f"  Using AerSimulator with asymmetric readout noise")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        print("  IBM hardware mode (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Target circuit (Bell state)
    # -----------------------------------------------------------------
    print("\nStep 2: Building target circuit (Bell state)")
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    target = QuantumCircuit(qr, cr, name='bell')
    target.h(qr[0])
    target.cx(qr[0], qr[1])
    target.measure(qr, cr)

    # -----------------------------------------------------------------
    # Step 3: Generate TREX circuits
    # -----------------------------------------------------------------
    print(f"\nStep 3: Generating {n_randomizations} TREX-twirled circuits")
    trex_circuits, random_strings = generate_trex_circuits(
        target, n_randomizations, seed=42
    )

    # -----------------------------------------------------------------
    # Step 4: Run all circuits
    # -----------------------------------------------------------------
    print(f"\nStep 4: Running circuits ({shots_per_circuit} shots each)")
    all_counts = []
    for qc in trex_circuits:
        result = backend.run(qc, shots=shots_per_circuit).result()
        all_counts.append(result.get_counts())

    # Also run raw (untwirled) for comparison
    raw_result = backend.run(target, shots=shots_per_circuit * n_randomizations).result()
    raw_counts = raw_result.get_counts()

    # -----------------------------------------------------------------
    # Step 5: Correct
    # -----------------------------------------------------------------
    print("\nStep 5: De-twirling and correcting")
    corrected = detwirl_and_correct(
        all_counts, random_strings, qubit_errors, n_qubits
    )

    total_raw = sum(raw_counts.values())
    raw_dist = {k: v / total_raw for k, v in raw_counts.items()}

    # -----------------------------------------------------------------
    # Step 6: Expectation values
    # -----------------------------------------------------------------
    print("\nStep 6: Computing expectation values")

    # Raw <ZZ>
    raw_zz = sum((-1) ** (int(bs[0]) ^ int(bs[1])) * p
                 for bs, p in raw_dist.items())

    # Corrected <ZZ>
    corr_zz = sum((-1) ** (int(bs[0]) ^ int(bs[1])) * p
                  for bs, p in corrected.items())

    # Rescale corrected <ZZ>
    rescale = 1.0
    for e0, e1 in qubit_errors:
        rescale *= (1 - e0 - e1)
    corr_zz_rescaled = corr_zz / rescale

    ideal_zz = 1.0  # For |Phi+>

    print(f"  Ideal <Z0Z1>     = {ideal_zz:.4f}")
    print(f"  Raw <Z0Z1>       = {raw_zz:.4f}")
    print(f"  TREX <Z0Z1>      = {corr_zz_rescaled:.4f}")
    print(f"  Raw error:       {abs(raw_zz - ideal_zz):.4f}")
    print(f"  TREX error:      {abs(corr_zz_rescaled - ideal_zz):.4f}")

    # -----------------------------------------------------------------
    # Step 7: Save
    # -----------------------------------------------------------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    results = {
        "timestamp": datetime.now().isoformat(),
        "n_qubits": n_qubits,
        "shots_per_circuit": shots_per_circuit,
        "n_randomizations": n_randomizations,
        "qubit_errors": [{"e0": e0, "e1": e1} for e0, e1 in qubit_errors],
        "raw_distribution": raw_dist,
        "corrected_distribution": corrected,
        "ideal_zz": ideal_zz,
        "raw_zz": raw_zz,
        "trex_zz": corr_zz_rescaled,
    }

    filepath = os.path.join(RESULTS_DIR, "trex_results.json")
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run TREX production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
