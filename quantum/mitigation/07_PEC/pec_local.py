"""
Probabilistic Error Cancellation (PEC) - Local Simulator Implementation
=========================================================================

Demonstrates PEC: decompose ideal gates as quasi-probability mixtures
of noisy operations, sample with sign corrections, and recover unbiased
expectation values. Includes noise tomography and overhead analysis.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
PEC: G_ideal = sum_i eta_i G_noisy_i, where eta_i can be negative.
Sample from |eta_i|/gamma, correct by sign. Exact in expectation.
Sampling overhead: gamma^2 = (sum |eta_i|)^2 per gate.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error


# =============================================================================
# NOISE MODEL AND CHARACTERIZATION
# =============================================================================

def create_known_noise_model(
    p_1q: float = 0.01,
    p_2q: float = 0.03
) -> Tuple[NoiseModel, Dict]:
    """
    Create a Pauli noise model with known parameters.

    Depolarizing noise (see explanation_physicist.md, Section 3.2):
        E(rho) = (1-p)rho + (p/3)(XrhoX + YrhoY + ZrhoZ)

    Args:
        p_1q: Single-qubit depolarizing rate.
        p_2q: Two-qubit depolarizing rate.

    Returns:
        Tuple of (NoiseModel, noise_params dict).
    """
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p_1q, 1), ['x', 'h', 'sx', 'ry', 'rz']
    )
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p_2q, 2), ['cx']
    )

    noise_params = {
        '1q': {
            'p_total': p_1q,
            'p_X': p_1q / 3,
            'p_Y': p_1q / 3,
            'p_Z': p_1q / 3,
        },
        '2q': {
            'p_total': p_2q,
        }
    }

    return noise_model, noise_params


def compute_quasi_probabilities_1q(p: float) -> Tuple[Dict[str, float], float]:
    """
    Compute quasi-probability decomposition for 1Q depolarizing noise.

    Inverse channel (see explanation_physicist.md, Section 3.2):
        eta_I = (3 - 3p) / (3 - 4p)
        eta_X = eta_Y = eta_Z = -p / (3 - 4p)
        gamma = (3 + 2p) / (3 - 4p)

    Args:
        p: Depolarizing error probability.

    Returns:
        Tuple of (quasi-probability dict, gamma factor).
    """
    denom = 3 - 4 * p

    eta_I = (3 - 3 * p) / denom
    eta_P = -p / denom  # eta_X = eta_Y = eta_Z

    quasi_probs = {
        'I': eta_I,
        'X': eta_P,
        'Y': eta_P,
        'Z': eta_P,
    }

    gamma = abs(eta_I) + 3 * abs(eta_P)

    return quasi_probs, gamma


def compute_quasi_probabilities_2q(p: float) -> Tuple[Dict[str, float], float]:
    """
    Compute quasi-probability decomposition for 2Q depolarizing noise.

    For 2-qubit depolarizing with error rate p:
        E(rho) = (1-p)rho + (p/15) sum_{P!=II} P rho P^dag

    The inverse has quasi-probabilities:
        eta_II = (15 - 15p) / (15 - 16p)
        eta_P  = -p / (15 - 16p) for P != II

    Args:
        p: 2-qubit depolarizing error probability.

    Returns:
        Tuple of (quasi-probability dict, gamma factor).
    """
    denom = 15 - 16 * p

    eta_II = (15 - 15 * p) / denom
    eta_P = -p / denom

    paulis_2q = []
    for p1 in ['I', 'X', 'Y', 'Z']:
        for p2 in ['I', 'X', 'Y', 'Z']:
            paulis_2q.append(p1 + p2)

    quasi_probs = {}
    for label in paulis_2q:
        if label == 'II':
            quasi_probs[label] = eta_II
        else:
            quasi_probs[label] = eta_P

    gamma = abs(eta_II) + 15 * abs(eta_P)

    return quasi_probs, gamma


# =============================================================================
# PEC SAMPLING
# =============================================================================

def sample_pec_correction(
    quasi_probs: Dict[str, float],
    gamma: float,
    rng: np.random.Generator
) -> Tuple[str, float]:
    """
    Sample a Pauli correction from the quasi-probability distribution.

    Sampling (see explanation_physicist.md, Section 2.3):
        Sample i with probability |eta_i|/gamma.
        Record sign = sgn(eta_i).
        The correction for this sample is sign_i.

    Args:
        quasi_probs: Quasi-probability dictionary.
        gamma: One-norm (sum |eta_i|).
        rng: Random number generator.

    Returns:
        Tuple of (sampled Pauli label, sign).
    """
    labels = list(quasi_probs.keys())
    probs = np.array([abs(quasi_probs[l]) for l in labels])
    probs = probs / probs.sum()  # Normalize to valid distribution

    idx = rng.choice(len(labels), p=probs)
    label = labels[idx]
    sign = 1.0 if quasi_probs[label] >= 0 else -1.0

    return label, sign


def apply_pauli_correction(qc: QuantumCircuit, pauli_label: str, qubits: List[int]):
    """
    Apply a Pauli operation to specified qubits.

    Args:
        qc: Circuit to modify.
        pauli_label: Pauli string (e.g., 'X', 'XY', 'IZ').
        qubits: Qubit indices.
    """
    for char, qubit in zip(pauli_label, qubits):
        if char == 'X':
            qc.x(qubit)
        elif char == 'Y':
            qc.y(qubit)
        elif char == 'Z':
            qc.z(qubit)
        # 'I' -> do nothing


def build_pec_circuit_instance(
    base_circuit: QuantumCircuit,
    quasi_probs_1q: Dict[str, float],
    quasi_probs_2q: Dict[str, float],
    gamma_1q: float,
    gamma_2q: float,
    rng: np.random.Generator
) -> Tuple[QuantumCircuit, float, float]:
    """
    Build one PEC circuit instance with sampled corrections.

    PEC instance (see explanation_physicist.md, Section 6.1):
        For each gate, sample a correction from the quasi-probability
        distribution. Track total gamma and total sign.

    Args:
        base_circuit: Original circuit with measurements.
        quasi_probs_1q: 1Q quasi-probabilities.
        quasi_probs_2q: 2Q quasi-probabilities.
        gamma_1q: 1Q gamma factor.
        gamma_2q: 2Q gamma factor.
        rng: Random number generator.

    Returns:
        Tuple of (modified circuit, total gamma, total sign).
    """
    n_q = base_circuit.num_qubits
    n_c = base_circuit.num_clbits

    qr = QuantumRegister(n_q, 'q')
    cr = ClassicalRegister(n_c, 'c')
    pec_qc = QuantumCircuit(qr, cr)

    total_gamma = 1.0
    total_sign = 1.0

    for inst in base_circuit.data:
        op = inst.operation
        qargs = [qr[base_circuit.qubits.index(q)] for q in inst.qubits]

        if op.name == 'measure':
            cargs = [cr[base_circuit.clbits.index(c)] for c in inst.clbits]
            pec_qc.measure(qargs[0], cargs[0])
            continue
        if op.name == 'barrier':
            pec_qc.barrier()
            continue

        # Apply original gate
        pec_qc.append(op, qargs)

        # Sample and apply PEC correction
        if len(qargs) == 1:
            label, sign = sample_pec_correction(quasi_probs_1q, gamma_1q, rng)
            apply_pauli_correction(pec_qc, label, [qargs[0]])
            total_gamma *= gamma_1q
            total_sign *= sign
        elif len(qargs) == 2:
            label, sign = sample_pec_correction(quasi_probs_2q, gamma_2q, rng)
            qubit_indices = [qargs[0], qargs[1]]
            apply_pauli_correction(pec_qc, label, qubit_indices)
            total_gamma *= gamma_2q
            total_sign *= sign

    return pec_qc, total_gamma, total_sign


# =============================================================================
# PEC ESTIMATOR
# =============================================================================

def run_pec_estimation(
    base_circuit: QuantumCircuit,
    observable_qubits: List[int],
    noise_params: Dict,
    backend: AerSimulator,
    n_samples: int = 500,
    shots_per_sample: int = 1,
    seed: int = 42
) -> Tuple[float, float, float]:
    """
    Run PEC estimation of an expectation value.

    PEC estimator (see explanation_physicist.md, Section 2.3):
        E[o_PEC] = <O>_ideal (unbiased!)
        Var(o_PEC) = gamma_total^2 * Var(o)

    Args:
        base_circuit: Original circuit with measurements.
        observable_qubits: Qubits participating in Z observable.
        noise_params: Dictionary of noise parameters.
        backend: Simulator backend.
        n_samples: Number of PEC Monte Carlo samples.
        shots_per_sample: Shots per sample circuit.
        seed: Random seed.

    Returns:
        Tuple of (PEC estimate, standard error, mean gamma).
    """
    rng = np.random.default_rng(seed)
    n_qubits = base_circuit.num_qubits

    # Compute quasi-probabilities
    qp_1q, gamma_1q = compute_quasi_probabilities_1q(noise_params['1q']['p_total'])
    qp_2q, gamma_2q = compute_quasi_probabilities_2q(noise_params['2q']['p_total'])

    pec_values = []

    for _ in range(n_samples):
        pec_qc, total_gamma, total_sign = build_pec_circuit_instance(
            base_circuit, qp_1q, qp_2q, gamma_1q, gamma_2q, rng
        )

        result = backend.run(pec_qc, shots=shots_per_sample).result()
        counts = result.get_counts()

        # Compute observable value from this sample
        total = sum(counts.values())
        for bs, count in counts.items():
            parity = sum(int(bs.zfill(n_qubits)[n_qubits - 1 - q]) for q in observable_qubits) % 2
            o_val = (-1) ** parity * count / total

            # PEC correction
            pec_val = total_gamma * total_sign * o_val
            pec_values.append(pec_val)

    pec_estimate = np.mean(pec_values)
    pec_stderr = np.std(pec_values) / np.sqrt(len(pec_values))
    mean_gamma = total_gamma  # Same for all samples with same circuit structure

    return pec_estimate, pec_stderr, mean_gamma


# =============================================================================
# TEST CIRCUITS
# =============================================================================

def build_bell_circuit() -> QuantumCircuit:
    """Build Bell state circuit."""
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr, name='Bell')
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.measure(qr, cr)
    return qc


def build_ghz_circuit(n_qubits: int = 3) -> QuantumCircuit:
    """Build GHZ state circuit."""
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='GHZ')
    qc.h(qr[0])
    for i in range(1, n_qubits):
        qc.cx(qr[0], qr[i])
    qc.measure(qr, cr)
    return qc


# =============================================================================
# DEMONSTRATIONS
# =============================================================================

def demo_pec_basic():
    """
    Basic PEC demonstration on a Bell state.

    Shows exact error cancellation via quasi-probability sampling.
    """
    print("=" * 70)
    print("DEMO 1: Basic PEC on Bell State")
    print("=" * 70)

    p_1q = 0.01
    p_2q = 0.03

    noise_model, noise_params = create_known_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    # Quasi-probabilities
    qp_1q, gamma_1q = compute_quasi_probabilities_1q(p_1q)
    qp_2q, gamma_2q = compute_quasi_probabilities_2q(p_2q)

    print(f"\n  Noise parameters: p_1q = {p_1q}, p_2q = {p_2q}")
    print(f"\n  1Q quasi-probabilities:")
    for label, eta in qp_1q.items():
        print(f"    eta_{label} = {eta:+.6f}")
    print(f"    gamma_1q = {gamma_1q:.6f}")

    print(f"\n  2Q gamma factor: {gamma_2q:.6f}")

    # Bell state: ideal <ZZ> = 1
    qc = build_bell_circuit()
    ideal_zz = 1.0

    # Raw noisy measurement
    result = sim.run(qc, shots=20000).result()
    raw_counts = result.get_counts()
    total = sum(raw_counts.values())
    raw_zz = sum((-1) ** (int(bs[0]) ^ int(bs[1])) * c / total for bs, c in raw_counts.items())

    # PEC estimation
    print(f"\n  Running PEC estimation (1000 samples)...")
    pec_est, pec_err, gamma_total = run_pec_estimation(
        qc, [0, 1], noise_params, sim,
        n_samples=1000, shots_per_sample=1, seed=42
    )

    print(f"\n  Results:")
    print(f"    Ideal <ZZ>:        {ideal_zz:.6f}")
    print(f"    Raw (noisy) <ZZ>:  {raw_zz:.6f} (error: {abs(raw_zz - ideal_zz):.6f})")
    print(f"    PEC <ZZ>:          {pec_est:.6f} +/- {pec_err:.6f} (error: {abs(pec_est - ideal_zz):.6f})")
    print(f"    Total gamma:       {gamma_total:.4f}")
    print(f"    Sampling overhead:  {gamma_total**2:.2f}x")

    return ideal_zz, raw_zz, pec_est, pec_err


def demo_pec_convergence():
    """
    Show PEC convergence with increasing number of samples.
    """
    print("\n" + "=" * 70)
    print("DEMO 2: PEC Convergence Analysis")
    print("=" * 70)

    p_1q = 0.01
    p_2q = 0.03
    noise_model, noise_params = create_known_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    qc = build_bell_circuit()
    ideal_zz = 1.0

    sample_counts = [50, 100, 200, 500, 1000, 2000, 5000]

    print(f"\n  {'N_samples':<12} {'PEC <ZZ>':<12} {'Std Error':<12} {'|Bias|':<12}")
    print(f"  {'-'*48}")

    for n in sample_counts:
        pec_est, pec_err, _ = run_pec_estimation(
            qc, [0, 1], noise_params, sim,
            n_samples=n, shots_per_sample=1, seed=42
        )
        bias = abs(pec_est - ideal_zz)
        print(f"  {n:<12} {pec_est:<12.6f} {pec_err:<12.6f} {bias:<12.6f}")


def demo_overhead_scaling():
    """
    Analyze PEC sampling overhead scaling with noise and circuit depth.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: PEC Sampling Overhead Scaling")
    print("=" * 70)

    print(f"\n  Gamma factor vs error rate (1Q depolarizing):")
    print(f"  {'p':<10} {'gamma_1q':<12} {'gamma^2':<12} {'Overhead':<12}")
    print(f"  {'-'*46}")
    for p in [0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]:
        _, gamma = compute_quasi_probabilities_1q(p)
        print(f"  {p:<10.3f} {gamma:<12.6f} {gamma**2:<12.4f} {gamma**2:<12.1f}x")

    print(f"\n  Total overhead vs circuit depth (p_1q=0.01, p_2q=0.03):")
    _, gamma_1q = compute_quasi_probabilities_1q(0.01)
    _, gamma_2q = compute_quasi_probabilities_2q(0.03)

    print(f"  {'Gates (1Q+2Q)':<18} {'gamma_total':<14} {'gamma^2':<14} {'Overhead':<12}")
    print(f"  {'-'*58}")
    for n_1q, n_2q in [(5, 2), (10, 5), (20, 10), (50, 25), (100, 50)]:
        gamma_total = gamma_1q ** n_1q * gamma_2q ** n_2q
        print(f"  {f'{n_1q}+{n_2q}':<18} {gamma_total:<14.4f} {gamma_total**2:<14.2f} {gamma_total**2:<12.0f}x")


def demo_pec_vs_zne():
    """
    Compare PEC with ZNE on the same circuit.
    """
    print("\n" + "=" * 70)
    print("DEMO 4: PEC vs ZNE Comparison")
    print("=" * 70)

    p_1q = 0.01
    p_2q = 0.03
    noise_model, noise_params = create_known_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    n_qubits = 2
    qc = build_bell_circuit()
    ideal_zz = 1.0

    # Raw
    result = sim.run(qc, shots=20000).result()
    raw_counts = result.get_counts()
    total = sum(raw_counts.values())
    raw_zz = sum((-1) ** (int(bs[0]) ^ int(bs[1])) * c / total for bs, c in raw_counts.items())

    # PEC
    pec_est, pec_err, gamma = run_pec_estimation(
        qc, [0, 1], noise_params, sim,
        n_samples=2000, shots_per_sample=1, seed=42
    )

    # ZNE (simple gate folding)
    qc_base = QuantumCircuit(2)
    qc_base.h(0)
    qc_base.cx(0, 1)

    zne_lambdas = [1, 3, 5]
    zne_values = []
    for lam in zne_lambdas:
        folded = qc_base.copy()
        for _ in range((lam - 1) // 2):
            folded = folded.compose(qc_base.inverse())
            folded = folded.compose(qc_base.copy())
        folded.measure_all()
        result = sim.run(folded, shots=20000).result()
        counts = result.get_counts()
        total = sum(counts.values())
        val = sum((-1) ** (int(bs[0]) ^ int(bs[1])) * c / total for bs, c in counts.items())
        zne_values.append(val)

    # ZNE extrapolation (linear)
    coeffs = np.polyfit(zne_lambdas, zne_values, 1)
    zne_est = np.polyval(coeffs, 0)

    print(f"\n  {'Method':<20} {'Estimate':<12} {'|Error|':<12} {'Notes':<25}")
    print(f"  {'-'*69}")
    print(f"  {'Ideal':<20} {ideal_zz:<12.6f} {'---':<12} {'---':<25}")
    print(f"  {'Raw':<20} {raw_zz:<12.6f} {abs(raw_zz-ideal_zz):<12.6f} {'No mitigation':<25}")
    print(f"  {'PEC':<20} {pec_est:<12.6f} {abs(pec_est-ideal_zz):<12.6f} {f'gamma^2={gamma**2:.1f}x overhead':<25}")
    print(f"  {'ZNE (linear)':<20} {zne_est:<12.6f} {abs(zne_est-ideal_zz):<12.6f} {'Approximate (biased)':<25}")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_pec_convergence():
    """Plot PEC convergence with sample count."""
    p_1q, p_2q = 0.01, 0.03
    noise_model, noise_params = create_known_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)
    qc = build_bell_circuit()

    samples = [20, 50, 100, 200, 500, 1000, 2000]
    estimates = []
    errors = []

    for n in samples:
        est, err, _ = run_pec_estimation(
            qc, [0, 1], noise_params, sim, n_samples=n, seed=42
        )
        estimates.append(est)
        errors.append(err)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(samples, estimates, yerr=errors, fmt='bo-', capsize=5, label='PEC estimate')
    ax.axhline(y=1.0, color='green', linestyle='--', linewidth=2, label='Ideal <ZZ> = 1')
    ax.set_xlabel('Number of PEC samples')
    ax.set_ylabel('<ZZ> estimate')
    ax.set_title('PEC Convergence')
    ax.set_xscale('log')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run all PEC demonstrations.

    Covers:
    - Basic PEC on Bell state
    - Convergence with sample count
    - Sampling overhead scaling analysis
    - PEC vs ZNE comparison
    """
    print("Probabilistic Error Cancellation (PEC) - Local Demonstrations")
    print("=" * 70)
    print("See explanation_physicist.md for theoretical background.")
    print("See explanation_simple.md for intuitive explanation.")
    print()

    demo_pec_basic()
    demo_pec_convergence()
    demo_overhead_scaling()
    demo_pec_vs_zne()

    print("\n" + "=" * 70)
    print("Generating PEC convergence plot...")
    plot_pec_convergence()

    print("\nAll demonstrations complete.")


if __name__ == '__main__':
    main()
