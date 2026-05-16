"""
ADMM (Alternating Direction Method of Multipliers) - Local Simulator
=====================================================================

This script demonstrates ADMM for constrained quantum optimization,
comparing it with pure QAOA on a portfolio optimization problem with
a budget constraint.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
ADMM decomposes a constrained optimization problem into:
    1. A QUBO subproblem (binary variables) -> solved on quantum hardware
    2. A continuous subproblem (slack/continuous vars) -> solved classically
    3. A dual update step -> adjusts Lagrange multipliers

The augmented Lagrangian:
    L_rho(x, z, lambda) = f(x) + g(z) + lambda^T(Ax + Bz - c) + (rho/2)||Ax + Bz - c||^2

At each iteration:
    x^{k+1} = argmin_x QUBO(x; z^k, lambda^k)    [QUANTUM: QAOA/VQE]
    z^{k+1} = argmin_z QP(z; x^{k+1}, lambda^k)   [CLASSICAL: convex QP]
    lambda^{k+1} = lambda^k + rho*(Ax^{k+1} + Bz^{k+1} - c)  [DUAL UPDATE]

Key advantage: constraints are handled via the ADMM decomposition rather
than being encoded as large penalty terms in the QUBO, which would require
careful penalty weight tuning and degrade solution quality.

See explanation_physicist.md, Sections 3 and 5 for the full derivation
and worked example.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer import AerSimulator
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import (
    ADMMOptimizer,
    ADMMParameters,
    MinimumEigenOptimizer,
)
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.translators import to_ising
from qiskit_algorithms.minimum_eigensolvers import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer.primitives import EstimatorV2 as AerEstimator, SamplerV2 as AerSampler


def create_portfolio_problem(num_assets=4, budget=2):
    """
    Create a constrained portfolio optimization problem.

    See explanation_physicist.md, Section 5.1.

    Problem:
        minimize    x^T Sigma x - mu^T x     (risk - return)
        subject to  sum(x) = budget           (invest in exactly 'budget' assets)
                    x in {0, 1}^n             (binary: invest or not)

    This problem has:
        - A quadratic objective (risk-return trade-off)
        - An equality constraint (budget constraint)
        - Binary variables (invest or not in each asset)

    The budget constraint makes this unsuitable for direct QAOA
    without penalty encoding. ADMM handles this naturally.

    Args:
        num_assets: Number of assets (qubits)
        budget: Number of assets to invest in

    Returns:
        QuadraticProgram: The portfolio optimization problem
        dict: Problem metadata (covariance, returns, etc.)
    """
    # Covariance matrix (risk correlations between assets)
    # See explanation_physicist.md, Section 5.1 for these values
    sigma = np.array([
        [0.50, 0.10, -0.05, 0.02],
        [0.10, 0.40, 0.08, -0.03],
        [-0.05, 0.08, 0.60, 0.10],
        [0.02, -0.03, 0.10, 0.30],
    ])

    # Expected returns for each asset
    mu = np.array([0.12, 0.10, 0.07, 0.15])

    # Build the QuadraticProgram
    qp = QuadraticProgram("portfolio_with_budget")

    # Add binary decision variables: x_i = 1 if we invest in asset i
    for i in range(num_assets):
        qp.binary_var(f"x{i}")

    # Objective: minimize x^T Sigma x - mu^T x
    # Linear coefficients: -mu (we want to maximize return, so minimize -return)
    linear = {f"x{i}": -mu[i] for i in range(num_assets)}

    # Quadratic coefficients: Sigma (risk/covariance)
    quadratic = {}
    for i in range(num_assets):
        for j in range(i, num_assets):
            if i == j:
                quadratic[(f"x{i}", f"x{j}")] = sigma[i, j]
            else:
                # Off-diagonal: factor of 2 because qiskit uses
                # sum_{i<j} q_{ij} x_i x_j (not the full symmetric form)
                quadratic[(f"x{i}", f"x{j}")] = 2 * sigma[i, j]

    qp.minimize(linear=linear, quadratic=quadratic)

    # Budget constraint: sum(x_i) = budget
    # This is the KEY constraint that ADMM handles naturally
    constraint_linear = {f"x{i}": 1.0 for i in range(num_assets)}
    qp.linear_constraint(
        linear=constraint_linear,
        sense="==",
        rhs=budget,
        name="budget",
    )

    metadata = {
        "num_assets": num_assets,
        "budget": budget,
        "covariance": sigma.tolist(),
        "expected_returns": mu.tolist(),
    }

    return qp, metadata


def solve_brute_force(qp, metadata):
    """
    Solve the portfolio problem by brute force (enumerate all feasible solutions).

    For n=4, budget=2: there are C(4,2)=6 feasible portfolios.

    See explanation_physicist.md, Section 5.4 for the verification table.

    Args:
        qp: QuadraticProgram
        metadata: Problem metadata

    Returns:
        dict: All feasible solutions with their objective values
        tuple: (best_solution, best_objective)
    """
    n = metadata["num_assets"]
    budget = metadata["budget"]
    sigma = np.array(metadata["covariance"])
    mu = np.array(metadata["expected_returns"])

    feasible = {}
    best_obj = float("inf")
    best_sol = None

    for idx in range(2**n):
        x = np.array([int(b) for b in format(idx, f"0{n}b")])

        # Check budget constraint
        if x.sum() != budget:
            continue

        # Compute objective: x^T Sigma x - mu^T x
        risk = x @ sigma @ x
        ret = mu @ x
        obj = risk - ret

        bitstring = "".join(str(int(b)) for b in x)
        assets = [f"A{i}" for i in range(n) if x[i] == 1]
        feasible[bitstring] = {
            "x": x.tolist(),
            "risk": float(risk),
            "return": float(ret),
            "objective": float(obj),
            "assets": assets,
        }

        if obj < best_obj:
            best_obj = obj
            best_sol = bitstring

    return feasible, (best_sol, best_obj)


def solve_with_admm(qp, rho_initial=1000, max_iter=100, tol=1e-6):
    """
    Solve the constrained portfolio problem using ADMM with a quantum subroutine.

    See explanation_physicist.md, Section 3.4 for the complete algorithm.

    ADMM decomposes the problem as:
        - Binary subproblem (QUBO): solved by QAOA on the quantum simulator
        - Continuous subproblem: solved by a classical optimizer
        - Dual update: gradient ascent on Lagrange multipliers

    The QUBO at each ADMM iteration is:
        Q_eff = Q + (rho/2) A^T A
        q_eff = q + A^T lambda^k + rho * A^T (Bz^k - b)

    See explanation_physicist.md, Section 3.2 for how the QUBO is constructed.

    Args:
        qp: QuadraticProgram (constrained)
        rho_initial: Initial penalty parameter (see Section 4.4)
        max_iter: Maximum ADMM iterations
        tol: Convergence tolerance

    Returns:
        result: ADMMOptimizationResult
        params: ADMMParameters used
    """
    # Configure ADMM parameters
    # See explanation_physicist.md, Section 4.4 for parameter selection
    params = ADMMParameters(
        rho_initial=rho_initial,    # Penalty weight for constraint violation
        factor_c=10,                # Factor to update penalty (rho *= factor_c)
        beta=1000,                  # Penalty for equality constraints
        maxiter=max_iter,           # Maximum outer ADMM iterations
        tol=tol,                    # Convergence tolerance on residuals
        three_block=True,           # Use 3-block ADMM variant
    )

    # Quantum solver for the QUBO subproblem (Step 1 in the algorithm)
    # At each ADMM iteration, the binary subproblem is a QUBO that
    # gets solved by QAOA on the quantum simulator.
    estimator = AerEstimator()
    sampler = AerSampler()

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=COBYLA(maxiter=200),
        reps=2,  # QAOA depth p=2
    )
    qubo_optimizer = MinimumEigenOptimizer(qaoa)

    # Create the ADMM optimizer
    # This orchestrates the outer ADMM loop:
    #   1. Calls qubo_optimizer for the binary subproblem (quantum step)
    #   2. Solves the continuous subproblem internally (classical step)
    #   3. Updates dual variables (dual step)
    admm = ADMMOptimizer(
        qubo_optimizer=qubo_optimizer,
        continuous_optimizer=None,  # Uses default internal solver
        params=params,
    )

    # Solve the problem
    result = admm.solve(qp)

    return result, params


def solve_with_qaoa_penalty(qp, penalty_weight=10.0):
    """
    Solve the problem with pure QAOA using penalty encoding for constraints.

    This is the alternative to ADMM: encode constraints directly as
    penalty terms in the QUBO. The objective becomes:

        minimize  x^T Sigma x - mu^T x + penalty * (sum(x) - budget)^2

    The penalty weight must be large enough to enforce the constraint,
    but too large a penalty distorts the optimization landscape.

    See explanation_physicist.md, Section 6.2 for comparison.

    Args:
        qp: QuadraticProgram (constrained)
        penalty_weight: Weight for the penalty term

    Returns:
        result: MinimumEigenOptimizationResult
    """
    # Convert the constrained QP to a QUBO using penalty encoding
    converter = QuadraticProgramToQubo(penalty=penalty_weight)
    qubo = converter.convert(qp)

    # Solve with QAOA
    estimator = AerEstimator()
    sampler = AerSampler()

    qaoa = QAOA(
        estimator=estimator,
        sampler=sampler,
        optimizer=COBYLA(maxiter=300),
        reps=2,
    )
    optimizer = MinimumEigenOptimizer(qaoa)
    result = optimizer.solve(qubo)

    # Interpret the result back in the original problem space
    original_result = converter.interpret(result)
    return original_result


def solve_with_numpy_exact(qp):
    """
    Solve using NumPy exact eigensolver (for reference).

    This gives the exact quantum-optimal solution as a baseline.
    """
    exact_solver = NumPyMinimumEigensolver()
    exact_optimizer = MinimumEigenOptimizer(exact_solver)

    # ADMM with exact solver for the QUBO subproblem
    params = ADMMParameters(
        rho_initial=1000,
        factor_c=10,
        beta=1000,
        maxiter=100,
        tol=1e-6,
        three_block=True,
    )

    admm_exact = ADMMOptimizer(
        qubo_optimizer=exact_optimizer,
        continuous_optimizer=None,
        params=params,
    )

    return admm_exact.solve(qp)


def main():
    print("=" * 70)
    print("ADMM - Constrained Quantum Optimization (Local Simulator)")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Problem Setup
    # =========================================================================

    print("\n--- Step 1: Portfolio Optimization Problem ---")

    qp, metadata = create_portfolio_problem(num_assets=4, budget=2)
    print(f"Assets: {metadata['num_assets']}")
    print(f"Budget: invest in exactly {metadata['budget']} assets")
    print(f"Expected returns: {metadata['expected_returns']}")

    print(f"\nProblem formulation:")
    print(qp.prettyprint())

    # =========================================================================
    # STEP 2: Brute Force Reference Solution
    # =========================================================================

    print("\n--- Step 2: Brute Force (all feasible portfolios) ---")

    feasible, (best_sol, best_obj) = solve_brute_force(qp, metadata)

    print(f"\nAll feasible portfolios (budget = {metadata['budget']}):")
    print(f"{'Portfolio':<12} {'Assets':<12} {'Risk':>8} {'Return':>8} {'Objective':>10}")
    print("-" * 55)
    for bs, info in sorted(feasible.items(), key=lambda x: x[1]["objective"]):
        marker = " <-- OPTIMAL" if bs == best_sol else ""
        print(
            f"|{bs}>      {str(info['assets']):>12s}  "
            f"{info['risk']:8.4f} {info['return']:8.4f} {info['objective']:10.4f}{marker}"
        )

    print(f"\nExact optimal: |{best_sol}> with objective = {best_obj:.4f}")

    # =========================================================================
    # STEP 3: ADMM with QAOA (quantum subroutine)
    # =========================================================================

    print("\n--- Step 3: ADMM with QAOA ---")
    print("  (ADMM decomposes the constrained problem into QUBO subproblems)")
    print("  (Each QUBO is solved by QAOA on the Aer simulator)")

    admm_result, admm_params = solve_with_admm(qp)

    admm_x = admm_result.x
    admm_obj = admm_result.fval
    admm_vars = {v.name: admm_x[i] for i, v in enumerate(qp.variables)}
    admm_budget = sum(admm_x)

    print(f"\n  ADMM + QAOA result:")
    print(f"    Solution: {admm_x}")
    print(f"    Variables: {admm_vars}")
    print(f"    Objective: {admm_obj:.4f}")
    print(f"    Budget used: {admm_budget:.0f} (required: {metadata['budget']})")
    print(f"    Constraint satisfied: {'YES' if admm_budget == metadata['budget'] else 'NO'}")

    # =========================================================================
    # STEP 4: ADMM with Exact Solver (upper bound on ADMM quality)
    # =========================================================================

    print("\n--- Step 4: ADMM with Exact Solver (reference) ---")

    admm_exact_result = solve_with_numpy_exact(qp)

    exact_x = admm_exact_result.x
    exact_obj = admm_exact_result.fval
    exact_budget = sum(exact_x)

    print(f"  ADMM + Exact result:")
    print(f"    Solution: {exact_x}")
    print(f"    Objective: {exact_obj:.4f}")
    print(f"    Budget used: {exact_budget:.0f}")

    # =========================================================================
    # STEP 5: Pure QAOA with Penalty Encoding (comparison)
    # =========================================================================

    print("\n--- Step 5: Pure QAOA with Penalty Encoding (comparison) ---")
    print("  (Constraints encoded as penalty terms in the objective)")

    penalty_results = {}
    for penalty in [1.0, 5.0, 10.0, 50.0]:
        qaoa_result = solve_with_qaoa_penalty(qp, penalty_weight=penalty)

        qaoa_x = qaoa_result.x
        qaoa_obj = qaoa_result.fval
        qaoa_budget = sum(qaoa_x)
        is_feasible = qaoa_budget == metadata["budget"]

        penalty_results[penalty] = {
            "x": qaoa_x.tolist() if hasattr(qaoa_x, "tolist") else list(qaoa_x),
            "objective": float(qaoa_obj),
            "budget": float(qaoa_budget),
            "feasible": is_feasible,
        }

        status = "FEASIBLE" if is_feasible else "INFEASIBLE"
        print(
            f"  Penalty={penalty:5.1f}: x={qaoa_x}, obj={qaoa_obj:8.4f}, "
            f"budget={qaoa_budget:.0f} [{status}]"
        )

    # =========================================================================
    # STEP 6: Sensitivity Analysis (rho parameter)
    # =========================================================================

    print("\n--- Step 6: ADMM Penalty Parameter Sensitivity ---")
    print("  (See explanation_physicist.md, Section 4.4)")

    rho_results = {}
    for rho in [10, 100, 1000, 10000]:
        rho_result, _ = solve_with_admm(qp, rho_initial=rho)
        rho_x = rho_result.x
        rho_obj = rho_result.fval
        rho_budget = sum(rho_x)
        is_feasible = rho_budget == metadata["budget"]

        rho_results[rho] = {
            "objective": float(rho_obj),
            "feasible": is_feasible,
            "budget": float(rho_budget),
        }

        status = "FEASIBLE" if is_feasible else "INFEASIBLE"
        print(
            f"  rho={rho:6d}: obj={rho_obj:8.4f}, budget={rho_budget:.0f} [{status}]"
        )

    # =========================================================================
    # STEP 7: Visualization
    # =========================================================================

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("ADMM for Constrained Quantum Optimization", fontsize=16, fontweight="bold")

    # Plot 1: Feasible portfolio comparison
    portfolios = sorted(feasible.keys(), key=lambda k: feasible[k]["objective"])
    objectives = [feasible[p]["objective"] for p in portfolios]
    labels = [str(feasible[p]["assets"]) for p in portfolios]
    colors_bar = [
        "#2ecc71" if p == best_sol else "#95a5a6" for p in portfolios
    ]

    bars = axes[0, 0].barh(range(len(portfolios)), objectives, color=colors_bar)
    axes[0, 0].set_yticks(range(len(portfolios)))
    axes[0, 0].set_yticklabels(labels, fontsize=9)
    axes[0, 0].set_xlabel("Objective (lower is better)", fontsize=11)
    axes[0, 0].set_title("All Feasible Portfolios (Brute Force)", fontsize=13)
    axes[0, 0].axvline(x=best_obj, color="red", linestyle="--", alpha=0.7, label="Optimal")
    if admm_obj is not None:
        axes[0, 0].axvline(
            x=admm_obj, color="blue", linestyle=":", alpha=0.7, label="ADMM+QAOA"
        )
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(True, alpha=0.3, axis="x")

    # Plot 2: ADMM vs QAOA penalty methods
    methods = ["Exact\n(brute force)", "ADMM+QAOA", "ADMM+Exact"]
    method_objs = [best_obj, admm_obj, exact_obj]
    method_feasible = [True, admm_budget == metadata["budget"], exact_budget == metadata["budget"]]
    method_colors = ["#2ecc71" if f else "#e74c3c" for f in method_feasible]

    # Add penalty method results
    for pen, res in penalty_results.items():
        methods.append(f"QAOA\npen={pen}")
        method_objs.append(res["objective"])
        method_feasible.append(res["feasible"])
        method_colors.append("#2ecc71" if res["feasible"] else "#e74c3c")

    bars2 = axes[0, 1].bar(range(len(methods)), method_objs, color=method_colors)
    axes[0, 1].set_xticks(range(len(methods)))
    axes[0, 1].set_xticklabels(methods, fontsize=8, rotation=0)
    axes[0, 1].set_ylabel("Objective value", fontsize=11)
    axes[0, 1].set_title("Method Comparison (green=feasible, red=infeasible)", fontsize=13)
    axes[0, 1].axhline(y=best_obj, color="black", linestyle="--", alpha=0.3)
    axes[0, 1].grid(True, alpha=0.3, axis="y")

    # Plot 3: Rho sensitivity
    rho_vals = sorted(rho_results.keys())
    rho_objs = [rho_results[r]["objective"] for r in rho_vals]
    rho_feas = [rho_results[r]["feasible"] for r in rho_vals]
    rho_colors = ["#2ecc71" if f else "#e74c3c" for f in rho_feas]

    axes[1, 0].bar(
        [str(r) for r in rho_vals],
        rho_objs,
        color=rho_colors,
    )
    axes[1, 0].axhline(y=best_obj, color="black", linestyle="--", alpha=0.5, label="Exact optimal")
    axes[1, 0].set_xlabel("rho (penalty parameter)", fontsize=11)
    axes[1, 0].set_ylabel("Objective value", fontsize=11)
    axes[1, 0].set_title("ADMM Sensitivity to rho", fontsize=13)
    axes[1, 0].legend(fontsize=9)
    axes[1, 0].grid(True, alpha=0.3, axis="y")

    # Plot 4: Risk-Return visualization of portfolios
    risks = [feasible[p]["risk"] for p in portfolios]
    returns = [feasible[p]["return"] for p in portfolios]

    axes[1, 1].scatter(risks, returns, s=120, c=objectives, cmap="RdYlGn_r",
                       edgecolors="black", linewidth=1, zorder=5)
    for i, p in enumerate(portfolios):
        axes[1, 1].annotate(
            str(feasible[p]["assets"]),
            (risks[i], returns[i]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=7,
        )

    # Highlight the optimal and ADMM solutions
    opt_info = feasible[best_sol]
    axes[1, 1].scatter(
        [opt_info["risk"]], [opt_info["return"]],
        s=200, marker="*", c="gold", edgecolors="black", linewidth=1.5,
        zorder=10, label="Optimal",
    )

    axes[1, 1].set_xlabel("Risk (x^T Sigma x)", fontsize=11)
    axes[1, 1].set_ylabel("Return (mu^T x)", fontsize=11)
    axes[1, 1].set_title("Efficient Frontier (Feasible Portfolios)", fontsize=13)
    axes[1, 1].legend(fontsize=9)
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        "quantum/algorithms/07_ADMM/admm_results.png",
        dpi=150,
        bbox_inches="tight",
    )
    plt.show()
    print("\nPlot saved to quantum/algorithms/07_ADMM/admm_results.png")

    # =========================================================================
    # Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    ADMM for Constrained Portfolio Optimization ({metadata['num_assets']} assets, budget={metadata['budget']}):

    Brute force optimal: |{best_sol}> with objective = {best_obj:.4f}

    ADMM + QAOA:  x = {admm_x}, obj = {admm_obj:.4f}
      Budget satisfied: {'YES' if admm_budget == metadata['budget'] else 'NO'}

    ADMM + Exact: x = {exact_x}, obj = {exact_obj:.4f}
      Budget satisfied: {'YES' if exact_budget == metadata['budget'] else 'NO'}

    Key observations:
    1. ADMM naturally handles the budget constraint (sum(x) = {metadata['budget']})
       without penalty weight tuning
    2. Pure QAOA with penalties requires careful tuning: too low -> infeasible,
       too high -> distorted landscape
    3. ADMM decomposes the problem so the quantum solver only sees a QUBO
       (no constraints to worry about)
    4. The penalty parameter rho controls the constraint enforcement strength
    5. ADMM typically converges within 5-50 outer iterations

    When to use ADMM:
    - Problems with equality/inequality constraints
    - Mixed binary-continuous variable problems
    - When penalty-based constraint encoding fails or is fragile
    - Portfolio optimization, scheduling, resource allocation
    """)


if __name__ == "__main__":
    main()
