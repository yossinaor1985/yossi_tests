"""
Grover Adaptive Search - IBM Production-Ready Implementation
=============================================================

This script demonstrates Grover Adaptive Search using Qiskit's
GroverOptimizer from qiskit_optimization, configured for IBM hardware.

Qiskit Version: 2.4.1

Production considerations:
    - GroverOptimizer handles oracle construction automatically
    - Circuits can be very deep; transpilation is critical
    - Error mitigation is essential due to circuit depth
    - Best suited for small problem instances on NISQ hardware

NOTE: qiskit_optimization 0.7.0 is the last release. For newer
alternatives, see qiskit-addon-opt-mapper.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2 as AerSampler

# Qiskit Optimization imports
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import GroverOptimizer, MinimumEigenOptimizer
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_aer.primitives import EstimatorV2 as AerEstimator

# IBM Runtime imports (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session


def create_qubo_problem():
    """
    Create a QUBO (Quadratic Unconstrained Binary Optimization) problem.

    Problem: Portfolio-like selection
    Minimize: C(x) = -5x_0 + 2x_1 - 3x_2 + 4x_0*x_1 - 2x_1*x_2 + x_0*x_2

    This represents a simplified asset selection problem where:
        - x_i in {0, 1}: include asset i in portfolio or not
        - Linear terms: individual asset returns (negative = good)
        - Quadratic terms: correlations between assets

    Returns:
        QuadraticProgram: The optimization problem
    """
    qp = QuadraticProgram("portfolio_selection")

    # Add binary variables
    qp.binary_var("x0")
    qp.binary_var("x1")
    qp.binary_var("x2")

    # Set objective: minimize
    # Linear terms: -5*x0 + 2*x1 - 3*x2
    # Quadratic terms: 4*x0*x1 - 2*x1*x2 + 1*x0*x2
    qp.minimize(
        linear={"x0": -5, "x1": 2, "x2": -3},
        quadratic={("x0", "x1"): 4, ("x1", "x2"): -2, ("x0", "x2"): 1}
    )

    return qp


def solve_classically(qp):
    """
    Solve the QUBO problem by brute force for verification.

    Args:
        qp: QuadraticProgram

    Returns:
        dict: All solutions and their objective values
    """
    n = qp.get_num_vars()
    results = {}

    for i in range(2**n):
        x = [(i >> bit) & 1 for bit in range(n)]
        obj = qp.objective.evaluate(x)
        results[format(i, f'0{n}b')] = obj

    return results


def run_grover_optimizer_demo(qp):
    """
    Run Qiskit's GroverOptimizer on the QUBO problem.

    GroverOptimizer internally:
        1. Converts the QuadraticProgram to a quantum oracle
        2. Implements the cost function as a reversible circuit
        3. Applies Grover iterations with adaptive thresholding
        4. Returns the optimal solution

    Args:
        qp: QuadraticProgram to solve

    Returns:
        result: Optimization result
    """
    # Number of value qubits determines the precision of cost encoding
    # More value qubits = finer cost resolution, but deeper circuits
    num_value_qubits = 6  # Encodes costs in range [0, 2^6-1]

    grover_optimizer = GroverOptimizer(
        num_value_qubits=num_value_qubits,
        num_iterations=3,    # Max Grover iterations per round
        sampler=AerSampler(),
    )

    result = grover_optimizer.solve(qp)
    return result


def run_qaoa_comparison(qp):
    """
    Run QAOA on the same problem for comparison with Grover.

    This helps illustrate the trade-offs:
        - Grover: exact solution, deeper circuits
        - QAOA: approximate solution, shallower circuits

    Args:
        qp: QuadraticProgram

    Returns:
        result: Optimization result
    """
    estimator = AerEstimator()
    sampler = AerSampler()

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=COBYLA(maxiter=200),
        reps=2,
    )

    optimizer = MinimumEigenOptimizer(qaoa)
    result = optimizer.solve(qp)
    return result


def main():
    print("=" * 70)
    print("Grover Adaptive Search - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Problem Definition
    # =========================================================================

    print("\n--- Step 1: QUBO Problem ---")

    qp = create_qubo_problem()
    print(qp.prettyprint())

    # Classical brute-force solution for verification
    all_solutions = solve_classically(qp)
    print("\nAll solutions (brute force):")
    for bs, obj in sorted(all_solutions.items(), key=lambda x: x[1]):
        print(f"  |{bs}> : C = {obj:.1f}")

    best_bs = min(all_solutions, key=all_solutions.get)
    best_cost = all_solutions[best_bs]
    print(f"\nOptimal: |{best_bs}> with C = {best_cost:.1f}")

    # =========================================================================
    # STEP 2: Grover Optimizer
    # =========================================================================

    print("\n--- Step 2: GroverOptimizer ---")
    print("Running Grover Adaptive Search...")

    try:
        grover_result = run_grover_optimizer_demo(qp)
        print(f"\nGrover result:")
        print(f"  Solution: {grover_result.x}")
        print(f"  Variable values: {dict(zip([v.name for v in qp.variables], grover_result.x))}")
        print(f"  Objective: {grover_result.fval:.4f}")
        print(f"  Status: {grover_result.status}")
        grover_correct = np.isclose(grover_result.fval, best_cost)
        print(f"  Matches exact solution: {grover_correct}")
    except Exception as e:
        print(f"  GroverOptimizer encountered an error: {e}")
        print("  This can happen with complex problems on simulators.")
        print("  Falling back to QAOA comparison only.")
        grover_result = None

    # =========================================================================
    # STEP 3: QAOA Comparison
    # =========================================================================

    print("\n--- Step 3: QAOA Comparison ---")
    print("Running QAOA for comparison...")

    qaoa_result = run_qaoa_comparison(qp)
    print(f"\nQAOA result:")
    print(f"  Solution: {qaoa_result.x}")
    print(f"  Variable values: {dict(zip([v.name for v in qp.variables], qaoa_result.x))}")
    print(f"  Objective: {qaoa_result.fval:.4f}")
    print(f"  Status: {qaoa_result.status}")
    qaoa_correct = np.isclose(qaoa_result.fval, best_cost)
    print(f"  Matches exact solution: {qaoa_correct}")

    # =========================================================================
    # STEP 4: Save Results
    # =========================================================================

    print("\n--- Step 4: Saving Results ---")

    output_dir = "quantum/algorithms/03_grover_adaptive_search/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "Grover Adaptive Search",
        "qiskit_version": "2.4.1",
        "problem": {
            "type": "QUBO",
            "num_variables": qp.get_num_vars(),
            "all_solutions": all_solutions,
            "optimal_solution": best_bs,
            "optimal_value": float(best_cost),
        },
        "grover_result": {
            "solution": grover_result.x.tolist() if grover_result else None,
            "objective": float(grover_result.fval) if grover_result else None,
            "correct": bool(grover_correct) if grover_result else None,
        },
        "qaoa_result": {
            "solution": qaoa_result.x.tolist(),
            "objective": float(qaoa_result.fval),
            "correct": bool(qaoa_correct),
        },
    }

    filepath = os.path.join(output_dir, "grover_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2, default=str)
    print(f"Results saved to {filepath}")

    # =========================================================================
    # Comparison Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("ALGORITHM COMPARISON")
    print("=" * 70)
    print(f"""
    Exact solution:   |{best_bs}> = {best_cost:.1f}

    Grover:           {f"|{''.join(map(str, grover_result.x.astype(int)))}> = {grover_result.fval:.1f}" if grover_result else "N/A"}
    QAOA (p=2):       |{''.join(map(str, qaoa_result.x.astype(int)))}> = {qaoa_result.fval:.1f}

    Trade-offs:
    +------------------+-------------------+-------------------+
    | Property         | Grover            | QAOA              |
    +------------------+-------------------+-------------------+
    | Solution quality | Exact (provable)  | Approximate       |
    | Circuit depth    | Deep (oracle)     | Shallow (ansatz)  |
    | Parameters       | None (parameter-  | 2p (variational)  |
    |                  |  free)            |                   |
    | NISQ suitable    | No (deep circuits)| Yes               |
    | Speedup          | Quadratic (sqrt)  | Heuristic         |
    +------------------+-------------------+-------------------+

    For NISQ devices: QAOA is preferred.
    For fault-tolerant QC: Grover provides provable speedup.
    """)

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("=" * 70)
    print("PRODUCTION DEPLOYMENT NOTES")
    print("=" * 70)
    print("""
    IBM Hardware Considerations for Grover Search:

    1. Circuit Depth: The oracle circuit for real QUBO problems
       can be hundreds of gates deep. Current IBM hardware
       (T1 ~ 100-300 us) limits useful circuit depth to ~100
       two-qubit gates.

    2. Ancilla Qubits: The oracle requires additional qubits
       for arithmetic. A 10-variable QUBO might need 30+ qubits.

    3. Error Mitigation: Due to deep circuits, aggressive
       error mitigation (ZNE, PEC) is needed but adds overhead.

    4. Recommendation: For near-term applications, prefer
       QAOA or VQE. Reserve Grover search for:
       - Small instances (n <= 5)
       - Problems where exact solutions are critical
       - Future fault-tolerant hardware
    """)


if __name__ == "__main__":
    main()
