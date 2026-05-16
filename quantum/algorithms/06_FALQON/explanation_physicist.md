# FALQON (Feedback-based Algorithm for Quantum Optimization) - Physicist's Deep Dive

## 1. Overview

FALQON, introduced by Magann, Rudinger, Grace, and Sarovar (2022), is a quantum optimization algorithm that eliminates the classical optimization loop entirely. Instead of variationally optimizing circuit parameters, FALQON uses a feedback law derived from quantum optimal control theory to deterministically set the parameters of each new layer based on measurements from the previous layer.

**Key advantage:** FALQON requires only a single circuit evaluation per layer (no parameter optimization), making it significantly more efficient than QAOA in terms of quantum circuit evaluations.

---

## 2. Mathematical Foundation

### 2.1 Problem Setup

Like QAOA, FALQON addresses combinatorial optimization by encoding the problem in a cost Hamiltonian H_C. The goal is to prepare a state that minimizes <H_C>.

The algorithm uses two non-commuting Hamiltonians:
- **H_C:** Cost Hamiltonian (problem-encoding, diagonal in computational basis)
- **H_M:** Driver/mixer Hamiltonian (typically H_M = sum_i X_i)

### 2.2 The FALQON Ansatz

FALQON prepares the state:
```
|psi_k> = U_M(beta_k) U_C(gamma_k) ... U_M(beta_1) U_C(gamma_1) |psi_0>
```

This has the same structure as QAOA! The critical difference is HOW the parameters gamma_k, beta_k are determined.

### 2.3 The Feedback Law

FALQON determines the parameters using a Lyapunov-based feedback control law.

Define the cost function at layer k:
```
C_k = <psi_k| H_C |psi_k>
```

The change in cost due to the (k+1)-th layer is (to first order in dt):
```
dC/dt = <psi_k| i[H_C, H_drive(t)] |psi_k>
```

where H_drive(t) alternates between H_C and H_M.

**FALQON feedback rule for beta_k:**

After applying U_C(gamma_k), measure the operator:
```
A_k = i[H_C, H_M] = i * (H_C H_M - H_M H_C)
```

The feedback law sets:
```
beta_k = -dt * <psi_k'| A_k |psi_k'>
```

where |psi_k'> = U_C(gamma_k) |psi_{k-1}> is the state after the cost unitary, and dt > 0 is a step size parameter.

This choice guarantees that C_{k+1} < C_k (the cost decreases monotonically) as long as [H_C, H_M] != 0.

### 2.4 Why This Works: Lyapunov Stability Theory

Consider the Lyapunov function V = C(t) = <psi(t)|H_C|psi(t)>.

The time derivative of V under control u(t) is:
```
dV/dt = <psi(t)| i[H_C, u(t)*H_M] |psi(t)>
      = u(t) * <psi(t)| i[H_C, H_M] |psi(t)>
      = u(t) * <A(t)>
```

Choosing u(t) = -k * <A(t)> (with k > 0) gives:
```
dV/dt = -k * <A(t)>^2 <= 0
```

This is a negative semi-definite Lyapunov derivative, guaranteeing that V decreases monotonically. The system converges to a state where <A(t)> = 0 (a critical point of C).

### 2.5 Discretization

In the discrete (circuit-based) version:
```
gamma_k = dt_gamma  (fixed small step)
beta_k = -dt_beta * <psi_k'| i[H_C, H_M] |psi_k'>  (feedback)
```

where dt_gamma and dt_beta are step size hyperparameters.

### 2.6 Computing the Commutator

For MaxCut with H_C = sum_{(i,j)} J_{ij} Z_i Z_j and H_M = sum_k X_k:

```
[H_C, H_M] = sum_{(i,j)} sum_k J_{ij} [Z_i Z_j, X_k]
```

Using [Z, X] = 2iY:
```
[Z_i Z_j, X_k] = delta_{k,i} * 2i * Y_i Z_j + delta_{k,j} * 2i * Z_i Y_j
```

So:
```
i[H_C, H_M] = sum_{(i,j)} J_{ij} (-2) * (Y_i Z_j + Z_i Y_j)
```

Each term Y_i Z_j is a 2-qubit Pauli string that can be measured on the quantum computer.

---

## 3. Algorithm Step-by-Step

```
FALQON Algorithm:
    Input: H_C, H_M, step sizes dt_gamma, dt_beta, max layers K
    Initialize: |psi_0> = |+>^n

    For k = 1, ..., K:
        1. Apply cost unitary: |psi_k'> = exp(-i * dt_gamma * H_C) |psi_k-1>
        2. Measure: a_k = <psi_k'| i[H_C, H_M] |psi_k'>
        3. Set beta_k = -dt_beta * a_k
        4. Apply mixer: |psi_k> = exp(-i * beta_k * H_M) |psi_k'>
        5. Measure cost: C_k = <psi_k| H_C |psi_k>
        6. If |C_k - C_{k-1}| < tolerance: STOP

    Output: Sample |psi_K> to get the solution
```

---

## 4. Comparison with QAOA

| Property | QAOA | FALQON |
|----------|------|--------|
| Parameters | 2p (variational) | 1 per layer (feedback) |
| Classical optimization | Required (many evaluations) | Not needed |
| Circuit evaluations | O(iterations * p) | O(K) = 1 per layer |
| Convergence guarantee | No (may get stuck in local minima) | Yes (Lyapunov monotone decrease) |
| Parameter setting | Optimizer chooses | Feedback law determines |
| Depth flexibility | Fixed depth p | Growing depth |
| Performance | Better at fixed depth | Better with unlimited depth |

**Key trade-off:**
- QAOA at fixed depth p uses many evaluations to optimize 2p parameters
- FALQON at depth K uses K evaluations (one per layer) but the circuit grows

---

## 5. Worked Example: 3-Qubit MaxCut

### Problem
Triangle graph: edges (0,1), (1,2), (0,2). MaxCut = 2.

H_C = (1/2)[(I - Z_0 Z_1) + (I - Z_1 Z_2) + (I - Z_0 Z_2)]

### FALQON Execution (dt_gamma = 0.1, dt_beta = 0.5)

**Layer 1:**
1. |psi_0> = |+++>
2. Apply U_C(0.1): phases each basis state
3. Measure i[H_C, H_M]: a_1 ≈ 0.0 (by symmetry of |+++>)
4. beta_1 = -0.5 * 0.0 = 0 (no mixing at first step)
5. C_1 ≈ 1.5 (half the edges, by symmetry)

**Layer 2:**
1. Apply U_C(0.1): break symmetry slightly
2. Measure i[H_C, H_M]: a_2 ≈ -0.15 (symmetry broken)
3. beta_2 = -0.5 * (-0.15) = 0.075
4. Apply U_M(0.075)
5. C_2 ≈ 1.52 (slight improvement)

The cost decreases gradually over many layers, eventually approaching C = 2.

---

## 6. Practical Considerations

### 6.1 Step Size Selection
- **dt_gamma too large:** Cost unitary overshoots, oscillations
- **dt_gamma too small:** Very slow convergence, needs many layers
- **Typical:** dt_gamma = dt_beta = 0.01 to 0.1

### 6.2 Number of Layers
- More layers = better solution but deeper circuit
- On NISQ devices: limited by decoherence time
- Typical: K = 10-50 layers for small problems

### 6.3 Mid-Circuit Measurement
- FALQON requires measuring <i[H_C, H_M]> between layers
- This can be done with mid-circuit measurements (if hardware supports)
- Or: pre-compute beta values using classical simulation, then run full circuit

---

## 7. References

1. Magann, A. B., Rudinger, K. M., Grace, M. D., & Sarovar, M. "Feedback-based quantum optimization." Physical Review Letters 129, 250502 (2022).
2. Magann, A. B., et al. "From Pulses to Circuits and Back Again: A Quantum Optimal Control Perspective on Variational Quantum Algorithms." PRX Quantum 2, 010101 (2021).
3. Larsen, C. B. & Hadfield, S. "Feedback-Based Quantum Optimization with Soft Constraints." arXiv:2305.18567 (2023).
