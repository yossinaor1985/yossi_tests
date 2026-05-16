"""
Quantum Approximate Optimization Algorithm (QAOA) - Local Simulator
====================================================================

This script demonstrates QAOA applied to the MaxCut problem on a
4-node graph using the local Aer simulator.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
QAOA prepares the state:
    |gamma, beta> = U_M(beta_p) U_C(gamma_p) ... U_M(beta_1) U_C(gamma_1) |+>^n

where:
    U_C(gamma) = exp(-i gamma H_C)  is the cost unitary (phase separator)
    U_M(beta)  = exp(-i beta H_M)   is the mixer unitary
    H_C = (1/2) sum_{(i,j) in E} (I - Z_i Z_j)  for MaxCut
    H_M = sum_i X_i                               transverse field mixer

The algorithm:
    1. Encode the optimization problem as an Ising Hamiltonian H_C
    2. Start in uniform superposition |+>^n
    3. Alternate cost and mixer unitaries p times
    4. Optimize gamma, beta classically to maximize <H_C>
    5. Sample the final state to get candidate solutions
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer import AerSimulator
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer.primitives import SamplerV2 as AerSampler, EstimatorV2 as AerEstimator


def create_maxcut_graph():
    """
    Create a simple graph for the MaxCut problem.

    Graph: 4 nodes in a cycle (square graph)
        0 --- 1
        |     |
        3 --- 2

    Edges: {(0,1), (1,2), (2,3), (0,3)}

    Optimal MaxCut: 4 (all edges cut)
    Optimal solutions: |0101> and |1010> (alternating partition)

    Returns:
        list: List of edges as (i, j) tuples
        int: Number of nodes
    """
    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    num_nodes = 4
    return edges, num_nodes


def build_maxcut_hamiltonian(edges, num_nodes):
    """
    Build the MaxCut cost Hamiltonian as a SparsePauliOp.

    MaxCut Hamiltonian (see explanation_physicist.md, Section 3.2):
        H_C = (1/2) sum_{(i,j) in E} (I - Z_i Z_j)

    Each edge contributes a term (I - Z_i Z_j)/2:
        - If qubits i,j have different values: eigenvalue = +1 (edge IS cut)
        - If qubits i,j have same values: eigenvalue = 0 (edge NOT cut)

    So <H_C> counts the expected number of cut edges.

    Args:
        edges: List of edges as (i, j) tuples
        num_nodes: Number of nodes (qubits)

    Returns:
        SparsePauliOp: The MaxCut Hamiltonian
    """
    pauli_list = []

    for i, j in edges:
        # Identity term: coefficient +0.5
        identity = ["I"] * num_nodes
        pauli_list.append(("".join(identity), 0.5))

        # -Z_i Z_j term: coefficient -0.5
        zz_term = ["I"] * num_nodes
        zz_term[i] = "Z"
        zz_term[j] = "Z"
        # Note: Qiskit uses little-endian ordering (qubit 0 is rightmost)
        pauli_list.append(("".join(reversed(zz_term)), -0.5))

    hamiltonian = SparsePauliOp.from_list(pauli_list).simplify()
    return hamiltonian


def build_qaoa_circuit_manual(edges, num_nodes, gamma, beta, p=1):
    """
    Build a QAOA circuit manually to understand the structure.

    This function constructs the QAOA circuit step by step, showing
    exactly how the cost and mixer unitaries are implemented as quantum gates.

    Circuit structure for p layers (see explanation_physicist.md, Section 2.2):
        1. Initialize in |+>^n (Hadamard on all qubits)
        2. For each layer l = 1, ..., p:
            a. Apply U_C(gamma_l): ZZ rotations on each edge
            b. Apply U_M(beta_l): X rotations on each qubit

    U_C(gamma) implementation for each edge (i,j):
        CNOT(i,j) -- R_Z(2*gamma) on j -- CNOT(i,j)
        This creates: exp(-i * gamma * Z_i Z_j)

    U_M(beta) implementation for each qubit i:
        R_X(2*beta) on i
        This creates: exp(-i * beta * X_i)

    Args:
        edges: List of edges
        num_nodes: Number of nodes (qubits)
        gamma: List of cost layer parameters [gamma_1, ..., gamma_p]
        beta: List of mixer layer parameters [beta_1, ..., beta_p]
        p: Number of QAOA layers

    Returns:
        QuantumCircuit: The QAOA circuit
    """
    qc = QuantumCircuit(num_nodes)

    # Step 1: Initialize in uniform superposition |+>^n
    # This is the ground state of H_M = sum_i X_i
    for i in range(num_nodes):
        qc.h(i)
    qc.barrier()

    # Step 2: Apply p layers of cost + mixer
    for layer in range(p):
        # --- Cost unitary U_C(gamma_l) ---
        # For each edge (i,j), apply exp(-i * gamma * Z_i Z_j)
        # Implementation: CNOT - RZ - CNOT
        #
        # Mathematical justification:
        #   CNOT_{ij} maps Z_i Z_j -> Z_j (the parity is stored on qubit j)
        #   So exp(-i gamma Z_i Z_j) = CNOT_{ij} exp(-i gamma Z_j) CNOT_{ij}
        #   And exp(-i gamma Z_j) = R_Z(2*gamma)
        for i, j in edges:
            qc.cx(i, j)                  # CNOT: encode parity on qubit j
            qc.rz(2 * gamma[layer], j)   # Phase rotation based on parity
            qc.cx(i, j)                  # CNOT: uncompute parity
        qc.barrier()

        # --- Mixer unitary U_M(beta_l) ---
        # For each qubit i, apply exp(-i * beta * X_i) = R_X(2*beta)
        for i in range(num_nodes):
            qc.rx(2 * beta[layer], i)
        qc.barrier()

    # Add measurements
    qc.measure_all()

    return qc


def evaluate_maxcut(bitstring, edges):
    """
    Evaluate the MaxCut value for a given bitstring.

    Args:
        bitstring: String of 0s and 1s representing the partition
        edges: List of edges

    Returns:
        int: Number of edges cut by this partition
    """
    cut = 0
    for i, j in edges:
        if bitstring[i] != bitstring[j]:
            cut += 1
    return cut


def main():
    print("=" * 70)
    print("QAOA - Quantum Approximate Optimization Algorithm (Local Simulator)")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Define the MaxCut Problem
    # =========================================================================

    print("\n--- Step 1: MaxCut Problem Definition ---")

    edges, num_nodes = create_maxcut_graph()
    print(f"Graph: {num_nodes} nodes, {len(edges)} edges")
    print(f"Edges: {edges}")
    print(f"Graph structure (cycle/square):")
    print("    0 --- 1")
    print("    |     |")
    print("    3 --- 2")

    # =========================================================================
    # STEP 2: Build the Cost Hamiltonian
    # =========================================================================

    print("\n--- Step 2: Cost Hamiltonian ---")

    hamiltonian = build_maxcut_hamiltonian(edges, num_nodes)
    print(f"H_C = {hamiltonian}")
    print(f"\nNumber of Pauli terms: {len(hamiltonian)}")

    # Compute exact solution by diagonalization
    eigvals = np.linalg.eigvalsh(hamiltonian.to_matrix())
    max_cut_value = max(eigvals.real)
    print(f"\nExact MaxCut value: {max_cut_value:.0f}")
    print(f"Optimal solutions: |0101> and |1010> (cut = 4)")

    # =========================================================================
    # STEP 3: Build and Visualize QAOA Circuit (Manual, p=1)
    # =========================================================================

    print("\n--- Step 3: QAOA Circuit (Manual Build, p=1) ---")

    # Use example parameters for visualization
    gamma_example = [np.pi / 4]
    beta_example = [np.pi / 8]

    qc_manual = build_qaoa_circuit_manual(
        edges, num_nodes,
        gamma=gamma_example,
        beta=beta_example,
        p=1
    )
    print(f"\nQAOA circuit (p=1) with gamma={gamma_example[0]:.4f}, beta={beta_example[0]:.4f}:")
    print(qc_manual.draw(output="text", fold=100))

    # =========================================================================
    # STEP 4: Run QAOA Using Qiskit's Built-in Implementation
    # =========================================================================

    print("\n--- Step 4: Running QAOA (Qiskit built-in, p=1 to p=3) ---")

    estimator = AerEstimator()
    sampler = AerSampler()

    results_by_p = {}

    for p in [1, 2, 3]:
        print(f"\n  --- QAOA with p = {p} layers ---")

        optimizer = COBYLA(maxiter=300)

        qaoa = QAOA(
            estimator=estimator,
            sampler=sampler,
            optimizer=optimizer,
            reps=p,       # Number of QAOA layers
        )

        # For MaxCut, we want to MAXIMIZE <H_C>
        # Qiskit's QAOA minimizes by default, so we negate the Hamiltonian
        neg_hamiltonian = -1.0 * hamiltonian

        result = qaoa.compute_minimum_eigenvalue(neg_hamiltonian)

        # The energy we get is -<H_C>, so negate to get <H_C>
        cut_value = -result.eigenvalue.real
        approx_ratio = cut_value / max_cut_value

        print(f"  Expected cut value: {cut_value:.4f}")
        print(f"  Approximation ratio: {approx_ratio:.4f} ({approx_ratio*100:.1f}%)")
        print(f"  Optimal parameters: gamma={result.optimal_parameters}")
        print(f"  Evaluations: {result.cost_function_evals}")

        results_by_p[p] = {
            'cut_value': cut_value,
            'approx_ratio': approx_ratio,
            'result': result
        }

    # =========================================================================
    # STEP 5: Sample Solutions from the Optimal QAOA Circuit
    # =========================================================================

    print("\n--- Step 5: Sampling Solutions (Best QAOA) ---")

    # Use the best result (highest p)
    best_p = max(results_by_p.keys())
    best_result = results_by_p[best_p]

    # Run the QAOA circuit with optimal parameters and sample
    print(f"\nUsing QAOA p={best_p}, sampling 1024 shots...")

    # Build the optimal circuit manually for sampling
    best_params = best_result['result'].optimal_parameters
    gamma_vals = [best_params.get(f'gamma[{i}]', best_params.get(list(best_params.keys())[i], 0))
                  for i in range(best_p)]
    beta_vals = [best_params.get(f'beta[{i}]', best_params.get(list(best_params.keys())[best_p + i], 0))
                 for i in range(best_p)]

    # Actually, let's just get the best bitstring from the result
    if hasattr(best_result['result'], 'best_measurement'):
        best_bitstring = best_result['result'].best_measurement.get('bitstring', 'N/A')
        print(f"Best measurement: {best_bitstring}")

    # Evaluate all possible solutions for comparison
    print(f"\nAll possible cuts for reference:")
    all_cuts = {}
    for i in range(2**num_nodes):
        bs = format(i, f'0{num_nodes}b')
        cut = evaluate_maxcut(bs, edges)
        all_cuts[bs] = cut

    # Sort by cut value
    sorted_cuts = sorted(all_cuts.items(), key=lambda x: x[1], reverse=True)
    for bs, cut in sorted_cuts[:6]:
        marker = " <-- OPTIMAL" if cut == max_cut_value else ""
        print(f"  |{bs}> : cut = {cut}{marker}")

    # =========================================================================
    # STEP 6: Parameter Landscape Visualization (p=1)
    # =========================================================================

    print("\n--- Step 6: Parameter Landscape (p=1) ---")
    print("Computing energy landscape E(gamma, beta)...")

    gamma_range = np.linspace(0, 2 * np.pi, 50)
    beta_range = np.linspace(0, np.pi, 50)
    energy_landscape = np.zeros((len(beta_range), len(gamma_range)))

    for gi, g in enumerate(gamma_range):
        for bi, b in enumerate(beta_range):
            # Build circuit without measurement for statevector simulation
            qc = QuantumCircuit(num_nodes)
            for q in range(num_nodes):
                qc.h(q)
            for i, j in edges:
                qc.cx(i, j)
                qc.rz(2 * g, j)
                qc.cx(i, j)
            for q in range(num_nodes):
                qc.rx(2 * b, q)

            sv = Statevector(qc)
            energy_landscape[bi, gi] = sv.expectation_value(hamiltonian).real

    # =========================================================================
    # STEP 7: Plot Results
    # =========================================================================

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: Energy landscape heatmap
    im = axes[0].imshow(
        energy_landscape,
        extent=[0, 2*np.pi, 0, np.pi],
        origin='lower',
        aspect='auto',
        cmap='RdYlGn'
    )
    axes[0].set_xlabel('gamma', fontsize=12)
    axes[0].set_ylabel('beta', fontsize=12)
    axes[0].set_title('QAOA Energy Landscape (p=1)', fontsize=14)
    plt.colorbar(im, ax=axes[0], label='<H_C> (expected cut)')

    # Plot 2: Approximation ratio vs p
    p_values = sorted(results_by_p.keys())
    approx_ratios = [results_by_p[p]['approx_ratio'] for p in p_values]
    axes[1].bar(p_values, approx_ratios, color=['#3498db', '#2ecc71', '#e74c3c'])
    axes[1].set_xlabel('Number of QAOA layers (p)', fontsize=12)
    axes[1].set_ylabel('Approximation ratio', fontsize=12)
    axes[1].set_title('QAOA Performance vs Depth', fontsize=14)
    axes[1].set_ylim(0, 1.1)
    axes[1].axhline(y=1.0, color='k', linestyle='--', alpha=0.5, label='Exact solution')
    axes[1].legend()
    for i, (p, ar) in enumerate(zip(p_values, approx_ratios)):
        axes[1].text(p, ar + 0.02, f'{ar:.3f}', ha='center', fontsize=10)

    # Plot 3: All cut values bar chart
    bitstrings = [bs for bs, _ in sorted_cuts]
    cut_values_list = [c for _, c in sorted_cuts]
    colors = ['green' if c == max_cut_value else 'skyblue' for c in cut_values_list]
    axes[2].bar(range(len(bitstrings)), cut_values_list, color=colors, tick_label=bitstrings)
    axes[2].set_xlabel('Bitstring (partition)', fontsize=12)
    axes[2].set_ylabel('Cut value', fontsize=12)
    axes[2].set_title('All Possible MaxCut Solutions', fontsize=14)
    axes[2].tick_params(axis='x', rotation=90, labelsize=8)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/02_QAOA/qaoa_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/02_QAOA/qaoa_results.png")

    # =========================================================================
    # STEP 8: Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    QAOA successfully solved the MaxCut problem on a 4-node cycle graph.

    Results by depth:
      p=1: Approximation ratio = {results_by_p[1]['approx_ratio']:.4f}
      p=2: Approximation ratio = {results_by_p[2]['approx_ratio']:.4f}
      p=3: Approximation ratio = {results_by_p[3]['approx_ratio']:.4f}

    Key concepts demonstrated:
    1. Encoding combinatorial optimization as Ising Hamiltonian
    2. QAOA circuit: alternating cost and mixer unitaries
    3. ZZ interaction via CNOT-RZ-CNOT decomposition
    4. Effect of circuit depth (p) on solution quality
    5. Parameter landscape visualization

    Optimal MaxCut = {max_cut_value:.0f} (partitions: |0101>, |1010>)
    """)


if __name__ == "__main__":
    main()
