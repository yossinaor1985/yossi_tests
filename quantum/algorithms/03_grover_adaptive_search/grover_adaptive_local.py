"""
Grover Adaptive Search (GAS) for Optimization - Local Simulator
================================================================

This script demonstrates two approaches:
    A) Manual implementation of Grover's search with adaptive thresholding
    B) Qiskit's GroverOptimizer for QUBO problems

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
GAS applies Grover's search iteratively to find the minimum of a function:
    1. Start with a random solution x, set threshold y = f(x)
    2. Define oracle O_y that marks all x with f(x) < y
    3. Run Grover search to find x' with f(x') < y
    4. Update y = f(x'), repeat until no improvement found

The oracle encodes:
    O_y |x> = (-1)^{[f(x) < y]} |x>

The diffusion operator amplifies marked states:
    D = 2|+><+| - I

Each round uses O(sqrt(N/M)) iterations where M = #{x : f(x) < y}.

Total complexity: O(sqrt(N)) function evaluations.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


# =============================================================================
# PART A: Manual Grover's Search Implementation
# =============================================================================
# This part builds Grover's algorithm from scratch to demonstrate
# the core mechanism. We use a simple example: searching for a
# specific item in an unstructured database.

def grover_oracle(qc, marked_states, n_qubits):
    """
    Build an oracle that marks specified states by flipping their phase.

    The oracle implements: O|x> = (-1)^{f(x)} |x>
    where f(x) = 1 if x is in marked_states, 0 otherwise.

    See explanation_physicist.md, Section 2.1: Oracle operator.

    Implementation:
        For each marked state |m>, we apply a multi-controlled Z gate
        that flips the phase only when all qubits match the target pattern.

    Args:
        qc: QuantumCircuit to add the oracle to
        marked_states: List of integers representing marked states
        n_qubits: Number of qubits
    """
    for target in marked_states:
        # Convert target to binary and apply X gates to flip 0s
        # This creates |1...1> from the target state
        target_bits = format(target, f'0{n_qubits}b')

        # Flip qubits that should be |0> in the target
        for i, bit in enumerate(target_bits):
            if bit == '0':
                qc.x(i)

        # Multi-controlled Z gate: flip phase of |1...1>
        # MCZ = H on last qubit, then MCX (Toffoli generalized), then H
        if n_qubits == 1:
            qc.z(0)
        elif n_qubits == 2:
            qc.cz(0, 1)
        else:
            # For n >= 3, use multi-controlled Z
            qc.h(n_qubits - 1)
            qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
            qc.h(n_qubits - 1)

        # Undo the X flips
        for i, bit in enumerate(target_bits):
            if bit == '0':
                qc.x(i)


def grover_diffusion(qc, n_qubits):
    """
    Build the Grover diffusion operator D = 2|+><+| - I.

    See explanation_physicist.md, Section 3.2.

    Implementation:
        D = H^n * (2|0><0| - I) * H^n

    The operator (2|0><0| - I) flips the phase of |0...0>:
        (2|0><0| - I)|x> = -|x>  for x != 0...0
        (2|0><0| - I)|0> = +|0>

    Implemented as: X^n -> MCZ -> X^n (flip phase of |1...1>, which
    after X gates corresponds to |0...0>).

    Args:
        qc: QuantumCircuit to add the diffusion to
        n_qubits: Number of qubits
    """
    # Apply H to all qubits
    for i in range(n_qubits):
        qc.h(i)

    # Apply X to all qubits (convert |0...0> to |1...1>)
    for i in range(n_qubits):
        qc.x(i)

    # Multi-controlled Z on |1...1>
    if n_qubits == 1:
        qc.z(0)
    elif n_qubits == 2:
        qc.cz(0, 1)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)

    # Undo X gates
    for i in range(n_qubits):
        qc.x(i)

    # Apply H to all qubits
    for i in range(n_qubits):
        qc.h(i)


def run_grover_search(n_qubits, marked_states, num_iterations=None):
    """
    Run Grover's search algorithm.

    Args:
        n_qubits: Number of qubits
        marked_states: List of marked state indices
        num_iterations: Number of Grover iterations (auto-calculated if None)

    Returns:
        counts: Measurement results
        qc: The circuit
    """
    N = 2**n_qubits
    M = len(marked_states)

    # Optimal number of iterations (see explanation_physicist.md, Section 2.1)
    if num_iterations is None:
        theta = np.arcsin(np.sqrt(M / N))
        num_iterations = max(1, int(np.round(np.pi / (4 * theta) - 0.5)))

    qc = QuantumCircuit(n_qubits, n_qubits)

    # Initialize in uniform superposition
    for i in range(n_qubits):
        qc.h(i)

    # Apply Grover iterations
    for _ in range(num_iterations):
        qc.barrier()
        grover_oracle(qc, marked_states, n_qubits)
        qc.barrier()
        grover_diffusion(qc, n_qubits)

    # Measure
    qc.measure(range(n_qubits), range(n_qubits))

    # Run on simulator
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()

    return counts, qc, num_iterations


# =============================================================================
# PART B: Adaptive Grover Search for Minimum Finding
# =============================================================================
# This implements the Durr-Hoyer algorithm: iteratively use Grover's search
# to find solutions below a decreasing threshold.

def adaptive_grover_minimum(cost_function, n_qubits, max_rounds=10):
    """
    Find the minimum of cost_function using adaptive Grover search.

    This is a classical simulation of the GAS algorithm to demonstrate
    the adaptive threshold mechanism.

    See explanation_physicist.md, Section 2.3: Durr-Hoyer Algorithm.

    Algorithm:
        1. Pick random x, set threshold y = f(x)
        2. Find all x with f(x) < y using Grover
        3. Update threshold with the best found
        4. Repeat until no improvement

    Args:
        cost_function: Function mapping n-bit integers to real values
        n_qubits: Number of qubits (search space = 2^n_qubits)
        max_rounds: Maximum number of adaptive rounds

    Returns:
        best_x: Optimal solution (integer)
        best_cost: Minimum cost value
        history: List of (x, cost, threshold) tuples per round
    """
    N = 2**n_qubits
    history = []

    # Step 1: Start with a random solution
    rng = np.random.default_rng(42)
    best_x = rng.integers(0, N)
    best_cost = cost_function(best_x)
    threshold = best_cost

    print(f"  Initial: x = {best_x} ({format(best_x, f'0{n_qubits}b')}), "
          f"cost = {best_cost}, threshold = {threshold}")
    history.append((best_x, best_cost, threshold))

    for round_num in range(max_rounds):
        # Step 2: Find all states with cost < threshold
        marked = [x for x in range(N) if cost_function(x) < threshold]

        if not marked:
            print(f"  Round {round_num + 1}: No solutions below threshold {threshold}. DONE!")
            break

        # Step 3: Run Grover's search to find a marked state
        print(f"  Round {round_num + 1}: {len(marked)} states below threshold {threshold}")
        counts, _, n_iter = run_grover_search(n_qubits, marked)

        # Find the most common result
        best_measurement = max(counts, key=counts.get)
        found_x = int(best_measurement, 2)
        found_cost = cost_function(found_x)

        print(f"    Grover found: x = {found_x} ({best_measurement}), "
              f"cost = {found_cost}, iterations = {n_iter}")

        # Step 4: Update threshold
        if found_cost < best_cost:
            best_x = found_x
            best_cost = found_cost
            threshold = best_cost
            print(f"    NEW BEST! Updated threshold to {threshold}")

        history.append((found_x, found_cost, threshold))

    return best_x, best_cost, history


def main():
    print("=" * 70)
    print("Grover Adaptive Search for Optimization (Local Simulator)")
    print("=" * 70)

    # =========================================================================
    # PART A: Basic Grover Search Demo
    # =========================================================================

    print("\n" + "=" * 70)
    print("PART A: Basic Grover's Search")
    print("=" * 70)

    n_qubits = 3  # 8 possible states
    marked_states = [5]  # Looking for |101>

    print(f"\nSearch space: {2**n_qubits} states ({n_qubits} qubits)")
    print(f"Marked state: |{format(marked_states[0], f'0{n_qubits}b')}> (index {marked_states[0]})")

    counts, qc, n_iter = run_grover_search(n_qubits, marked_states)

    print(f"Grover iterations: {n_iter}")
    print(f"\nCircuit:")
    print(qc.draw(output="text", fold=80))

    print(f"\nMeasurement results (1024 shots):")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for bitstring, count in sorted_counts:
        marker = " <-- TARGET" if int(bitstring, 2) in marked_states else ""
        bar = "#" * (count // 20)
        print(f"  |{bitstring}> : {count:4d} ({count/1024*100:.1f}%) {bar}{marker}")

    # =========================================================================
    # PART B: Adaptive Grover Search for Optimization
    # =========================================================================

    print("\n" + "=" * 70)
    print("PART B: Adaptive Grover Search for Minimum Finding")
    print("=" * 70)

    # Define a cost function for a 4-qubit problem
    # Cost function: C(x) = a simple nonlinear function
    n_qubits_opt = 4  # 16 possible states

    def cost_function(x):
        """
        Example cost function for 4-bit optimization.

        This represents a simplified QUBO-like objective:
        C(x) = -2*x0 + 3*x1 - x2 + 2*x3 + 4*x0*x1 - 3*x1*x2 + x2*x3

        where x0, x1, x2, x3 are the binary digits of x.
        """
        x0 = (x >> 3) & 1
        x1 = (x >> 2) & 1
        x2 = (x >> 1) & 1
        x3 = x & 1
        return -2*x0 + 3*x1 - x2 + 2*x3 + 4*x0*x1 - 3*x1*x2 + x2*x3

    # Print all costs for reference
    print(f"\nSearch space: {2**n_qubits_opt} states ({n_qubits_opt} qubits)")
    print(f"\nAll possible costs:")
    costs = {}
    for x in range(2**n_qubits_opt):
        c = cost_function(x)
        costs[x] = c
        bs = format(x, f'0{n_qubits_opt}b')
        print(f"  |{bs}> (x={x:2d}): C = {c:3d}")

    min_x = min(costs, key=costs.get)
    min_cost = costs[min_x]
    print(f"\nExact minimum: C({format(min_x, f'0{n_qubits_opt}b')}) = {min_cost}")

    # Run Adaptive Grover Search
    print(f"\n--- Running Adaptive Grover Search ---\n")

    best_x, best_cost, history = adaptive_grover_minimum(
        cost_function, n_qubits_opt, max_rounds=10
    )

    print(f"\n  RESULT: Minimum found at x = {best_x} "
          f"({format(best_x, f'0{n_qubits_opt}b')}), C = {best_cost}")
    print(f"  Exact minimum: C({format(min_x, f'0{n_qubits_opt}b')}) = {min_cost}")
    print(f"  Correct: {'YES' if best_cost == min_cost else 'NO'}")

    # =========================================================================
    # PART C: Visualization
    # =========================================================================

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Plot 1: Grover search measurement probabilities
    states = sorted(counts.keys())
    probs = [counts.get(s, 0) / 1024 for s in states]
    colors = ['green' if int(s, 2) in marked_states else 'skyblue' for s in states]
    axes[0].bar(states, probs, color=colors)
    axes[0].set_xlabel('State', fontsize=12)
    axes[0].set_ylabel('Probability', fontsize=12)
    axes[0].set_title("Grover's Search (3 qubits, target=|101>)", fontsize=13)
    axes[0].tick_params(axis='x', rotation=45)

    # Plot 2: Cost function landscape
    x_vals = list(range(2**n_qubits_opt))
    cost_vals = [costs[x] for x in x_vals]
    labels = [format(x, f'0{n_qubits_opt}b') for x in x_vals]
    bar_colors = ['red' if costs[x] == min_cost else 'lightblue' for x in x_vals]
    axes[1].bar(range(len(x_vals)), cost_vals, color=bar_colors, tick_label=labels)
    axes[1].set_xlabel('State', fontsize=12)
    axes[1].set_ylabel('Cost C(x)', fontsize=12)
    axes[1].set_title('Cost Function Landscape', fontsize=13)
    axes[1].tick_params(axis='x', rotation=90, labelsize=7)
    axes[1].axhline(y=min_cost, color='red', linestyle='--', alpha=0.5)

    # Plot 3: Adaptive threshold convergence
    rounds = range(len(history))
    thresholds = [h[2] for h in history]
    found_costs = [h[1] for h in history]
    axes[2].step(rounds, thresholds, 'b-o', where='post', label='Threshold', linewidth=2)
    axes[2].scatter(rounds, found_costs, color='red', s=80, zorder=5, label='Found cost')
    axes[2].axhline(y=min_cost, color='green', linestyle='--', alpha=0.5, label=f'True min = {min_cost}')
    axes[2].set_xlabel('Round', fontsize=12)
    axes[2].set_ylabel('Cost / Threshold', fontsize=12)
    axes[2].set_title('Adaptive Threshold Convergence', fontsize=13)
    axes[2].legend(fontsize=10)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/03_grover_adaptive_search/grover_results.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/03_grover_adaptive_search/grover_results.png")

    # =========================================================================
    # Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    Grover Adaptive Search demonstrated:

    Part A - Basic Grover's Search:
      - Oracle flips phase of target state
      - Diffusion amplifies target amplitude
      - O(sqrt(N)) iterations to find target

    Part B - Adaptive Minimum Finding:
      - Iteratively lower threshold using Grover search
      - Each round finds solutions below current best
      - Converges to global minimum

    Key insight: Quadratic speedup (sqrt(N) vs N) for
    unstructured optimization problems.

    Practical note: On NISQ devices, the oracle circuit can be
    very deep for real problems. GAS is primarily suited for
    fault-tolerant quantum computers.
    """)


if __name__ == "__main__":
    main()
