"""
Zero-Noise Extrapolation (ZNE) - Local Simulator Implementation
=================================================================

Demonstrates ZNE: run circuits at multiple noise levels via gate folding,
then extrapolate to zero noise using linear, polynomial, and exponential
fits. Compares raw vs ZNE-mitigated expectation values.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Gate folding: G -> G G^dag G (triples noise, same ideal unitary).
Noise model: E(lambda) = E_ideal * exp(-gamma * lambda) approximately.
Extrapolation to lambda=0 yields E_ideal estimate.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typing import Dict, List, Tuple, Optional, Callable

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# =============================================================================
# NOISE MODEL
# =============================================================================

def create_depolarizing_noise_model(
    p_1q: float = 0.001,
    p_2q: float = 0.01
) -> NoiseModel:
    """
    Create depolarizing noise model.

    Depolarizing channel (see explanation_physicist.md, Section 4.3):
        E(rho) = (1-p) rho + p * I/d
        Under gate folding (lambda=2k+1), effective error: p -> lambda*p

    Args:
        p_1q: Single-qubit depolarizing error probability.
        p_2q: Two-qubit depolarizing error probability.

    Returns:
        NoiseModel with depolarizing errors.
    """
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p_1q, 1), ['x', 'y', 'z', 'h', 'rx', 'ry', 'rz', 'sx'])
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p_2q, 2), ['cx'])
    return noise_model


# =============================================================================
# GATE FOLDING
# =============================================================================

def fold_circuit_global(circuit: QuantumCircuit, noise_factor: int) -> QuantumCircuit:
    """
    Apply global gate folding to amplify noise.

    Global folding (see explanation_physicist.md, Section 4.1):
        C -> C . (C^dag . C)^k  for noise_factor = 2k+1
        The folded circuit is identical to C in the noiseless case.

    Args:
        circuit: Original circuit (without measurements).
        noise_factor: Odd integer >= 1 (noise amplification factor).

    Returns:
        Folded circuit with same ideal action but amplified noise.
    """
    if noise_factor == 1:
        return circuit.copy()

    assert noise_factor % 2 == 1, "Noise factor must be odd for global folding"
    n_folds = (noise_factor - 1) // 2

    folded = circuit.copy()
    for _ in range(n_folds):
        folded = folded.compose(circuit.inverse())
        folded = folded.compose(circuit.copy())

    return folded


def fold_gates_local(
    circuit: QuantumCircuit,
    noise_factor: float
) -> QuantumCircuit:
    """
    Apply local gate folding for fractional noise amplification.

    Local folding (see explanation_physicist.md, Section 4.2):
        Fold individual gates G -> G G^dag G.
        For noise_factor = 1 + 2*f, fold fraction f of gates.

    Args:
        circuit: Original circuit (without measurements).
        noise_factor: Float >= 1.0.

    Returns:
        Locally folded circuit.
    """
    if noise_factor <= 1.0:
        return circuit.copy()

    # Number of complete folds for all gates
    n_complete_folds = int((noise_factor - 1) // 2)
    fractional_part = (noise_factor - 1) / 2 - n_complete_folds

    # Get list of non-barrier, non-measure instructions
    gate_data = [inst for inst in circuit.data
                 if inst.operation.name not in ('barrier', 'measure')]
    n_gates = len(gate_data)

    # Number of gates to fold one additional time
    n_extra_fold = int(round(fractional_part * n_gates))

    # Build folded circuit
    n_qubits = circuit.num_qubits
    folded = QuantumCircuit(n_qubits)

    for i, inst in enumerate(circuit.data):
        op = inst.operation
        if op.name in ('barrier', 'measure'):
            continue

        qargs = [circuit.qubits.index(q) for q in inst.qubits]

        # Apply original gate
        folded.append(op, qargs)

        # Complete folds
        for _ in range(n_complete_folds):
            folded.append(op.inverse(), qargs)
            folded.append(op, qargs)

        # Extra fold for fractional part
        gate_idx = [j for j, d in enumerate(circuit.data)
                    if d.operation.name not in ('barrier', 'measure')].index(
                        circuit.data.index(inst)) if inst in gate_data else -1

        if gate_idx >= 0 and gate_idx < n_extra_fold:
            folded.append(op.inverse(), qargs)
            folded.append(op, qargs)

    return folded


# =============================================================================
# EXTRAPOLATION METHODS
# =============================================================================

def extrapolate_linear(
    noise_factors: List[float],
    expectation_values: List[float]
) -> float:
    """
    Linear extrapolation to zero noise.

    Linear model (see explanation_physicist.md, Section 3.1):
        E(lambda) = a + b * lambda
        E_ZNE = a (intercept at lambda=0)

    Args:
        noise_factors: Noise amplification factors.
        expectation_values: Measured expectation values.

    Returns:
        Extrapolated zero-noise value.
    """
    coeffs = np.polyfit(noise_factors, expectation_values, deg=1)
    return np.polyval(coeffs, 0)


def extrapolate_polynomial(
    noise_factors: List[float],
    expectation_values: List[float],
    degree: int = 2
) -> float:
    """
    Polynomial extrapolation to zero noise.

    Polynomial model (see explanation_physicist.md, Section 3.2):
        E(lambda) = a_0 + a_1*lambda + ... + a_d*lambda^d
        E_ZNE = a_0

    Args:
        noise_factors: Noise factors.
        expectation_values: Measured values.
        degree: Polynomial degree.

    Returns:
        Extrapolated zero-noise value.
    """
    degree = min(degree, len(noise_factors) - 1)
    coeffs = np.polyfit(noise_factors, expectation_values, deg=degree)
    return np.polyval(coeffs, 0)


def extrapolate_exponential(
    noise_factors: List[float],
    expectation_values: List[float]
) -> float:
    """
    Exponential extrapolation to zero noise.

    Exponential model (see explanation_physicist.md, Section 3.3):
        E(lambda) = A * exp(-B * lambda) + C
        E_ZNE = A + C (lambda=0)

    For depolarizing noise, this is the physically motivated model.

    Args:
        noise_factors: Noise factors.
        expectation_values: Measured values.

    Returns:
        Extrapolated zero-noise value.
    """
    x = np.array(noise_factors)
    y = np.array(expectation_values)

    def exp_model(lam, a, b, c):
        return a * np.exp(-b * lam) + c

    try:
        # Initial guess
        p0 = [y[0], 0.1, 0.0]
        popt, _ = curve_fit(exp_model, x, y, p0=p0, maxfev=5000)
        return float(exp_model(0, *popt))
    except (RuntimeError, ValueError):
        # Fall back to linear
        return extrapolate_linear(noise_factors, expectation_values)


def richardson_extrapolation(
    noise_factors: List[float],
    expectation_values: List[float]
) -> float:
    """
    Richardson extrapolation.

    Richardson (see explanation_physicist.md, Section 3.4):
        E_ZNE = sum_i w_i * E(lambda_i)
        Weights chosen to cancel first M-1 error terms.

    Args:
        noise_factors: Noise factors.
        expectation_values: Measured values.

    Returns:
        Richardson-extrapolated zero-noise value.
    """
    M = len(noise_factors)
    lambdas = np.array(noise_factors)
    E_vals = np.array(expectation_values)

    # Solve for weights: sum w_i * lambda_i^k = delta_{k,0} for k=0,...,M-1
    V = np.vander(lambdas, M, increasing=True).T  # Vandermonde-like
    rhs = np.zeros(M)
    rhs[0] = 1.0

    try:
        weights = np.linalg.solve(V, rhs)
    except np.linalg.LinAlgError:
        weights = np.linalg.lstsq(V, rhs, rcond=None)[0]

    return float(weights @ E_vals)


# =============================================================================
# EXPECTATION VALUE COMPUTATION
# =============================================================================

def compute_expectation_value(
    counts: Dict[str, int],
    observable: str,
    n_qubits: int
) -> float:
    """
    Compute expectation value of a Pauli observable from counts.

    For ZZ...Z on all qubits:
        <ZZ...Z> = sum_x (-1)^{parity(x)} * P(x)

    For a general Pauli string, we measure in the appropriate basis
    (here assuming Z-basis measurement).

    Args:
        counts: Measurement counts.
        observable: Pauli string (e.g., 'ZZ', 'ZI', 'IZ').
        n_qubits: Number of qubits.

    Returns:
        Expectation value.
    """
    total = sum(counts.values())
    exp_val = 0.0

    for bitstring, count in counts.items():
        bs = bitstring.zfill(n_qubits)
        # Compute eigenvalue: product of (-1)^{bit} for each Z in observable
        eigenvalue = 1.0
        for i, pauli in enumerate(observable):
            if pauli == 'Z':
                bit = int(bs[i])
                eigenvalue *= (-1) ** bit
            # I contributes factor 1 (no dependence on bit)

        exp_val += eigenvalue * count / total

    return exp_val


# =============================================================================
# TEST CIRCUITS
# =============================================================================

def build_variational_circuit(theta: float, n_qubits: int = 2) -> QuantumCircuit:
    """
    Build a simple variational circuit.

    Creates an entangled state with tunable parameter theta.

    Args:
        theta: Variational parameter.
        n_qubits: Number of qubits.

    Returns:
        Parametric circuit (without measurements).
    """
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.ry(theta, 0)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    return qc


def build_ghz_circuit(n_qubits: int = 3) -> QuantumCircuit:
    """
    Build GHZ state circuit.

    |GHZ> = (|00...0> + |11...1>) / sqrt(2)
    Ideal: <ZZ...Z> = 1 (all qubits same parity)

    Args:
        n_qubits: Number of qubits.

    Returns:
        GHZ circuit (without measurements).
    """
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)
    return qc


# =============================================================================
# DEMONSTRATIONS
# =============================================================================

def demo_basic_zne():
    """
    Basic ZNE demonstration with gate folding.

    Runs a simple circuit at noise factors 1, 3, 5 and extrapolates
    to zero noise using multiple extrapolation methods.
    """
    print("=" * 70)
    print("DEMO 1: Basic ZNE with Gate Folding")
    print("=" * 70)

    n_qubits = 2
    theta = np.pi / 4
    shots = 20000
    noise_factors = [1, 3, 5]

    p_1q, p_2q = 0.002, 0.015
    print(f"\n  Noise: p_1q = {p_1q}, p_2q = {p_2q}")
    print(f"  Noise factors: {noise_factors}")
    print(f"  Shots per noise level: {shots}")

    noise_model = create_depolarizing_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    # Build base circuit
    base_qc = build_variational_circuit(theta, n_qubits)

    # Compute ideal expectation value
    sv = Statevector.from_instruction(base_qc)
    ideal_probs = sv.probabilities_dict()
    ideal_zz = sum((-1) ** (int(k[0]) ^ int(k[1])) * v for k, v in ideal_probs.items())
    print(f"\n  Ideal <ZZ> = {ideal_zz:.6f}")

    # Run at each noise level
    noisy_values = []
    print(f"\n  {'lambda':<10} {'<ZZ>_noisy':<15} {'Depth':<10}")
    print(f"  {'-'*35}")

    for lam in noise_factors:
        # Fold circuit
        folded = fold_circuit_global(base_qc, lam)
        depth = folded.depth()

        # Add measurements
        qc_meas = folded.copy()
        qc_meas.measure_all()

        # Run
        result = sim.run(qc_meas, shots=shots).result()
        counts = result.get_counts()
        zz_val = compute_expectation_value(counts, 'ZZ', n_qubits)
        noisy_values.append(zz_val)

        print(f"  {lam:<10} {zz_val:<15.6f} {depth:<10}")

    # Extrapolate
    print(f"\n  Extrapolation results:")
    print(f"  {'Method':<20} {'E_ZNE':<12} {'|Error|':<12}")
    print(f"  {'-'*44}")

    methods = {
        'Linear': extrapolate_linear(noise_factors, noisy_values),
        'Quadratic': extrapolate_polynomial(noise_factors, noisy_values, degree=2),
        'Exponential': extrapolate_exponential(noise_factors, noisy_values),
        'Richardson': richardson_extrapolation(noise_factors, noisy_values),
    }

    for name, zne_val in methods.items():
        error = abs(zne_val - ideal_zz)
        print(f"  {name:<20} {zne_val:<12.6f} {error:<12.6f}")

    raw_error = abs(noisy_values[0] - ideal_zz)
    best_method = min(methods.items(), key=lambda x: abs(x[1] - ideal_zz))
    print(f"\n  Raw error (lambda=1): {raw_error:.6f}")
    print(f"  Best ZNE method: {best_method[0]} (error = {abs(best_method[1] - ideal_zz):.6f})")
    print(f"  Improvement: {raw_error / abs(best_method[1] - ideal_zz):.1f}x" if abs(best_method[1] - ideal_zz) > 1e-8 else "  Improvement: Perfect!")

    return noise_factors, noisy_values, ideal_zz, methods


def demo_local_folding():
    """
    Demonstrate local gate folding for finer noise control.
    """
    print("\n" + "=" * 70)
    print("DEMO 2: Local Gate Folding (Fractional Noise Factors)")
    print("=" * 70)

    n_qubits = 2
    shots = 20000

    p_1q, p_2q = 0.002, 0.015
    noise_model = create_depolarizing_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    base_qc = build_ghz_circuit(n_qubits)

    # Ideal
    ideal_zz = 1.0  # For GHZ state, <ZZ> = 1
    print(f"\n  Ideal <ZZ> = {ideal_zz}")

    # Fine-grained noise factors via local folding
    noise_factors = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
    noisy_values = []

    print(f"\n  {'lambda':<10} {'<ZZ>_noisy':<15}")
    print(f"  {'-'*25}")

    for lam in noise_factors:
        if lam == int(lam) and int(lam) % 2 == 1:
            folded = fold_circuit_global(base_qc, int(lam))
        else:
            folded = fold_gates_local(base_qc, lam)

        qc_meas = folded.copy()
        qc_meas.measure_all()

        result = sim.run(qc_meas, shots=shots).result()
        counts = result.get_counts()
        zz_val = compute_expectation_value(counts, 'ZZ', n_qubits)
        noisy_values.append(zz_val)
        print(f"  {lam:<10.1f} {zz_val:<15.6f}")

    # Extrapolate with more data points
    zne_lin = extrapolate_linear(noise_factors[:3], noisy_values[:3])
    zne_exp = extrapolate_exponential(noise_factors, noisy_values)
    zne_rich = richardson_extrapolation(noise_factors[:4], noisy_values[:4])

    print(f"\n  Extrapolation with {len(noise_factors)} data points:")
    print(f"    Linear (3 pts):      {zne_lin:.6f} (error: {abs(zne_lin - ideal_zz):.6f})")
    print(f"    Exponential (all):   {zne_exp:.6f} (error: {abs(zne_exp - ideal_zz):.6f})")
    print(f"    Richardson (4 pts):  {zne_rich:.6f} (error: {abs(zne_rich - ideal_zz):.6f})")


def demo_zne_sweep():
    """
    ZNE across a range of variational parameters.

    Shows that ZNE consistently improves expectation value estimates
    across different circuit configurations.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: ZNE Across Variational Parameter Sweep")
    print("=" * 70)

    n_qubits = 2
    shots = 15000
    noise_factors = [1, 3, 5]

    p_1q, p_2q = 0.003, 0.02
    noise_model = create_depolarizing_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    thetas = np.linspace(0, np.pi, 9)
    ideal_values = []
    raw_values = []
    zne_values = []

    for theta in thetas:
        base_qc = build_variational_circuit(theta, n_qubits)

        # Ideal
        sv = Statevector.from_instruction(base_qc)
        ideal_probs = sv.probabilities_dict()
        ideal_zz = sum((-1) ** (int(k[0]) ^ int(k[1])) * v for k, v in ideal_probs.items())
        ideal_values.append(ideal_zz)

        # Noisy at each noise level
        noisy_at_levels = []
        for lam in noise_factors:
            folded = fold_circuit_global(base_qc, lam)
            qc_meas = folded.copy()
            qc_meas.measure_all()
            result = sim.run(qc_meas, shots=shots).result()
            counts = result.get_counts()
            zz = compute_expectation_value(counts, 'ZZ', n_qubits)
            noisy_at_levels.append(zz)

        raw_values.append(noisy_at_levels[0])

        # ZNE via exponential extrapolation
        zne_val = extrapolate_exponential(noise_factors, noisy_at_levels)
        zne_values.append(zne_val)

    print(f"\n  {'theta/pi':<10} {'Ideal':<12} {'Raw':<12} {'ZNE':<12} {'Improv.':<10}")
    print(f"  {'-'*56}")
    for i, theta in enumerate(thetas):
        raw_err = abs(raw_values[i] - ideal_values[i])
        zne_err = abs(zne_values[i] - ideal_values[i])
        improv = raw_err / zne_err if zne_err > 1e-6 else float('inf')
        print(f"  {theta/np.pi:<10.3f} {ideal_values[i]:<12.4f} {raw_values[i]:<12.4f} "
              f"{zne_values[i]:<12.4f} {improv:<10.1f}x")

    rms_raw = np.sqrt(np.mean([(r - i)**2 for r, i in zip(raw_values, ideal_values)]))
    rms_zne = np.sqrt(np.mean([(z - i)**2 for z, i in zip(zne_values, ideal_values)]))
    print(f"\n  RMS error (raw): {rms_raw:.6f}")
    print(f"  RMS error (ZNE): {rms_zne:.6f}")
    print(f"  Overall improvement: {rms_raw/rms_zne:.1f}x")

    return thetas, ideal_values, raw_values, zne_values


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_zne_extrapolation(noise_factors, noisy_values, ideal, methods, save_path=None):
    """Plot ZNE extrapolation curves."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Data points
    ax.scatter(noise_factors, noisy_values, color='red', s=100, zorder=5, label='Noisy measurements')

    # Ideal
    ax.axhline(y=ideal, color='green', linestyle='--', linewidth=2, label=f'Ideal = {ideal:.4f}')

    # Extrapolation curves
    lam_fine = np.linspace(0, max(noise_factors) * 1.1, 100)

    # Linear fit
    coeffs_lin = np.polyfit(noise_factors, noisy_values, 1)
    ax.plot(lam_fine, np.polyval(coeffs_lin, lam_fine), 'b-', alpha=0.5, label='Linear fit')

    # Exponential fit
    try:
        def exp_model(l, a, b, c):
            return a * np.exp(-b * l) + c
        from scipy.optimize import curve_fit
        popt, _ = curve_fit(exp_model, noise_factors, noisy_values, p0=[noisy_values[0], 0.1, 0])
        ax.plot(lam_fine, exp_model(lam_fine, *popt), 'r-', alpha=0.5, label='Exponential fit')
    except Exception:
        pass

    # ZNE estimates
    for name, val in methods.items():
        ax.scatter([0], [val], marker='*', s=200, zorder=6, label=f'{name}: {val:.4f}')

    ax.set_xlabel('Noise Factor (lambda)')
    ax.set_ylabel('Expectation Value <ZZ>')
    ax.set_title('Zero-Noise Extrapolation')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_xlim(-0.5, max(noise_factors) + 0.5)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run all ZNE demonstrations.

    Covers:
    - Basic ZNE with global gate folding
    - Local gate folding for fine noise control
    - ZNE across variational parameter sweep
    - Extrapolation curve visualization
    """
    print("Zero-Noise Extrapolation (ZNE) - Local Demonstrations")
    print("=" * 70)
    print("See explanation_physicist.md for theoretical background.")
    print("See explanation_simple.md for intuitive explanation.")
    print()

    # Demo 1: Basic ZNE
    nf, nv, ideal, methods = demo_basic_zne()

    # Demo 2: Local folding
    demo_local_folding()

    # Demo 3: Parameter sweep
    demo_zne_sweep()

    # Plot
    print("\n" + "=" * 70)
    print("Generating ZNE extrapolation plot...")
    plot_zne_extrapolation(nf, nv, ideal, methods)

    print("\nAll demonstrations complete.")


if __name__ == '__main__':
    main()
