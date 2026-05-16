"""
Bacon-Shor Code (3x3) - IBM Production-Ready Implementation
=============================================================

Production workflow for the [[9,1,3]] Bacon-Shor subsystem code
on IBM Quantum hardware. Exploits 2-body gauge measurements which
are hardware-friendly (native 2-qubit gates on IBM devices).

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Key Production Advantage:
-------------------------
The Bacon-Shor code requires only weight-2 gauge measurements (XX and ZZ
on adjacent pairs). On IBM hardware:
- Each gauge measurement needs only 1 CNOT gate (native on IBM)
- No weight-4 stabilizer circuits needed (unlike surface code)
- Fewer CNOT gates -> less decoherence -> better syndrome accuracy
- 2-body interactions map directly to device coupling map
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session


# =============================================================================
# CONFIGURATION
# =============================================================================

RESULTS_DIR = "quantum/error_correction/11_bacon_shor_code/production_results"

ROWS = 3
COLS = 3
N_DATA = ROWS * COLS  # 9


def qubit_index(row, col):
    """Map (row, col) to linear index on 3x3 grid."""
    return row * COLS + col


# =============================================================================
# CIRCUIT CONSTRUCTION
# =============================================================================

def build_encoding_circuit(data):
    """
    Encode |0_L> for the 3x3 Bacon-Shor code.

    Strategy: H on top row, CNOT down each column.
    This prepares the +1 eigenstate of all stabilizers with Z_L = +1.

    Circuit depth: 1 (H layer) + 2 (CNOT layers) = 3.
    All CNOTs are nearest-neighbor on the grid (hardware-friendly).
    """
    qc = QuantumCircuit(data, name='encode')

    # Hadamard on row 0
    for col in range(COLS):
        qc.h(data[qubit_index(0, col)])

    # CNOT down each column (row 0 -> row 1 -> row 2)
    for col in range(COLS):
        for row in range(ROWS - 1):
            qc.cx(data[qubit_index(row, col)], data[qubit_index(row + 1, col)])

    return qc


def build_gauge_measurement_block(data, x_anc, z_anc, x_bits, z_bits):
    """
    Build one round of gauge measurements for syndrome extraction.

    X-type gauge: measure X_{i,j} X_{i+1,j} (vertical XX pairs)
        - 2 row-pairs * 3 columns = 6 measurements
        - Circuit: H-CNOT-CNOT-H pattern on ancilla

    Z-type gauge: measure Z_{i,j} Z_{i,j+1} (horizontal ZZ pairs)
        - 3 rows * 2 column-pairs = 6 measurements
        - Circuit: CNOT-CNOT pattern on ancilla

    HARDWARE NOTE: All measurements are weight-2 (single CNOT per data qubit).
    This is the key advantage over stabilizer codes requiring weight-4 measurements.
    On IBM devices, each gauge measurement maps to exactly 2 CNOT gates.
    """
    qc = QuantumCircuit(data, x_anc, z_anc, x_bits, z_bits,
                        name='gauge_meas')

    # X-type gauge: X_{i,j} X_{i+1,j}
    anc_idx = 0
    for row_pair in range(ROWS - 1):
        for col in range(COLS):
            q1 = qubit_index(row_pair, col)
            q2 = qubit_index(row_pair + 1, col)

            qc.h(x_anc[anc_idx])
            qc.cx(x_anc[anc_idx], data[q1])
            qc.cx(x_anc[anc_idx], data[q2])
            qc.h(x_anc[anc_idx])
            qc.measure(x_anc[anc_idx], x_bits[anc_idx])
            anc_idx += 1

    # Z-type gauge: Z_{i,j} Z_{i,j+1}
    anc_idx = 0
    for row in range(ROWS):
        for col_pair in range(COLS - 1):
            q1 = qubit_index(row, col_pair)
            q2 = qubit_index(row, col_pair + 1)

            qc.cx(data[q1], z_anc[anc_idx])
            qc.cx(data[q2], z_anc[anc_idx])
            qc.measure(z_anc[anc_idx], z_bits[anc_idx])
            anc_idx += 1

    return qc


def build_full_circuit(error_qubit=None, error_type='X', n_syndrome_rounds=1):
    """
    Build the complete Bacon-Shor production circuit.

    Stages:
        1. Encode |0_L>
        2. (Optional) Inject error for testing
        3. Gauge measurements (repeated for fault tolerance)
        4. (Correction would be applied classically in production)

    For production deployment:
    - Multiple syndrome rounds with majority vote
    - Classical post-processing decodes gauge -> stabilizer syndromes
    - Correction applied in subsequent circuit or tracked in software (Pauli frame)
    """
    data = QuantumRegister(N_DATA, 'd')
    x_anc = QuantumRegister(6, 'xa')
    z_anc = QuantumRegister(6, 'za')

    # Classical registers for each syndrome round
    x_bits_list = []
    z_bits_list = []
    for r in range(n_syndrome_rounds):
        x_bits_list.append(ClassicalRegister(6, f'xg_r{r}'))
        z_bits_list.append(ClassicalRegister(6, f'zg_r{r}'))

    qc = QuantumCircuit(data, x_anc, z_anc)
    for xb in x_bits_list:
        qc.add_register(xb)
    for zb in z_bits_list:
        qc.add_register(zb)

    # Stage 1: Encode
    for col in range(COLS):
        qc.h(data[qubit_index(0, col)])
    for col in range(COLS):
        for row in range(ROWS - 1):
            qc.cx(data[qubit_index(row, col)], data[qubit_index(row + 1, col)])
    qc.barrier(label='encoded')

    # Stage 2: Error injection (testing only)
    if error_qubit is not None:
        if error_type == 'X':
            qc.x(data[error_qubit])
        elif error_type == 'Z':
            qc.z(data[error_qubit])
        elif error_type == 'Y':
            qc.y(data[error_qubit])
        qc.barrier(label='error')

    # Stage 3: Gauge measurements (possibly repeated)
    for r in range(n_syndrome_rounds):
        # Reset ancillae for each round
        if r > 0:
            for i in range(6):
                qc.reset(x_anc[i])
                qc.reset(z_anc[i])

        # X-type gauge measurements
        anc_idx = 0
        for row_pair in range(ROWS - 1):
            for col in range(COLS):
                q1 = qubit_index(row_pair, col)
                q2 = qubit_index(row_pair + 1, col)
                qc.h(x_anc[anc_idx])
                qc.cx(x_anc[anc_idx], data[q1])
                qc.cx(x_anc[anc_idx], data[q2])
                qc.h(x_anc[anc_idx])
                qc.measure(x_anc[anc_idx], x_bits_list[r][anc_idx])
                anc_idx += 1

        qc.barrier()

        # Z-type gauge measurements
        anc_idx = 0
        for row in range(ROWS):
            for col_pair in range(COLS - 1):
                q1 = qubit_index(row, col_pair)
                q2 = qubit_index(row, col_pair + 1)
                qc.cx(data[q1], z_anc[anc_idx])
                qc.cx(data[q2], z_anc[anc_idx])
                qc.measure(z_anc[anc_idx], z_bits_list[r][anc_idx])
                anc_idx += 1

        qc.barrier(label=f'round_{r}')

    return qc


# =============================================================================
# CLASSICAL POST-PROCESSING
# =============================================================================

def decode_gauge_results(x_gauge_bits, z_gauge_bits):
    """
    Classical post-processing: compute stabilizer syndromes from gauge outcomes.

    X-type stabilizer S^X_i = product of X-gauge results across columns:
        S^X_0 = x[0] XOR x[1] XOR x[2]   (row pair 0-1)
        S^X_1 = x[3] XOR x[4] XOR x[5]   (row pair 1-2)

    Z-type stabilizer S^Z_j = product of Z-gauge results across rows:
        S^Z_0 = z[0] XOR z[2] XOR z[4]   (col pair 0-1)
        S^Z_1 = z[1] XOR z[3] XOR z[5]   (col pair 1-2)
    """
    sx0 = x_gauge_bits[0] ^ x_gauge_bits[1] ^ x_gauge_bits[2]
    sx1 = x_gauge_bits[3] ^ x_gauge_bits[4] ^ x_gauge_bits[5]

    sz0 = z_gauge_bits[0] ^ z_gauge_bits[2] ^ z_gauge_bits[4]
    sz1 = z_gauge_bits[1] ^ z_gauge_bits[3] ^ z_gauge_bits[5]

    return (sx0, sx1), (sz0, sz1)


def majority_vote_syndromes(all_round_syndromes):
    """
    Apply majority vote across multiple syndrome rounds.

    For fault tolerance: single measurement errors are corrected
    by taking the majority over repeated rounds.
    """
    n_rounds = len(all_round_syndromes)
    if n_rounds == 1:
        return all_round_syndromes[0]

    # Vote on each syndrome bit independently
    x_syns = [s[0] for s in all_round_syndromes]
    z_syns = [s[1] for s in all_round_syndromes]

    sx0_vote = int(sum(s[0] for s in x_syns) > n_rounds / 2)
    sx1_vote = int(sum(s[1] for s in x_syns) > n_rounds / 2)
    sz0_vote = int(sum(s[0] for s in z_syns) > n_rounds / 2)
    sz1_vote = int(sum(s[1] for s in z_syns) > n_rounds / 2)

    return (sx0_vote, sx1_vote), (sz0_vote, sz1_vote)


def determine_correction(x_syndrome, z_syndrome):
    """
    Determine correction based on decoded syndromes.

    X-type syndrome (sx0, sx1) detects Z errors -> identifies row:
        (0,0) -> no Z error
        (1,0) -> row 0
        (1,1) -> row 1
        (0,1) -> row 2

    Z-type syndrome (sz0, sz1) detects X errors -> identifies column:
        (0,0) -> no X error
        (1,0) -> col 0
        (1,1) -> col 1
        (0,1) -> col 2

    Correction: apply Z to any qubit in the identified row (gauge freedom),
                apply X to any qubit in the identified column (gauge freedom).
    """
    sx0, sx1 = x_syndrome
    sz0, sz1 = z_syndrome

    corrections = []

    # Z correction (for Z errors detected by X-type syndrome)
    z_row = {(1, 0): 0, (1, 1): 1, (0, 1): 2}.get((sx0, sx1))
    if z_row is not None:
        corrections.append(('Z', qubit_index(z_row, 0)))

    # X correction (for X errors detected by Z-type syndrome)
    x_col = {(1, 0): 0, (1, 1): 1, (0, 1): 2}.get((sz0, sz1))
    if x_col is not None:
        corrections.append(('X', qubit_index(0, x_col)))

    return corrections


# =============================================================================
# PRODUCTION RUN
# =============================================================================

def run_production():
    """
    Execute the Bacon-Shor code production pipeline.

    Workflow:
    1. Build circuits for various error scenarios
    2. Run on simulator (swap for IBM hardware in production)
    3. Classical post-processing of gauge measurement results
    4. Decode syndromes and determine corrections
    5. Report accuracy metrics
    """
    print("=" * 70)
    print("Bacon-Shor [[9,1,3]] - IBM Production Pipeline")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Grid: {ROWS}x{COLS} = {N_DATA} data qubits + 12 ancillae")
    print(f"Measurement weight: 2 (hardware-friendly)")
    print(f"Syndrome rounds: 1")

    sim = AerSimulator()
    shots = 8192

    # Test scenarios
    test_cases = [
        ("No error", None, None),
        ("X on q4 (center)", 4, 'X'),
        ("Z on q2 (corner)", 2, 'Z'),
        ("X on q6 (corner)", 6, 'X'),
        ("Z on q4 (center)", 4, 'Z'),
        ("Y on q1 (edge)", 1, 'Y'),
    ]

    results = {}
    for name, err_q, err_type in test_cases:
        qc = build_full_circuit(
            error_qubit=err_q,
            error_type=err_type if err_type else 'X',
            n_syndrome_rounds=1
        )

        # Transpile for target backend
        pm = generate_preset_pass_manager(optimization_level=1)
        transpiled = pm.run(qc)

        # Execute
        counts = sim.run(transpiled, shots=shots).result().get_counts()

        # Post-process: decode each shot
        syndrome_stats = {}
        correction_stats = {}

        for bitstring, count in counts.items():
            parts = bitstring.split()
            # Register order depends on circuit construction
            # We extract x_gauge and z_gauge bits
            if len(parts) >= 2:
                z_bits_str = parts[0]
                x_bits_str = parts[1]
            else:
                full = bitstring.replace(' ', '')
                half = len(full) // 2
                x_bits_str = full[half:]
                z_bits_str = full[:half]

            x_gauge = [int(b) for b in reversed(x_bits_str)]
            z_gauge = [int(b) for b in reversed(z_bits_str)]

            # Pad if needed
            while len(x_gauge) < 6:
                x_gauge.append(0)
            while len(z_gauge) < 6:
                z_gauge.append(0)

            x_syn, z_syn = decode_gauge_results(x_gauge[:6], z_gauge[:6])
            corrections = determine_correction(x_syn, z_syn)

            syn_key = (x_syn, z_syn)
            syndrome_stats[syn_key] = syndrome_stats.get(syn_key, 0) + count

            corr_key = tuple(corrections) if corrections else ('none',)
            correction_stats[corr_key] = correction_stats.get(corr_key, 0) + count

        # Find dominant syndrome
        dominant = max(syndrome_stats, key=syndrome_stats.get)
        dominant_frac = syndrome_stats[dominant] / shots
        dominant_corrections = determine_correction(dominant[0], dominant[1])

        # Expected behavior
        if err_q is not None:
            r, c = divmod(err_q, COLS)
            expected_info = f"grid ({r},{c})"
        else:
            expected_info = "none"

        results[name] = {
            'dominant_syndrome': str(dominant),
            'dominant_fraction': dominant_frac,
            'corrections': str(dominant_corrections),
            'n_distinct_syndromes': len(syndrome_stats),
        }

        print(f"\n  {name} (qubit={err_q}, type={err_type}):")
        print(f"    Dominant syndrome: X={dominant[0]}, Z={dominant[1]}  "
              f"[{dominant_frac:.1%}]")
        print(f"    Corrections: {dominant_corrections}")
        print(f"    Distinct syndromes observed: {len(syndrome_stats)}")
        print(f"    Expected error location: {expected_info}")

    # Circuit metrics
    print(f"\n" + "-" * 70)
    print(f"  Circuit Metrics (single round):")
    qc_ref = build_full_circuit(error_qubit=None, n_syndrome_rounds=1)
    pm = generate_preset_pass_manager(optimization_level=1)
    qc_transpiled = pm.run(qc_ref)
    print(f"    Total qubits: {qc_ref.num_qubits} "
          f"({N_DATA} data + 12 ancillae)")
    print(f"    Circuit depth (pre-transpile): {qc_ref.depth()}")
    print(f"    Circuit depth (post-transpile): {qc_transpiled.depth()}")
    print(f"    Measurement weight: 2 (all gauge operators)")

    # Hardware comparison note
    print(f"\n  Hardware Notes:")
    print(f"    - All gauge measurements are weight-2 (single CNOT per data qubit)")
    print(f"    - Surface code would need weight-4 stabilizer measurements")
    print(f"    - Bacon-Shor 2-body measurements map directly to IBM CX gates")
    print(f"    - Fewer CNOT layers -> less decoherence during syndrome extraction")
    print(f"    - Mid-circuit measurement supported on IBM Eagle/Heron processors")
    print(f"    - Dynamic circuits enable real-time correction (Pauli frame tracking)")

    # Save results
    os.makedirs(RESULTS_DIR, exist_ok=True)
    output = {
        "timestamp": datetime.now().isoformat(),
        "code": "Bacon-Shor [[9,1,3]]",
        "grid": f"{ROWS}x{COLS}",
        "measurement_weight": 2,
        "shots": shots,
        "syndrome_rounds": 1,
        "results": results,
    }
    filepath = os.path.join(RESULTS_DIR, "results.json")
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MULTI-ROUND FAULT-TOLERANT DEMO
# =============================================================================

def demo_multi_round():
    """
    Demonstrate multi-round syndrome extraction with majority voting.

    For fault-tolerant operation:
    - Single gauge measurement can have errors
    - Repeat d=3 rounds and take majority vote on each stabilizer syndrome
    - This corrects single measurement errors
    """
    print("\n" + "=" * 70)
    print("Multi-Round Syndrome Extraction (Fault Tolerance)")
    print("=" * 70)

    sim = AerSimulator()
    shots = 4096
    n_rounds = 3

    qc = build_full_circuit(
        error_qubit=qubit_index(1, 1),
        error_type='X',
        n_syndrome_rounds=n_rounds
    )

    counts = sim.run(qc, shots=shots).result().get_counts()

    print(f"\n  Error: X on q(1,1), {n_rounds} syndrome rounds")
    print(f"  Shots: {shots}")

    # For each shot, decode each round and apply majority vote
    vote_results = {}
    for bitstring, count in counts.items():
        parts = bitstring.split()

        # Extract per-round gauge bits
        # Register layout: zg_r2, zg_r1, zg_r0, xg_r2, xg_r1, xg_r0
        # (Qiskit puts later registers to the left in bitstrings)
        round_syndromes = []
        if len(parts) >= 2 * n_rounds:
            for r in range(n_rounds):
                z_idx = n_rounds - 1 - r
                x_idx = 2 * n_rounds - 1 - r
                z_str = parts[z_idx] if z_idx < len(parts) else '000000'
                x_str = parts[x_idx] if x_idx < len(parts) else '000000'
                x_gauge = [int(b) for b in reversed(x_str)]
                z_gauge = [int(b) for b in reversed(z_str)]
                while len(x_gauge) < 6:
                    x_gauge.append(0)
                while len(z_gauge) < 6:
                    z_gauge.append(0)
                syn = decode_gauge_results(x_gauge[:6], z_gauge[:6])
                round_syndromes.append(syn)

            # Majority vote
            voted = majority_vote_syndromes(round_syndromes)
            vote_key = str(voted)
            vote_results[vote_key] = vote_results.get(vote_key, 0) + count

    if vote_results:
        print(f"\n  Majority-voted syndrome distribution:")
        for syn, cnt in sorted(vote_results.items(), key=lambda x: -x[1])[:5]:
            print(f"    {syn}: {cnt}/{shots} = {cnt / shots:.3f}")
    else:
        print(f"\n  (Multi-round decoding requires careful register parsing;")
        print(f"   see production deployment for full implementation)")

    print(f"\n  Fault-tolerance benefit:")
    print(f"    - Single measurement error in 1 of {n_rounds} rounds -> corrected by vote")
    print(f"    - Effective measurement error rate: O(p_meas^2) with 3 rounds")


# =============================================================================
# MAIN
# =============================================================================

def main():
    run_production()
    demo_multi_round()

    print("\n" + "=" * 70)
    print("PRODUCTION SUMMARY")
    print("=" * 70)
    print("""
    Bacon-Shor [[9,1,3]] Production Notes:

    Hardware advantages:
    - Weight-2 gauge measurements (vs weight-4 for surface code)
    - Each gauge measurement: 2 CNOT gates + 1 measurement
    - Native on IBM Eagle/Heron coupling maps
    - Fewer error propagation paths (no hook errors from multi-body)

    Deployment checklist:
    - [ ] Select backend with sufficient connectivity (9 data + 12 ancilla)
    - [ ] Map grid to device coupling map (minimize SWAP overhead)
    - [ ] Enable dynamic circuits for mid-circuit measurement
    - [ ] Implement Pauli frame tracking for real-time correction
    - [ ] Use multiple syndrome rounds (d=3 minimum) for fault tolerance
    - [ ] Enable readout error mitigation (M3/TREX)
    - [ ] Benchmark against surface code on same hardware
    """)


if __name__ == "__main__":
    main()
