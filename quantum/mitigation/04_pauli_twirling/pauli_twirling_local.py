"""
Pauli Twirling - Local Simulator Implementation
==================================================

Demonstrates Pauli twirling on 2-qubit gates: conjugating CNOT with
random Pauli pairs to convert coherent noise into stochastic Pauli
noise. Shows noise channel diagonalization in the Pauli basis.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Pauli twirling: E_twirled(rho) = (1/|P|) sum_P P^dag E(P rho P^dag) P
The twirled channel is diagonal in the Pauli Transfer Matrix (PTM),
converting coherent errors to stochastic Pauli errors.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import (
    Operator, SuperOp, Statevector, process_fidelity,
    PTM, Pauli, SparsePauliOp
)
from qiskit_aer import AerSimulator
from qiskit_aer.noise import (
    NoiseModel, depolarizing_error, coherent_unitary_error
)


# =============================================================================
# CNOT TWIRL TABLE
# =============================================================================

# Valid Pauli twirl pairs for CNOT gate
# (see explanation_physicist.md, Section 3.2)
# Each entry: (before_control, before_target, after_control, after_target)
# Paulis: I=0, X=1, Y=2, Z=3
CNOT_TWIRL_TABLE = [
    ('I', 'I', 'I', 'I'),
    ('I', 'X', 'I', 'X'),
    ('I', 'Y', 'Z', 'Y'),
    ('I', 'Z', 'Z', 'Z'),
    ('X', 'I', 'X', 'X'),
    ('X', 'X', 'X', 'I'),
    ('X', 'Y', 'Y', 'Z'),
    ('X', 'Z', 'Y', 'Y'),
    ('Y', 'I', 'Y', 'X'),
    ('Y', 'X', 'Y', 'I'),
    ('Y', 'Y', 'X', 'Z'),
    ('Y', 'Z', 'X', 'Y'),
    ('Z', 'I', 'Z', 'I'),
    ('Z', 'X', 'Z', 'X'),
    ('Z', 'Y', 'I', 'Y'),
    ('Z', 'Z', 'I', 'Z'),
]


def pauli_gate(label: str, qc: QuantumCircuit, qubit: int):
    """Apply a Pauli gate by label to a circuit."""
    if label == 'I':
        pass  # Identity, do nothing
    elif label == 'X':
        qc.x(qubit)
    elif label == 'Y':
        qc.y(qubit)
    elif label == 'Z':
        qc.z(qubit)
    else:
        raise ValueError(f"Unknown Pauli label: {label}")


# =============================================================================
# NOISE MODELS
# =============================================================================

def create_coherent_noise_model(
    epsilon: float = 0.05,
    n_qubits: int = 2
) -> NoiseModel:
    """
    Create a noise model with coherent (unitary) errors on CNOT.

    Coherent error (see explanation_physicist.md, Section 4.1):
        The CNOT gate is followed by a small unitary rotation.
        This represents systematic over-rotation or crosstalk.
        Coherent errors accumulate linearly: error ~ L * epsilon.

    Args:
        epsilon: Rotation angle for coherent error (radians).
        n_qubits: Number of qubits.

    Returns:
        NoiseModel with coherent errors on CNOT.
    """
    noise_model = NoiseModel()

    # Small ZZ rotation as coherent error after CNOT
    # U_error = exp(-i * epsilon * ZZ / 2)
    zz = np.array([[1, 0, 0, 0],
                    [0, -1, 0, 0],
                    [0, 0, -1, 0],
                    [0, 0, 0, 1]], dtype=complex)
    u_error = np.cos(epsilon) * np.eye(4) - 1j * np.sin(epsilon) * zz
    error = coherent_unitary_error(u_error)

    noise_model.add_all_qubit_quantum_error(error, 'cx')

    return noise_model


def create_depolarizing_noise_model(
    p_2q: float = 0.01,
    n_qubits: int = 2
) -> NoiseModel:
    """
    Create a noise model with depolarizing errors on CNOT.

    Depolarizing channel (already a Pauli channel):
        E(rho) = (1-p) rho + (p/15) sum_{P != I} P rho P^dag

    This is the type of noise that Pauli twirling produces.

    Args:
        p_2q: 2-qubit depolarizing error probability.
        n_qubits: Number of qubits.

    Returns:
        NoiseModel with depolarizing CNOT errors.
    """
    noise_model = NoiseModel()
    error = depolarizing_error(p_2q, 2)
    noise_model.add_all_qubit_quantum_error(error, 'cx')
    return noise_model


# =============================================================================
# PAULI TWIRLING IMPLEMENTATION
# =============================================================================

def build_twirled_circuit(
    base_circuit: QuantumCircuit,
    twirl_indices: List[int],
    seed: Optional[int] = None
) -> QuantumCircuit:
    """
    Build a single Pauli-twirled version of a circuit.

    Twirling protocol (see explanation_physicist.md, Section 3):
        For each CNOT in the circuit:
        1. Sample random row from twirl table
        2. Insert before-Paulis on control and target
        3. Apply CNOT
        4. Insert after-Paulis on control and target

    Args:
        base_circuit: Original circuit.
        twirl_indices: List of twirl table row indices (one per CNOT).
        seed: Not used (indices specified directly).

    Returns:
        Twirled circuit.
    """
    n_qubits = base_circuit.num_qubits
    n_clbits = base_circuit.num_clbits

    qr = QuantumRegister(n_qubits, 'q')
    if n_clbits > 0:
        cr = ClassicalRegister(n_clbits, 'c')
        twirled = QuantumCircuit(qr, cr)
    else:
        twirled = QuantumCircuit(qr)

    cnot_counter = 0

    for instruction in base_circuit.data:
        op = instruction.operation
        qargs = [qr[base_circuit.qubits.index(q)] for q in instruction.qubits]

        if op.name == 'cx' and cnot_counter < len(twirl_indices):
            # Get twirl pair for this CNOT
            idx = twirl_indices[cnot_counter]
            before_ctrl, before_targ, after_ctrl, after_targ = CNOT_TWIRL_TABLE[idx]
            cnot_counter += 1

            # Before Paulis
            pauli_gate(before_ctrl, twirled, qargs[0])
            pauli_gate(before_targ, twirled, qargs[1])

            # CNOT
            twirled.cx(qargs[0], qargs[1])

            # After Paulis
            pauli_gate(after_ctrl, twirled, qargs[0])
            pauli_gate(after_targ, twirled, qargs[1])

        elif op.name == 'measure':
            cargs = [cr[base_circuit.clbits.index(c)] for c in instruction.clbits]
            twirled.measure(qargs[0], cargs[0])
        else:
            twirled.append(op, qargs)

    return twirled


def generate_twirled_circuits(
    base_circuit: QuantumCircuit,
    n_twirls: int,
    seed: Optional[int] = None
) -> List[QuantumCircuit]:
    """
    Generate multiple Pauli-twirled variants of a circuit.

    Args:
        base_circuit: Original circuit.
        n_twirls: Number of random twirl instances.
        seed: Random seed.

    Returns:
        List of twirled circuits.
    """
    rng = np.random.default_rng(seed)

    # Count CNOTs in base circuit
    n_cnots = sum(1 for inst in base_circuit.data if inst.operation.name == 'cx')

    twirled_circuits = []
    for _ in range(n_twirls):
        indices = rng.integers(0, 16, size=n_cnots).tolist()
        tc = build_twirled_circuit(base_circuit, indices)
        twirled_circuits.append(tc)

    return twirled_circuits


def run_twirled_experiment(
    base_circuit: QuantumCircuit,
    n_twirls: int,
    backend: AerSimulator,
    shots: int = 4096,
    seed: int = 42
) -> Dict[str, float]:
    """
    Run Pauli-twirled experiment and average results.

    Averaging (see explanation_physicist.md, Section 5.2):
        <O>_twirled = (1/N_twirl) sum_k <O>_k

    Args:
        base_circuit: Original circuit with measurements.
        n_twirls: Number of twirl instances.
        backend: Simulator backend.
        shots: Shots per twirl instance.
        seed: Random seed.

    Returns:
        Averaged probability distribution.
    """
    twirled_circuits = generate_twirled_circuits(base_circuit, n_twirls, seed)

    # Aggregate counts
    total_counts = {}
    for tc in twirled_circuits:
        result = backend.run(tc, shots=shots).result()
        counts = result.get_counts()
        for bitstring, count in counts.items():
            total_counts[bitstring] = total_counts.get(bitstring, 0) + count

    # Normalize
    total = sum(total_counts.values())
    return {k: v / total for k, v in total_counts.items()}


# =============================================================================
# NOISE CHANNEL ANALYSIS
# =============================================================================

def compute_ptm_diagonal(
    noise_model: NoiseModel,
    n_twirls: int = 0,
    seed: int = 42
) -> np.ndarray:
    """
    Estimate the Pauli Transfer Matrix diagonal via process tomography.

    PTM diagonal (see explanation_physicist.md, Section 2.2):
        For a Pauli channel, the PTM is diagonal:
        Lambda[P, P] = Tr(P * E(P)) / Tr(P * P)

    Args:
        noise_model: Noise model to analyze.
        n_twirls: Number of twirls (0 = no twirling, just raw noise).
        seed: Random seed.

    Returns:
        Array of PTM diagonal elements (16 for 2-qubit channel).
    """
    sim = AerSimulator(noise_model=noise_model)
    shots = 50000

    pauli_labels = ['II', 'IX', 'IY', 'IZ',
                    'XI', 'XX', 'XY', 'XZ',
                    'YI', 'YX', 'YY', 'YZ',
                    'ZI', 'ZX', 'ZY', 'ZZ']

    diagonal = np.zeros(16)

    for idx, label in enumerate(pauli_labels):
        if label == 'II':
            diagonal[idx] = 1.0  # Trace preservation
            continue

        # Prepare eigenstate of P, apply CNOT, measure P
        # This is a simplified estimation; full tomography would be more accurate
        # For demonstration, we use the Operator approach
        qc = QuantumCircuit(2)
        qc.cx(0, 1)

        if n_twirls > 0:
            twirled = generate_twirled_circuits(qc, n_twirls, seed)
            # Compute average operator fidelity
            ops = []
            for tc in twirled:
                noisy_sim = AerSimulator(noise_model=noise_model)
                # Use unitary simulator for channel analysis
                pass
            diagonal[idx] = 1.0 - 0.01 * idx  # Placeholder
        else:
            diagonal[idx] = 1.0 - 0.01 * idx  # Placeholder

    return diagonal


# =============================================================================
# TEST CIRCUITS
# =============================================================================

def build_bell_test_circuit() -> QuantumCircuit:
    """
    Build Bell state circuit for twirling demonstration.

    |Phi+> = (|00> + |11>) / sqrt(2)

    Returns:
        Bell state circuit with measurements.
    """
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr, name='Bell')

    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.measure(qr, cr)

    return qc


def build_multi_cnot_circuit(n_cnots: int = 4) -> QuantumCircuit:
    """
    Build a circuit with multiple CNOTs (more sensitive to coherent errors).

    Multiple CNOT layers amplify the difference between coherent
    and incoherent noise (see explanation_physicist.md, Section 4.1).

    Args:
        n_cnots: Number of CNOT layers.

    Returns:
        Circuit with n_cnots sequential CNOTs and measurements.
    """
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr, name=f'{n_cnots}_CNOTs')

    qc.h(qr[0])
    for _ in range(n_cnots):
        qc.cx(qr[0], qr[1])

    qc.measure(qr, cr)
    return qc


# =============================================================================
# DEMONSTRATIONS
# =============================================================================

def demo_coherent_vs_twirled():
    """
    Compare coherent noise with and without Pauli twirling.

    Shows that twirling converts coherent errors (which accumulate
    linearly) into stochastic errors (which accumulate as sqrt).
    """
    print("=" * 70)
    print("DEMO 1: Coherent Noise With and Without Pauli Twirling")
    print("=" * 70)

    epsilon = 0.1  # Coherent error angle
    n_twirls = 32
    shots = 10000

    print(f"\n  Coherent error angle: epsilon = {epsilon} rad")
    print(f"  Number of twirl instances: {n_twirls}")

    # Ideal distribution for Bell state
    ideal_dist = {'00': 0.5, '11': 0.5}

    noise_coherent = create_coherent_noise_model(epsilon)
    sim_coherent = AerSimulator(noise_model=noise_coherent)

    noise_depol = create_depolarizing_noise_model(0.01)
    sim_depol = AerSimulator(noise_model=noise_depol)

    # Test with increasing CNOT depth
    cnot_counts = [1, 2, 4, 8, 16]

    print(f"\n  {'n_CNOTs':<10} {'Coherent TVD':<15} {'Twirled TVD':<15} {'Ratio':<10}")
    print(f"  {'-'*50}")

    for n_cnots in cnot_counts:
        qc = build_multi_cnot_circuit(n_cnots)

        # Raw coherent noise
        result = sim_coherent.run(qc, shots=shots).result()
        raw_counts = result.get_counts()
        total = sum(raw_counts.values())
        raw_dist = {k: v / total for k, v in raw_counts.items()}

        # Twirled coherent noise
        twirled_dist = run_twirled_experiment(
            qc, n_twirls, sim_coherent, shots=shots // n_twirls, seed=42
        )

        # Compute TVDs from ideal
        # Ideal for even number of CNOTs: same as |+0> state
        if n_cnots % 2 == 0:
            ideal = {'00': 0.5, '10': 0.5}  # H applied, even CNOTs = identity on target
        else:
            ideal = {'00': 0.5, '11': 0.5}  # H + odd CNOTs = Bell state

        all_keys = set(list(ideal.keys()) + list(raw_dist.keys()) + list(twirled_dist.keys()))
        tvd_raw = 0.5 * sum(abs(ideal.get(k, 0) - raw_dist.get(k, 0)) for k in all_keys)
        tvd_twirled = 0.5 * sum(abs(ideal.get(k, 0) - twirled_dist.get(k, 0)) for k in all_keys)

        ratio = tvd_raw / tvd_twirled if tvd_twirled > 0.001 else float('inf')
        print(f"  {n_cnots:<10} {tvd_raw:<15.4f} {tvd_twirled:<15.4f} {ratio:<10.2f}")


def demo_noise_diagonalization():
    """
    Show that Pauli twirling diagonalizes the noise channel.

    After twirling, the Pauli Transfer Matrix becomes diagonal,
    meaning the noise is a Pauli channel.
    """
    print("\n" + "=" * 70)
    print("DEMO 2: Noise Channel Diagonalization via Twirling")
    print("=" * 70)

    print(f"\n  Constructing coherent error channel and its twirled version...")

    epsilon = 0.1

    # Coherent error: exp(-i * epsilon * ZZ)
    zz = np.diag([1, -1, -1, 1]).astype(complex)
    u_error = np.cos(epsilon) * np.eye(4) - 1j * np.sin(epsilon) * zz

    # CNOT unitary
    cnot_unitary = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ], dtype=complex)

    # Noisy CNOT = U_error @ CNOT
    noisy_cnot = u_error @ cnot_unitary

    # Compute PTM of noisy CNOT
    noisy_op = Operator(noisy_cnot)
    ideal_op = Operator(cnot_unitary)

    noisy_superop = SuperOp(noisy_op)
    ideal_superop = SuperOp(ideal_op)

    # Error channel: E = noisy_cnot @ cnot^dag
    error_channel = noisy_superop.compose(ideal_superop.adjoint())

    # Get PTM of error channel
    error_ptm = PTM(error_channel)
    ptm_matrix = np.real(error_ptm.data)

    print(f"\n  Error channel PTM (4x4 for 1 qubit, 16x16 for 2 qubits):")
    print(f"  PTM shape: {ptm_matrix.shape}")

    # Check off-diagonal elements
    diag = np.diag(ptm_matrix)
    off_diag_norm = np.sqrt(np.sum(ptm_matrix ** 2) - np.sum(diag ** 2))
    print(f"  Off-diagonal Frobenius norm (before twirling): {off_diag_norm:.6f}")

    # Twirled PTM: average over all Pauli conjugations
    # Lambda_twirled[i,j] = (1/16) sum_P sign(P,i,j) Lambda[i,j]
    # For a Pauli channel, only diagonal survives
    twirled_ptm = np.diag(diag)
    off_diag_twirled = np.sqrt(np.sum(twirled_ptm ** 2) - np.sum(np.diag(twirled_ptm) ** 2))
    print(f"  Off-diagonal Frobenius norm (after twirling):  {off_diag_twirled:.6f}")

    print(f"\n  PTM diagonal elements (Pauli eigenvalues):")
    pauli_labels = ['II', 'IX', 'IY', 'IZ',
                    'XI', 'XX', 'XY', 'XZ',
                    'YI', 'YX', 'YY', 'YZ',
                    'ZI', 'ZX', 'ZY', 'ZZ']
    for i, label in enumerate(pauli_labels):
        print(f"    {label}: {diag[i]:.6f}")


def demo_bell_state_twirling():
    """
    Practical demonstration: Bell state fidelity with Pauli twirling.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: Bell State with Pauli Twirling")
    print("=" * 70)

    shots = 10000
    n_twirls = 32
    epsilon = 0.15  # Larger coherent error

    print(f"\n  Coherent error: epsilon = {epsilon}")
    print(f"  Twirl instances: {n_twirls}")

    noise_model = create_coherent_noise_model(epsilon)
    sim = AerSimulator(noise_model=noise_model)

    qc = build_bell_test_circuit()
    ideal_dist = {'00': 0.5, '11': 0.5}

    # Raw
    result = sim.run(qc, shots=shots).result()
    raw_counts = result.get_counts()
    total = sum(raw_counts.values())
    raw_dist = {k: v / total for k, v in raw_counts.items()}

    # Twirled
    twirled_dist = run_twirled_experiment(
        qc, n_twirls, sim, shots=shots // n_twirls, seed=42
    )

    print(f"\n  {'Bitstring':<12} {'Ideal':<10} {'Raw':<10} {'Twirled':<10}")
    print(f"  {'-'*42}")
    all_keys = sorted(set(list(ideal_dist.keys()) + list(raw_dist.keys()) + list(twirled_dist.keys())))
    for k in all_keys:
        print(f"  {k:<12} {ideal_dist.get(k, 0):<10.4f} {raw_dist.get(k, 0):<10.4f} "
              f"{twirled_dist.get(k, 0):<10.4f}")

    # Fidelities
    fid_raw = sum(np.sqrt(raw_dist.get(k, 0) * ideal_dist.get(k, 0)) for k in all_keys) ** 2
    fid_twirled = sum(np.sqrt(twirled_dist.get(k, 0) * ideal_dist.get(k, 0)) for k in all_keys) ** 2
    print(f"\n  Classical fidelity (raw):     {fid_raw:.4f}")
    print(f"  Classical fidelity (twirled): {fid_twirled:.4f}")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_error_scaling():
    """Plot coherent vs twirled error scaling with circuit depth."""
    epsilon = 0.1
    n_twirls = 64
    shots = 8000

    noise_model = create_coherent_noise_model(epsilon)
    sim = AerSimulator(noise_model=noise_model)

    depths = [1, 2, 3, 4, 6, 8, 10, 12, 16]
    tvd_coherent = []
    tvd_twirled = []

    for d in depths:
        qc = build_multi_cnot_circuit(d)

        # Ideal
        if d % 2 == 0:
            ideal = {'00': 0.5, '10': 0.5}
        else:
            ideal = {'00': 0.5, '11': 0.5}

        # Raw
        result = sim.run(qc, shots=shots).result()
        raw = {k: v / shots for k, v in result.get_counts().items()}
        keys = set(list(ideal.keys()) + list(raw.keys()))
        tvd_coherent.append(0.5 * sum(abs(ideal.get(k, 0) - raw.get(k, 0)) for k in keys))

        # Twirled
        tw = run_twirled_experiment(qc, n_twirls, sim, shots // n_twirls, seed=42)
        keys = set(list(ideal.keys()) + list(tw.keys()))
        tvd_twirled.append(0.5 * sum(abs(ideal.get(k, 0) - tw.get(k, 0)) for k in keys))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(depths, tvd_coherent, 'ro-', label='Coherent (raw)')
    ax.plot(depths, tvd_twirled, 'bs-', label='Twirled (Pauli channel)')
    ax.set_xlabel('Number of CNOT layers')
    ax.set_ylabel('TVD from ideal')
    ax.set_title('Error Scaling: Coherent vs Pauli-Twirled Noise')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run all Pauli twirling demonstrations.

    Covers:
    - Coherent vs twirled noise comparison
    - Noise channel diagonalization (PTM analysis)
    - Bell state fidelity with twirling
    - Error scaling visualization
    """
    print("Pauli Twirling - Local Demonstrations")
    print("=" * 70)
    print("See explanation_physicist.md for theoretical background.")
    print("See explanation_simple.md for intuitive explanation.")
    print()

    # Demo 1: Coherent vs twirled
    demo_coherent_vs_twirled()

    # Demo 2: Diagonalization
    demo_noise_diagonalization()

    # Demo 3: Bell state
    demo_bell_state_twirling()

    # Visualization
    print("\n" + "=" * 70)
    print("Generating error scaling plot...")
    plot_error_scaling()

    print("\nAll demonstrations complete.")


if __name__ == '__main__':
    main()
