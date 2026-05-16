"""
FALQON (Feedback-based Algorithm for Quantum Optimization) - Local Simulator
==============================================================================

This script implements FALQON from scratch and compares it with QAOA
on the MaxCut problem.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
FALQON eliminates classical optimization by using a feedback control law:
    beta_k = -dt * <psi_k'| i[H_C, H_M] |psi_k'>

This guarantees monotonic decrease of the cost function (Lyapunov stability).

Algorithm:
    1. Initialize |psi_0> = |+>^n
    2. For each layer k:
        a. Apply U_C(dt_gamma): cost unitary with fixed small step
        b. Measure A_k = <i[H_C, H_M]>: the "gradient" direction
        c. Set beta_k = -dt_beta * A_k
        d. Apply U_M(beta_k): mixer with feedback-determined parameter
    3. Measure final state
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer import AerSimulator


def build_maxcut_hamiltonian(edges, num_nodes):
    """Build MaxCut cost Hamiltonian."""
    pauli_list = []
    for i, j in edges:
        id_str = "I" * num_nodes
        pauli_list.append((id_str, 0.5))
        zz_list = ["I"] * num_nodes
        zz_list[num_nodes - 1 - i] = "Z"
        zz_list[num_nodes - 1 - j] = "Z"
        pauli_list.append(("".join(zz_list), -0.5))
    return SparsePauliOp.from_list(pauli_list).simplify()


def build_mixer_hamiltonian(num_nodes):
    """
    Build the mixer Hamiltonian H_M = sum_i X_i.

    This is the standard transverse-field mixer used in QAOA/FALQON.
    """
    pauli_list = []
    for i in range(num_nodes):
        x_str = ["I"] * num_nodes
        x_str[num_nodes - 1 - i] = "X"
        pauli_list.append(("".join(x_str), 1.0))
    return SparsePauliOp.from_list(pauli_list)


def compute_commutator(H_C, H_M):
    """
    Compute i[H_C, H_M] = i(H_C H_M - H_M H_C).

    This is the key quantity for the FALQON feedback law.

    See explanation_physicist.md, Section 2.3 and 2.6.

    For MaxCut:
        i[H_C, H_M] = sum_{(i,j)} J_{ij} (-2) * (Y_i Z_j + Z_i Y_j)

    The commutator tells us the "gradient direction" - which way to
    adjust the mixer parameter to decrease the cost.

    Args:
        H_C: Cost Hamiltonian (SparsePauliOp)
        H_M: Mixer Hamiltonian (SparsePauliOp)

    Returns:
        SparsePauliOp: The operator i[H_C, H_M]
    """
    # Compute matrix commutator
    HC_matrix = H_C.to_matrix()
    HM_matrix = H_M.to_matrix()

    commutator_matrix = 1j * (HC_matrix @ HM_matrix - HM_matrix @ HC_matrix)

    # Convert back to SparsePauliOp
    n = int(np.log2(HC_matrix.shape[0]))
    commutator_op = SparsePauliOp.from_operator(commutator_matrix)

    return commutator_op


def run_falqon(edges, num_nodes, num_layers, dt_gamma=0.1, dt_beta=0.5):
    """
    Run the FALQON algorithm.

    See explanation_physicist.md, Section 3: Algorithm Step-by-Step.

    Args:
        edges: Graph edges
        num_nodes: Number of qubits
        num_layers: Maximum number of FALQON layers (K)
        dt_gamma: Step size for cost unitary
        dt_beta: Step size for feedback (mixer)

    Returns:
        cost_history: List of cost values at each layer
        beta_history: List of feedback parameters
        final_state: The final quantum state
    """
    H_C = build_maxcut_hamiltonian(edges, num_nodes)
    H_M = build_mixer_hamiltonian(num_nodes)
    A_op = compute_commutator(H_C, H_M)  # i[H_C, H_M]

    # Initialize in uniform superposition |+>^n
    qc = QuantumCircuit(num_nodes)
    for i in range(num_nodes):
        qc.h(i)
    state = Statevector(qc)

    cost_history = []
    beta_history = []
    commutator_history = []

    # Initial cost
    C_0 = state.expectation_value(H_C).real
    cost_history.append(C_0)

    print(f"  Layer 0 (initial): C = {C_0:.6f}")

    for k in range(1, num_layers + 1):
        # --- Step 1: Apply cost unitary U_C(dt_gamma) ---
        # U_C(gamma) = exp(-i * gamma * H_C)
        # On the statevector level: |psi'> = U_C |psi>
        HC_matrix = H_C.to_matrix()
        U_C = np.linalg.matrix_power(
            np.eye(2**num_nodes), 1  # placeholder
        )
        # Actually compute the matrix exponential
        from scipy.linalg import expm
        U_C = expm(-1j * dt_gamma * HC_matrix)
        state_prime = Statevector(U_C @ state.data)

        # --- Step 2: Measure the commutator <i[H_C, H_M]> ---
        # This is the "gradient" that tells us which direction to go
        a_k = state_prime.expectation_value(A_op).real
        commutator_history.append(a_k)

        # --- Step 3: Compute feedback parameter ---
        # beta_k = -dt_beta * a_k
        # The negative sign ensures cost DECREASES (Lyapunov stability)
        beta_k = -dt_beta * a_k
        beta_history.append(beta_k)

        # --- Step 4: Apply mixer unitary U_M(beta_k) ---
        HM_matrix = H_M.to_matrix()
        U_M = expm(-1j * beta_k * HM_matrix)
        state = Statevector(U_M @ state_prime.data)

        # --- Step 5: Measure cost ---
        C_k = state.expectation_value(H_C).real
        cost_history.append(C_k)

        if k <= 10 or k % 10 == 0:
            print(f"  Layer {k:3d}: C = {C_k:.6f}, beta = {beta_k:+.6f}, "
                  f"<[H_C, H_M]> = {a_k:+.6f}")

    return cost_history, beta_history, commutator_history, state


def run_qaoa_for_comparison(edges, num_nodes, p):
    """Run standard QAOA for comparison."""
    from qiskit_algorithms.minimum_eigensolvers import QAOA
    from qiskit_algorithms.optimizers import COBYLA
    from qiskit_aer.primitives import EstimatorV2 as AerEstimator, SamplerV2 as AerSampler

    H_C = build_maxcut_hamiltonian(edges, num_nodes)
    neg_H = -1.0 * H_C

    estimator = AerEstimator()
    sampler = AerSampler()

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=COBYLA(maxiter=300),
        reps=p,
    )

    result = qaoa.compute_minimum_eigenvalue(neg_H)
    return -result.eigenvalue.real, result.cost_function_evals


def main():
    print("=" * 70)
    print("FALQON - Feedback-based Quantum Optimization (Local Simulator)")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Problem Setup
    # =========================================================================

    print("\n--- Step 1: MaxCut Problem ---")

    # 5-node graph for a more interesting example
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
    num_nodes = 5

    H_C = build_maxcut_hamiltonian(edges, num_nodes)

    # Exact MaxCut
    max_cut = 0
    for x in range(2**num_nodes):
        bs = format(x, f'0{num_nodes}b')
        cut = sum(1 for (i, j) in edges if bs[i] != bs[j])
        max_cut = max(max_cut, cut)

    print(f"Graph: {num_nodes} nodes, {len(edges)} edges")
    print(f"Edges: {edges}")
    print(f"MaxCut: {max_cut}")

    # =========================================================================
    # STEP 2: Run FALQON
    # =========================================================================

    print("\n--- Step 2: FALQON (dt_gamma=0.1, dt_beta=0.5, K=50 layers) ---\n")

    cost_history, beta_history, comm_history, final_state = run_falqon(
        edges, num_nodes,
        num_layers=50,
        dt_gamma=0.1,
        dt_beta=0.5
    )

    print(f"\n  Final cost: {cost_history[-1]:.6f}")
    print(f"  MaxCut value: {max_cut}")
    print(f"  Approx ratio: {cost_history[-1]/max_cut:.4f}")
    print(f"  Total circuit evaluations: {len(cost_history) - 1}")

    # =========================================================================
    # STEP 3: Compare with QAOA
    # =========================================================================

    print("\n--- Step 3: QAOA Comparison ---")

    qaoa_results = {}
    for p in [1, 2, 3, 5]:
        cut_val, n_evals = run_qaoa_for_comparison(edges, num_nodes, p)
        qaoa_results[p] = (cut_val, n_evals)
        print(f"  QAOA p={p}: <H_C> = {cut_val:.4f} "
              f"(ratio = {cut_val/max_cut:.4f}), evals = {n_evals}")

    # =========================================================================
    # STEP 4: FALQON with Different Step Sizes
    # =========================================================================

    print("\n--- Step 4: FALQON Step Size Sensitivity ---")

    dt_configs = [
        (0.05, 0.3, "conservative"),
        (0.1, 0.5, "standard"),
        (0.2, 1.0, "aggressive"),
    ]

    sensitivity_results = {}
    for dt_g, dt_b, label in dt_configs:
        print(f"\n  {label}: dt_gamma={dt_g}, dt_beta={dt_b}")
        costs, _, _, _ = run_falqon(edges, num_nodes, num_layers=30, dt_gamma=dt_g, dt_beta=dt_b)
        sensitivity_results[label] = costs
        print(f"    Final ratio: {costs[-1]/max_cut:.4f}")

    # =========================================================================
    # STEP 5: Analyze Final State
    # =========================================================================

    print("\n--- Step 5: Final State Analysis ---")

    probs = final_state.probabilities_dict()
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    print(f"\nTop 10 measurement outcomes from FALQON final state:")
    for bs, prob in sorted_probs[:10]:
        # Evaluate cut value
        cut = sum(1 for (i, j) in edges if bs[i] != bs[j])
        marker = " <-- OPTIMAL" if cut == max_cut else ""
        print(f"  |{bs}> : prob = {prob:.4f}, cut = {cut}{marker}")

    # =========================================================================
    # STEP 6: Visualization
    # =========================================================================

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: FALQON convergence
    axes[0, 0].plot(range(len(cost_history)), cost_history, 'b-', linewidth=2, label='FALQON')
    axes[0, 0].axhline(y=max_cut, color='r', linestyle='--', label=f'MaxCut = {max_cut}')
    axes[0, 0].set_xlabel('Layer', fontsize=12)
    axes[0, 0].set_ylabel('Cost <H_C>', fontsize=12)
    axes[0, 0].set_title('FALQON Convergence', fontsize=14)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Feedback parameters
    axes[0, 1].plot(range(1, len(beta_history) + 1), beta_history, 'g-', linewidth=1.5)
    axes[0, 1].set_xlabel('Layer', fontsize=12)
    axes[0, 1].set_ylabel('beta_k (feedback parameter)', fontsize=12)
    axes[0, 1].set_title('FALQON Feedback Parameters', fontsize=14)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=0, color='k', linewidth=0.5)

    # Plot 3: Step size sensitivity
    for label, costs in sensitivity_results.items():
        axes[1, 0].plot(range(len(costs)), costs, linewidth=2, label=label)
    axes[1, 0].axhline(y=max_cut, color='r', linestyle='--', alpha=0.5)
    axes[1, 0].set_xlabel('Layer', fontsize=12)
    axes[1, 0].set_ylabel('Cost <H_C>', fontsize=12)
    axes[1, 0].set_title('Step Size Sensitivity', fontsize=14)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: FALQON vs QAOA comparison
    methods = ['FALQON\n(K=50)'] + [f'QAOA\n(p={p})' for p in qaoa_results.keys()]
    ratios = [cost_history[-1] / max_cut] + [v[0] / max_cut for v in qaoa_results.values()]
    evals = [50] + [v[1] for v in qaoa_results.values()]
    colors = ['#e74c3c'] + ['#3498db'] * len(qaoa_results)

    bars = axes[1, 1].bar(methods, ratios, color=colors)
    axes[1, 1].set_ylabel('Approximation ratio', fontsize=12)
    axes[1, 1].set_title('FALQON vs QAOA', fontsize=14)
    axes[1, 1].set_ylim(0, 1.1)
    axes[1, 1].axhline(y=1.0, color='k', linestyle='--', alpha=0.3)
    for bar, ev in zip(bars, evals):
        axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                        f'{ev} evals', ha='center', fontsize=8)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/06_FALQON/falqon_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/06_FALQON/falqon_results.png")

    # =========================================================================
    # Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    FALQON on {num_nodes}-node MaxCut:

    FALQON:  ratio = {cost_history[-1]/max_cut:.4f} (50 layers, 50 evals)
    QAOA p=1: ratio = {qaoa_results[1][0]/max_cut:.4f} ({qaoa_results[1][1]} evals)
    QAOA p=3: ratio = {qaoa_results[3][0]/max_cut:.4f} ({qaoa_results[3][1]} evals)

    Key observations:
    1. FALQON converges monotonically (Lyapunov guarantee)
    2. No classical optimizer needed (feedback law sets parameters)
    3. Each layer requires only 1 circuit evaluation
    4. Trade-off: deeper circuit but fewer total evaluations

    FALQON is most valuable when:
    - Classical optimization is expensive (many parameters)
    - Monotonic convergence is desired
    - Hardware can handle moderately deep circuits
    """)


if __name__ == "__main__":
    main()
