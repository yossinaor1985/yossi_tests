"""
ADMM - IBM Production-Ready Implementation
=============================================

Production ADMM for constrained portfolio optimization on IBM Quantum hardware.

Qiskit Version: 2.4.1

Production Considerations:
    - ADMM calls the quantum solver (QAOA) multiple times (once per outer iteration)
    - Each QAOA call involves its own variational optimization loop
    - Total quantum circuit executions = (ADMM iters) * (QAOA optimizer iters) * (shots)
    - Session management is critical for cost control on IBM hardware
    - Error mitigation should be applied at the QAOA level (inside ADMM)
    - The QUBO subproblem changes at each ADMM iteration (different coefficients)
    - Warm-starting QAOA parameters between ADMM iterations can reduce cost

Architecture:
    ADMM Outer Loop (classical)
        |
        +-- Iteration k:
        |       |
        |       +-- Build QUBO_k(x; z^k, lambda^k)    [classical]
        |       +-- Solve QUBO_k with QAOA              [QUANTUM]
        |       +-- Solve continuous QP for z^{k+1}     [classical]
        |       +-- Update lambda^{k+1}                 [classical]
        |       +-- Check convergence                   [classical]
        |
        +-- Return (x*, z*, lambda*)
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2 as AerEstimator, SamplerV2 as AerSampler
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import (
    ADMMOptimizer,
    ADMMParameters,
    MinimumEigenOptimizer,
)
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms.minimum_eigensolvers import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA, SPSA

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, SamplerV2, Session


def create_production_portfolio(num_assets=4, budget=2):
    """
    Create a constrained portfolio problem for production use.

    See admm_local.py for detailed documentation of the problem formulation
    and explanation_physicist.md, Section 5 for the mathematical background.

    This is identical to the local version but with production-grade
    parameter choices and documentation.

    Args:
        num_assets: Number of investable assets
        budget: Number of assets to select

    Returns:
        QuadraticProgram: Constrained portfolio optimization problem
        dict: Problem metadata
    """
    # Covariance matrix (from historical price data in production)
    sigma = np.array([
        [0.50, 0.10, -0.05, 0.02],
        [0.10, 0.40, 0.08, -0.03],
        [-0.05, 0.08, 0.60, 0.10],
        [0.02, -0.03, 0.10, 0.30],
    ])

    # Expected returns
    mu = np.array([0.12, 0.10, 0.07, 0.15])

    qp = QuadraticProgram("portfolio_production")

    for i in range(num_assets):
        qp.binary_var(f"x{i}")

    # Objective: minimize risk - return = x^T Sigma x - mu^T x
    linear = {f"x{i}": -mu[i] for i in range(num_assets)}
    quadratic = {}
    for i in range(num_assets):
        for j in range(i, num_assets):
            if i == j:
                quadratic[(f"x{i}", f"x{j}")] = sigma[i, j]
            else:
                quadratic[(f"x{i}", f"x{j}")] = 2 * sigma[i, j]

    qp.minimize(linear=linear, quadratic=quadratic)

    # Budget equality constraint
    qp.linear_constraint(
        linear={f"x{i}": 1.0 for i in range(num_assets)},
        sense="==",
        rhs=budget,
        name="budget",
    )

    metadata = {
        "num_assets": num_assets,
        "budget": budget,
        "covariance": sigma.tolist(),
        "expected_returns": mu.tolist(),
        "asset_names": [f"Asset_{i}" for i in range(num_assets)],
    }

    return qp, metadata


def compute_exact_solution(qp, metadata):
    """
    Compute the exact solution by enumerating all feasible portfolios.

    Production note: For small problems (n <= 20), this serves as
    validation. For larger problems, use classical solvers as reference.

    Args:
        qp: QuadraticProgram
        metadata: Problem metadata

    Returns:
        dict: Exact solution details
    """
    n = metadata["num_assets"]
    budget = metadata["budget"]
    sigma = np.array(metadata["covariance"])
    mu = np.array(metadata["expected_returns"])

    best_obj = float("inf")
    best_x = None
    all_feasible = []

    for idx in range(2**n):
        x = np.array([int(b) for b in format(idx, f"0{n}b")])
        if x.sum() != budget:
            continue

        obj = float(x @ sigma @ x - mu @ x)
        all_feasible.append({
            "x": x.tolist(),
            "objective": obj,
            "assets": [i for i in range(n) if x[i] == 1],
        })
        if obj < best_obj:
            best_obj = obj
            best_x = x.tolist()

    return {
        "optimal_x": best_x,
        "optimal_objective": best_obj,
        "num_feasible": len(all_feasible),
        "all_feasible": all_feasible,
    }


def run_admm_simulator(qp, admm_config):
    """
    Run ADMM with QAOA on the Aer simulator.

    This mirrors the production flow but uses the local simulator
    instead of IBM hardware.

    Args:
        qp: QuadraticProgram
        admm_config: Dict of ADMM and QAOA configuration parameters

    Returns:
        dict: Results including solution, objective, timing
    """
    start_time = datetime.now()

    # ADMM parameters
    params = ADMMParameters(
        rho_initial=admm_config["rho_initial"],
        factor_c=admm_config["factor_c"],
        beta=admm_config["beta"],
        maxiter=admm_config["maxiter"],
        tol=admm_config["tol"],
        three_block=admm_config.get("three_block", True),
    )

    # QAOA for the QUBO subproblem
    estimator = AerEstimator()
    sampler = AerSampler()

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=COBYLA(maxiter=admm_config["qaoa_maxiter"]),
        reps=admm_config["qaoa_reps"],
    )
    qubo_optimizer = MinimumEigenOptimizer(qaoa)

    # ADMM optimizer
    admm = ADMMOptimizer(
        qubo_optimizer=qubo_optimizer,
        continuous_optimizer=None,
        params=params,
    )

    result = admm.solve(qp)
    end_time = datetime.now()

    return {
        "x": result.x.tolist() if hasattr(result.x, "tolist") else list(result.x),
        "objective": float(result.fval),
        "budget_used": float(sum(result.x)),
        "variables": {
            v.name: float(result.x[i]) for i, v in enumerate(qp.variables)
        },
        "elapsed_seconds": (end_time - start_time).total_seconds(),
    }


def run_admm_exact_reference(qp, admm_config):
    """
    Run ADMM with exact eigensolver as upper bound on quality.

    This shows the best ADMM can do when the QUBO subproblem is
    solved exactly (no quantum noise or QAOA approximation error).

    Args:
        qp: QuadraticProgram
        admm_config: ADMM configuration

    Returns:
        dict: Reference results
    """
    params = ADMMParameters(
        rho_initial=admm_config["rho_initial"],
        factor_c=admm_config["factor_c"],
        beta=admm_config["beta"],
        maxiter=admm_config["maxiter"],
        tol=admm_config["tol"],
        three_block=admm_config.get("three_block", True),
    )

    exact_solver = NumPyMinimumEigensolver()
    exact_optimizer = MinimumEigenOptimizer(exact_solver)

    admm = ADMMOptimizer(
        qubo_optimizer=exact_optimizer,
        continuous_optimizer=None,
        params=params,
    )

    result = admm.solve(qp)

    return {
        "x": result.x.tolist() if hasattr(result.x, "tolist") else list(result.x),
        "objective": float(result.fval),
        "budget_used": float(sum(result.x)),
    }


def run_production():
    print("=" * 70)
    print("ADMM - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # Configuration
    # =========================================================================

    NUM_ASSETS = 4
    BUDGET = 2

    # ADMM configuration
    # See explanation_physicist.md, Section 4.4 for parameter guidance
    admm_config = {
        "rho_initial": 1000,     # Initial augmented Lagrangian penalty
        "factor_c": 10,          # Penalty update factor
        "beta": 1000,            # Equality constraint penalty
        "maxiter": 100,          # Max ADMM outer iterations
        "tol": 1e-6,             # Convergence tolerance
        "three_block": True,     # Use 3-block ADMM
        "qaoa_reps": 2,          # QAOA circuit depth
        "qaoa_maxiter": 200,     # QAOA optimizer iterations
    }

    print(f"\nPortfolio: {NUM_ASSETS} assets, budget = {BUDGET}")
    print(f"ADMM config: rho={admm_config['rho_initial']}, "
          f"maxiter={admm_config['maxiter']}, tol={admm_config['tol']}")
    print(f"QAOA config: reps={admm_config['qaoa_reps']}, "
          f"maxiter={admm_config['qaoa_maxiter']}")

    # =========================================================================
    # STEP 1: Problem Formulation
    # =========================================================================

    print("\n--- Step 1: Problem Formulation ---")

    qp, metadata = create_production_portfolio(NUM_ASSETS, BUDGET)
    print(qp.prettyprint())

    # =========================================================================
    # STEP 2: Exact Reference Solution
    # =========================================================================

    print("\n--- Step 2: Exact Reference Solution ---")

    exact = compute_exact_solution(qp, metadata)
    print(f"Optimal portfolio: assets {exact['optimal_x']}")
    print(f"Optimal objective: {exact['optimal_objective']:.6f}")
    print(f"Number of feasible portfolios: {exact['num_feasible']}")

    for sol in exact["all_feasible"]:
        marker = " <-- OPTIMAL" if sol["objective"] == exact["optimal_objective"] else ""
        assets_str = ", ".join(f"A{i}" for i in sol["assets"])
        print(f"  [{assets_str:>8s}]: objective = {sol['objective']:.4f}{marker}")

    # =========================================================================
    # STEP 3: ADMM with QAOA (Simulator)
    # =========================================================================

    print("\n--- Step 3: ADMM with QAOA (Aer Simulator) ---")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL IBM HARDWARE:
    #
    # service = QiskitRuntimeService(
    #     channel="ibm_quantum",
    #     token="YOUR_IBM_QUANTUM_TOKEN",
    # )
    # backend = service.least_busy(
    #     simulator=False,
    #     min_num_qubits=NUM_ASSETS,
    # )
    # print(f"Using backend: {backend.name}")
    #
    # # For production, use a Session to batch the QAOA calls within ADMM:
    # # Each ADMM iteration calls QAOA once, and QAOA itself runs many
    # # circuit evaluations. A Session keeps these on the same backend.
    # #
    # # NOTE: The current qiskit_optimization ADMMOptimizer does not
    # # natively support Sessions. For production, you would need to:
    # # 1. Use a custom QAOA wrapper that manages the Session
    # # 2. Or manually implement the ADMM loop with Session control
    # #
    # # with Session(service=service, backend=backend) as session:
    # #     estimator = EstimatorV2(
    # #         session=session,
    # #         options={
    # #             "resilience_level": 1,  # TREX error mitigation
    # #             "optimization_level": 3,  # Aggressive transpilation
    # #         },
    # #     )
    # #     sampler = SamplerV2(session=session)
    # #     # ... build QAOA and ADMM with these primitives ...
    #
    # # Error mitigation options for the QAOA subroutine:
    # # - resilience_level=0: No mitigation (fastest)
    # # - resilience_level=1: TREX (readout error mitigation)
    # # - resilience_level=2: ZNE (zero-noise extrapolation)
    # #
    # # For ADMM, resilience_level=1 is recommended because:
    # # - Each ADMM iteration solves a different QUBO
    # # - ZNE (level 2) is expensive and the QUBO changes each iteration
    # # - TREX (level 1) provides good noise reduction at low cost
    # -------------------------------------------------------------------------

    admm_result = run_admm_simulator(qp, admm_config)

    print(f"\n  ADMM + QAOA result:")
    print(f"    Solution: {admm_result['x']}")
    print(f"    Variables: {admm_result['variables']}")
    print(f"    Objective: {admm_result['objective']:.6f}")
    print(f"    Budget used: {admm_result['budget_used']:.0f} (required: {BUDGET})")
    print(f"    Feasible: {'YES' if admm_result['budget_used'] == BUDGET else 'NO'}")
    print(f"    Time: {admm_result['elapsed_seconds']:.1f}s")

    # =========================================================================
    # STEP 4: ADMM with Exact Solver (Quality Upper Bound)
    # =========================================================================

    print("\n--- Step 4: ADMM with Exact Solver (reference) ---")

    exact_admm = run_admm_exact_reference(qp, admm_config)

    print(f"  ADMM + Exact result:")
    print(f"    Solution: {exact_admm['x']}")
    print(f"    Objective: {exact_admm['objective']:.6f}")
    print(f"    Feasible: {'YES' if exact_admm['budget_used'] == BUDGET else 'NO'}")

    # =========================================================================
    # STEP 5: Save Results
    # =========================================================================

    print("\n--- Step 5: Saving Results ---")

    output_dir = "quantum/algorithms/07_ADMM/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "ADMM (Quantum-Classical Hybrid)",
        "qiskit_version": "2.4.1",
        "problem": {
            "type": "Constrained Portfolio Optimization",
            "num_assets": NUM_ASSETS,
            "budget": BUDGET,
            "covariance": metadata["covariance"],
            "expected_returns": metadata["expected_returns"],
        },
        "admm_config": admm_config,
        "exact_solution": {
            "optimal_x": exact["optimal_x"],
            "optimal_objective": exact["optimal_objective"],
            "num_feasible": exact["num_feasible"],
        },
        "admm_qaoa_result": {
            "solution": admm_result["x"],
            "objective": admm_result["objective"],
            "budget_used": admm_result["budget_used"],
            "feasible": admm_result["budget_used"] == BUDGET,
            "elapsed_seconds": admm_result["elapsed_seconds"],
        },
        "admm_exact_result": {
            "solution": exact_admm["x"],
            "objective": exact_admm["objective"],
            "feasible": exact_admm["budget_used"] == BUDGET,
        },
        "hardware_config": {
            "backend": "AerSimulator (local)",
            "note": "Uncomment IBM Runtime section for real hardware",
        },
    }

    filepath = os.path.join(output_dir, "admm_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"Results saved to {filepath}")

    # =========================================================================
    # Production Notes & Deployment Checklist
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print(f"""
    ADMM on IBM Quantum Hardware:

    1. Resource Estimation:
       - ADMM outer iterations: typically 5-50
       - QAOA evaluations per ADMM iteration: ~200 (COBYLA budget)
       - Shots per QAOA evaluation: 1024-8192
       - Total quantum circuits: ~{admm_config['maxiter']} * {admm_config['qaoa_maxiter']} * shots
       - IMPORTANT: This can be expensive. Use Sessions for batch pricing.

    2. Session Management:
       - Use a single Session for all ADMM iterations
       - Each ADMM iteration calls QAOA, which runs many circuits
       - Session keeps circuits on the same backend (no re-queuing)
       - Set session max_time based on expected total runtime

    3. Error Mitigation Strategy:
       - Use resilience_level=1 (TREX) for the QAOA subroutine
       - Avoid resilience_level=2 (ZNE) due to high circuit overhead
         and the fact that each ADMM iteration solves a different QUBO
       - Consider dynamical decoupling for idle qubits during ZZ gates

    4. QAOA Configuration for ADMM:
       - Use moderate depth (reps=1-2) to limit circuit noise
       - COBYLA optimizer: maxiter=100-200 per ADMM iteration
       - SPSA is an alternative if noise is significant (hardware)
       - Consider warm-starting QAOA from previous ADMM iteration's params

    5. ADMM Parameter Tuning:
       - rho_initial: start with 1000, adjust based on constraint residuals
       - factor_c: 10 is a good default (multiplier for rho updates)
       - beta: should be comparable to rho_initial
       - tol: 1e-4 to 1e-6 depending on required precision
       - maxiter: 50-100 (ADMM usually converges faster)

    6. Scaling Considerations:
       - Number of qubits = number of binary variables
       - Continuous variables are handled classically (no qubit cost)
       - For n > 20 binary variables, QAOA subroutine becomes impractical
       - Consider quantum annealing (D-Wave) for larger QUBO subproblems

    7. Deployment Checklist:
       [ ] Verify problem formulation (constraints, objective)
       [ ] Test with AerSimulator first (this script)
       [ ] Validate against exact solution for small instances
       [ ] Estimate total circuit count and cost
       [ ] Set up QiskitRuntimeService with production token
       [ ] Configure Session with appropriate max_time
       [ ] Set error mitigation (resilience_level=1)
       [ ] Run on hardware and compare with simulator results
       [ ] Save results to JSON for audit trail
       [ ] Monitor convergence (primal/dual residuals)
    """)


if __name__ == "__main__":
    run_production()
