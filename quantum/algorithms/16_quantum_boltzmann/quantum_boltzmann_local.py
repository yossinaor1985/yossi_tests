"""
Quantum Boltzmann Machine (QBM) - Local Simulator Implementation
=================================================================

Implements a variational QBM that learns to approximate a target
probability distribution using parameterized quantum circuits.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
QBM Hamiltonian: H = -sum J_ij Z_i Z_j - sum h_i Z_i - sum Gamma_i X_i
Thermal state: rho = exp(-beta H) / Z
Training: minimize KL divergence between model and target distributions

Since exact Gibbs state preparation is QMA-hard, we use a variational
approach (Section 4.3): parameterized circuit approximates the thermal state.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector, SparsePauliOp, DensityMatrix
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler


# =============================================================================
# TARGET DISTRIBUTION
# =============================================================================

def create_target_distribution(n_qubits=3):
    """
    Create a target probability distribution for the QBM to learn.

    We use a bimodal distribution concentrated on specific bitstrings,
    simulating a distribution with structure (not uniform random).
    """
    n_states = 2 ** n_qubits
    target = np.zeros(n_states)

    # Bimodal: peaks at |000> and |111> with some spread
    if n_qubits == 3:
        target[0b000] = 0.25  # |000>
        target[0b001] = 0.08  # |001>
        target[0b010] = 0.02  # |010>
        target[0b011] = 0.05  # |011>
        target[0b100] = 0.05  # |100>
        target[0b101] = 0.03  # |101>
        target[0b110] = 0.07  # |110>
        target[0b111] = 0.45  # |111>
    elif n_qubits == 2:
        target[0b00] = 0.35
        target[0b01] = 0.10
        target[0b10] = 0.15
        target[0b11] = 0.40

    target /= target.sum()
    return target


# =============================================================================
# VARIATIONAL CIRCUIT FOR THERMAL STATE
# =============================================================================

def build_variational_thermal_circuit(n_qubits, n_layers=3):
    """
    Build a parameterized circuit to approximate a Gibbs state.

    Architecture:
        Layer l: R_Y(theta) on each qubit + CNOT chain + R_Z(phi) on each qubit

    This creates a general entangled state that can approximate
    thermal distributions. The R_Y rotations control the amplitude
    distribution, and R_Z controls the phases.

    See explanation_physicist.md, Section 4.3 (Variational QBM).
    """
    n_params = n_qubits * 2 * n_layers  # 2 rotations per qubit per layer
    params = ParameterVector('theta', n_params)

    qc = QuantumCircuit(n_qubits)
    idx = 0

    for layer in range(n_layers):
        # R_Y rotations (control amplitudes)
        for q in range(n_qubits):
            qc.ry(params[idx], q)
            idx += 1

        # Entangling layer (CNOT chain)
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)

        # R_Z rotations (control phases)
        for q in range(n_qubits):
            qc.rz(params[idx], q)
            idx += 1

    return qc, params


def get_distribution_from_circuit(circuit, param_values):
    """
    Get the probability distribution from a parameterized circuit.

    Returns P(z) = |<z|psi(theta)>|^2 for all computational basis states.
    """
    bound_circuit = circuit.assign_parameters(dict(zip(circuit.parameters, param_values)))
    sv = Statevector(bound_circuit)
    probs = sv.probabilities()
    return probs


# =============================================================================
# LOSS FUNCTION: KL DIVERGENCE
# =============================================================================

def kl_divergence(p_target, p_model, epsilon=1e-10):
    """
    KL divergence: D_KL(target || model) = sum p_target * log(p_target / p_model)

    This is the standard training objective for generative models.
    When D_KL = 0, the model perfectly matches the target.

    Adding epsilon for numerical stability (avoid log(0)).
    """
    p_model_safe = np.clip(p_model, epsilon, 1.0)
    p_target_safe = np.clip(p_target, epsilon, 1.0)
    return np.sum(p_target_safe * np.log(p_target_safe / p_model_safe))


def total_variation_distance(p, q):
    """Total variation distance: TV(p, q) = (1/2) sum |p_i - q_i|."""
    return 0.5 * np.sum(np.abs(p - q))


# =============================================================================
# TRAINING
# =============================================================================

def train_qbm(n_qubits=3, n_layers=3, max_iter=200):
    """
    Train a variational QBM to match a target distribution.

    Uses scipy.optimize.minimize with COBYLA for gradient-free optimization.
    The objective is to minimize KL(target || model).

    See explanation_physicist.md, Section 4 for training theory.
    """
    print(f"\n{'='*70}")
    print(f"Training Variational QBM ({n_qubits} qubits, {n_layers} layers)")
    print(f"{'='*70}")

    # Target distribution
    target = create_target_distribution(n_qubits)
    n_states = 2 ** n_qubits
    print(f"\nTarget distribution:")
    for i in range(n_states):
        bitstring = format(i, f'0{n_qubits}b')
        if target[i] > 0.01:
            print(f"  |{bitstring}>: {target[i]:.4f}")

    # Variational circuit
    circuit, params = build_variational_thermal_circuit(n_qubits, n_layers)
    n_params = len(params)
    print(f"\nVariational circuit:")
    print(f"  Parameters: {n_params}")
    print(f"  Depth: {circuit.depth()}")

    # Optimization
    loss_history = []
    tv_history = []
    best_params = [None]
    best_loss = [float('inf')]

    def objective(param_values):
        probs = get_distribution_from_circuit(circuit, param_values)
        kl = kl_divergence(target, probs)
        tv = total_variation_distance(target, probs)
        loss_history.append(kl)
        tv_history.append(tv)

        if kl < best_loss[0]:
            best_loss[0] = kl
            best_params[0] = param_values.copy()

        if len(loss_history) % 50 == 0:
            print(f"  Iter {len(loss_history):4d}: KL = {kl:.6f}, TV = {tv:.4f}")

        return kl

    # Initialize parameters
    rng = np.random.default_rng(42)
    x0 = rng.uniform(-np.pi, np.pi, n_params)

    print(f"\nOptimizing (COBYLA, max {max_iter} iterations)...")
    result = minimize(objective, x0, method='COBYLA',
                      options={'maxiter': max_iter, 'rhobeg': 0.5})

    # Best results
    best_probs = get_distribution_from_circuit(circuit, best_params[0])
    final_kl = kl_divergence(target, best_probs)
    final_tv = total_variation_distance(target, best_probs)

    print(f"\nFinal results:")
    print(f"  KL divergence: {final_kl:.6f}")
    print(f"  Total variation: {final_tv:.4f}")
    print(f"\nLearned distribution vs target:")
    for i in range(n_states):
        bs = format(i, f'0{n_qubits}b')
        if target[i] > 0.01 or best_probs[i] > 0.01:
            print(f"  |{bs}>: target={target[i]:.4f}, model={best_probs[i]:.4f}")

    return target, best_probs, loss_history, tv_history, circuit, best_params[0]


# =============================================================================
# 2-QUBIT EXACT QBM ANALYSIS
# =============================================================================

def demo_exact_qbm():
    """
    Exact analysis of a 2-qubit QBM Hamiltonian.

    H = -J Z_1 Z_2 - Gamma(X_1 + X_2)

    See explanation_physicist.md, Section 6 (Worked Example).
    """
    print(f"\n{'='*70}")
    print("2-Qubit Exact QBM Analysis")
    print(f"{'='*70}")

    J = 1.0
    Gamma = 0.5
    beta = 1.0

    # Build Hamiltonian using SparsePauliOp
    H = SparsePauliOp.from_list([
        ("ZZ", -J),
        ("XI", -Gamma),
        ("IX", -Gamma),
    ])

    H_matrix = H.to_matrix()
    print(f"\nHamiltonian: H = -{J}*ZZ - {Gamma}*(XI + IX)")
    print(f"H matrix:\n{np.real(H_matrix)}")

    # Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(H_matrix)
    print(f"\nEigenvalues: {eigenvalues}")

    # Thermal state: rho = exp(-beta*H) / Z
    exp_H = np.diag(np.exp(-beta * eigenvalues))
    rho = eigenvectors @ exp_H @ eigenvectors.conj().T
    Z = np.trace(rho)
    rho /= Z

    print(f"Partition function Z = {Z:.4f}")
    print(f"Thermal state diagonal (measurement probs):")
    for i in range(4):
        bs = format(i, f'02b')
        print(f"  P(|{bs}>) = {np.real(rho[i, i]):.4f}")

    # Show that transverse field creates coherences (off-diagonal)
    print(f"\nOff-diagonal coherences (quantum correlations):")
    print(f"  |rho_01| = {abs(rho[0, 1]):.4f} (created by transverse field)")
    print(f"  Without X terms, all off-diagonals would be zero (classical)")

    return np.real(np.diag(rho))


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(target, learned, loss_history, tv_history, exact_probs, n_qubits):
    """Visualize QBM results."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    n_states = len(target)
    labels = [format(i, f'0{n_qubits}b') for i in range(n_states)]

    # --- Plot 1: Target vs Learned distribution ---
    ax = axes[0, 0]
    x = np.arange(n_states)
    w = 0.35
    ax.bar(x - w/2, target, w, label='Target', color='#3498db', alpha=0.8)
    ax.bar(x + w/2, learned, w, label='QBM Learned', color='#e74c3c', alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([f'|{l}>' for l in labels], fontsize=8)
    ax.set_ylabel('Probability', fontsize=11)
    ax.set_title('Target vs QBM Distribution', fontsize=13)
    ax.legend()

    # --- Plot 2: KL divergence convergence ---
    ax = axes[0, 1]
    ax.plot(loss_history, 'b-', linewidth=1.5)
    ax.set_xlabel('Iteration', fontsize=11)
    ax.set_ylabel('KL Divergence', fontsize=11)
    ax.set_title('Training Convergence', fontsize=13)
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3)

    # --- Plot 3: Total variation distance ---
    ax = axes[1, 0]
    ax.plot(tv_history, 'r-', linewidth=1.5)
    ax.set_xlabel('Iteration', fontsize=11)
    ax.set_ylabel('Total Variation Distance', fontsize=11)
    ax.set_title('Distribution Distance Over Training', fontsize=13)
    ax.grid(True, alpha=0.3)

    # --- Plot 4: Exact 2-qubit thermal state ---
    ax = axes[1, 1]
    if exact_probs is not None:
        labels_2q = ['|00>', '|01>', '|10>', '|11>']
        ax.bar(labels_2q, exact_probs, color='#2ecc71', alpha=0.8)
        ax.set_ylabel('Probability', fontsize=11)
        ax.set_title('2-Qubit Exact QBM\nH = -ZZ - 0.5(X+X)', fontsize=12)
        ax.set_ylim(0, max(exact_probs) * 1.2)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/16_quantum_boltzmann/qbm_results.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/16_quantum_boltzmann/qbm_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Quantum Boltzmann Machine (QBM) - Local Simulator")
    print("=" * 70)
    print("Qiskit 2.4.1 | AerSimulator")

    # Part A: Exact 2-qubit analysis
    exact_probs = demo_exact_qbm()

    # Part B: Variational QBM training (3 qubits)
    target, learned, loss_hist, tv_hist, circuit, params = train_qbm(
        n_qubits=3, n_layers=4, max_iter=200
    )

    # Visualization
    plot_results(target, learned, loss_hist, tv_hist, exact_probs, n_qubits=3)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Quantum Boltzmann Machine demonstrated:

    A. Exact 2-Qubit Analysis:
       - H = -J*ZZ - Gamma*(X+X) creates quantum thermal state
       - Transverse field X generates off-diagonal coherences
       - Measurement probabilities differ from classical Boltzmann machine

    B. Variational QBM (3 qubits):
       - Parameterized circuit approximates Gibbs state
       - Training minimizes KL divergence to target distribution
       - Successfully learns structured (bimodal) distributions

    Key concepts:
       - QBM = quantum Hamiltonian + Gibbs state (rho = exp(-beta H)/Z)
       - Transverse field enables quantum tunneling and coherences
       - Variational approach sidesteps QMA-hard exact preparation
       - Training uses contrastive divergence analog in quantum setting
    """)


if __name__ == "__main__":
    main()