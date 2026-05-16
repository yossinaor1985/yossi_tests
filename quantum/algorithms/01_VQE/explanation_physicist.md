# Variational Quantum Eigensolver (VQE) - Physicist's Deep Dive

## 1. Overview

The Variational Quantum Eigensolver (VQE) is a hybrid quantum-classical algorithm designed to find the ground-state energy of a quantum Hamiltonian. It was first proposed by Peruzzo et al. (2014) and is one of the most studied algorithms for near-term (NISQ) quantum devices.

**Core idea:** VQE uses a parameterized quantum circuit (ansatz) to prepare trial wavefunctions, measures the expectation value of the Hamiltonian on the quantum computer, and uses a classical optimizer to minimize that expectation value. By the variational principle, the minimum found is an upper bound to the true ground-state energy.

---

## 2. Mathematical Foundation

### 2.1 The Variational Principle

The variational principle is the theoretical backbone of VQE. For any Hamiltonian H with ground-state energy E_0 and ground state |psi_0>, the following holds for **any** normalized trial state |psi(theta)>:

```
E_0 <= <psi(theta)| H |psi(theta)> = E(theta)
```

**Proof:**

Let {|E_n>} be the eigenstates of H with eigenvalues {E_n}, ordered so that E_0 <= E_1 <= E_2 <= ...

Expand the trial state in this eigenbasis:

```
|psi(theta)> = sum_n c_n(theta) |E_n>
```

Then:

```
E(theta) = <psi(theta)| H |psi(theta)>
         = sum_n |c_n(theta)|^2 E_n
         >= sum_n |c_n(theta)|^2 E_0
         = E_0 * sum_n |c_n(theta)|^2
         = E_0
```

where we used E_n >= E_0 for all n, and the normalization condition sum_n |c_n|^2 = 1.

Equality holds if and only if |psi(theta)> = |E_0> (up to a global phase).

### 2.2 The Cost Function

VQE minimizes the cost function:

```
C(theta) = <psi(theta)| H |psi(theta)>
```

where |psi(theta)> = U(theta)|0>^{otimes n} is the state prepared by the parameterized circuit U(theta) acting on the initial state |0...0>.

### 2.3 Hamiltonian Decomposition

A general Hamiltonian on n qubits can be decomposed into a sum of Pauli tensor products (Pauli strings):

```
H = sum_i alpha_i P_i
```

where each P_i is a tensor product of Pauli matrices {I, X, Y, Z} acting on individual qubits, and alpha_i are real coefficients.

Example for a 2-qubit Hamiltonian:

```
H = 0.5 * II + 0.3 * ZZ - 0.2 * XX + 0.1 * YY
```

The expectation value then decomposes linearly:

```
<H> = sum_i alpha_i <P_i>
```

Each <P_i> = <psi(theta)| P_i |psi(theta)> can be measured independently on the quantum computer by measuring each qubit in the appropriate Pauli basis.

### 2.4 Measurement Protocol

To measure <P_i>, we need to rotate each qubit into the eigenbasis of the corresponding Pauli operator:

- **I or Z**: Measure in the computational basis (no rotation needed)
- **X**: Apply a Hadamard gate H before measurement
- **Y**: Apply S^dag then H before measurement (equivalently, R_x(pi/2))

After many shots (measurements), we estimate <P_i> from the statistics of the measurement outcomes:

```
<P_i> ≈ (N_+ - N_-) / (N_+ + N_-)
```

where N_+ and N_- are the counts of outcomes with eigenvalue +1 and -1, respectively.

---

## 3. The Ansatz (Parameterized Quantum Circuit)

### 3.1 Hardware-Efficient Ansatz

Layers of single-qubit rotations followed by entangling gates (e.g., CNOT):

```
Layer l: [R_Y(theta_{l,1}) R_Z(theta_{l,1})] [R_Y(theta_{l,2}) R_Z(theta_{l,2})] ... [CNOT chain]
```

The circuit depth is D layers, giving 2nD + n parameters for n qubits.

**Advantages:** Short circuit depth, compatible with hardware connectivity.
**Disadvantages:** Can suffer from barren plateaus (exponentially vanishing gradients) for deep circuits.

### 3.2 Chemistry-Inspired Ansatz (UCCSD)

Unitary Coupled Cluster Singles and Doubles:

```
U(theta) = exp(T(theta) - T^dag(theta))
```

where T(theta) = T_1(theta) + T_2(theta) includes single and double excitation operators:

```
T_1 = sum_{i,a} theta_{i}^{a} a_a^dag a_i
T_2 = sum_{i<j, a<b} theta_{ij}^{ab} a_a^dag a_b^dag a_j a_i
```

Here, i,j index occupied orbitals and a,b index virtual (unoccupied) orbitals.

After Jordan-Wigner or Bravyi-Kitaev transformation, these fermionic operators map to qubit operators (Pauli strings), and the UCCSD unitary becomes a product of Pauli rotations.

### 3.3 EfficientSU2 Ansatz (Qiskit)

Qiskit provides the `EfficientSU2` ansatz, which is a hardware-efficient ansatz using layers of single-qubit SU(2) rotations (R_Y, R_Z) and a chosen entanglement pattern (linear, full, circular, etc.):

```
|psi(theta)> = [prod_{l=1}^{D} U_ent * prod_{q=1}^{n} R_Z(theta_{l,q,2}) R_Y(theta_{l,q,1})] |0...0>
```

---

## 4. Classical Optimization

### 4.1 Gradient-Free Methods

- **COBYLA** (Constrained Optimization BY Linear Approximation): Does not require gradient computation. Good for noisy cost function landscapes.
- **Nelder-Mead**: Simplex-based method. Robust to noise but can be slow.
- **SPSA** (Simultaneous Perturbation Stochastic Approximation): Only requires 2 function evaluations per iteration regardless of parameter count. Particularly well-suited for noisy quantum hardware.

### 4.2 Gradient-Based Methods

The gradient of the cost function with respect to parameter theta_j can be computed using the **parameter shift rule**:

```
dC/d(theta_j) = [C(theta_j + pi/2) - C(theta_j - pi/2)] / 2
```

This is exact (not a finite-difference approximation) for gates of the form exp(-i theta_j G / 2) where G has eigenvalues +/- 1.

**Proof of parameter shift rule:**

Consider a gate U_j(theta_j) = exp(-i theta_j G / 2) where G^2 = I. The expectation value is:

```
C(theta_j) = <0| U^dag(theta) H U(theta) |0>
```

Since G has eigenvalues +/- 1, we can write G = |+><+| - |-><-|, and:

```
U_j(theta_j) = cos(theta_j/2) I - i sin(theta_j/2) G
```

Differentiating:

```
dU_j/d(theta_j) = -sin(theta_j/2)/2 * I - i cos(theta_j/2)/2 * G
                = -i/2 * G * U_j(theta_j)
```

After working through the chain rule:

```
dC/d(theta_j) = (1/2)[C(theta_j + pi/2) - C(theta_j - pi/2)]
```

---

## 5. Convergence and Complexity

### 5.1 Number of Measurements

The statistical error in estimating <P_i> from N_shots measurements is:

```
epsilon_i = sqrt(Var(P_i) / N_shots) <= 1 / sqrt(N_shots)
```

For the full Hamiltonian with M Pauli terms:

```
epsilon_total = sqrt(sum_i alpha_i^2 / N_shots_i)
```

To achieve total error epsilon with equal shots per term:

```
N_total = M * (sum_i |alpha_i|)^2 / epsilon^2
```

### 5.2 Barren Plateaus

For random parameterized circuits, the variance of the cost function gradient can vanish exponentially with the number of qubits:

```
Var[dC/d(theta_j)] = O(1/2^n)
```

This means that for large n, the gradient landscape becomes exponentially flat, making optimization intractable. This is the **barren plateau** problem (McClean et al., 2018).

**Mitigation strategies:**
- Use problem-inspired ansatze (e.g., UCCSD)
- Initialize parameters close to the identity
- Use local cost functions instead of global ones
- Layer-wise training (growing the circuit gradually)

---

## 6. Worked Example: H_2 Molecule Ground State

### Problem Setup

The hydrogen molecule H_2 in the STO-3G minimal basis set can be mapped to a 2-qubit Hamiltonian (after symmetry reduction):

```
H = g_0 * II + g_1 * ZI + g_2 * IZ + g_3 * ZZ + g_4 * XX + g_5 * YY
```

At the equilibrium bond length (0.735 A), typical coefficients are:

```
g_0 = -0.8105, g_1 = 0.1721, g_2 = -0.2257, g_3 = 0.1721, g_4 = 0.0454, g_5 = 0.0454
```

### Ansatz

Use a simple 2-qubit ansatz:

```
|psi(theta)> = CNOT_{01} * (R_Y(theta) tensor I) |00>
             = cos(theta/2) |00> + sin(theta/2) |11>
```

This creates a state in the subspace {|00>, |11>}, parameterized by a single angle theta.

### Energy Landscape

```
E(theta) = g_0 + g_1 cos(theta) + g_2 cos(theta) + g_3 cos^2(theta) - g_3 sin^2(theta)
         + (g_4 + g_5) sin^2(theta/2) cos^2(theta/2) ... [simplified]
```

The exact energy landscape can be computed analytically. The minimum occurs at theta* ≈ 2.84 rad, giving E(theta*) ≈ -1.137 Ha, which matches the exact ground-state energy of H_2 at this geometry.

### Optimization Trace

Starting from theta_0 = 0:

```
Iteration 0:  theta = 0.000, E = -0.6917 Ha
Iteration 5:  theta = 1.523, E = -1.0512 Ha
Iteration 10: theta = 2.514, E = -1.1205 Ha
Iteration 15: theta = 2.804, E = -1.1361 Ha
Iteration 20: theta = 2.839, E = -1.1373 Ha  (converged)
```

Exact energy: E_0 = -1.1373 Ha (Full Configuration Interaction)

---

## 7. VQE Variants and Extensions

### 7.1 Adapt-VQE
Grows the ansatz iteratively by selecting operators from a pool based on the gradient magnitude. This avoids the problem of choosing an ansatz a priori.

### 7.2 Subspace-Search VQE (SSVQE)
Extends VQE to find excited states by orthogonalizing against previously found states.

### 7.3 Weighted VQE
Uses CVaR (Conditional Value at Risk) to focus on the tail of the energy distribution, improving convergence for combinatorial optimization problems.

---

## 8. References

1. Peruzzo, A., et al. "A variational eigenvalue solver on a photonic quantum processor." Nature Communications 5, 4213 (2014).
2. McClean, J. R., et al. "The theory of variational hybrid quantum-classical algorithms." New Journal of Physics 18, 023023 (2016).
3. McClean, J. R., et al. "Barren plateaus in quantum neural network training landscapes." Nature Communications 9, 4812 (2018).
4. Kandala, A., et al. "Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets." Nature 549, 242-246 (2017).
5. Grimsley, H. R., et al. "An adaptive variational algorithm for exact molecular simulations on a quantum computer." Nature Communications 10, 3007 (2019).
6. Tilly, J., et al. "The Variational Quantum Eigensolver: A review of methods and best practices." Physics Reports 986, 1-128 (2022).
