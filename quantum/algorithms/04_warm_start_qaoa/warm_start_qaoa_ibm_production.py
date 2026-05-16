"""
Warm-Start QAOA - IBM Production-Ready Implementation
=======================================================

This script demonstrates production Warm-Start QAOA for MaxCut,
using Qiskit's built-in warm-start capabilities.

Qiskit Version: 2.4.1

For real hardware deployment:
    - Warm-starting is especially valuable on noisy hardware because
      it reduces the number of optimization iterations needed
    - The initial state preparation adds minimal circuit overhead
      (only n single-qubit gates)
    - Combined with error mitigation, WS-QAOA often outperforms
      standard QAOA at equivalent circuit depth

NOTE: Real hardware execution is commented out.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_aer.primitives import EstimatorV2 as AerEstimator, SamplerV2 as AerSampler
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer, WarmStartQAOAOptimizer

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, SamplerV2, Session


def create_maxcut_quadratic_program(edges, num_nodes):
    """
    Create a MaxCut QUBO using qiskit_optimization's QuadraticProgram.

    This allows us to use Qiskit's built-in WarmStartQAOAOptimizer
    which handles the classical relaxation and warm-starting automatically.

    Returns:
        QuadraticProgram: The MaxCut problem
    """
    qp = QuadraticProgram("maxcut")

    # Add binary variables
    for i in range(num_nodes):
        qp.binary_var(f"x{i}")

    # MaxCut objective: maximize sum_{(i,j) in E} (x_i + x_j - 2*x_i*x_j)
    # Equivalently minimize: -sum_{(i,j) in E} (x_i + x_j - 2*x_i*x_j)
    linear = {}
    quadratic = {}

    for i, j in edges:
        linear[f"x{i}"] = linear.get(f"x{i}", 0) - 1
        linear[f"x{j}"] = linear.get(f"x{j}", 0) - 1
        quadratic[(f"x{i}", f"x{j}")] = 2

    qp.minimize(linear=linear, quadratic=quadratic)
    return qp


def run_production():
    print("=" * 70)
    print("Warm-Start QAOA - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # Configuration
    # =========================================================================

    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    num_nodes = 6
    QAOA_DEPTH = 2

    print(f"\nGraph: {num_nodes} nodes, {len(edges)} edges")
    print(f"QAOA depth: {QAOA_DEPTH}")

    # =========================================================================
    # STEP 1: Create the optimization problem
    # =========================================================================

    print("\n--- Step 1: Problem Formulation ---")

    qp = create_maxcut_quadratic_program(edges, num_nodes)
    print(qp.prettyprint())

    # =========================================================================
    # STEP 2: Standard QAOA (baseline)
    # =========================================================================

    print("\n--- Step 2: Standard QAOA (baseline) ---")

    estimator = AerEstimator()
    sampler = AerSampler()

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=COBYLA(maxiter=300),
        reps=QAOA_DEPTH,
    )

    std_optimizer = MinimumEigenOptimizer(qaoa)
    std_result = std_optimizer.solve(qp)

    print(f"Standard QAOA result:")
    print(f"  Solution: {std_result.x}")
    print(f"  Variables: {dict(zip([v.name for v in qp.variables], std_result.x))}")
    print(f"  Objective: {std_result.fval:.4f}")

    # =========================================================================
    # STEP 3: Warm-Start QAOA
    # =========================================================================

    print("\n--- Step 3: Warm-Start QAOA ---")

    # Qiskit's WarmStartQAOAOptimizer handles:
    #   1. Solving the continuous relaxation of the QUBO
    #   2. Computing the warm-start angles theta_i
    #   3. Constructing the custom initial state and mixer
    #   4. Running QAOA with the warm-start configuration

    qaoa_ws = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=COBYLA(maxiter=300),
        reps=QAOA_DEPTH,
    )

    ws_optimizer = WarmStartQAOAOptimizer(
        pre_solver=MinimumEigenOptimizer(
            QAOA(
                estimator=estimator,
                sampler=sampler,
                optimizer=COBYLA(maxiter=100),
                reps=1,
            )
        ),
        relax_for_pre_solver=True,  # Solve relaxation first
        qaoa=qaoa_ws,
        epsilon=0.25,  # Relaxation rounding threshold
    )

    ws_result = ws_optimizer.solve(qp)

    print(f"Warm-Start QAOA result:")
    print(f"  Solution: {ws_result.x}")
    print(f"  Variables: {dict(zip([v.name for v in qp.variables], ws_result.x))}")
    print(f"  Objective: {ws_result.fval:.4f}")

    # =========================================================================
    # STEP 4: Compare results
    # =========================================================================

    print("\n--- Step 4: Comparison ---")

    # Compute actual MaxCut values
    def maxcut_value(x, edges):
        return sum(1 for i, j in edges if x[i] != x[j])

    std_cut = maxcut_value(std_result.x.astype(int), edges)
    ws_cut = maxcut_value(ws_result.x.astype(int), edges)

    # Exact solution
    max_cut = 0
    for i in range(2**num_nodes):
        bs = [int(b) for b in format(i, f'0{num_nodes}b')]
        cut = maxcut_value(bs, edges)
        max_cut = max(max_cut, cut)

    print(f"\n  Exact MaxCut: {max_cut}")
    print(f"  Standard QAOA cut: {std_cut} (ratio = {std_cut/max_cut:.4f})")
    print(f"  Warm-Start QAOA cut: {ws_cut} (ratio = {ws_cut/max_cut:.4f})")

    # =========================================================================
    # STEP 5: Save Results
    # =========================================================================

    output_dir = "quantum/algorithms/04_warm_start_qaoa/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "Warm-Start QAOA",
        "qiskit_version": "2.4.1",
        "problem": {
            "type": "MaxCut",
            "num_nodes": num_nodes,
            "edges": edges,
            "exact_maxcut": max_cut,
        },
        "standard_qaoa": {
            "solution": std_result.x.tolist(),
            "objective": float(std_result.fval),
            "cut_value": int(std_cut),
        },
        "warmstart_qaoa": {
            "solution": ws_result.x.tolist(),
            "objective": float(ws_result.fval),
            "cut_value": int(ws_cut),
        },
    }

    filepath = os.path.join(output_dir, "warmstart_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"\nResults saved to {filepath}")

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print("""
    Warm-Start QAOA on IBM Hardware:

    1. Classical Pre-solving:
       - Run LP/SDP relaxation on classical hardware first
       - Use WarmStartQAOAOptimizer for automatic handling
       - epsilon parameter controls rounding threshold

    2. Circuit Overhead:
       - Initial state: n R_Y gates (negligible vs standard H gates)
       - Custom mixer: 2n extra R_Z gates per layer (minimal)
       - Total overhead: ~3n single-qubit gates (trivial on hardware)

    3. When to Use:
       - Low-depth QAOA (p=1,2): maximum benefit
       - Large problem instances: classical heuristic provides good starting point
       - Noisy hardware: fewer iterations = fewer error-prone circuit executions

    4. Production Pipeline:
       Classical solver -> Warm-start angles -> WS-QAOA circuit ->
       Transpile -> Execute on IBM backend -> Post-process results

    5. Error Mitigation:
       Same as standard QAOA: TREX, dynamical decoupling, Pauli twirling
    """)


if __name__ == "__main__":
    run_production()
