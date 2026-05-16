# Quantum Support Vector Classifier (QSVC) - Physicist's Deep Dive

## 1. Overview

The Quantum Support Vector Classifier (QSVC) is a quantum machine learning algorithm that leverages quantum feature maps to construct kernel functions for classical Support Vector Machine (SVM) classification. The central idea is that a quantum computer can efficiently compute kernel functions in exponentially large Hilbert spaces where classical kernels cannot reach, potentially providing a classification advantage for certain data distributions.

QSVC is **not** a fully quantum algorithm: the kernel matrix is computed on a quantum device, but the optimization (finding support vectors) is solved classically. This hybrid structure makes it one of the most practical near-term QML algorithms.

---

## 2. Classical SVM Recap

### 2.1 Primal Formulation

Given a training set {(x_i, y_i)}_{i=1}^{N} with x_i in R^d, y_i in {-1, +1}, the SVM finds a separating hyperplane that maximizes the margin.

**Hard margin (linearly separable case):**
```
minimize     (1/2) ||w||^2
subject to   y_i (w^T x_i + b) >= 1,   for all i = 1, ..., N
```

**Soft margin (C-SVM):**
```
minimize     (1/2) ||w||^2 + C * sum_{i=1}^{N} xi_i
subject to   y_i (w^T x_i + b) >= 1 - xi_i,   xi_i >= 0
```

where C > 0 is the regularization parameter controlling the trade-off between margin width and classification error, and xi_i are slack variables.

### 2.2 Dual Formulation

Introducing Lagrange multipliers alpha_i >= 0, the dual problem is:

```
maximize     sum_i alpha_i - (1/2) sum_{i,j} alpha_i alpha_j y_i y_j K(x_i, x_j)
subject to   0 <= alpha_i <= C,   sum_i alpha_i y_i = 0
```

The key insight: the data x_i only appears through the **kernel function** K(x_i, x_j). This is the "kernel trick" -- we never need to compute the feature map phi(x) explicitly, only its inner products.

### 2.3 The Kernel Trick

Define a feature map phi: R^d -> H (a higher-dimensional Hilbert space). The kernel function is:

```
K(x_i, x_j) = <phi(x_i), phi(x_j)>_H
```

Common classical kernels:
- **Linear:** K(x, y) = x^T y
- **Polynomial:** K(x, y) = (gamma * x^T y + r)^d
- **RBF (Gaussian):** K(x, y) = exp(-gamma ||x - y||^2)

**Mercer's theorem** guarantees that any positive semi-definite function K can be expressed as an inner product in some feature space.

### 2.4 Decision Function

The classifier is:

```
f(x) = sign(sum_{i in SV} alpha_i y_i K(x_i, x) + b)
```

where SV is the set of support vectors (data points with alpha_i > 0).

---

## 3. Quantum Kernels

### 3.1 Quantum Feature Map

A quantum feature map is a unitary circuit U_phi(x) that encodes a classical data point x in R^d into a quantum state:

```
|phi(x)> = U_phi(x) |0>^n
```

The quantum feature space is the 2^n-dimensional Hilbert space of n qubits. The encoding circuit U_phi(x) maps classical data into this exponentially large space.

### 3.2 Quantum Kernel Definition

The quantum kernel is the fidelity between two encoded quantum states:

```
K_Q(x_i, x_j) = |<phi(x_i)|phi(x_j)>|^2 = |<0|^n U_phi(x_i)^dag U_phi(x_j) |0>^n|^2
```

This is a valid kernel because:
1. K_Q(x_i, x_j) = |<phi(x_i)|phi(x_j)>|^2 >= 0
2. K_Q(x_i, x_i) = |<phi(x_i)|phi(x_i)>|^2 = 1
3. K_Q(x_i, x_j) = K_Q(x_j, x_i) (symmetry)
4. The kernel matrix K_{ij} = K_Q(x_i, x_j) is positive semi-definite (Gram matrix of transition amplitudes)

**Proof of PSD property:**

Define the matrix of transition amplitudes A_{ij} = <phi(x_i)|phi(x_j)>. Then K = A (*) A* (Hadamard product of A with its conjugate), which is PSD by the Schur product theorem since A is PSD (being a Gram matrix).

### 3.3 Circuit for Kernel Computation

To compute K_Q(x_i, x_j) on a quantum computer:

```
|0>^n --[U_phi(x_j)]--[U_phi(x_i)^dag]--[Measure]-->

Probability of measuring |0>^n = |<0|^n U_phi(x_i)^dag U_phi(x_j) |0>^n|^2 = K_Q(x_i, x_j)
```

This is a **swap test** variant (inversion test) that requires only 2 * depth(U_phi) circuit depth.

### 3.4 Fidelity Quantum Kernel

In Qiskit, the `FidelityQuantumKernel` implements this computation. It uses the `ComputeUncompute` fidelity circuit:

```
Circuit = U_phi(x_j) followed by U_phi(x_i)^dag

K_Q(x_i, x_j) = Prob(|0...0>) from this circuit
```

This avoids the overhead of ancilla qubits required by the standard swap test.

---

## 4. Feature Map Design

### 4.1 ZFeatureMap

Encodes each feature x_k into a single-qubit Z rotation:

```
U_Z(x) = [prod_{l=1}^{r} H^n * prod_{k=1}^{n} exp(i x_k Z_k)] |0>^n
```

where r is the number of repetitions (reps).

This creates no entanglement between qubits. The resulting kernel is a product kernel:
```
K_Z(x, y) = prod_k cos^2((x_k - y_k)/2)
```

### 4.2 ZZFeatureMap

Adds pairwise entangling ZZ interactions:

```
U_ZZ(x) = [prod_{l=1}^{r} H^n * prod_k exp(i x_k Z_k) * prod_{k<m} exp(i (pi - x_k)(pi - x_m) Z_k Z_m)]
```

The ZZ interaction creates entanglement and introduces nonlinear features:
```
(pi - x_k)(pi - x_m)
```

This is the most commonly used feature map for QSVC because:
- It creates genuine quantum correlations (entanglement)
- The kernel is classically intractable for sufficient reps and qubits
- The nonlinear feature interaction (pi - x_k)(pi - x_m) captures pairwise data relationships

### 4.3 PauliFeatureMap (General)

Configurable feature map with arbitrary Pauli strings:

```
U_P(x) = prod_{l=1}^{r} [H^n * prod_{S in Paulis} exp(i * phi_S(x) * prod_{k in S} P_k)]
```

where phi_S(x) = x_k (for single Paulis) or phi_S(x) = (pi - x_k)(pi - x_m) (for pairs).

### 4.4 Data Encoding Functions

The encoding function phi_S(x) determines the complexity of the feature map:

```
First-order:   phi_{k}(x) = x_k
Second-order:  phi_{k,m}(x) = (pi - x_k)(pi - x_m)
Custom:        phi_S(x) = arbitrary function of x
```

The choice of encoding function directly affects the expressiveness and inductive bias of the kernel.

---

## 5. QSVC Algorithm

### 5.1 Training Phase

**Input:** Training data {(x_i, y_i)}_{i=1}^{N}

**Step 1: Compute the Kernel Matrix**

For all pairs (i, j), compute:
```
K_{ij} = |<0|^n U_phi(x_i)^dag U_phi(x_j) |0>^n|^2
```

This requires O(N^2) quantum circuit evaluations (each with O(shots) measurements).

For N training samples, the kernel matrix K is an N x N symmetric PSD matrix with K_{ii} = 1.

**Step 2: Solve Classical SVM**

Pass the precomputed kernel matrix K to a classical SVM solver (e.g., scikit-learn's SVC with `kernel='precomputed'`):

```
maximize     sum_i alpha_i - (1/2) sum_{i,j} alpha_i alpha_j y_i y_j K_{ij}
subject to   0 <= alpha_i <= C,   sum_i alpha_i y_i = 0
```

This is a standard quadratic program with complexity O(N^2) to O(N^3).

**Output:** Support vectors {x_s}_{s in SV}, dual coefficients {alpha_s}, bias b.

### 5.2 Inference Phase

**Input:** Test point x_new

**Step 1: Compute kernel with support vectors**

For each support vector x_s:
```
K(x_s, x_new) = |<phi(x_s)|phi(x_new)>|^2
```

This requires |SV| quantum circuit evaluations.

**Step 2: Classify**

```
y_pred = sign(sum_{s in SV} alpha_s y_s K(x_s, x_new) + b)
```

### 5.3 Total Quantum Resource Estimate

| Phase | Quantum circuits | Shots per circuit | Total shots |
|-------|-----------------|-------------------|-------------|
| Training kernel | N(N+1)/2 | S | S * N^2 / 2 |
| Prediction (M test points) | M * |SV| | S | S * M * |SV| |

Typically |SV| << N, so prediction is much cheaper than training.

---

## 6. Computational Complexity Analysis

### 6.1 Classical SVM Complexity

- Kernel computation: O(N^2 * d) where d is the feature dimension
- QP solver: O(N^2) to O(N^3)
- Prediction: O(|SV| * d) per test point

### 6.2 Quantum Kernel Complexity

- **Kernel circuit depth:** O(r * n) where r is the number of reps and n is the number of qubits
- **Kernel matrix computation:** O(N^2) circuits, each requiring O(S) shots, where S = O(1/epsilon^2) for precision epsilon
- **Total quantum time:** O(N^2 * S * depth(U_phi))
- **Classical QP solver:** O(N^2) to O(N^3) (same as classical)

### 6.3 When Does Quantum Win?

The potential quantum advantage comes from the **kernel function evaluation**, not the optimization. Specifically:

1. **Expressiveness:** The quantum kernel K_Q operates in a 2^n-dimensional feature space. Computing it classically requires simulating the quantum circuit, which scales as O(4^n).

2. **Havlicek et al. (2019) result:** There exist data distributions for which:
   - The quantum kernel achieves perfect classification
   - Any classical kernel of polynomial size fails
   - These distributions are based on the discrete logarithm problem

3. **Practical caveat:** For most real-world datasets, classical kernels (RBF, polynomial) perform comparably or better. The quantum advantage is proven only for contrived (cryptographic) distributions.

4. **Huang et al. (2021) framework:** Defined "quantum kernel advantage" rigorously:
   - Compute the geometric difference g(K_C, K_Q) between classical and quantum kernels
   - If g >> 1, the quantum kernel provides an advantage
   - For most real datasets tested, g ~ 1 (no advantage)

### 6.4 The Curse of Exponential Feature Space

For large n, the quantum feature space is exponentially large. This can lead to:

```
K_Q(x_i, x_j) -> delta_{ij}   (exponential concentration)
```

When the kernel matrix approaches the identity, every point is equally "far" from every other, and the SVM cannot generalize. This is analogous to overfitting in exponentially high-dimensional spaces.

**Mitigation:**
- Use shallow feature maps (small reps)
- Project data to match the qubit count (n ~ log(d) or n ~ d)
- Use projected quantum kernels (Huang et al., 2021)

---

## 7. Projected Quantum Kernels

To combat exponential concentration, Huang et al. proposed projected quantum kernels:

```
K_proj(x_i, x_j) = exp(-gamma * sum_k ||rho_k(x_i) - rho_k(x_j)||_F^2)
```

where rho_k(x) = Tr_{not k}(|phi(x)><phi(x)|) is the reduced density matrix of qubit k.

This projects from the 2^n-dimensional space to an O(n)-dimensional classical shadow, avoiding exponential concentration while retaining quantum correlations.

---

## 8. Connection to Reproducing Kernel Hilbert Spaces

### 8.1 RKHS Framework

The quantum kernel K_Q defines a reproducing kernel Hilbert space (RKHS) H_Q with:

```
f(x) = <f, K_Q(x, .)>_{H_Q}
```

The representer theorem guarantees that the optimal classifier lies in the span of the kernel evaluated at training points:

```
f*(x) = sum_{i=1}^{N} alpha_i K_Q(x_i, x)
```

### 8.2 Feature Map Interpretation

The quantum feature map phi: R^d -> C^{2^n} induces the kernel:

```
K_Q(x, y) = |<phi(x)|phi(y)>|^2
```

Note: this is the **squared** inner product, not the inner product itself. This means K_Q is not the standard inner product kernel in C^{2^n}, but rather corresponds to the inner product in the **symmetric tensor product** space (or equivalently, the space of density matrices).

---

## 9. Noise Effects and Error Mitigation

### 9.1 Noise Model

On noisy hardware, the ideal kernel is corrupted:

```
K_noisy(x_i, x_j) = K_ideal(x_i, x_j) * F_device + (1 - F_device) / 2^n
```

where F_device is the effective circuit fidelity. As circuit depth increases, F_device -> 0 and:

```
K_noisy -> 1/2^n * Identity  (uniform noise floor)
```

### 9.2 Error Mitigation for Kernels

1. **Readout error mitigation:** Apply the inverse confusion matrix to measurement outcomes
2. **Zero-noise extrapolation (ZNE):** Run at multiple noise levels, extrapolate to zero noise
3. **Kernel matrix regularization:** Add lambda * I to the kernel matrix (equivalent to L2 regularization of SVM weights)
4. **Symmetrization:** Enforce K_{ij} = K_{ji} by averaging

---

## 10. References

1. Havlicek, V., et al. "Supervised learning with quantum-enhanced feature spaces." Nature 567, 209-212 (2019).
2. Schuld, M., & Killoran, N. "Quantum Machine Learning in Feature Hilbert Spaces." Physical Review Letters 122, 040504 (2019).
3. Huang, H.-Y., et al. "Power of data in quantum machine learning." Nature Communications 12, 2631 (2021).
4. Kubler, J., Buchholz, S., & Scholkopf, B. "The Inductive Bias of Quantum Kernels." NeurIPS 2021.
5. Thanasilp, S., et al. "Exponential concentration and untrainability in quantum kernel methods." arXiv:2208.11060 (2022).
6. Liu, Y., Arunachalam, S., & Temme, K. "A rigorous and robust quantum speed-up in supervised machine learning." Nature Physics 17, 1013-1017 (2021).
7. Vapnik, V. N. "The Nature of Statistical Learning Theory." Springer, 2nd ed. (2000).
8. Scholkopf, B., & Smola, A. J. "Learning with Kernels." MIT Press (2002).
