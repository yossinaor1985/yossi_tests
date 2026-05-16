# Warm-Start QAOA - Physicist's Deep Dive

## 1. Overview

Warm-Start QAOA (WS-QAOA) improves upon standard QAOA by initializing the quantum state using information from a classical approximate solution, rather than starting from the uniform superposition |+>^n. This approach was introduced by Egger et al. (2021) and has been shown to significantly improve convergence and solution quality, especially at low circuit depths (small p).

**Key insight:** Standard QAOA begins from the uniform superposition, which treats all 2^n solutions equally. If a classical heuristic already provides a good approximate solution, we should bias the initial state toward that solution while still allowing quantum exploration of nearby solutions.

---

## 2. Mathematical Foundation

### 2.1 Standard QAOA Initial State

In standard QAOA, the initial state is:
```
|s> = |+>^n = H^n |0>^n = (1/sqrt(2^n)) sum_{x in {0,1}^n} |x>
```

This is the ground state of the mixer Hamiltonian H_M = sum_i X_i.

### 2.2 Warm-Start Initial State

Given a classical solution c = (c_1, ..., c_n) with c_i in [0, 1] (relaxed binary values from, e.g., a convex relaxation or LP relaxation), the warm-start initial state is:

```
|s_c> = tensor_{i=1}^{n} [cos(theta_i/2)|0> + sin(theta_i/2)|1>]
```

where:
```
theta_i = 2 * arcsin(sqrt(c_i))
```

This means:
- If c_i = 0 (classical solution says x_i = 0): theta_i = 0, qubit i is |0>
- If c_i = 1 (classical solution says x_i = 1): theta_i = pi, qubit i is |1>
- If c_i = 0.5 (uncertain): theta_i = pi/2, qubit i is |+> (maximum superposition)

The probability of measuring qubit i as 1 is sin^2(theta_i/2) = c_i.

### 2.3 Modified Mixer Hamiltonian

The standard mixer H_M = sum_i X_i has |+>^n as its ground state. For warm-start, we need a mixer whose ground state is |s_c>. This is achieved with the **custom mixer**:

```
H_M^{WS} = sum_i [cos(theta_i) X_i + sin(theta_i) Z_i]
```

The ground state of each term cos(theta_i) X_i + sin(theta_i) Z_i is precisely:
```
cos(theta_i/2)|0> + sin(theta_i/2)|1>
```

**Proof:**
The operator cos(theta) X + sin(theta) Z has matrix:
```
[sin(theta)    cos(theta)]
[cos(theta)   -sin(theta)]
```

Eigenvalues: +/- 1. The eigenstate with eigenvalue -1 (ground state) is:
```
|-> = cos(theta/2)|0> + sin(theta/2)|1>
```
which is exactly the warm-start qubit state.

### 2.4 Warm-Start Mixer Unitary

The warm-start mixer unitary is:

```
U_M^{WS}(beta) = exp(-i beta H_M^{WS})
               = prod_i exp(-i beta [cos(theta_i) X_i + sin(theta_i) Z_i])
```

Each single-qubit term can be implemented as:
```
R_Z(-theta_i) R_X(2*beta) R_Z(theta_i)
```

This rotates to the frame where the custom mixer is aligned with X, applies the X-rotation, and rotates back.

### 2.5 Complete WS-QAOA State

```
|gamma, beta>_{WS} = U_M^{WS}(beta_p) U_C(gamma_p) ... U_M^{WS}(beta_1) U_C(gamma_1) |s_c>
```

---

## 3. Classical Warm-Start Strategies

### 3.1 LP/SDP Relaxation

Relax binary variables x_i in {0,1} to continuous variables c_i in [0,1]. Solve the resulting linear/semidefinite program to get c = (c_1, ..., c_n). This gives a continuous relaxation of the original problem.

For MaxCut, the Goemans-Williamson SDP relaxation provides a 0.878-approximation.

### 3.2 Greedy Classical Heuristic

Run a greedy classical algorithm (e.g., for MaxCut: iteratively assign each node to the partition that maximizes the cut). The binary solution c_i in {0, 1} is used directly.

### 3.3 Rounding the Relaxation

If c_i in [0,1], one can:
1. **Direct use:** Keep c_i as continuous values for theta_i = 2*arcsin(sqrt(c_i))
2. **Soft rounding:** Push c_i toward 0 or 1 with a sigmoid: c_i' = sigma(alpha * (c_i - 0.5))
3. **Random rounding:** Sample x_i ~ Bernoulli(c_i) multiple times, keep the best

---

## 4. Theoretical Advantages

### 4.1 Improved Approximation at Low Depth

For MaxCut on 3-regular graphs at p = 1:
- Standard QAOA: approximation ratio >= 0.6924
- WS-QAOA: approximation ratio can exceed 0.6924, especially when the classical solution is already good

The improvement depends on the quality of the classical warm-start solution.

### 4.2 Faster Convergence

WS-QAOA typically requires fewer optimizer iterations because:
1. The initial state is biased toward good solutions
2. The parameter landscape has a clearer gradient direction
3. The optimizer starts closer to the optimum in parameter space

### 4.3 Avoiding Barren Plateaus

By starting from a biased state (rather than maximally mixed), the cost function landscape tends to have larger gradients, mitigating the barren plateau problem.

---

## 5. Worked Example: MaxCut on 4-Node Graph

### Problem

Same graph as QAOA tutorial:
```
0 --- 1
|     |
3 --- 2
```
Edges: {(0,1), (1,2), (2,3), (0,3)}. MaxCut = 4.

### Classical Warm-Start

Running a greedy heuristic:
1. Assign node 0 to partition A
2. Node 1: neighbor of 0 (partition A), assign to B -> cuts edge (0,1)
3. Node 2: neighbor of 1 (partition B), assign to A -> cuts edge (1,2)
4. Node 3: neighbors 0 (A) and 2 (A), assign to B -> cuts edges (2,3) and (0,3)

Result: c = (0, 1, 0, 1) = |0101>. This cuts all 4 edges - already optimal!

With theta_i:
```
theta_0 = 2*arcsin(sqrt(0)) = 0     -> qubit 0 initialized to |0>
theta_1 = 2*arcsin(sqrt(1)) = pi    -> qubit 1 initialized to |1>
theta_2 = 2*arcsin(sqrt(0)) = 0     -> qubit 2 initialized to |0>
theta_3 = 2*arcsin(sqrt(1)) = pi    -> qubit 3 initialized to |1>
```

Initial state: |0101>, which IS the optimal solution. The QAOA optimization then fine-tunes around this.

### More Interesting Case: Relaxed Solution

Suppose LP relaxation gives c = (0.3, 0.8, 0.2, 0.7):
```
theta_0 = 2*arcsin(sqrt(0.3)) = 1.159 rad
theta_1 = 2*arcsin(sqrt(0.8)) = 2.214 rad
theta_2 = 2*arcsin(sqrt(0.2)) = 0.927 rad
theta_3 = 2*arcsin(sqrt(0.7)) = 1.982 rad
```

The initial state biases toward |0101> (the classical hint) but maintains superposition to explore nearby solutions.

---

## 6. Implementation Considerations

### 6.1 Circuit Overhead

Compared to standard QAOA:
- **Initial state:** n R_Y gates instead of n Hadamard gates (minimal overhead)
- **Mixer:** Each qubit requires R_Z(-theta_i) R_X(2*beta) R_Z(theta_i) instead of just R_X(2*beta). This adds 2n R_Z gates per mixer layer.
- **Total overhead:** 2np additional single-qubit gates (negligible for NISQ)

### 6.2 When to Use Warm-Start

- **Use when:** A good classical approximate solution is available (e.g., LP relaxation, greedy heuristic)
- **Skip when:** No classical solution available, or the problem has no known efficient relaxation
- **Especially useful for:** Low-depth QAOA (p = 1, 2) where standard QAOA struggles

---

## 7. References

1. Egger, D. J., et al. "Warm-starting quantum optimization." Quantum 5, 479 (2021).
2. Tate, R., et al. "Bridging Classical and Quantum with SDP initialized warm-starting QAOA." ACM TQC 4, 2 (2023).
3. Truger, F., et al. "Warm-starting and quantum computing: A systematic mapping study." arXiv:2303.06133 (2023).
