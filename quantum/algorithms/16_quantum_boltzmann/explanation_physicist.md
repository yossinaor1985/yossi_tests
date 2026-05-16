# Quantum Boltzmann Machines (QBM) - Physicist's Deep Dive

## 1. Overview

Quantum Boltzmann Machines (QBMs) are quantum generalizations of classical Boltzmann machines -- energy-based generative models that learn probability distributions. The key enhancement: replacing the classical energy function with a quantum Hamiltonian, enabling the model to exploit quantum tunneling and superposition to represent distributions inaccessible to classical Boltzmann machines.

---

## 2. Classical Boltzmann Machine Recap

### 2.1 Energy-Based Model

A classical Boltzmann machine assigns an energy to each configuration v = (v_1, ..., v_n) of binary units:

```
E(v) = -sum_{i<j} J_ij v_i v_j - sum_i h_i v_i
```

The probability of configuration v follows the Gibbs distribution:

```
P(v) = exp(-beta * E(v)) / Z
```

where Z = sum_v exp(-beta * E(v)) is the partition function and beta = 1/(k_B T).

### 2.2 Restricted Boltzmann Machine (RBM)

An RBM has visible units v and hidden units h with bipartite connectivity:

```
E(v, h) = -v^T W h - b^T v - c^T h
```

The marginal over visible units:
```
P(v) = sum_h exp(-E(v,h)) / Z
```

Training via contrastive divergence: maximize log-likelihood of training data.

### 2.3 Limitations

Classical BMs can only represent distributions arising from diagonal Hamiltonians (classical Ising-type). They cannot natively capture quantum correlations or distributions with complex interference patterns.

---

## 3. Quantum Boltzmann Machine

### 3.1 Quantum Hamiltonian

The QBM replaces the classical energy function with a quantum Hamiltonian:

```
H = -sum_{i<j} J_ij Z_i Z_j - sum_i h_i Z_i - sum_i Gamma_i X_i
```

The first two terms are the classical Ising Hamiltonian. The third term adds **transverse field** interactions (X_i = sigma_x on qubit i), introducing quantum effects:
- Superposition of spin configurations
- Quantum tunneling through energy barriers
- Off-diagonal elements in the density matrix

### 3.2 Thermal State

The QBM models the quantum Gibbs (thermal) state:

```
rho = exp(-beta H) / Z
```

where Z = Tr[exp(-beta H)] is the quantum partition function.

For a purely diagonal H (Gamma_i = 0), rho reduces to a classical Gibbs distribution. The transverse field terms create genuinely quantum thermal states with coherences.

### 3.3 Measurement Outcomes

When we measure the thermal state rho in the computational basis, the probability of outcome z is:

```
P(z) = <z| rho |z>
```

This is the distribution the QBM aims to match to the training data.

---

## 4. Training

### 4.1 Objective: Quantum Relative Entropy

The training objective is to minimize the quantum relative entropy between the target distribution (from training data) and the model distribution:

```
S(sigma || rho) = Tr[sigma (log sigma - log rho)]
```

where sigma encodes the training data and rho = exp(-beta H)/Z is the model state.

### 4.2 Gradient of the Objective

For a parameter lambda (e.g., J_ij, h_i, or Gamma_i):

```
dS/d(lambda) = beta * [<dH/d(lambda)>_rho - <dH/d(lambda)>_sigma]
```

This has a form reminiscent of contrastive divergence:
- "Positive phase": expectation under data distribution (clamped)
- "Negative phase": expectation under model distribution (free-running)

### 4.3 Variational QBM

Since preparing exact Gibbs states is hard, a practical approach uses a variational circuit to approximate the thermal state:

```
rho_theta = |psi(theta)><psi(theta)|
```

where |psi(theta)> is prepared by a parameterized circuit. The variational parameters theta are optimized to minimize the KL divergence between the measurement distribution of rho_theta and the target distribution.

### 4.4 Golden-Thompson Inequality

Amin et al. (2018) proposed a bound-based training method using the Golden-Thompson inequality:

```
Tr[exp(A + B)] <= Tr[exp(A) * exp(B)]
```

This provides an upper bound on the partition function, leading to a tractable training objective.

---

## 5. Quantum Advantage

### 5.1 Tunneling Through Barriers

Classical Boltzmann machines explore the energy landscape via thermal fluctuations. QBMs additionally exploit quantum tunneling, enabling faster exploration of multimodal distributions.

### 5.2 Richer Distributions

The transverse field creates distributions with quantum coherences that have no classical analog. Specifically, a QBM with n qubits can represent distributions that require exponentially many hidden units in a classical RBM.

### 5.3 Computational Complexity

Preparing thermal states is QMA-hard in general. Practical implementations use:
- Variational approximation (VQE-like)
- Quantum imaginary time evolution
- Trotterized Gibbs state preparation

---

## 6. Worked Example: 2-Qubit QBM

Consider H = -J Z_1 Z_2 - Gamma (X_1 + X_2) with J = 1, Gamma = 0.5, beta = 1.

The 4x4 Hamiltonian matrix:
```
H = -J Z_1 Z_2 - Gamma(X_1 + X_2)
  = -[|00><00| - |01><01| - |10><10| + |11><11|]
    -0.5[|01><00| + |00><01| + |11><10| + |10><11|
         + |10><00| + |00><10| + |11><01| + |01><11|]
```

Diagonalizing and computing rho = exp(-H)/Z gives a non-trivial distribution over {00, 01, 10, 11} with quantum correlations.

---

## 7. References

1. Amin, M. H., et al. "Quantum Boltzmann Machine." Physical Review X 8, 021050 (2018).
2. Kieferova, M. & Wiebe, N. "Tomography and generative training with quantum Boltzmann machines." Physical Review A 96, 062327 (2017).
3. Zoufal, C., Lucchi, A., & Woerner, S. "Variational quantum Boltzmann machines." Quantum Machine Intelligence 3, 7 (2021).
4. Hinton, G. E. "Training products of experts by minimizing contrastive divergence." Neural Computation 14, 1771-1800 (2002).
5. Kappen, H. J. "Learning quantum models from quantum or classical data." Journal of Physics A 53, 214003 (2020).