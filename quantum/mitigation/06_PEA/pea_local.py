"""
Probabilistic Error Amplification (PEA) - Local Simulator Implementation
==========================================================================

Demonstrates PEA for controlled noise amplification combined with ZNE.
PEA injects Pauli errors probabilistically to achieve continuous noise
scaling, then extrapolates to zero noise.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
PEA amplifies noise by injecting Pauli errors with probability
p_inject = (lambda-1)*p / (1-p) after each gate. Total effective
error rate becomes lambda*p. Combined with ZNE for extrapolation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typing import Dict, List, Tuple, Optional

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, pauli_error


# =============================================================================
# NOISE MODEL
# =============================================================================

def create_pauli_noise_model(
    p_1q: float = 0.005,
    p_2q: float = 0.02,
    pauli_ratios_1q: Tuple[float, float, float] = (1/3, 1/3, 1/3),
    pauli_ratios_2q: Optional[Dict[str, float]] = None
) -> NoiseModel:
    """
    Create a Pauli noise model with known error rates.

    Pauli channel (see explanation_physicist.md, Section 3.1):
        Lambda(rho) = (1-p)*rho + p*sum_k q_k P_k rho P_k^dag
        For depolarizing: q_X = q_Y = q_Z = 1/3

    Args:
        p_1q: Single-qubit total error probability.
        p_2q: Two-qubit total error probability.
        pauli_ratios_1q: Relative probabilities (q_X, q_Y, q_Z).
        pauli_ratios_2q: 2-qubit Pauli ratios (default: uniform depolarizing).

    Returns:
        NoiseModel with known Pauli error rates.
    """
    noise_model = NoiseModel()

    # Single-qubit Pauli error
    qx, qy, qz = pauli_ratios_1q
    error_1q = pauli_error([
        ('X', p_1q * qx),
        ('Y', p_1q * qy),
        ('Z', p_1q * qz),
        ('I', 1 - p_1q)
    ])
    noise_model.add_all_qubit_quantum_error(error_1q, ['x', 'h', 'sx', 'ry', 'rz'])

    # Two-qubit depolarizing error
    error_2q = depolarizing_error(p_2q, 2)
    noise_model.add_all_qubit_quantum_error(error_2q, ['cx'])

    return noise_model


# =============================================================================
# PEA IMPLEMENTATION
# =============================================================================

def compute_injection_probabilities(
    base_error_rate: float,
    noise_factor: float,
    pauli_ratios: Tuple[float, float, float] = (1/3, 1/3, 1/3)
) -> Dict[str, float]:
    """
    Compute Pauli injection probabilities for PEA.

    PEA injection (see explanation_physicist.md, Section 3.2):
        p_inject_total = (lambda - 1) * p / (1 - p)
        p_inject_k = p_inject_total * q_k

    Args:
        base_error_rate: Original error probability p.
        noise_factor: Desired noise amplification lambda (>= 1).
        pauli_ratios: Relative Pauli error probabilities (q_X, q_Y, q_Z).

    Returns:
        Dictionary of Pauli injection probabilities.
    """
    if noise_factor <= 1.0:
        return {'X': 0.0, 'Y': 0.0, 'Z': 0.0}

    # Total injection probability (see explanation_physicist.md, Section 3.2)
    p = base_error_rate
    p_inject_total = (noise_factor - 1) * p / (1 - p)

    # Clip to valid range
    p_inject_total = min(p_inject_total, 1.0)

    qx, qy, qz = pauli_ratios
    return {
        'X': p_inject_total * qx,
        'Y': p_inject_total * qy,
        'Z': p_inject_total * qz,
    }


def build_pea_circuit(
    base_circuit: QuantumCircuit,
    injection_probs_1q: Dict[str, float],
    injection_probs_2q: float,
    rng: np.random.Generator
) -> QuantumCircuit:
    """
    Build a PEA-amplified circuit instance.

    PEA per-shot randomization (see explanation_physicist.md, Section 6.1):
        After each gate, with computed probability, insert a random
        Pauli error from the learned noise distribution.

    Args:
        base_circuit: Original circuit (with measurements).
        injection_probs_1q: 1Q Pauli injection probabilities.
        injection_probs_2q: Total 2Q injection probability.
        rng: Random number generator.

    Returns:
        Circuit with probabilistically injected Pauli errors.
    """
    n_qubits = base_circuit.num_qubits
    n_clbits = base_circuit.num_clbits

    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_clbits, 'c')
    pea_qc = QuantumCircuit(qr, cr)

    p_total_1q = sum(injection_probs_1q.values())

    for inst in base_circuit.data:
        op = inst.operation
        qargs = [qr[base_circuit.qubits.index(q)] for q in inst.qubits]

        if op.name == 'measure':
            cargs = [cr[base_circuit.clbits.index(c)] for c in inst.clbits]
            pea_qc.measure(qargs[0], cargs[0])
            continue

        if op.name == 'barrier':
            pea_qc.barrier()
            continue

        # Apply the original gate
        pea_qc.append(op, qargs)

        # Probabilistically inject Pauli errors after 1Q gates
        if len(qargs) == 1 and p_total_1q > 0:
            if rng.random() < p_total_1q:
                # Choose which Pauli
                r = rng.random() * p_total_1q
                cumulative = 0
                for pauli, prob in injection_probs_1q.items():
                    cumulative += prob
                    if r < cumulative:
                        if pauli == 'X':
                            pea_qc.x(qargs[0])
                        elif pauli == 'Y':
                            pea_qc.y(qargs[0])
                        elif pauli == 'Z':
                            pea_qc.z(qargs[0])
                        break

        # Inject errors after 2Q gates
        elif len(qargs) == 2 and injection_probs_2q > 0:
            if rng.random() < injection_probs_2q:
                # Random 2-qubit Pauli
                paulis = ['X', 'Y', 'Z']
                for q in qargs:
                    p_choice = rng.choice(paulis)
                    if p_choice == 'X':
                        pea_qc.x(q)
                    elif p_choice == 'Y':
                        pea_qc.y(q)
                    elif p_choice == 'Z':
                        pea_qc.z(q)

    return pea_qc


def run_pea_experiment(
    base_circuit: QuantumCircuit,
    noise_factor: float,
    base_error_1q: float,
    base_error_2q: float,
    backend: AerSimulator,
    n_samples: int = 50,
    shots_per_sample: int = 200,
    seed: int = 42
) -> Dict[str, int]:
    """
    Run PEA experiment at a given noise factor.

    PEA protocol (see explanation_physicist.md, Section 6.1):
        For each sample, generate a randomly error-injected circuit
        instance, run it, and aggregate results.

    Args:
        base_circuit: Original circuit with measurements.
        noise_factor: Desired noise amplification.
        base_error_1q: Base 1Q error rate.
        base_error_2q: Base 2Q error rate.
        backend: Simulator backend.
        n_samples: Number of random PEA instances.
        shots_per_sample: Shots per instance.
        seed: Random seed.

    Returns:
        Aggregated measurement counts.
    """
    rng = np.random.default_rng(seed)

    # Compute injection probabilities
    inj_1q = compute_injection_probabilities(base_error_1q, noise_factor)
    p_inject_2q = (noise_factor - 1) * base_error_2q / (1 - base_error_2q) if noise_factor > 1 else 0

    total_counts = {}

    for _ in range(n_samples):
        pea_qc = build_pea_circuit(base_circuit, inj_1q, p_inject_2q, rng)
        result = backend.run(pea_qc, shots=shots_per_sample).result()
        counts = result.get_counts()
        for bs, count in counts.items():
            total_counts[bs] = total_counts.get(bs, 0) + count

    return total_counts


# =============================================================================
# ZNE EXTRAPOLATION
# =============================================================================

def extrapolate_exponential(lambdas, values):
    """Exponential extrapolation to lambda=0."""
    def model(x, a, b, c):
        return a * np.exp(-b * x) + c
    try:
        popt, _ = curve_fit(model, lambdas, values, p0=[values[0], 0.1, 0], maxfev=5000)
        return float(model(0, *popt))
    except Exception:
        coeffs = np.polyfit(lambdas, values, 1)
        return float(np.polyval(coeffs, 0))


def extrapolate_linear(lambdas, values):
    """Linear extrapolation to lambda=0."""
    coeffs = np.polyfit(lambdas, values, 1)
    return float(np.polyval(coeffs, 0))


# =============================================================================
# EXPECTATION VALUE COMPUTATION
# =============================================================================

def compute_zz_expectation(counts: Dict[str, int], n_qubits: int) -> float:
    """Compute <ZZ...Z> from counts."""
    total = sum(counts.values())
    exp_val = 0.0
    for bs, count in counts.items():
        parity = sum(int(b) for b in bs.zfill(n_qubits)) % 2
        exp_val += (-1) ** parity * count / total
    return exp_val


# =============================================================================
# TEST CIRCUITS
# =============================================================================

def build_ghz_circuit(n_qubits: int = 3) -> QuantumCircuit:
    """Build GHZ state circuit with measurements."""
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='GHZ')
    qc.h(qr[0])
    for i in range(1, n_qubits):
        qc.cx(qr[0], qr[i])
    qc.measure(qr, cr)
    return qc


def build_variational_circuit(theta: float) -> QuantumCircuit:
    """Build a 2-qubit variational circuit with measurements."""
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.ry(theta, qr[0])
    qc.cx(qr[0], qr[1])
    qc.measure(qr, cr)
    return qc


# =============================================================================
# DEMONSTRATIONS
# =============================================================================

def demo_pea_basic():
    """
    Basic PEA demonstration: amplify noise at continuous lambda values.

    Shows that PEA produces the expected noise scaling compared to
    theoretical prediction.
    """
    print("=" * 70)
    print("DEMO 1: Basic PEA Noise Amplification")
    print("=" * 70)

    n_qubits = 3
    p_1q = 0.005
    p_2q = 0.02

    print(f"\n  Base error rates: p_1q = {p_1q}, p_2q = {p_2q}")

    noise_model = create_pauli_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    qc = build_ghz_circuit(n_qubits)
    ideal_value = 1.0  # <ZZZ> for GHZ

    # PEA at continuous noise factors
    noise_factors = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    pea_values = []

    n_samples = 40
    shots_per = 500

    print(f"\n  {'lambda':<10} {'<ZZZ>':<12} {'PEA inject. prob':<20}")
    print(f"  {'-'*42}")

    for lam in noise_factors:
        inj = compute_injection_probabilities(p_1q, lam)
        p_total = sum(inj.values())

        counts = run_pea_experiment(
            qc, lam, p_1q, p_2q, sim,
            n_samples=n_samples, shots_per_sample=shots_per, seed=42
        )
        val = compute_zz_expectation(counts, n_qubits)
        pea_values.append(val)

        print(f"  {lam:<10.1f} {val:<12.6f} {p_total:<20.6f}")

    return noise_factors, pea_values


def demo_pea_zne():
    """
    PEA + ZNE pipeline: use PEA for noise amplification, ZNE for extrapolation.

    Compares PEA+ZNE with gate-folding+ZNE and raw (no mitigation).
    """
    print("\n" + "=" * 70)
    print("DEMO 2: PEA + ZNE Pipeline")
    print("=" * 70)

    n_qubits = 2
    p_1q = 0.005
    p_2q = 0.02

    noise_model = create_pauli_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    theta = np.pi / 3
    qc = build_variational_circuit(theta)

    # Compute ideal
    qc_ideal = QuantumCircuit(2)
    qc_ideal.h(0)
    qc_ideal.cx(0, 1)
    qc_ideal.ry(theta, 0)
    qc_ideal.cx(0, 1)
    sv = Statevector.from_instruction(qc_ideal)
    ideal_probs = sv.probabilities_dict()
    ideal_zz = sum((-1) ** (int(k[0]) ^ int(k[1])) * v for k, v in ideal_probs.items())

    print(f"\n  Ideal <ZZ> = {ideal_zz:.6f}")
    print(f"  theta = pi/3, p_1q = {p_1q}, p_2q = {p_2q}")

    # === PEA + ZNE ===
    pea_lambdas = [1.0, 1.5, 2.0, 2.5, 3.0]
    pea_values = []

    print(f"\n  PEA noise amplification:")
    for lam in pea_lambdas:
        counts = run_pea_experiment(
            qc, lam, p_1q, p_2q, sim,
            n_samples=60, shots_per_sample=300, seed=42
        )
        val = compute_zz_expectation(counts, n_qubits)
        pea_values.append(val)
        print(f"    lambda={lam:.1f}: <ZZ> = {val:.6f}")

    pea_zne_exp = extrapolate_exponential(pea_lambdas, pea_values)
    pea_zne_lin = extrapolate_linear(pea_lambdas[:2], pea_values[:2])

    # === Gate Folding + ZNE (for comparison) ===
    gf_lambdas = [1, 3, 5]
    gf_values = []

    print(f"\n  Gate folding noise amplification:")
    for lam in gf_lambdas:
        # Build folded circuit
        qc_base = QuantumCircuit(2)
        qc_base.h(0)
        qc_base.cx(0, 1)
        qc_base.ry(theta, 0)
        qc_base.cx(0, 1)

        folded = qc_base.copy()
        n_folds = (lam - 1) // 2
        for _ in range(n_folds):
            folded = folded.compose(qc_base.inverse())
            folded = folded.compose(qc_base.copy())
        folded.measure_all()

        result = sim.run(folded, shots=18000).result()
        counts = result.get_counts()
        val = compute_zz_expectation(counts, n_qubits)
        gf_values.append(val)
        print(f"    lambda={lam}: <ZZ> = {val:.6f}")

    gf_zne_exp = extrapolate_exponential(gf_lambdas, gf_values)

    # === Raw (no mitigation) ===
    raw_val = pea_values[0]  # lambda=1

    # === Compare ===
    print(f"\n  {'Method':<25} {'<ZZ>':<12} {'|Error|':<12}")
    print(f"  {'-'*49}")
    print(f"  {'Ideal':<25} {ideal_zz:<12.6f} {'---':<12}")
    print(f"  {'Raw (no mitigation)':<25} {raw_val:<12.6f} {abs(raw_val - ideal_zz):<12.6f}")
    print(f"  {'PEA+ZNE (exp.)':<25} {pea_zne_exp:<12.6f} {abs(pea_zne_exp - ideal_zz):<12.6f}")
    print(f"  {'PEA+ZNE (linear)':<25} {pea_zne_lin:<12.6f} {abs(pea_zne_lin - ideal_zz):<12.6f}")
    print(f"  {'Gate Fold+ZNE (exp.)':<25} {gf_zne_exp:<12.6f} {abs(gf_zne_exp - ideal_zz):<12.6f}")

    return pea_lambdas, pea_values, ideal_zz


def demo_continuous_lambda():
    """
    Show PEA's advantage: fine-grained continuous noise scaling.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: Continuous Noise Scaling with PEA")
    print("=" * 70)

    n_qubits = 2
    p_1q = 0.005
    p_2q = 0.02

    noise_model = create_pauli_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    qc = build_ghz_circuit(2)
    ideal_zz = 1.0

    # Dense lambda sweep
    lambdas = np.arange(1.0, 6.1, 0.5)
    values = []

    print(f"\n  Fine-grained PEA sweep ({len(lambdas)} noise factors):")
    print(f"  {'lambda':<10} {'<ZZ>':<12}")
    print(f"  {'-'*22}")

    for lam in lambdas:
        counts = run_pea_experiment(
            qc, lam, p_1q, p_2q, sim,
            n_samples=30, shots_per_sample=400, seed=42
        )
        val = compute_zz_expectation(counts, n_qubits)
        values.append(val)
        print(f"  {lam:<10.1f} {val:<12.6f}")

    # Fit exponential
    def exp_model(x, a, b, c):
        return a * np.exp(-b * x) + c
    try:
        popt, _ = curve_fit(exp_model, lambdas, values, p0=[1, 0.1, 0])
        zne_val = exp_model(0, *popt)
        print(f"\n  Exponential fit -> E(0) = {zne_val:.6f}")
        print(f"  Error: {abs(zne_val - ideal_zz):.6f}")
    except Exception as e:
        print(f"\n  Fit failed: {e}")

    return lambdas, values


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_pea_results(lambdas, values, ideal, save_path=None):
    """Plot PEA noise scaling and extrapolation."""
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(lambdas, values, color='red', s=80, zorder=5, label='PEA measurements')
    ax.axhline(y=ideal, color='green', linestyle='--', linewidth=2, label=f'Ideal = {ideal:.4f}')

    # Fit and plot
    from scipy.optimize import curve_fit
    def exp_model(x, a, b, c):
        return a * np.exp(-b * x) + c
    try:
        popt, _ = curve_fit(exp_model, lambdas, values, p0=[values[0], 0.1, 0])
        lam_fine = np.linspace(0, max(lambdas) + 0.5, 100)
        ax.plot(lam_fine, exp_model(lam_fine, *popt), 'b-', alpha=0.5, label='Exponential fit')
        zne = exp_model(0, *popt)
        ax.scatter([0], [zne], marker='*', s=300, color='blue', zorder=6,
                   label=f'ZNE = {zne:.4f}')
    except Exception:
        pass

    ax.set_xlabel('Noise Factor (lambda)')
    ax.set_ylabel('Expectation Value')
    ax.set_title('PEA + ZNE: Probabilistic Error Amplification')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run all PEA demonstrations.

    Covers:
    - Basic PEA noise amplification
    - PEA + ZNE pipeline (vs gate folding + ZNE)
    - Continuous lambda sweep
    """
    print("Probabilistic Error Amplification (PEA) - Local Demonstrations")
    print("=" * 70)
    print("See explanation_physicist.md for theoretical background.")
    print("See explanation_simple.md for intuitive explanation.")
    print()

    # Demo 1: Basic PEA
    demo_pea_basic()

    # Demo 2: PEA + ZNE
    pea_lambdas, pea_values, ideal = demo_pea_zne()

    # Demo 3: Continuous lambda
    demo_continuous_lambda()

    # Plot
    print("\n" + "=" * 70)
    print("Generating PEA+ZNE plot...")
    plot_pea_results(pea_lambdas, pea_values, ideal)

    print("\nAll demonstrations complete.")


if __name__ == '__main__':
    main()
