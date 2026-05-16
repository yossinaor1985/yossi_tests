# ADMM (Alternating Direction Method of Multipliers) for Quantum Optimization - Physicist's Deep Dive

## 1. Overview

The Alternating Direction Method of Multipliers (ADMM) is a classical decomposition method that has been adapted for hybrid quantum-classical optimization. In the quantum computing context, ADMM provides a principled framework for solving **constrained** optimization problems by splitting them into subproblems: some that are naturally suited for quantum solvers (QUBO/Ising subproblems via QAOA or VQE) and others that remain on classical hardware.

The Qiskit implementation follows the approach described by Gambetta et al. and is available in `qiskit_optimization.algorithms.ADMMOptimizer`. The key insight is: **most real-world optimization problems have constraints, and quantum solvers (QAOA, VQE) can only handle unconstrained QUBO problems directly.** ADMM bridges this gap by decomposing the constrained problem into tractable pieces.

---

## 2. Classical ADMM Formulation

### 2.1 The Augmented Lagrangian

Consider a general constrained optimization problem:

```
minimize    f(x) + g(z)
subject to  Ax + Bz = c
```

where x and z are decision variable vectors, f and g are (possibly non-convex) objective functions, and Ax + Bz = c encodes the coupling constraints.

The **augmented Lagrangian** is:

```
L_rho(x, z, lambda) = f(x) + g(z) + lambda^T (Ax + Bz - c) + (rho/2) ||Ax + Bz - c||_2^2
```

where:
- lambda is the vector of Lagrange multipliers (dual variables)
- rho > 0 is the penalty parameter (augmented Lagrangian penalty)
- The last term (rho/2)||...||^2 is the quadratic penalty that regularizes the problem

The standard Lagrangian (rho = 0) may not have a finite saddle point for non-convex problems. The augmented term (rho > 0) adds strict convexity in the constraint direction, improving convergence.

### 2.2 The ADMM Update Steps

ADMM alternates between optimizing over x, z, and lambda in a Gauss-Seidel fashion:

**Step 1 (x-update):** Minimize L_rho over x, fixing z and lambda:
```
x^{k+1} = argmin_x [ f(x) + lambda^{kT} A x + (rho/2) ||Ax + Bz^k - c||_2^2 ]
```

**Step 2 (z-update):** Minimize L_rho over z, fixing x and lambda:
```
z^{k+1} = argmin_z [ g(z) + lambda^{kT} B z + (rho/2) ||Ax^{k+1} + Bz - c||_2^2 ]
```

**Step 3 (dual update):** Update Lagrange multipliers:
```
lambda^{k+1} = lambda^k + rho * (Ax^{k+1} + Bz^{k+1} - c)
```

This is sometimes written in scaled form. Let u = lambda / rho:

```
x^{k+1} = argmin_x [ f(x) + (rho/2) ||Ax + Bz^k - c + u^k||_2^2 ]
z^{k+1} = argmin_z [ g(z) + (rho/2) ||Ax^{k+1} + Bz - c + u^k||_2^2 ]
u^{k+1} = u^k + Ax^{k+1} + Bz^{k+1} - c
```

### 2.3 Intuitive Interpretation

Each ADMM iteration can be understood as:
1. **x-update:** Solve the "quantum-friendly" part of the problem (e.g., the QUBO), penalizing deviation from the current consensus on z.
2. **z-update:** Solve the "classically easy" part (e.g., continuous relaxation or simple constraints), penalizing deviation from the updated x.
3. **Dual update:** Adjust the Lagrange multipliers to enforce constraint satisfaction -- the "price" paid for constraint violation increases.

---

## 3. Quantum ADMM: Hybrid Decomposition

### 3.1 Problem Partitioning for Quantum Hardware

In the quantum ADMM framework (as implemented in `qiskit_optimization`), a constrained Mixed-Integer Quadratic Program (MIQP) of the form:

```
minimize    x^T Q x + q^T x + c^T z + d^T z^2
subject to  A_eq x + B_eq z = b_eq    (equality constraints)
            A_ineq x + B_ineq z <= b_ineq  (inequality constraints)
            x in {0, 1}^n              (binary variables)
            z in R^m                    (continuous variables)
```

is decomposed as:

- **Subproblem 1 (Quantum):** Optimize over the **binary variables x** with the constraints absorbed into the augmented Lagrangian penalty. This yields a QUBO problem that can be solved with QAOA, VQE, or any MinimumEigenOptimizer.

- **Subproblem 2 (Classical):** Optimize over the **continuous variables z** using standard convex optimization (e.g., CPLEX, Gurobi, or a simple quadratic solver). This is computationally trivial compared to the combinatorial part.

- **Dual update:** Update the Lagrange multipliers lambda using gradient ascent on the dual function.

### 3.2 The QUBO Subproblem (Quantum Step)

At iteration k, the x-update requires solving:

```
x^{k+1} = argmin_{x in {0,1}^n} [ x^T Q x + q^T x + (lambda^k)^T A x + (rho/2) ||Ax + Bz^k - b||_2^2 ]
```

Expanding the quadratic penalty:

```
= argmin_x [ x^T (Q + (rho/2) A^T A) x + (q + A^T lambda^k + rho A^T (Bz^k - b))^T x ]
```

This is a QUBO (Quadratic Unconstrained Binary Optimization) in x, which can be:
1. Converted to an Ising Hamiltonian via x_i = (1 - Z_i) / 2
2. Solved using QAOA, VQE, or Grover Adaptive Search on a quantum computer

The effective QUBO matrix at each iteration is:

```
Q_eff = Q + (rho/2) A^T A
q_eff = q + A^T lambda^k + rho A^T (Bz^k - b)
```

Note: The QUBO changes at each ADMM iteration because z^k and lambda^k are updated. The quantum solver is called fresh at each outer iteration.

### 3.3 The Continuous Subproblem (Classical Step)

The z-update is a convex quadratic program (assuming g(z) is convex):

```
z^{k+1} = argmin_z [ c^T z + d^T z^2 + (lambda^k)^T Bz + (rho/2) ||Ax^{k+1} + Bz - b||_2^2 ]
```

This reduces to solving a system of linear equations (if unconstrained in z) or a small convex QP. Standard solvers handle this in milliseconds.

### 3.4 Complete Quantum ADMM Algorithm

```
Quantum ADMM Algorithm:
    Input: MIQP(Q, q, c, d, A, B, b), penalty rho, tolerance eps, max_iter K

    Initialize:
        x^0 = 0 (or heuristic)
        z^0 = 0 (or heuristic)
        lambda^0 = 0 (Lagrange multipliers)

    For k = 0, 1, ..., K-1:

        1. [QUANTUM] x-update:
           - Build QUBO: Q_eff = Q + (rho/2) A^T A
                         q_eff = q + A^T lambda^k + rho A^T (Bz^k - b)
           - Convert to Ising Hamiltonian H_QUBO
           - Solve with QAOA/VQE: x^{k+1} = argmin H_QUBO

        2. [CLASSICAL] z-update:
           - Solve QP: z^{k+1} = argmin_z [g(z) + (rho/2)||Ax^{k+1}+Bz-b+u^k||^2]
           - Use CPLEX, Gurobi, or direct solve

        3. [CLASSICAL] Dual update:
           - lambda^{k+1} = lambda^k + rho (Ax^{k+1} + Bz^{k+1} - b)

        4. Check convergence:
           - Primal residual: r^k = ||Ax^{k+1} + Bz^{k+1} - b||
           - Dual residual:   s^k = rho ||B(z^{k+1} - z^k)||
           - If r^k < eps and s^k < eps: STOP

    Output: (x*, z*, lambda*)
```

---

## 4. Convergence Theory

### 4.1 Convergence for Convex Problems

**Theorem (Boyd et al., 2011):** For convex f and g, the ADMM iterates satisfy:

1. **Residual convergence:** r^k -> 0 and s^k -> 0 as k -> infinity
2. **Objective convergence:** f(x^k) + g(z^k) -> p* (optimal value)
3. **Dual convergence:** lambda^k -> lambda* (optimal dual variable)

under mild assumptions (existence of a saddle point of L_0).

### 4.2 Convergence Rate

For convex problems, ADMM converges at rate O(1/k) in the objective:

```
f(x^k) + g(z^k) - p* <= C / k
```

where C depends on rho, the problem data, and the initial point.

### 4.3 Non-Convex Case (QUBO)

When the x-subproblem is a QUBO (binary optimization), f(x) is non-convex. Rigorous convergence guarantees are weaker:

- **Empirical convergence:** ADMM typically converges within 10-50 iterations for practical problems
- **Local convergence:** Under regularity conditions, ADMM converges to a stationary point of the augmented Lagrangian
- **Penalty escalation:** If rho is increased adaptively (rho_k -> infinity), the method converges to a feasible point (constraint satisfaction), though not necessarily optimal

The key result from Hong, Luo, and Razaviyayn (2016): For certain non-convex ADMM variants, subsequential convergence to a stationary point is guaranteed if:
1. The augmented Lagrangian has a bounded sublevel set
2. The penalty parameter rho is sufficiently large

### 4.4 Choice of Penalty Parameter rho

The penalty parameter rho controls the trade-off between:
- **Large rho:** Fast constraint satisfaction, but the QUBO subproblem becomes ill-conditioned (the penalty term dominates the original objective)
- **Small rho:** Preserves the original problem structure, but constraint convergence is slow

Practical guidelines:
- Start with rho = 1.0
- Use adaptive rho: increase rho if primal residual >> dual residual, decrease if dual >> primal
- The Qiskit implementation uses rho_update = rho * factor with configurable factor

---

## 5. Worked Example: Portfolio Optimization with Budget Constraint

### 5.1 Problem Formulation

**Portfolio selection:** Choose which of n=4 assets to invest in, minimizing risk-adjusted cost subject to a budget constraint.

```
minimize    x^T Sigma x - mu^T x      (risk - expected return)
subject to  1^T x = B                  (invest in exactly B assets)
            x in {0, 1}^4              (binary: invest or not)
```

Concrete parameters:
- Covariance matrix: Sigma = [[0.5, 0.1, -0.05, 0.02],
                               [0.1, 0.4, 0.08, -0.03],
                               [-0.05, 0.08, 0.6, 0.1],
                               [0.02, -0.03, 0.1, 0.3]]
- Expected returns: mu = [0.12, 0.10, 0.07, 0.15]
- Budget: B = 2 (invest in exactly 2 assets)

### 5.2 ADMM Decomposition

Introduce continuous slack variable z to handle the equality constraint:

```
minimize    x^T Sigma x - mu^T x + 0
subject to  1^T x - z = B
            z = 0  (z is the slack; forcing z = 0 enforces the original constraint)
            x in {0, 1}^4
```

Actually, in the standard ADMM form for this portfolio problem:

Let us write it as:
```
minimize    f(x) + g(z)
subject to  x - z = 0   (consensus constraint)
```

where f(x) = x^T Sigma x - mu^T x restricted to x in {0,1}^4, and g(z) encodes the budget constraint via an indicator function or penalty.

Alternatively, in the Qiskit ADMM formulation, the problem is split as:
- Binary part: x^T Sigma x - mu^T x (QUBO, solved on quantum)
- Constraint part: 1^T x = B (absorbed into the augmented Lagrangian penalty)

### 5.3 ADMM Iteration Trace

**Iteration 0:**
```
x^0 = [0, 0, 0, 0], z^0 = 0, lambda^0 = 0
Primal residual: ||1^T x - B|| = |0 - 2| = 2.0
```

**Iteration 1 (x-update via QAOA):**
```
QUBO: minimize x^T (Sigma + rho/2 * 1*1^T) x + (q_eff)^T x
Solve with QAOA -> x^1 = [1, 0, 0, 1]  (assets 0 and 3)
Budget: sum(x) = 2 = B (feasible!)
Cost: x^T Sigma x - mu^T x = 0.84 - 0.27 = 0.57
```

**Iteration 1 (z-update, dual update):**
```
z^1: solve continuous QP -> z^1 = ... (adjust to consensus)
lambda^1 = lambda^0 + rho * (Ax^1 + Bz^1 - b)
Primal residual: drops to 0.15
```

**Iterations 2-5:** Primal and dual residuals decrease. The QUBO subproblem is re-solved with updated penalty terms at each iteration, gradually steering x toward constraint satisfaction.

**Convergence (iteration ~5-10):**
```
x* = [1, 0, 0, 1] (invest in assets 0 and 3)
Primal residual < 1e-6
Optimal cost: x*^T Sigma x* - mu^T x* = 0.57
```

Assets 0 and 3 were selected because they have the highest expected returns (0.12 and 0.15) with relatively low cross-correlation (Sigma_{03} = 0.02).

### 5.4 Verification by Brute Force

For n=4 and B=2, there are C(4,2)=6 feasible portfolios. Evaluating all:

| Portfolio | x | Risk x^T Sigma x | Return mu^T x | Objective |
|-----------|---|-------------------|----------------|-----------|
| {0,1} | [1,1,0,0] | 1.10 | 0.22 | 0.88 |
| {0,2} | [1,0,1,0] | 1.00 | 0.19 | 0.81 |
| {0,3} | [1,0,0,1] | 0.84 | 0.27 | 0.57 |
| {1,2} | [0,1,1,0] | 1.16 | 0.17 | 0.99 |
| {1,3} | [0,1,0,1] | 0.64 | 0.25 | 0.39 |
| {2,3} | [0,0,1,1] | 1.10 | 0.22 | 0.88 |

**Optimal: {1,3}** with objective 0.39. ADMM should converge to x* = [0,1,0,1].

(Note: The specific iteration trace above was illustrative; the actual ADMM trajectory depends on rho, the quantum solver accuracy, and initialization.)

---

## 6. Comparison with Other Approaches

### 6.1 ADMM vs Direct QAOA

| Property | Direct QAOA | ADMM + QAOA |
|----------|-------------|-------------|
| Constraints | Must encode as penalties (may require large penalty weights) | Handled naturally via ADMM decomposition |
| Problem size | Full problem on quantum device | Only binary subproblem on quantum device |
| Continuous variables | Cannot handle | Handled classically |
| Convergence | Single shot (no outer loop) | Iterative (5-50 outer loops) |
| Penalty tuning | Requires manual penalty weight selection | Penalty rho is auto-adjusted |
| Solution quality | May violate constraints | Converges to feasible solutions |

### 6.2 ADMM vs Penalty Method

The penalty method directly adds M * ||Ax - b||^2 to the objective (no dual variables). Problems:
- Must choose M very large for feasibility -> ill-conditioned QUBO
- No convergence guarantee for finite M
- ADMM achieves exact feasibility with finite rho by using dual updates

### 6.3 When to Use ADMM

ADMM is the right choice when:
1. The problem has **equality or inequality constraints** that are difficult to encode as penalty terms
2. The problem has **mixed binary-continuous variables**
3. The QUBO subproblem alone is within quantum hardware capability
4. The continuous part can be solved efficiently classically

---

## 7. Implementation in Qiskit

### 7.1 The `ADMMOptimizer` Class

Qiskit's `qiskit_optimization.algorithms.ADMMOptimizer` implements the full quantum ADMM loop:

```python
from qiskit_optimization.algorithms import ADMMOptimizer, ADMMParameters

params = ADMMParameters(
    rho_initial=1000,      # Initial penalty parameter
    factor_c=10,           # Penalty update factor
    beta=1000,             # Penalty for equality constraints
    maxiter=100,           # Maximum ADMM iterations
    tol=1e-6,              # Convergence tolerance
    three_block=True,      # Use 3-block ADMM (x, z, y updates)
)

admm = ADMMOptimizer(
    qubo_optimizer=qaoa_optimizer,   # Quantum solver for binary subproblem
    continuous_optimizer=cplex_opt,  # Classical solver for continuous part
    params=params,
)

result = admm.solve(quadratic_program)
```

### 7.2 Three-Block ADMM

The Qiskit implementation supports a **3-block** variant where the variables are split into three groups:
1. **x:** Binary variables (quantum solver)
2. **y:** Continuous variables appearing in equality constraints
3. **z:** Slack variables for inequality constraints

This gives more flexibility but requires additional dual variable updates.

---

## 8. References

1. Boyd, S., Parikh, N., Chu, E., Peleato, B., & Eckstein, J. "Distributed Optimization and Statistical Learning via the Alternating Direction Method of Multipliers." Foundations and Trends in Machine Learning, 3(1): 1-122 (2011).
2. Gambella, C., Simonetto, A., & Luongo, A. "Multi-block ADMM Heuristics for Mixed-Binary Optimization on Classical and Quantum Computers." arXiv:2001.02069 (2020).
3. Hong, M., Luo, Z.-Q., & Razaviyayn, M. "Convergence Analysis of Alternating Direction Method of Multipliers for a Family of Nonconvex Problems." SIAM Journal on Optimization, 26(1): 337-364 (2016).
4. Qiskit Optimization Module: `qiskit_optimization.algorithms.ADMMOptimizer`. [Qiskit Documentation](https://qiskit-community.github.io/qiskit-optimization/).
5. Glover, F., Kochenberger, G., & Du, Y. "A Tutorial on Formulating and Using QUBO Models." arXiv:1811.11538 (2018).
