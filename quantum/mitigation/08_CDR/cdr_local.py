"""
Clifford Data Regression (CDR) - Local Simulator Implementation
=================================================================

Demonstrates CDR: generate near-Clifford training circuits, compute
exact results classically, run noisy versions, fit linear regression,
and apply correction to the target circuit.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
CDR trains on Clifford circuits (classically simulable) to learn the
noise-induced mapping: E_noisy -> E_ideal. Linear model:
E_ideal = a * E_noisy + b. Applied to target circuit for correction.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error


# =============================================================================
# NOISE MODEL
# =============================================================================

def create_noise_model(
    p_1q: float = 0.005,
    p_2q: float = 0.02
) -> NoiseModel:
    """
    Create a depolarizing noise model.

    Under depolarizing noise (see explanation_physicist.md, Section 4.2):
        E_noisy = alpha * E_ideal + beta
        where alpha, beta depend on noise but NOT on the specific state.
        This linearity is why CDR with linear regression works.

    Args:
        p_1q: Single-qubit depolarizing error rate.
        p_2q: Two-qubit depolarizing error rate.

    Returns:
        NoiseModel with depolarizing errors.
    """
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p_1q, 1), ['x', 'h', 'sx', 'ry', 'rz', 'rx']
    )
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p_2q, 2), ['cx']
    )
    return noise_model


# =============================================================================
# CIRCUIT BUILDERS
# =============================================================================

def build_target_circuit(thetas: List[float], n_qubits: int = 2) -> QuantumCircuit:
    """
    Build a target circuit with non-Clifford (arbitrary rotation) gates.

    The target circuit has a structure typical of variational algorithms:
    entangling layer + rotation layer + entangling layer.

    Args:
        thetas: List of rotation angles for Ry gates.
        n_qubits: Number of qubits.

    Returns:
        Target circuit (without measurements).
    """
    qc = QuantumCircuit(n_qubits, name='target')

    # Layer 1: Hadamard + entangling
    for i in range(n_qubits):
        qc.h(i)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)

    # Layer 2: Non-Clifford rotations (Ry(theta))
    for i, theta in enumerate(thetas):
        if i < n_qubits:
            qc.ry(theta, i)

    # Layer 3: Entangling
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)

    return qc


def generate_near_clifford_circuits(
    target_circuit: QuantumCircuit,
    thetas: List[float],
    n_training: int = 20,
    seed: int = 42
) -> List[Tuple[QuantumCircuit, List[float]]]:
    """
    Generate near-Clifford training circuits.

    Training circuit generation (see explanation_physicist.md, Section 3.1):
        Replace each Ry(theta) with Ry(k*pi/2) for random k in {0,1,2,3}.
        The resulting circuit is a Clifford circuit (classically simulable).

    Args:
        target_circuit: The original target circuit.
        thetas: Original rotation angles.
        n_training: Number of training circuits to generate.
        seed: Random seed.

    Returns:
        List of (training_circuit, clifford_angles) tuples.
    """
    rng = np.random.default_rng(seed)
    n_qubits = target_circuit.num_qubits

    # Clifford-equivalent angles for Ry: {0, pi/2, pi, 3pi/2}
    clifford_angles = [0, np.pi / 2, np.pi, 3 * np.pi / 2]

    training_circuits = []

    for _ in range(n_training):
        # For each non-Clifford angle, randomly choose a Clifford replacement
        cliff_thetas = []
        for _ in thetas:
            cliff_theta = rng.choice(clifford_angles)
            cliff_thetas.append(cliff_theta)

        # Build training circuit with same structure but Clifford angles
        qc = QuantumCircuit(n_qubits, name='training')

        # Layer 1: same as target
        for i in range(n_qubits):
            qc.h(i)
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)

        # Layer 2: Clifford rotations
        for i, theta in enumerate(cliff_thetas):
            if i < n_qubits:
                qc.ry(theta, i)

        # Layer 3: same as target
        for i in range(n_qubits - 1):
            qc.cx(i, i + 1)

        training_circuits.append((qc, cliff_thetas))

    return training_circuits


# =============================================================================
# EXACT CLASSICAL SIMULATION
# =============================================================================

def compute_exact_expectation(
    circuit: QuantumCircuit,
    observable_qubits: List[int]
) -> float:
    """
    Compute the exact expectation value via statevector simulation.

    Gottesman-Knill (see explanation_physicist.md, Section 2.2):
        Clifford circuits can be simulated in O(n^2) per gate.
        For small circuits, we use full statevector simulation.

    Args:
        circuit: Circuit to simulate (without measurements).
        observable_qubits: Qubits for Z observable.

    Returns:
        Exact expectation value of Z^(x)n on specified qubits.
    """
    sv = Statevector.from_instruction(circuit)
    probs = sv.probabilities_dict()

    n_qubits = circuit.num_qubits
    exp_val = 0.0

    for bitstring, prob in probs.items():
        bs = bitstring.zfill(n_qubits)
        parity = sum(int(bs[n_qubits - 1 - q]) for q in observable_qubits) % 2
        exp_val += (-1) ** parity * prob

    return exp_val


def compute_noisy_expectation(
    circuit: QuantumCircuit,
    observable_qubits: List[int],
    backend: AerSimulator,
    shots: int = 10000
) -> float:
    """
    Compute the noisy expectation value from hardware/simulator.

    Args:
        circuit: Circuit (without measurements).
        observable_qubits: Qubits for Z observable.
        backend: Noisy simulator.
        shots: Number of measurement shots.

    Returns:
        Noisy expectation value.
    """
    n_qubits = circuit.num_qubits
    qc = circuit.copy()
    qc.measure_all()

    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()
    total = sum(counts.values())

    exp_val = 0.0
    for bitstring, count in counts.items():
        bs = bitstring.zfill(n_qubits)
        parity = sum(int(bs[n_qubits - 1 - q]) for q in observable_qubits) % 2
        exp_val += (-1) ** parity * count / total

    return exp_val


# =============================================================================
# CDR REGRESSION
# =============================================================================

def fit_linear_regression(
    noisy_values: List[float],
    exact_values: List[float]
) -> Tuple[float, float, float]:
    """
    Fit linear regression: E_exact = a * E_noisy + b.

    Linear regression (see explanation_physicist.md, Section 3.3):
        a = Cov(E_noisy, E_exact) / Var(E_noisy)
        b = mean(E_exact) - a * mean(E_noisy)

    Args:
        noisy_values: Noisy expectation values (training).
        exact_values: Exact expectation values (training).

    Returns:
        Tuple of (slope a, intercept b, R-squared).
    """
    x = np.array(noisy_values)
    y = np.array(exact_values)

    # Least squares fit
    coeffs = np.polyfit(x, y, 1)
    a, b = coeffs[0], coeffs[1]

    # R-squared
    y_pred = a * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    return a, b, r_squared


def apply_cdr_correction(noisy_value: float, a: float, b: float) -> float:
    """
    Apply CDR correction to a noisy expectation value.

    Correction (see explanation_physicist.md, Section 3.4):
        E_corrected = a * E_noisy + b

    Args:
        noisy_value: Noisy expectation value from target circuit.
        a: Regression slope.
        b: Regression intercept.

    Returns:
        Corrected expectation value.
    """
    return a * noisy_value + b


# =============================================================================
# DEMONSTRATIONS
# =============================================================================

def demo_basic_cdr():
    """
    Basic CDR demonstration on a 2-qubit variational circuit.

    Full CDR pipeline:
    1. Define target circuit with non-Clifford gates
    2. Generate near-Clifford training circuits
    3. Collect training data (exact + noisy)
    4. Fit linear regression
    5. Apply correction to target circuit
    """
    print("=" * 70)
    print("DEMO 1: Basic CDR on 2-Qubit Variational Circuit")
    print("=" * 70)

    n_qubits = 2
    thetas = [0.7, 1.3]  # Non-Clifford angles
    observable_qubits = [0, 1]  # Measure <ZZ>
    n_training = 20
    shots = 15000

    p_1q, p_2q = 0.005, 0.02
    print(f"\n  Target angles: theta = {thetas}")
    print(f"  Noise: p_1q = {p_1q}, p_2q = {p_2q}")
    print(f"  Training circuits: {n_training}")

    noise_model = create_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    # Step 1: Build target circuit
    target_qc = build_target_circuit(thetas, n_qubits)

    # Ideal expectation value
    ideal_value = compute_exact_expectation(target_qc, observable_qubits)
    print(f"\n  Step 1: Target circuit ideal <ZZ> = {ideal_value:.6f}")

    # Noisy expectation value
    noisy_target = compute_noisy_expectation(target_qc, observable_qubits, sim, shots)
    print(f"  Target noisy <ZZ> = {noisy_target:.6f}")

    # Step 2: Generate training circuits
    print(f"\n  Step 2: Generating {n_training} near-Clifford training circuits...")
    training_data = generate_near_clifford_circuits(target_qc, thetas, n_training, seed=42)

    # Step 3: Collect training data
    print("  Step 3: Collecting training data...")
    exact_train = []
    noisy_train = []

    for i, (train_qc, cliff_thetas) in enumerate(training_data):
        exact_val = compute_exact_expectation(train_qc, observable_qubits)
        noisy_val = compute_noisy_expectation(train_qc, observable_qubits, sim, shots)
        exact_train.append(exact_val)
        noisy_train.append(noisy_val)

    print(f"    Training range (exact):  [{min(exact_train):.4f}, {max(exact_train):.4f}]")
    print(f"    Training range (noisy):  [{min(noisy_train):.4f}, {max(noisy_train):.4f}]")

    # Step 4: Fit regression
    print(f"\n  Step 4: Fitting linear regression...")
    a, b, r_squared = fit_linear_regression(noisy_train, exact_train)
    print(f"    E_exact = {a:.4f} * E_noisy + {b:.4f}")
    print(f"    R-squared = {r_squared:.4f}")

    # Step 5: Apply correction
    corrected_value = apply_cdr_correction(noisy_target, a, b)
    print(f"\n  Step 5: CDR correction")
    print(f"    E_corrected = {a:.4f} * {noisy_target:.4f} + {b:.4f} = {corrected_value:.6f}")

    # Summary
    print(f"\n  {'Method':<20} {'<ZZ>':<12} {'|Error|':<12}")
    print(f"  {'-'*44}")
    print(f"  {'Ideal':<20} {ideal_value:<12.6f} {'---':<12}")
    print(f"  {'Raw (noisy)':<20} {noisy_target:<12.6f} {abs(noisy_target - ideal_value):<12.6f}")
    print(f"  {'CDR corrected':<20} {corrected_value:<12.6f} {abs(corrected_value - ideal_value):<12.6f}")

    raw_err = abs(noisy_target - ideal_value)
    cdr_err = abs(corrected_value - ideal_value)
    if cdr_err > 1e-8:
        print(f"\n  Improvement: {raw_err / cdr_err:.1f}x")
    else:
        print(f"\n  Improvement: Perfect correction!")

    return exact_train, noisy_train, a, b, ideal_value, noisy_target, corrected_value


def demo_cdr_sweep():
    """
    CDR across a range of target rotation angles.

    Shows that a single CDR model (trained once) can correct
    multiple target circuits with different parameters.
    """
    print("\n" + "=" * 70)
    print("DEMO 2: CDR Across Parameter Sweep")
    print("=" * 70)

    n_qubits = 2
    observable_qubits = [0, 1]
    n_training = 30
    shots = 15000

    p_1q, p_2q = 0.005, 0.02
    noise_model = create_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    # Generate ONE set of training data (reusable for multiple targets)
    print(f"\n  Training CDR model with {n_training} near-Clifford circuits...")
    base_thetas = [1.0, 0.5]
    base_qc = build_target_circuit(base_thetas, n_qubits)
    training_data = generate_near_clifford_circuits(base_qc, base_thetas, n_training, seed=42)

    exact_train = []
    noisy_train = []
    for train_qc, _ in training_data:
        exact_train.append(compute_exact_expectation(train_qc, observable_qubits))
        noisy_train.append(compute_noisy_expectation(train_qc, observable_qubits, sim, shots))

    a, b, r_squared = fit_linear_regression(noisy_train, exact_train)
    print(f"  CDR model: E = {a:.4f} * E_noisy + {b:.4f} (R^2 = {r_squared:.4f})")

    # Sweep target angles
    target_thetas_list = [(t, 0.5) for t in np.linspace(0.1, 3.0, 10)]

    print(f"\n  {'theta_0':<10} {'Ideal':<10} {'Raw':<10} {'CDR':<10} {'Improv.':<10}")
    print(f"  {'-'*50}")

    ideal_vals, raw_vals, cdr_vals = [], [], []

    for thetas in target_thetas_list:
        thetas_list = list(thetas)
        target_qc = build_target_circuit(thetas_list, n_qubits)

        ideal_v = compute_exact_expectation(target_qc, observable_qubits)
        noisy_v = compute_noisy_expectation(target_qc, observable_qubits, sim, shots)
        cdr_v = apply_cdr_correction(noisy_v, a, b)

        ideal_vals.append(ideal_v)
        raw_vals.append(noisy_v)
        cdr_vals.append(cdr_v)

        raw_err = abs(noisy_v - ideal_v)
        cdr_err = abs(cdr_v - ideal_v)
        improv = raw_err / cdr_err if cdr_err > 1e-6 else float('inf')

        print(f"  {thetas[0]:<10.2f} {ideal_v:<10.4f} {noisy_v:<10.4f} {cdr_v:<10.4f} {improv:<10.1f}x")

    rms_raw = np.sqrt(np.mean([(r - i)**2 for r, i in zip(raw_vals, ideal_vals)]))
    rms_cdr = np.sqrt(np.mean([(c - i)**2 for c, i in zip(cdr_vals, ideal_vals)]))
    print(f"\n  RMS error (raw): {rms_raw:.6f}")
    print(f"  RMS error (CDR): {rms_cdr:.6f}")
    print(f"  Overall improvement: {rms_raw/rms_cdr:.1f}x")

    return ideal_vals, raw_vals, cdr_vals


def demo_training_size():
    """
    Analyze the effect of training set size on CDR quality.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: CDR Training Set Size Analysis")
    print("=" * 70)

    n_qubits = 2
    thetas = [0.8, 1.5]
    observable_qubits = [0, 1]
    shots = 15000

    p_1q, p_2q = 0.005, 0.02
    noise_model = create_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    target_qc = build_target_circuit(thetas, n_qubits)
    ideal_value = compute_exact_expectation(target_qc, observable_qubits)
    noisy_target = compute_noisy_expectation(target_qc, observable_qubits, sim, shots)

    # Generate a large pool of training circuits
    all_training = generate_near_clifford_circuits(target_qc, thetas, 100, seed=42)
    all_exact = [compute_exact_expectation(qc, observable_qubits) for qc, _ in all_training]
    all_noisy = [compute_noisy_expectation(qc, observable_qubits, sim, shots) for qc, _ in all_training]

    training_sizes = [3, 5, 10, 20, 30, 50, 100]

    print(f"\n  Ideal <ZZ> = {ideal_value:.6f}")
    print(f"  Raw <ZZ> = {noisy_target:.6f} (error: {abs(noisy_target - ideal_value):.6f})")

    print(f"\n  {'M (training)':<15} {'R^2':<10} {'CDR <ZZ>':<12} {'|Error|':<12}")
    print(f"  {'-'*49}")

    for M in training_sizes:
        exact_sub = all_exact[:M]
        noisy_sub = all_noisy[:M]
        a, b, r2 = fit_linear_regression(noisy_sub, exact_sub)
        cdr_v = apply_cdr_correction(noisy_target, a, b)
        err = abs(cdr_v - ideal_value)
        print(f"  {M:<15} {r2:<10.4f} {cdr_v:<12.6f} {err:<12.6f}")


def demo_regression_comparison():
    """
    Compare linear vs quadratic CDR regression.
    """
    print("\n" + "=" * 70)
    print("DEMO 4: Linear vs Quadratic CDR Regression")
    print("=" * 70)

    n_qubits = 2
    thetas = [1.2, 0.8]
    observable_qubits = [0, 1]
    n_training = 40
    shots = 15000

    p_1q, p_2q = 0.008, 0.03  # Slightly higher noise
    noise_model = create_noise_model(p_1q, p_2q)
    sim = AerSimulator(noise_model=noise_model)

    target_qc = build_target_circuit(thetas, n_qubits)
    ideal_value = compute_exact_expectation(target_qc, observable_qubits)
    noisy_target = compute_noisy_expectation(target_qc, observable_qubits, sim, shots)

    training_data = generate_near_clifford_circuits(target_qc, thetas, n_training, seed=42)
    exact_train = [compute_exact_expectation(qc, observable_qubits) for qc, _ in training_data]
    noisy_train = [compute_noisy_expectation(qc, observable_qubits, sim, shots) for qc, _ in training_data]

    # Linear fit
    a_lin, b_lin, r2_lin = fit_linear_regression(noisy_train, exact_train)
    cdr_linear = a_lin * noisy_target + b_lin

    # Quadratic fit
    coeffs_quad = np.polyfit(noisy_train, exact_train, 2)
    cdr_quad = np.polyval(coeffs_quad, noisy_target)
    y_pred_quad = np.polyval(coeffs_quad, noisy_train)
    ss_res = np.sum((np.array(exact_train) - y_pred_quad) ** 2)
    ss_tot = np.sum((np.array(exact_train) - np.mean(exact_train)) ** 2)
    r2_quad = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    print(f"\n  Ideal <ZZ> = {ideal_value:.6f}")
    print(f"  Raw <ZZ>   = {noisy_target:.6f}")
    print(f"\n  {'Model':<15} {'R^2':<10} {'CDR <ZZ>':<12} {'|Error|':<12}")
    print(f"  {'-'*49}")
    print(f"  {'Linear':<15} {r2_lin:<10.4f} {cdr_linear:<12.6f} {abs(cdr_linear - ideal_value):<12.6f}")
    print(f"  {'Quadratic':<15} {r2_quad:<10.4f} {cdr_quad:<12.6f} {abs(cdr_quad - ideal_value):<12.6f}")


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_cdr_regression(exact_train, noisy_train, a, b, ideal, noisy_target, corrected,
                        save_path=None):
    """Plot CDR training data and regression line."""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Training data
    ax.scatter(noisy_train, exact_train, color='blue', alpha=0.6, s=60,
               label='Training (Clifford circuits)')

    # Regression line
    x_range = np.linspace(min(noisy_train) - 0.1, max(noisy_train) + 0.1, 100)
    y_fit = a * x_range + b
    ax.plot(x_range, y_fit, 'r-', linewidth=2,
            label=f'Fit: E_exact = {a:.3f}*E_noisy + {b:.3f}')

    # Target point
    ax.scatter([noisy_target], [ideal], marker='*', s=300, color='green', zorder=5,
               label=f'Target (ideal={ideal:.4f})')
    ax.scatter([noisy_target], [corrected], marker='D', s=200, color='red', zorder=5,
               label=f'CDR corrected = {corrected:.4f}')

    # Arrow from noisy to corrected
    ax.annotate('', xy=(noisy_target, corrected), xytext=(noisy_target, noisy_target),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2))

    # Perfect line (y=x)
    lim = [min(min(noisy_train), min(exact_train)) - 0.2,
           max(max(noisy_train), max(exact_train)) + 0.2]
    ax.plot(lim, lim, 'k--', alpha=0.3, label='y = x (no noise)')

    ax.set_xlabel('Noisy Expectation Value')
    ax.set_ylabel('Exact Expectation Value')
    ax.set_title('Clifford Data Regression (CDR)')
    ax.legend(loc='best', fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_aspect('equal')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run all CDR demonstrations.

    Covers:
    - Basic CDR pipeline (train, fit, correct)
    - CDR across parameter sweep
    - Training set size analysis
    - Linear vs quadratic regression
    - Visualization
    """
    print("Clifford Data Regression (CDR) - Local Demonstrations")
    print("=" * 70)
    print("See explanation_physicist.md for theoretical background.")
    print("See explanation_simple.md for intuitive explanation.")
    print()

    # Demo 1: Basic CDR
    exact_train, noisy_train, a, b, ideal, noisy_target, corrected = demo_basic_cdr()

    # Demo 2: Parameter sweep
    demo_cdr_sweep()

    # Demo 3: Training size
    demo_training_size()

    # Demo 4: Regression comparison
    demo_regression_comparison()

    # Plot
    print("\n" + "=" * 70)
    print("Generating CDR regression plot...")
    plot_cdr_regression(exact_train, noisy_train, a, b, ideal, noisy_target, corrected)

    print("\nAll demonstrations complete.")


if __name__ == '__main__':
    main()
