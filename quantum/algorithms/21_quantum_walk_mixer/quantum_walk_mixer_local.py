"""
Quantum Walk Mixer (Generalized QAOA) - Local Simulator
========================================================

This script demonstrates the Quantum Alternating Operator Ansatz (QAOAz)
with an XY mixer applied to the Max Bisection problem on a 4-node cycle
graph using the local Aer simulator.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Standard QAOA uses a transverse-field mixer H_M = sum_i X_i, which does
not preserve constraints. For constrained optimization, the Quantum
Alternating Operator Ansatz (Hadfield et al., 2019) replaces this with
a constraint-preserving mixer.

For Hamming-weight constraints (exactly k ones out of n bits), the
XY mixer is the natural choice:

    H_XY = sum_{(i,j)} (X_i X_j + Y_i Y_j) / 2

This mixer preserves Hamming weight because it swaps excitations between
qubits without creating or destroying them. The algorithm uses:

    1. Initial state: Dicke state |D_n^k> (equal superposition over
       all weight-k bitstrings)
    2. Cost unitary: U_C(gamma) = exp(-i gamma H_C) (same as QAOA)
    3. XY mixer unitary: U_XY(beta) = exp(-i beta H_XY)
       (preserves Hamming weight)

The XY mixer implements a continuous-time quantum walk on the Johnson
graph J(n, k), whose nodes are weight-k bitstrings connected by
single-excitation swaps.

Problem: Max Bisection on a 4-node cycle graph
    - Constraint: exactly 2 nodes per partition (Hamming weight = 2)
    - 6 feasible solutions out of 16 total
    - Optimal: |0101> and |1010> (cut all 4 edges, C_max = 4)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from itertools import combinations

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.circuit.library import XXPlusYYGate
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler, EstimatorV2 as AerEstimator
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA


def create_max_bisection_graph():
    """
    Create a simple graph for the Max Bisection problem.

    Graph: 4 nodes in a cycle (same as algorithm 02_QAOA)
        0 --- 1
        |     |
        3 --- 2

    Edges: {(0,1), (1,2), (2,3), (0,3)}

    Max Bisection: partition into two EQUAL sets of size 2
    to maximize edges cut.

    Optimal Max Bisection = 4 (all edges cut)
    Optimal solutions: |0101> and |1010>

    Returns:
        list: List of edges as (i, j) tuples
        int: Number of nodes
        int: Required Hamming weight (n/2)
    """
    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    num_nodes = 4
    hamming_weight = num_nodes // 2
    return edges, num_nodes, hamming_weight


def build_maxcut_hamiltonian(edges, num_nodes):
    """
    Build the MaxCut cost Hamiltonian as a SparsePauliOp.

    H_C = (1/2) sum_{(i,j) in E} (I - Z_i Z_j)

    This is identical to the standard MaxCut Hamiltonian (see algorithm 02).
    The cost function is the same for MaxCut and Max Bisection; only the
    constraint (and hence the mixer and initial state) differs.

    Args:
        edges: List of edges as (i, j) tuples
        num_nodes: Number of nodes (qubits)

    Returns:
        SparsePauliOp: The MaxCut Hamiltonian
    """
    pauli_list = []
    for i, j in edges:
        identity = "I" * num_nodes
        pauli_list.append((identity, 0.5))

        zz_term = ["I"] * num_nodes
        zz_term[i] = "Z"
        zz_term[j] = "Z"
        pauli_list.append(("".join(reversed(zz_term)), -0.5))

    return SparsePauliOp.from_list(pauli_list).simplify()


def build_xy_mixer_hamiltonian(num_nodes):
    """
    Build the XY mixer Hamiltonian as a SparsePauliOp.

    H_XY = sum_{i<j} (X_i X_j + Y_i Y_j) / 2

    This mixer preserves Hamming weight: [H_XY, sum_i Z_i] = 0.

    We sum over ALL qubit pairs (complete mixer graph) to ensure
    full connectivity on the Johnson graph J(n, k).

    Args:
        num_nodes: Number of qubits

    Returns:
        SparsePauliOp: The XY mixer Hamiltonian
    """
    pauli_list = []
    for i, j in combinations(range(num_nodes), 2):
        # XX term: coefficient +0.5
        xx_term = ["I"] * num_nodes
        xx_term[i] = "X"
        xx_term[j] = "X"
        pauli_list.append(("".join(reversed(xx_term)), 0.5))

        # YY term: coefficient +0.5
        yy_term = ["I"] * num_nodes
        yy_term[i] = "Y"
        yy_term[j] = "Y"
        pauli_list.append(("".join(reversed(yy_term)), 0.5))

    return SparsePauliOp.from_list(pauli_list).simplify()


def prepare_dicke_state_vector(num_nodes, hamming_weight):
    """
    Compute the Dicke state |D_n^k> as a numpy array.

    |D_n^k> = (1/sqrt(C(n,k))) sum_{|z|=k} |z>

    This is the equal-amplitude superposition of all n-qubit states
    with exactly k ones. It serves as the initial state for QAOAz
    with the XY mixer.

    Args:
        num_nodes: Number of qubits (n)
        hamming_weight: Target Hamming weight (k)

    Returns:
        np.array: The Dicke state vector (length 2^n)
    """
    state = np.zeros(2**num_nodes)
    positions = list(combinations(range(num_nodes), hamming_weight))
    amplitude = 1.0 / np.sqrt(len(positions))
    for pos in positions:
        index = sum(1 << p for p in pos)
        state[index] = amplitude
    return state


def build_quantum_walk_mixer_circuit(edges, num_nodes, gammas, betas, p,
                                     hamming_weight):
    """
    Build the QAOAz circuit with XY mixer (manual construction).

    Circuit structure:
        |D_n^k> --[U_C(g1)]--[U_XY(b1)]--...--[U_C(gp)]--[U_XY(bp)]-- Measure

    The cost unitary U_C(gamma) is identical to standard QAOA:
        For each edge (i,j): CNOT(i,j) - RZ(2*gamma) - CNOT(i,j)
        This implements exp(-i gamma Z_i Z_j).

    The XY mixer U_XY(beta) uses XXPlusYYGate on all qubit pairs:
        XXPlusYYGate(2*beta) implements exp(-i beta (XX + YY)/2)

    Args:
        edges: List of graph edges
        num_nodes: Number of qubits
        gammas: Cost layer parameters [gamma_1, ..., gamma_p]
        betas: Mixer layer parameters [beta_1, ..., beta_p]
        p: Number of QAOAz layers
        hamming_weight: Target Hamming weight for Dicke state

    Returns:
        QuantumCircuit: The QAOAz circuit with measurements
    """
    qc = QuantumCircuit(num_nodes)

    # Step 1: Initialize Dicke state |D_n^k>
    dicke_state = prepare_dicke_state_vector(num_nodes, hamming_weight)
    qc.initialize(dicke_state, range(num_nodes))
    qc.barrier()

    # Step 2: Apply p layers of cost + XY mixer
    for layer in range(p):
        # --- Cost unitary U_C(gamma_l) ---
        # For each edge (i,j), apply exp(-i * gamma * Z_i Z_j)
        # Implementation: CNOT - RZ(2*gamma) - CNOT
        for i, j in edges:
            qc.cx(i, j)
            qc.rz(2 * gammas[layer], j)
            qc.cx(i, j)
        qc.barrier()

        # --- XY Mixer U_XY(beta_l) ---
        # For each qubit pair (i,j), apply exp(-i * beta * (XX + YY)/2)
        # XXPlusYYGate(theta) = exp(-i (theta/4)(XX+YY))
        # So theta = 2*beta gives exp(-i beta (XX+YY)/2)
        for i, j in combinations(range(num_nodes), 2):
            qc.append(XXPlusYYGate(2 * betas[layer]), [i, j])
        qc.barrier()

    qc.measure_all()
    return qc


def build_quantum_walk_mixer_statevector(edges, num_nodes, gammas, betas, p,
                                          hamming_weight):
    """
    Build the QAOAz circuit WITHOUT measurements for Statevector simulation.

    Used for computing expectation values during optimization.

    Args:
        edges: List of graph edges
        num_nodes: Number of qubits
        gammas: Cost layer parameters
        betas: Mixer layer parameters
        p: Number of QAOAz layers
        hamming_weight: Target Hamming weight

    Returns:
        QuantumCircuit: The QAOAz circuit without measurements
    """
    qc = QuantumCircuit(num_nodes)

    dicke_state = prepare_dicke_state_vector(num_nodes, hamming_weight)
    qc.initialize(dicke_state, range(num_nodes))

    for layer in range(p):
        for i, j in edges:
            qc.cx(i, j)
            qc.rz(2 * gammas[layer], j)
            qc.cx(i, j)
        for i, j in combinations(range(num_nodes), 2):
            qc.append(XXPlusYYGate(2 * betas[layer]), [i, j])

    return qc


def build_standard_qaoa_circuit_statevector(edges, num_nodes, gammas, betas, p):
    """
    Build a standard QAOA circuit (transverse-field mixer) for comparison.

    This uses H_M = sum_i X_i and starts from |+>^n.
    It does NOT preserve Hamming weight constraints.

    Args:
        edges: List of graph edges
        num_nodes: Number of qubits
        gammas: Cost layer parameters
        betas: Mixer layer parameters
        p: Number of QAOA layers

    Returns:
        QuantumCircuit: Standard QAOA circuit without measurements
    """
    qc = QuantumCircuit(num_nodes)

    # Initialize |+>^n
    for q in range(num_nodes):
        qc.h(q)

    for layer in range(p):
        # Cost unitary
        for i, j in edges:
            qc.cx(i, j)
            qc.rz(2 * gammas[layer], j)
            qc.cx(i, j)
        # Standard mixer: R_X(2*beta) on each qubit
        for q in range(num_nodes):
            qc.rx(2 * betas[layer], q)

    return qc


def evaluate_max_bisection(bitstring, edges, target_weight):
    """
    Evaluate the cut value for a Max Bisection solution.

    Args:
        bitstring: String of 0s and 1s representing the partition
        edges: List of edges
        target_weight: Required Hamming weight (n/2)

    Returns:
        int: Number of edges cut, or -1 if infeasible
    """
    hw = sum(int(b) for b in bitstring)
    if hw != target_weight:
        return -1
    cut = 0
    for i, j in edges:
        if bitstring[i] != bitstring[j]:
            cut += 1
    return cut


def enumerate_feasible_solutions(num_nodes, hamming_weight, edges):
    """
    List all feasible solutions with their cut values.

    Args:
        num_nodes: Number of nodes
        hamming_weight: Required Hamming weight
        edges: List of edges

    Returns:
        list: List of (bitstring, cut_value) tuples, sorted by cut value
    """
    feasible = []
    for i in range(2**num_nodes):
        bs = format(i, f'0{num_nodes}b')
        hw = sum(int(b) for b in bs)
        if hw == hamming_weight:
            cut = sum(1 for a, b in edges if bs[a] != bs[b])
            feasible.append((bs, cut))
    return sorted(feasible, key=lambda x: x[1], reverse=True)


def main():
    print("=" * 70)
    print("Quantum Walk Mixer (QAOAz) - Local Simulator")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Define the Max Bisection Problem
    # =========================================================================

    print("\n--- Step 1: Max Bisection Problem Definition ---")

    edges, num_nodes, hamming_weight = create_max_bisection_graph()
    print(f"Graph: {num_nodes} nodes, {len(edges)} edges")
    print(f"Edges: {edges}")
    print(f"Graph structure (cycle/square):")
    print("    0 --- 1")
    print("    |     |")
    print("    3 --- 2")
    print(f"\nConstraint: Hamming weight = {hamming_weight} "
          f"(equal partition size)")

    feasible = enumerate_feasible_solutions(num_nodes, hamming_weight, edges)
    max_bisection_value = feasible[0][1]
    optimal_solutions = [bs for bs, c in feasible if c == max_bisection_value]

    print(f"\nFeasible solutions ({len(feasible)} out of {2**num_nodes}):")
    for bs, cut in feasible:
        marker = " <-- OPTIMAL" if cut == max_bisection_value else ""
        print(f"  |{bs}> : cut = {cut}{marker}")
    print(f"\nMax Bisection value: {max_bisection_value}")
    print(f"Optimal partitions: {optimal_solutions}")

    # =========================================================================
    # STEP 2: Build Hamiltonians
    # =========================================================================

    print("\n--- Step 2: Cost and Mixer Hamiltonians ---")

    hamiltonian = build_maxcut_hamiltonian(edges, num_nodes)
    print(f"Cost Hamiltonian H_C = {hamiltonian}")

    xy_mixer = build_xy_mixer_hamiltonian(num_nodes)
    print(f"\nXY Mixer H_XY = {xy_mixer}")
    print(f"Number of XY pair terms: {len(list(combinations(range(num_nodes), 2)))}")

    # Verify [H_XY, sum_i Z_i] = 0 (Hamming weight preservation)
    total_z_list = []
    for i in range(num_nodes):
        z_term = ["I"] * num_nodes
        z_term[i] = "Z"
        total_z_list.append(("".join(reversed(z_term)), 1.0))
    total_z = SparsePauliOp.from_list(total_z_list)

    commutator = (xy_mixer @ total_z - total_z @ xy_mixer).simplify()
    commutator_norm = np.max(np.abs(commutator.to_matrix()))
    print(f"\n[H_XY, sum_i Z_i] norm = {commutator_norm:.2e} "
          f"({'PASS: Hamming weight preserved' if commutator_norm < 1e-10 else 'FAIL'})")

    # =========================================================================
    # STEP 3: Prepare and Verify Dicke State
    # =========================================================================

    print("\n--- Step 3: Dicke State |D_4^2> ---")

    dicke_vec = prepare_dicke_state_vector(num_nodes, hamming_weight)
    dicke_sv = Statevector(dicke_vec)

    print(f"Dicke state |D_{num_nodes}^{hamming_weight}> amplitudes:")
    probs = dicke_sv.probabilities_dict()
    for bs in sorted(probs.keys()):
        if probs[bs] > 1e-10:
            hw = sum(int(b) for b in bs)
            print(f"  |{bs}> : prob = {probs[bs]:.4f}, "
                  f"Hamming weight = {hw}")

    # Verify all nonzero amplitudes have correct Hamming weight
    all_correct = all(
        sum(int(b) for b in bs) == hamming_weight
        for bs, p in probs.items() if p > 1e-10
    )
    print(f"\nAll amplitudes have Hamming weight {hamming_weight}: "
          f"{'PASS' if all_correct else 'FAIL'}")

    # =========================================================================
    # STEP 4: Build and Visualize QAOAz Circuit (p=1)
    # =========================================================================

    print("\n--- Step 4: QAOAz Circuit with XY Mixer (p=1) ---")

    gamma_example = [np.pi / 4]
    beta_example = [np.pi / 8]

    qc_example = build_quantum_walk_mixer_circuit(
        edges, num_nodes,
        gammas=gamma_example,
        betas=beta_example,
        p=1,
        hamming_weight=hamming_weight
    )
    print(f"\nQAOAz circuit (p=1) with gamma={gamma_example[0]:.4f}, "
          f"beta={beta_example[0]:.4f}:")
    print(qc_example.draw(output="text", fold=120))

    # Verify the circuit output preserves Hamming weight
    qc_sv = build_quantum_walk_mixer_statevector(
        edges, num_nodes,
        gammas=gamma_example,
        betas=beta_example,
        p=1,
        hamming_weight=hamming_weight
    )
    sv_out = Statevector(qc_sv)
    probs_out = sv_out.probabilities_dict()
    infeasible_prob = sum(
        p for bs, p in probs_out.items()
        if sum(int(b) for b in bs) != hamming_weight and p > 1e-12
    )
    print(f"\nProbability of infeasible states: {infeasible_prob:.2e} "
          f"({'PASS' if infeasible_prob < 1e-10 else 'FAIL'})")

    # =========================================================================
    # STEP 5: Run QAOAz with XY Mixer (p=1 to p=3)
    # =========================================================================

    print("\n--- Step 5: Running QAOAz with XY Mixer (p=1 to p=3) ---")

    qw_results = {}

    for p in [1, 2, 3]:
        print(f"\n  --- QAOAz with XY mixer, p = {p} ---")

        def objective(params, _p=p):
            gammas = params[:_p]
            betas = params[_p:]
            qc = build_quantum_walk_mixer_statevector(
                edges, num_nodes, gammas, betas, _p, hamming_weight
            )
            sv = Statevector(qc)
            energy = sv.expectation_value(hamiltonian).real
            return -energy  # Minimize negative energy = maximize energy

        optimizer = COBYLA(maxiter=500)
        x0 = np.random.uniform(0, np.pi, 2 * p)
        opt_result = optimizer.minimize(objective, x0)

        cut_value = -opt_result.fun
        approx_ratio = cut_value / max_bisection_value

        # Get the probability distribution at optimal parameters
        opt_gammas = opt_result.x[:p]
        opt_betas = opt_result.x[p:]
        qc_opt = build_quantum_walk_mixer_statevector(
            edges, num_nodes, opt_gammas, opt_betas, p, hamming_weight
        )
        sv_opt = Statevector(qc_opt)
        probs_opt = sv_opt.probabilities_dict()

        print(f"  Expected cut value: {cut_value:.4f}")
        print(f"  Approximation ratio: {approx_ratio:.4f} "
              f"({approx_ratio * 100:.1f}%)")
        print(f"  Optimizer evaluations: {opt_result.nfev}")

        qw_results[p] = {
            'cut_value': cut_value,
            'approx_ratio': approx_ratio,
            'probs': probs_opt,
            'params': opt_result.x,
        }

    # =========================================================================
    # STEP 6: Run Standard QAOA for Comparison (p=1 to p=3)
    # =========================================================================

    print("\n--- Step 6: Standard QAOA for Comparison (p=1 to p=3) ---")

    std_results = {}

    for p in [1, 2, 3]:
        print(f"\n  --- Standard QAOA, p = {p} ---")

        def std_objective(params, _p=p):
            gammas = params[:_p]
            betas = params[_p:]
            qc = build_standard_qaoa_circuit_statevector(
                edges, num_nodes, gammas, betas, _p
            )
            sv = Statevector(qc)
            energy = sv.expectation_value(hamiltonian).real
            return -energy

        optimizer = COBYLA(maxiter=500)
        x0 = np.random.uniform(0, np.pi, 2 * p)
        opt_result = optimizer.minimize(std_objective, x0)

        cut_value = -opt_result.fun
        approx_ratio = cut_value / max_bisection_value

        opt_gammas = opt_result.x[:p]
        opt_betas = opt_result.x[p:]
        qc_opt = build_standard_qaoa_circuit_statevector(
            edges, num_nodes, opt_gammas, opt_betas, p
        )
        sv_opt = Statevector(qc_opt)
        probs_opt = sv_opt.probabilities_dict()

        # Compute feasibility rate
        feasible_prob = sum(
            prob for bs, prob in probs_opt.items()
            if sum(int(b) for b in bs) == hamming_weight
        )

        print(f"  Expected cut value (all states): {cut_value:.4f}")
        print(f"  Approximation ratio: {approx_ratio:.4f} "
              f"({approx_ratio * 100:.1f}%)")
        print(f"  Feasibility rate: {feasible_prob:.4f} "
              f"({feasible_prob * 100:.1f}%)")

        std_results[p] = {
            'cut_value': cut_value,
            'approx_ratio': approx_ratio,
            'feasible_prob': feasible_prob,
            'probs': probs_opt,
        }

    # =========================================================================
    # STEP 7: Feasibility Analysis
    # =========================================================================

    print("\n--- Step 7: Feasibility Comparison ---")
    print(f"\n{'p':>3} | {'QW Mixer Feasibility':>22} | "
          f"{'Std QAOA Feasibility':>22} | "
          f"{'QW Approx Ratio':>16} | {'Std Approx Ratio':>16}")
    print("-" * 90)
    for p in [1, 2, 3]:
        print(f"{p:>3} | {'100.00%':>22} | "
              f"{std_results[p]['feasible_prob'] * 100:>21.2f}% | "
              f"{qw_results[p]['approx_ratio']:>16.4f} | "
              f"{std_results[p]['approx_ratio']:>16.4f}")

    # =========================================================================
    # STEP 8: Visualization
    # =========================================================================

    print("\n--- Step 8: Visualization ---")
    print("Generating plots...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    # --- Plot 1: Approximation Ratio Comparison ---
    p_values = [1, 2, 3]
    qw_ratios = [qw_results[p]['approx_ratio'] for p in p_values]
    std_ratios = [std_results[p]['approx_ratio'] for p in p_values]

    x = np.arange(len(p_values))
    width = 0.35
    bars1 = axes[0, 0].bar(x - width / 2, qw_ratios, width,
                            label='QW Mixer (XY)', color='#2ecc71')
    bars2 = axes[0, 0].bar(x + width / 2, std_ratios, width,
                            label='Standard QAOA', color='#3498db')
    axes[0, 0].axhline(y=1.0, color='k', linestyle='--', alpha=0.5,
                        label='Exact solution')
    axes[0, 0].set_xlabel('Number of layers (p)', fontsize=12)
    axes[0, 0].set_ylabel('Approximation ratio', fontsize=12)
    axes[0, 0].set_title('Approximation Ratio: XY Mixer vs Standard QAOA',
                          fontsize=13)
    axes[0, 0].set_xticks(x)
    axes[0, 0].set_xticklabels(p_values)
    axes[0, 0].set_ylim(0, 1.15)
    axes[0, 0].legend(fontsize=10)
    for bar in bars1:
        axes[0, 0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                        f'{bar.get_height():.3f}', ha='center', fontsize=9)
    for bar in bars2:
        axes[0, 0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                        f'{bar.get_height():.3f}', ha='center', fontsize=9)

    # --- Plot 2: Feasibility Rate ---
    qw_feas = [100.0] * 3
    std_feas = [std_results[p]['feasible_prob'] * 100 for p in p_values]

    bars1 = axes[0, 1].bar(x - width / 2, qw_feas, width,
                            label='QW Mixer (XY)', color='#2ecc71')
    bars2 = axes[0, 1].bar(x + width / 2, std_feas, width,
                            label='Standard QAOA', color='#3498db')
    axes[0, 1].set_xlabel('Number of layers (p)', fontsize=12)
    axes[0, 1].set_ylabel('Feasibility rate (%)', fontsize=12)
    axes[0, 1].set_title('Feasibility: XY Mixer Always Preserves Constraints',
                          fontsize=13)
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(p_values)
    axes[0, 1].set_ylim(0, 115)
    axes[0, 1].legend(fontsize=10)
    for bar in bars2:
        axes[0, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                        f'{bar.get_height():.1f}%', ha='center', fontsize=9)

    # --- Plot 3: Probability Distribution (QW Mixer, best p) ---
    best_p = max(qw_results.keys())
    best_probs = qw_results[best_p]['probs']

    feasible_bs = [bs for bs, _ in feasible]
    feasible_probs = [best_probs.get(bs, 0.0) for bs in feasible_bs]
    colors = ['#2ecc71' if bs in optimal_solutions else '#3498db'
              for bs in feasible_bs]

    axes[1, 0].bar(range(len(feasible_bs)), feasible_probs, color=colors)
    axes[1, 0].set_xlabel('Feasible bitstring', fontsize=12)
    axes[1, 0].set_ylabel('Probability', fontsize=12)
    axes[1, 0].set_title(f'QW Mixer Output Distribution (p={best_p})',
                          fontsize=13)
    axes[1, 0].set_xticks(range(len(feasible_bs)))
    axes[1, 0].set_xticklabels([f'|{bs}>' for bs in feasible_bs],
                                rotation=45, fontsize=9)
    # Add legend for colors
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#2ecc71', label='Optimal (cut=4)'),
                       Patch(facecolor='#3498db', label='Suboptimal (cut=2)')]
    axes[1, 0].legend(handles=legend_elements, fontsize=10)

    # --- Plot 4: Energy Landscape (p=1) ---
    print("Computing p=1 energy landscape...")
    gamma_range = np.linspace(0, 2 * np.pi, 40)
    beta_range = np.linspace(0, np.pi, 40)
    energy_landscape = np.zeros((len(beta_range), len(gamma_range)))

    for gi, g in enumerate(gamma_range):
        for bi, b in enumerate(beta_range):
            qc = build_quantum_walk_mixer_statevector(
                edges, num_nodes, [g], [b], 1, hamming_weight
            )
            sv = Statevector(qc)
            energy_landscape[bi, gi] = sv.expectation_value(hamiltonian).real

    im = axes[1, 1].imshow(
        energy_landscape,
        extent=[0, 2 * np.pi, 0, np.pi],
        origin='lower',
        aspect='auto',
        cmap='RdYlGn'
    )
    axes[1, 1].set_xlabel('gamma', fontsize=12)
    axes[1, 1].set_ylabel('beta', fontsize=12)
    axes[1, 1].set_title('QW Mixer Energy Landscape (p=1)', fontsize=13)
    plt.colorbar(im, ax=axes[1, 1], label='<H_C> (expected cut)')

    plt.tight_layout()
    plt.savefig("quantum/algorithms/21_quantum_walk_mixer/"
                "quantum_walk_mixer_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/21_quantum_walk_mixer/"
          "quantum_walk_mixer_results.png")

    # =========================================================================
    # STEP 9: Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    Quantum Walk Mixer (QAOAz) successfully solved Max Bisection
    on a 4-node cycle graph with Hamming-weight constraint.

    QAOAz with XY Mixer Results:
      p=1: Approximation ratio = {qw_results[1]['approx_ratio']:.4f}, Feasibility = 100%
      p=2: Approximation ratio = {qw_results[2]['approx_ratio']:.4f}, Feasibility = 100%
      p=3: Approximation ratio = {qw_results[3]['approx_ratio']:.4f}, Feasibility = 100%

    Standard QAOA Results (for comparison):
      p=1: Approx ratio = {std_results[1]['approx_ratio']:.4f}, Feasibility = {std_results[1]['feasible_prob']*100:.1f}%
      p=2: Approx ratio = {std_results[2]['approx_ratio']:.4f}, Feasibility = {std_results[2]['feasible_prob']*100:.1f}%
      p=3: Approx ratio = {std_results[3]['approx_ratio']:.4f}, Feasibility = {std_results[3]['feasible_prob']*100:.1f}%

    Key concepts demonstrated:
    1. XY mixer preserves Hamming weight (constraint preservation)
    2. Dicke state as feasible initial state
    3. XXPlusYYGate for implementing the XY mixer
    4. 100% feasibility vs ~{std_results[1]['feasible_prob']*100:.0f}% for standard QAOA
    5. Quantum walk on the Johnson graph J({num_nodes}, {hamming_weight})

    Max Bisection = {max_bisection_value} (partitions: {', '.join(optimal_solutions)})
    """)


if __name__ == "__main__":
    main()
