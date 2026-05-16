# Quantum Kernel Methods (FidelityQuantumKernel) - Physicist's Deep Dive

## 1. Overview

Quantum kernel methods represent one of the most mathematically rigorous pathways to quantum advantage in machine learning. The central idea is deceptively simple: use a quantum computer to evaluate inner products in an exponentially large Hilbert space that no classical computer can efficiently access.

Rather than training variational parameters on a quantum circuit (as in VQC or QNN), kernel methods offload all optimization to a classical SVM or other kernel-based algorithm. The quantum computer is used only to compute the kernel matrix -- the pairwise similarity between data points as measured in quantum state space.

This topic is foundational for Topics 11-18 (QSVC, VQC, QNN, VQR, hybrid networks, Boltzmann machines, QGANs, and quantum reservoir computing), all of which build on the quantum feature map and kernel concepts developed here.

---

## 2. Classical Kernel Methods Recap

### 2.1 The Kernel Trick

Consider a binary classification problem with data {(x_i, y_i)} where x_i in R^d and y_i in {-1, +1}. A linear classifier finds a hyperplane w . x + b = 0. But many datasets are not linearly separable in the original space.

The kernel trick maps data into a higher-dimensional feature space via phi: R^d -> F, then finds a linear separator in F:

```
f(x) = w . phi(x) + b
```

The key insight (due to Aizerman, 1964; popularized by Vapnik, 1995): the optimization problem for SVM depends on the data only through inner products phi(x_i) . phi(x_j). We never need to compute phi(x) explicitly -- we only need the **kernel function**:

```
K(x_i, x_j) = <phi(x_i), phi(x_j)>
```

### 2.2 Mercer's Theorem

A function K: X x X -> R is a valid kernel (i.e., corresponds to an inner product in some feature space F) if and only if K is a **positive semi-definite kernel**:

```
For all N, for all {x_1, ..., x_N}, for all {c_1, ..., c_N} in R:
    sum_{i,j} c_i c_j K(x_i, x_j) >= 0
```

Equivalently, the Gram matrix K_{ij} = K(x_i, x_j) must be positive semi-definite.

**Mercer's theorem** (1909): If K is a continuous, symmetric, positive semi-definite kernel on a compact domain X, then there exists a (possibly infinite-dimensional) feature space F and a map phi: X -> F such that:

```
K(x, y) = sum_{k=0}^{infinity} lambda_k * e_k(x) * e_k(y)
```

where {lambda_k} are non-negative eigenvalues and {e_k} are eigenfunctions. The feature map is phi(x) = (sqrt(lambda_0) e_0(x), sqrt(lambda_1) e_1(x), ...).

### 2.3 Common Classical Kernels

| Kernel | Formula | Feature Space Dimension |
|--------|---------|------------------------|
| Linear | K(x,y) = x . y | d |
| Polynomial | K(x,y) = (x . y + c)^p | C(d+p, p) |
| RBF/Gaussian | K(x,y) = exp(-\|\|x-y\|\|^2 / 2sigma^2) | infinite |

The RBF kernel maps into an infinite-dimensional feature space, which is why SVMs with RBF kernels are so powerful. Quantum kernels take this further by mapping into an exponentially large but finite-dimensional space.

---

## 3. Quantum Feature Maps: Encoding Data into Hilbert Space

### 3.1 The Quantum Feature Map

A quantum feature map is a unitary circuit U_phi(x) that encodes a classical data point x in R^d into a quantum state in an n-qubit Hilbert space H = (C^2)^{tensor n}:

```
|phi(x)> = U_phi(x) |0>^n  in  C^{2^n}
```

This is a map phi: R^d -> C^{2^n}, embedding d-dimensional classical data into a 2^n-dimensional Hilbert space. For n qubits, the feature space has dimension 2^n -- exponential in the number of qubits.

### 3.2 ZFeatureMap

The simplest feature map uses single-qubit Z rotations:

```
U_Z(x) = [prod_{l=1}^{r} H^{tensor n} * prod_{i=1}^{n} exp(i x_i Z_i)]
```

For a single layer (r=1) on qubit i, the data encoding is:

```
H * R_Z(2 x_i) |0> = H * [exp(-i x_i) |0> + exp(i x_i) |1>] / ...
```

Working through the algebra for one qubit:

```
|0> -> H -> |+> = (|0> + |1>)/sqrt(2)
    -> R_Z(2x) -> (exp(-ix)|0> + exp(ix)|1>)/sqrt(2)
```

This encodes x_i into the relative phase of the qubit. With n qubits, each data feature x_i is encoded independently -- there are no cross-feature correlations.

### 3.3 ZZFeatureMap (Key for Quantum Kernels)

The ZZFeatureMap adds pairwise entangling interactions, creating non-trivial correlations between features:

```
U_ZZ(x) = prod_{l=1}^{r} [H^{tensor n} * prod_i exp(i x_i Z_i) * prod_{i<j} exp(i (pi - x_i)(pi - x_j) Z_i Z_j)]
```

The ZZ interaction term for qubits i, j is:

```
exp(i (pi - x_i)(pi - x_j) Z_i Z_j)
```

This two-qubit gate creates entanglement that depends on the product of two features. The function (pi - x_i)(pi - x_j) is chosen so that:
- It is symmetric in (x_i, x_j)
- It is zero when either x_i = pi or x_j = pi (creating a natural "center")
- It produces non-linear feature interactions in the kernel

**Circuit decomposition of exp(i phi Z_i Z_j):**

```
--*--------*--
  |        |
--X--RZ(2phi)--X--
```

(CNOT, RZ on target, CNOT)

### 3.4 PauliFeatureMap (Generalization)

The PauliFeatureMap generalizes to arbitrary Pauli strings:

```
U_P(x) = prod_{l=1}^{r} [H^{tensor n} * prod_{S in P} exp(i phi_S(x) * tensor_{j in S} sigma_j)]
```

where P is a set of Pauli strings (e.g., {Z, ZZ, XZ, YY}) and phi_S(x) is a data-encoding function for each string S.

---

## 4. The Quantum Kernel

### 4.1 Fidelity Kernel Definition

Given a quantum feature map U_phi(x), the **fidelity quantum kernel** is defined as:

```
K(x_i, x_j) = |<phi(x_i)|phi(x_j)>|^2
             = |<0|^n U_phi(x_i)^dagger U_phi(x_j) |0>^n|^2
             = Tr[|phi(x_i)><phi(x_i)| * |phi(x_j)><phi(x_j)|]
```

This is the **transition probability** (fidelity) between the two quantum states. It satisfies:
- K(x, x) = 1 (self-similarity is maximal)
- 0 <= K(x, y) <= 1 (bounded)
- K(x, y) = K(y, x) (symmetric)

### 4.2 Proof that the Fidelity Kernel is a Valid Kernel

**Claim:** K(x_i, x_j) = |<phi(x_i)|phi(x_j)>|^2 is a positive semi-definite kernel.

**Proof:**

Write the quantum state in the computational basis:

```
|phi(x)> = sum_{k=0}^{2^n - 1} alpha_k(x) |k>
```

Then:

```
K(x_i, x_j) = |<phi(x_i)|phi(x_j)>|^2
             = |sum_k alpha_k(x_i)* alpha_k(x_j)|^2
             = [sum_k alpha_k(x_i)* alpha_k(x_j)] * [sum_l alpha_l(x_i) alpha_l(x_j)*]
             = sum_{k,l} [alpha_k(x_i)* alpha_l(x_i)] * [alpha_k(x_j) alpha_l(x_j)*]
```

Define the feature vector in the "squared" feature space:

```
Phi_{kl}(x) = alpha_k(x)* alpha_l(x)
```

Then K(x_i, x_j) = sum_{k,l} Phi_{kl}(x_i)* Phi_{kl}(x_j) = <Phi(x_i), Phi(x_j)>.

This is an inner product in a (2^n)^2 = 4^n dimensional feature space, hence K is PSD by construction. QED.

**Key insight:** The fidelity kernel implicitly operates in a 4^n-dimensional feature space -- doubly exponential in the number of qubits! This is because it uses the squared amplitudes (density matrix elements), not just the state amplitudes.

### 4.3 Circuit for Kernel Evaluation

To evaluate K(x_i, x_j), we use the circuit:

```
|0>^n -> U_phi(x_j) -> U_phi(x_i)^dagger -> Measure all qubits
```

The probability of measuring the all-zeros outcome |0...0> is exactly K(x_i, x_j):

```
P(0...0) = |<0|^n U_phi(x_i)^dagger U_phi(x_j) |0>^n|^2 = K(x_i, x_j)
```

**Shot budget:** To estimate K(x_i, x_j) with precision epsilon, we need O(1/epsilon^2) shots. For a dataset of N points, we need N(N-1)/2 unique kernel entries, so total shots ~ N^2 / epsilon^2.

### 4.4 Worked Example: 1-Qubit ZFeatureMap Kernel

Consider n=1 qubit, ZFeatureMap with r=1 layer. For data point x:

```
|phi(x)> = H * R_Z(2x) * H |0>
```

Step by step:
```
|0> -> H -> (|0> + |1>)/sqrt(2)
     -> R_Z(2x) -> (e^{-ix}|0> + e^{ix}|1>)/sqrt(2)
     -> H -> e^{-ix}(|0>+|1>)/2 + e^{ix}(|0>-|1>)/2
           = cos(x)|0> - i*sin(x)|1>      ... (up to global phase)
```

Wait -- let me be more careful. With the standard ZFeatureMap encoding:

```
|phi(x)> = H R_Z(2x) H |0>
         = H R_Z(2x) |+>
```

R_Z(2x) |+> = (e^{-ix}|0> + e^{ix}|1>)/sqrt(2)

H applied: = e^{-ix}(|0>+|1>)/2 + e^{ix}(|0>-|1>)/2
           = [(e^{-ix}+e^{ix})/2]|0> + [(e^{-ix}-e^{ix})/2]|1>
           = cos(x)|0> - i sin(x)|1>
```

The kernel is:

```
K(x_1, x_2) = |<phi(x_1)|phi(x_2)>|^2
            = |cos(x_1)cos(x_2) + sin(x_1)sin(x_2)|^2
            = |cos(x_1 - x_2)|^2
            = cos^2(x_1 - x_2)
```

This is a periodic kernel! It measures similarity based on the difference x_1 - x_2 modulo pi.

### 4.5 Worked Example: 2-Qubit ZZFeatureMap Kernel

For n=2 qubits with ZZFeatureMap (r=1), the feature map is:

```
U_ZZ(x) = exp(i(pi - x_1)(pi - x_2) Z_1 Z_2) * R_Z(2x_2) * R_Z(2x_1) * H^2
```

The state |phi(x)> lives in C^4, and the kernel K(x, y) is a function of the four quantities x_1, x_2, y_1, y_2. Due to the ZZ interaction, the kernel captures non-linear correlations between features x_1 and x_2 -- something a simple product of 1-qubit kernels cannot do.

The kernel evaluates to:

```
K(x, y) = |a_1 a_2 + cross terms from ZZ interaction|^2
```

The ZZ interaction term exp(i phi Z_1 Z_2) introduces a data-dependent phase that creates correlations between features. This is precisely what gives the quantum kernel its power over separable (product) feature maps.

---

## 5. Quantum Kernel Advantage

### 5.1 The Promise: Exponential Feature Space

A classical computer representing a d-dimensional data point in a 2^n-dimensional feature space would require O(2^n) memory and computation. The quantum feature map achieves this implicitly:

- The quantum state |phi(x)> has 2^n amplitudes
- The kernel K(x, y) accesses the full 2^n-dimensional inner product
- The kernel evaluation circuit has depth O(poly(n)), not O(2^n)

**The key efficiency:** We never need to store or manipulate the 2^n-dimensional feature vector. We only need the O(N^2) kernel matrix entries.

### 5.2 When Does Quantum Advantage Exist?

Havlicek et al. (2019) showed that quantum kernel advantage requires:

1. **Hardness of classical simulation:** The kernel K(x, y) cannot be efficiently computed classically. This is expected when:
   - The feature map circuit generates highly entangled states
   - The circuit is deep enough that classical simulation is intractable
   - The data encoding uses non-Clifford gates

2. **Relevance to the classification problem:** The quantum feature space must align with the structure of the data. A random quantum kernel is useless even if classically hard to compute.

### 5.3 Formal Conditions for Advantage (Liu et al., 2021)

Liu et al. proved that quantum kernel methods can achieve exponential advantage for problems with specific group-theoretic structure:

**Theorem (informal):** There exist classification problems for which:
- The quantum kernel achieves zero generalization error with polynomial data
- Any classical method requires exponential data or computation

The proof constructs an explicit problem based on the discrete logarithm, where the quantum feature map naturally exploits the group structure.

### 5.4 Limitations and the "Curse of Exponentiality"

Thanasilp et al. (2022) showed a fundamental limitation:

**Theorem:** For generic quantum kernels with sufficiently expressive feature maps, the kernel values concentrate exponentially:

```
K(x_i, x_j) -> 2^{-n}  for  x_i != x_j  as  n -> infinity
```

with exponentially small variance. This means the kernel matrix approaches the identity matrix, making the SVM trivial (memorization without generalization).

**Mitigation strategies:**
1. Use shallow feature maps (low circuit depth)
2. Use problem-informed feature maps (encode domain knowledge)
3. Use quantum kernel alignment to optimize the feature map
4. Restrict to modest qubit counts where kernel values are not yet concentrated

---

## 6. Quantum Kernel Alignment

### 6.1 The Alignment Problem

Given a training set {(x_i, y_i)}, the ideal kernel matrix is:

```
K*_{ij} = y_i * y_j
```

(positive for same-class pairs, negative for different-class pairs). Kernel alignment measures how well a given kernel K matches this ideal:

```
A(K, K*) = <K, K*>_F / (||K||_F * ||K*||_F)
```

where <K, K*>_F = sum_{i,j} K_{ij} K*_{ij} is the Frobenius inner product.

### 6.2 Quantum Kernel Alignment (QKA)

The QKA algorithm (Glick et al., 2021) parameterizes the feature map with trainable parameters theta:

```
U_phi(x; theta) = prod_l [W_l(theta_l) * S_l(x)]
```

where S_l(x) is a data-encoding layer and W_l(theta) is a trainable variational layer. The kernel becomes:

```
K_theta(x_i, x_j) = |<0| U_phi(x_i; theta)^dagger U_phi(x_j; theta) |0>|^2
```

**Optimization:** Maximize the kernel-target alignment:

```
max_theta A(K_theta, K*)
```

This is a classical optimization over the kernel matrix, using the quantum computer only to evaluate K_theta entries.

### 6.3 Connection to Feature Map Optimization

QKA is equivalent to finding the feature map that best separates the classes in quantum state space. It is conceptually related to metric learning in classical ML: finding the right distance function for the problem.

---

## 7. FidelityQuantumKernel in Qiskit

### 7.1 Architecture in qiskit-machine-learning

The Qiskit implementation uses the `FidelityQuantumKernel` class:

```
FidelityQuantumKernel(feature_map, fidelity)
```

where:
- `feature_map`: A parameterized quantum circuit encoding data (e.g., ZZFeatureMap)
- `fidelity`: A fidelity estimator (e.g., `ComputeFidelity` based on the Sampler primitive)

**Kernel evaluation pipeline:**
1. For each pair (x_i, x_j), construct the fidelity circuit: U(x_i)^dagger U(x_j)
2. Run the circuit on the Sampler primitive
3. Extract P(0...0) as the kernel value
4. Assemble the N x N kernel matrix

### 7.2 Integration with scikit-learn

The kernel matrix K can be passed to any scikit-learn kernel-based algorithm:

```python
from sklearn.svm import SVC
svc = SVC(kernel='precomputed')
svc.fit(K_train, y_train)
y_pred = svc.predict(K_test)  # K_test is the test-vs-train kernel matrix
```

### 7.3 Computational Cost

For a training set of N points:
- Kernel matrix entries: N(N+1)/2 (symmetric)
- Circuits per entry: 1
- Shots per circuit: O(1/epsilon^2)
- Total circuits: O(N^2)
- Total shots: O(N^2 / epsilon^2)

For prediction on M test points:
- Additional circuits: M * N (each test point vs all training points)

---

## 8. Comparison with Other Approaches

### 8.1 Quantum Kernel vs Variational Quantum Classifier (VQC)

| Aspect | Quantum Kernel | VQC |
|--------|---------------|-----|
| Trainable parameters | None (or few for QKA) | Many (O(nL)) |
| Optimization | Classical SVM | Hybrid quantum-classical |
| Barren plateaus | Not applicable | Major concern |
| Circuit evaluations | O(N^2) for kernel matrix | O(iterations * N) |
| Theory | Kernel theory (well-understood) | Variational (less understood) |
| Scalability | Limited by O(N^2) kernel matrix | Better for large datasets |

### 8.2 When to Use Quantum Kernels

**Use quantum kernels when:**
- Dataset is small-to-moderate (N < 1000)
- You want rigorous theoretical guarantees
- The problem has structure matching the quantum feature map
- You want to avoid barren plateaus entirely

**Use VQC/QNN when:**
- Dataset is large
- You need online/streaming learning
- Feature map design is uncertain (let the model learn)

---

## 9. Mathematical Derivations Summary

### 9.1 Kernel Matrix Eigendecomposition

The kernel matrix K in R^{N x N} has eigendecomposition:

```
K = V Lambda V^T
```

where Lambda = diag(lambda_1, ..., lambda_N). For the SVM dual problem, the solution depends on the eigenvectors of K. The number of non-zero eigenvalues equals the rank of K, which is bounded by min(N, 2^n).

### 9.2 Generalization Bound

For SVM with kernel K, the generalization error is bounded by:

```
E[error] <= O(sqrt(R^2 / (N * gamma^2)))
```

where R = max_i sqrt(K(x_i, x_i)) = 1 (for fidelity kernel) and gamma is the margin. Larger margin = better generalization.

### 9.3 Kernel Value Distribution

For a random n-qubit feature map, the expected kernel value for two random data points is:

```
E[K(x, y)] = 1/2^n + (1 - 1/2^n) * delta(x, y)
```

in the limit of a Haar-random feature map. This shows the concentration phenomenon: as n grows, all off-diagonal kernel values approach 1/2^n.

---

## 10. References

1. Havlicek, V., et al. "Supervised learning with quantum-enhanced feature spaces." Nature 567, 209-212 (2019).
2. Schuld, M., & Killoran, N. "Quantum Machine Learning in Feature Hilbert Spaces." Physical Review Letters 122, 040504 (2019).
3. Liu, Y., Arunachalam, S., & Temme, K. "A rigorous and robust quantum speed-up in supervised machine learning." Nature Physics 17, 1013-1017 (2021).
4. Thanasilp, S., et al. "Exponential concentration and untrainability in quantum kernel methods." arXiv:2208.11060 (2022).
5. Glick, J. R., et al. "Covariant quantum kernels for data with group structure." Nature Physics 20, 479-483 (2024).
6. Huang, H.-Y., et al. "Power of data in quantum machine learning." Nature Communications 12, 2631 (2021).
7. Mercer, J. "Functions of positive and negative type, and their connection with the theory of integral equations." Philosophical Transactions A 209, 415-446 (1909).
8. Vapnik, V. "The Nature of Statistical Learning Theory." Springer (1995).
9. Qiskit Machine Learning documentation: https://qiskit-community.github.io/qiskit-machine-learning/
