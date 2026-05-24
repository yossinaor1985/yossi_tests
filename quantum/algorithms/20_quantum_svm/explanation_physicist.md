# Quantum SVM (Rebentrost-Mohseni-Lloyd) - Physicist's Deep Dive

## 1. Overview

The Quantum SVM algorithm of Rebentrost, Mohseni, and Lloyd (2014) is a **fully quantum** machine learning pipeline for binary classification. It promises exponential speedup over classical SVM training under certain assumptions.

**Critical distinction from QSVC (Topic 11):**

| Aspect | QSVC (Topic 11) | QSVM-RML (This Topic) |
|--------|------------------|------------------------|
| Kernel computation | Quantum (fidelity kernel) | Quantum (swap test) |
| Dual optimization | Classical (sklearn SVM solver) | Quantum (HHL algorithm) |
| Classification | Classical (weighted sum) | Quantum (swap test with |alpha>) |
| Data loading | Gate-based encoding | QRAM (assumed) |
| Speedup regime | Heuristic (kernel expressivity) | Provable O(log N) under QRAM |
| Near-term feasibility | Yes (NISQ-compatible) | No (requires QRAM + fault tolerance) |

QSVC replaces only the kernel computation with a quantum subroutine. The QSVM-RML algorithm replaces the **entire pipeline** -- data loading, kernel computation, dual optimization, and classification -- with quantum subroutines. The price is much stronger hardware assumptions.

---

## 2. Classical SVM Dual Recap

### 2.1 Primal Formulation

Given training data {(x_i, y_i)}_{i=1}^{N} with x_i in R^d, y_i in {-1, +1}, the SVM finds the maximum-margin separating hyperplane.

**Soft-margin primal:**
```
minimize     (1/2) ||w||^2 + C * sum_i xi_i
subject to   y_i (w^T phi(x_i) + b) >= 1 - xi_i,  xi_i >= 0
```

### 2.2 Standard Dual Formulation

The Lagrangian dual is:
```
maximize     sum_i alpha_i - (1/2) sum_{i,j} alpha_i alpha_j y_i y_j K(x_i, x_j)
subject to   0 <= alpha_i <= C,  sum_i alpha_i y_i = 0
```

This is a quadratic program (QP). Classical solvers (SMO, interior point) require O(N^2) to O(N^3) time depending on the method.

### 2.3 Least-Squares SVM (LS-SVM)

The Rebentrost et al. algorithm uses the **Least-Squares SVM** formulation, which replaces inequality constraints with equality constraints and uses squared slack variables:

**LS-SVM primal:**
```
minimize     (1/2) ||w||^2 + (gamma/2) sum_i e_i^2
subject to   y_i (w^T phi(x_i) + b) = 1 - e_i
```

The KKT conditions for LS-SVM yield a **linear system** (not a QP):

```
| 0    y^T  | | b |   | 0 |
| y  K+I/gamma | | alpha | = | 1 |
```

Or equivalently, the core linear system is:

```
(K + (1/gamma) I) alpha = y
```

where:
- K is the N x N kernel matrix with K_{ij} = K(x_i, x_j)
- gamma is the regularization parameter
- alpha is the vector of dual variables
- y is the label vector

**This is the key insight**: LS-SVM converts the SVM training problem into a linear system Ax = b, which is exactly what the HHL algorithm solves.

### 2.4 Kernel Trick

The kernel function K(x_i, x_j) = <phi(x_i), phi(x_j)> computes inner products in a (possibly infinite-dimensional) feature space without explicitly constructing phi(x). For the quantum version, the kernel is the inner product of quantum states:

```
K(x_i, x_j) = |<x_i|x_j>|^2
```

where |x_i> is the amplitude-encoded quantum state of data point x_i.

---

## 3. QRAM and Quantum Data Loading

### 3.1 The QRAM Model

Quantum Random Access Memory (QRAM) is a hypothetical device that stores classical data and allows quantum queries. Given N data points of dimension d, a QRAM performs:

```
|i>|0> -> |i>|x_i>
```

in time O(log(Nd)), where |x_i> is the amplitude encoding of data point x_i.

### 3.2 Amplitude Encoding

A data point x = (x_1, ..., x_d) in R^d is encoded as:

```
|x> = (1/||x||) sum_{j=1}^{d} x_j |j>
```

This requires ceil(log_2(d)) qubits. For d-dimensional data, the quantum state lives in a log(d)-qubit space, achieving exponential compression.

### 3.3 Full Data Matrix Encoding

The entire training set X (an N x d matrix) can be loaded into a quantum state:

```
|X> = (1/||X||_F) sum_{i=1}^{N} ||x_i|| |i>|x_i>
```

where ||X||_F is the Frobenius norm. This state encodes both the index of each data point and its contents.

### 3.4 The QRAM Problem

QRAM is the most controversial assumption in quantum machine learning:

1. **No physical implementation exists** at scale (as of 2025)
2. Hardware proposals (bucket-brigade QRAM) require O(Nd) physical qubits
3. Error rates accumulate: each memory call has noise O(Nd * epsilon)
4. Without QRAM, data loading alone takes O(Nd), destroying the speedup

This is not a minor caveat -- it is the central bottleneck of the entire algorithm.

---

## 4. Quantum Kernel Computation

### 4.1 The Swap Test

The swap test computes the squared inner product |<psi|phi>|^2 between two quantum states using a simple circuit:

```
Ancilla: |0> --[H]--[o]--[H]--[M]
                      |
State 1: |psi> ------[SWAP]------
                      |
State 2: |phi> ------[SWAP]------
```

The circuit:
1. Prepare ancilla in |0>, apply Hadamard: (|0> + |1>)/sqrt(2)
2. Apply controlled-SWAP between the two state registers, controlled on the ancilla
3. Apply Hadamard to ancilla
4. Measure ancilla

**Measurement probabilities:**
```
P(ancilla = 0) = (1 + |<psi|phi>|^2) / 2
P(ancilla = 1) = (1 - |<psi|phi>|^2) / 2
```

Therefore:
```
|<psi|phi>|^2 = 2 * P(ancilla = 0) - 1
```

### 4.2 Kernel Matrix Construction

To build the full kernel matrix K (N x N), we need N(N+1)/2 swap tests (exploiting symmetry K_{ij} = K_{ji}).

For each pair (i, j):
1. Load |x_i> and |x_j> from QRAM: O(log d) per load
2. Perform swap test: O(log d) gates
3. Repeat O(1/epsilon^2) times for precision epsilon

Total complexity for the full kernel matrix: O(N^2 * log(d) / epsilon^2).

**Note:** This N^2 scaling for the full matrix is no better than classical. The quantum advantage appears only when we avoid constructing the full matrix explicitly, instead accessing kernel entries on-the-fly during HHL.

### 4.3 Implicit Kernel Access in HHL

The key to the quantum speedup is that HHL does not need the full matrix K stored classically. Instead, HHL requires a Hamiltonian simulation of K, which can be performed using:

```
e^{iKt} |psi> = sum_j e^{i lambda_j t} |u_j><u_j|psi>
```

The density matrix exponentiation technique allows simulating e^{iKt} using O(t^2 / epsilon) copies of the quantum state encoding K, without ever constructing K explicitly.

---

## 5. HHL for Solving the Dual System

### 5.1 The Linear System

The LS-SVM dual problem reduces to solving:

```
A |alpha> = |y>
```

where A = K + (1/gamma) I is an N x N positive definite matrix.

### 5.2 HHL Algorithm (Reference: Topic 19)

The HHL algorithm solves A|x> = |b> by:

1. **Quantum Phase Estimation (QPE):** Decompose |b> in the eigenbasis of A:
   ```
   |b> = sum_j beta_j |u_j>  -->  sum_j beta_j |lambda_j>|u_j>
   ```

2. **Controlled rotation:** Rotate an ancilla qubit conditioned on eigenvalues:
   ```
   sum_j beta_j |lambda_j>|u_j>|0>  -->  sum_j beta_j |lambda_j>|u_j>(sqrt(1 - C^2/lambda_j^2)|0> + (C/lambda_j)|1>)
   ```

3. **Post-selection:** Measure ancilla as |1> to obtain:
   ```
   |x> = A^{-1}|b> = sum_j (beta_j / lambda_j) |u_j>
   ```

### 5.3 Complexity

HHL solves the N x N system in time:

```
O(log(N) * kappa^2 * s * poly(1/epsilon))
```

where:
- N = number of data points (matrix dimension)
- kappa = condition number of A = lambda_max / lambda_min
- s = sparsity of A (number of nonzero entries per row)
- epsilon = desired precision

For the SVM dual system:
- The regularization term (1/gamma)I ensures A is well-conditioned: kappa <= gamma * lambda_max(K) + 1
- The kernel matrix K is generally dense (s = N), but the density matrix exponentiation technique avoids the sparsity requirement

### 5.4 Output: Quantum State |alpha>

**Critical point:** HHL outputs the solution as a quantum state |alpha>, not a classical vector of alpha values. Reading out all N components of alpha would require O(N) measurements, destroying the speedup. The algorithm is useful only if we can use |alpha> directly in subsequent quantum computations -- which is exactly what the classification step does.

---

## 6. Quantum Classification

### 6.1 Classical Decision Function

Given a new data point x_new, the classical SVM classifies it as:

```
f(x_new) = sign(sum_i alpha_i y_i K(x_i, x_new) + b)
```

### 6.2 Quantum Classification via Swap Test

With the solution state |alpha> in hand, classification of a new point proceeds quantumly:

1. **Prepare the weighted training state:** Using |alpha> and QRAM, construct:
   ```
   |w> = sum_i alpha_i y_i |x_i>
   ```
   This is the quantum representation of the SVM weight vector in feature space.

2. **Prepare the new point state:** Load |x_new> from QRAM.

3. **Swap test for classification:** Perform a swap test between |w> and |x_new>:
   ```
   |<w|x_new>|^2 ~ (sum_i alpha_i y_i K(x_i, x_new))^2
   ```

4. **Extract the sign:** The sign of f(x_new) can be obtained by a more careful procedure involving controlled operations and ancilla measurements.

### 6.3 Classification Complexity

Each classification query requires:
- O(log N) for QRAM access
- O(log d) for state preparation
- O(1) for the swap test
- O(1/epsilon^2) repetitions for precision

Total: **O(log(Nd) / epsilon^2)** per classification, exponentially faster than the classical O(N * d).

---

## 7. Full Pipeline Diagram

```
CLASSICAL DATA                QUANTUM PROCESSING                    OUTPUT
=============                 ==================                    ======

{(x_i, y_i)}                                                    
     |                                                           
     v                                                           
  [QRAM]  ------>  |x_i> (amplitude encoded states)              
     |                                                           
     v                                                           
  [Swap Test]  -->  K_{ij} = |<x_i|x_j>|^2  (quantum kernel)     
     |                                                           
     v                                                           
  [HHL]  -------->  Solve (K + I/gamma)|alpha> = |y>              
     |                                    |                       
     v                                    v                       
  [QRAM + Swap]     |alpha> (quantum state, NOT classical)        
     |                                                           
     v                                                           
  f(x_new) = sign(<w|x_new>)  ------>  {+1, -1}  (class label)  
```

**Data flow:**
1. Classical data is loaded into QRAM
2. QRAM enables quantum kernel computation via swap test
3. Kernel matrix (accessed implicitly) feeds into HHL
4. HHL outputs quantum state |alpha>
5. |alpha> combined with QRAM enables quantum classification via swap test
6. Measurement yields the class label

---

## 8. Complexity Comparison

| Operation | Classical SVM | Quantum SVM (RML) | Speedup |
|-----------|--------------|-------------------|---------|
| Data loading | O(Nd) read from memory | O(log(Nd)) via QRAM | Exponential* |
| Kernel matrix | O(N^2 d) inner products | Implicit via density matrix exp. | Exponential* |
| Dual optimization | O(N^3) or O(N^2) (SMO) | O(log(N) kappa^2) via HHL | Exponential* |
| Classification | O(N_sv * d) per query | O(log(Nd)) per query | Exponential* |
| **Total training** | **O(N^2 d + N^3)** | **O(log(Nd) * kappa^2 * poly(1/eps))** | **Exponential*** |

*Exponential speedup is contingent on:
1. QRAM existing and being efficient (the dominant assumption)
2. Condition number kappa being poly(log N) (not always the case)
3. The output being a quantum state (not a full classical readout)
4. The data not having low-rank structure (see Section 9)

---

## 9. Caveats and Dequantization

### 9.1 The QRAM Problem

QRAM is the Achilles' heel of the quantum SVM:

- No scalable QRAM exists (as of 2025)
- Bucket-brigade proposals require O(Nd) physical qubits with active error correction
- Even with perfect QRAM, the loading assumption hides the data preparation cost
- As Aaronson (2015) noted: "If your data is classical, and your output is classical, then the quantum computer is just a fancy intermediary"

### 9.2 The Input/Output Problem

- **Input problem:** Loading N classical data points into quantum states naively requires O(Nd) operations, negating any speedup
- **Output problem:** HHL outputs |alpha> as a quantum state. Extracting all N alpha values requires O(N) measurements. The speedup holds only if the quantum state is used directly (e.g., for classification)
- **Tomography bottleneck:** Full state tomography of |alpha> requires O(N^2 / epsilon^2) measurements

### 9.3 Tang's Dequantization (2019)

Ewin Tang's landmark result showed that for **low-rank** data matrices, classical algorithms can achieve similar speedups:

**Theorem (Tang, 2019):** If the data matrix X has rank r, a classical algorithm can solve the SVM dual problem in time:

```
O(r^6 * kappa^6 * ||X||_F^6 / epsilon^6 * poly(log(Nd)))
```

This "dequantization" means:
- The quantum speedup is **not** exponential for low-rank data
- Many practical datasets ARE low-rank (e.g., image data with dominant principal components)
- The quantum advantage survives only for data with genuinely high rank (close to N)

### 9.4 Practical Assessment

The honest assessment of quantum SVM (RML) in 2025:

1. **Theoretical significance:** Demonstrated that quantum computing can in principle speed up a major ML algorithm
2. **Practical relevance:** Near zero, because (a) QRAM doesn't exist, (b) most real data is low-rank, (c) near-term devices lack fault tolerance
3. **Research direction:** Has shifted toward QSVC-style kernel methods (Topic 11) and variational approaches (Topics 12-15) that avoid QRAM assumptions

---

## 10. Worked Example: 4-Point 2D Classification

### 10.1 Setup

Consider 4 training points in R^2:

```
Point 1: x_1 = (0.2, 0.8),  y_1 = +1  (class A)
Point 2: x_2 = (0.3, 0.7),  y_2 = +1  (class A)
Point 3: x_3 = (0.8, 0.2),  y_3 = -1  (class B)
Point 4: x_4 = (0.7, 0.3),  y_4 = -1  (class B)
```

### 10.2 Amplitude Encoding

Each point is normalized and encoded as a single-qubit state:

```
|x_1> = (0.2|0> + 0.8|1>) / sqrt(0.04 + 0.64) = 0.243|0> + 0.970|1>
|x_2> = (0.3|0> + 0.7|1>) / sqrt(0.09 + 0.49) = 0.394|0> + 0.919|1>
|x_3> = (0.8|0> + 0.2|1>) / sqrt(0.64 + 0.04) = 0.970|0> + 0.243|1>
|x_4> = (0.7|0> + 0.3|1>) / sqrt(0.49 + 0.09) = 0.919|0> + 0.394|1>
```

### 10.3 Quantum Kernel Matrix

Compute K_{ij} = |<x_i|x_j>|^2 using inner products:

```
<x_1|x_2> = 0.243*0.394 + 0.970*0.919 = 0.0958 + 0.8914 = 0.9872
<x_1|x_3> = 0.243*0.970 + 0.970*0.243 = 0.2357 + 0.2357 = 0.4714
<x_1|x_4> = 0.243*0.919 + 0.970*0.394 = 0.2233 + 0.3822 = 0.6055
<x_2|x_3> = 0.394*0.970 + 0.919*0.243 = 0.3822 + 0.2233 = 0.6055
<x_2|x_4> = 0.394*0.919 + 0.919*0.394 = 0.3621 + 0.3621 = 0.7242
<x_3|x_4> = 0.970*0.919 + 0.243*0.394 = 0.8914 + 0.0958 = 0.9872
```

Kernel matrix (squared inner products):

```
K = | 1.0000  0.9746  0.2222  0.3666 |
    | 0.9746  1.0000  0.3666  0.5245 |
    | 0.2222  0.3666  1.0000  0.9746 |
    | 0.3666  0.5245  0.9746  1.0000 |
```

Note the block structure: K_{11}, K_{12}, K_{21}, K_{22} are large (same class), K_{13}, K_{14}, K_{23}, K_{24} are small (different classes). The kernel captures class similarity.

### 10.4 LS-SVM Dual System

With regularization gamma = 10 (so lambda = 1/gamma = 0.1):

```
A = K + 0.1 * I = | 1.1000  0.9746  0.2222  0.3666 |
                   | 0.9746  1.1000  0.3666  0.5245 |
                   | 0.2222  0.3666  1.1000  0.9746 |
                   | 0.3666  0.5245  0.9746  1.1000 |

y = (+1, +1, -1, -1)^T
```

Solving A * alpha = y:

```
alpha = A^{-1} y = (0.7712, 0.3901, -0.7712, -0.3901)^T
```

(Exact values depend on numerical precision.)

### 10.5 Support Vectors and Classification

All four points are support vectors (all |alpha_i| > 0 since LS-SVM has no sparsity). The decision function for a new point x_new is:

```
f(x_new) = sum_i alpha_i y_i K(x_i, x_new) + b
         = 0.7712 * K(x_1, x_new) + 0.3901 * K(x_2, x_new)
           - 0.7712 * K(x_3, x_new) - 0.3901 * K(x_4, x_new) + b
```

For x_new = (0.25, 0.75): similar to x_1, x_2 (class A), so positive terms dominate --> f > 0 --> class +1.

For x_new = (0.75, 0.25): similar to x_3, x_4 (class B), so negative terms dominate --> f < 0 --> class -1.

---

## 11. Comparison with QSVC (Topic 11)

| Feature | QSVC (Topic 11) | QSVM-RML (Topic 20) |
|---------|-----------------|----------------------|
| **Year** | Havlicek et al. 2019 | Rebentrost et al. 2014 |
| **Paradigm** | Hybrid quantum-classical | Fully quantum |
| **Kernel** | Fidelity: \|<0\|U_phi(x_j)^dag U_phi(x_i)\|0>\|^2 | Swap test: \|<x_i\|x_j>\|^2 |
| **Feature map** | Parameterized circuit (ZZFeatureMap) | Amplitude encoding via QRAM |
| **Optimization** | Classical SVM solver (SMO) | Quantum HHL algorithm |
| **Output** | Classical alpha vector | Quantum state \|alpha> |
| **Classification** | Classical weighted sum | Quantum swap test |
| **QRAM required** | No | Yes (critical dependency) |
| **NISQ compatible** | Yes | No |
| **Proven speedup** | No (heuristic advantage) | Yes (conditional on QRAM) |
| **Dequantized** | N/A | Yes (Tang 2019, for low-rank data) |
| **Practical use (2025)** | Possible on current hardware | Not feasible |
| **Best for** | Exploring quantum kernel expressivity | Theoretical complexity analysis |

**Summary:** QSVC is the practical choice for near-term quantum advantage exploration. QSVM-RML is the theoretically elegant but currently impractical "end game" that shows the full potential of quantum machine learning if hardware catches up.

---

## 12. References

1. **Rebentrost, P., Mohseni, M., & Lloyd, S.** (2014). "Quantum support vector machine for big data classification." *Physical Review Letters*, 113(13), 130503. arXiv:1307.0471

2. **Tang, E.** (2019). "A quantum-inspired classical algorithm for recommendation systems." *Proceedings of STOC 2019*. arXiv:1807.04271 (Dequantization of quantum ML algorithms)

3. **Havlicek, V., Córcoles, A. D., Temme, K., et al.** (2019). "Supervised learning with quantum-enhanced feature spaces." *Nature*, 567, 209-212

4. **Aaronson, S.** (2015). "Read the fine print." *Nature Physics*, 11, 291-293 (Critique of quantum ML speedup claims)

5. **Schuld, M.** (2021). "Supervised quantum machine learning models are kernel methods." arXiv:2101.11020

6. **Harrow, A. W., Hassidim, A., & Lloyd, S.** (2009). "Quantum algorithm for linear systems of equations." *Physical Review Letters*, 103(15), 150502 (The HHL algorithm used inside QSVM)

7. **Giovannetti, V., Lloyd, S., & Maccone, L.** (2008). "Quantum random access memory." *Physical Review Letters*, 100(16), 160501

8. **Suykens, J. A. K., & Vandewalle, J.** (1999). "Least squares support vector machine classifiers." *Neural Processing Letters*, 9(3), 293-300 (LS-SVM formulation used by Rebentrost et al.)
