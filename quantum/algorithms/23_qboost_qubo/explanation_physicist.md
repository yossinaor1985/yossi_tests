# QBoost -- QUBO Ensemble Selection - Physicist's Deep Dive

## 1. Overview

QBoost was introduced by Neven, Denchev, Rose, and Macready (2008, 2012) at Google/D-Wave as a hybrid quantum-classical machine learning algorithm. The central idea is elegant: given a pool of N classical weak classifiers (each only slightly better than random guessing), select an optimal *subset* that, when combined, forms a strong ensemble classifier.

The key innovation is that the subset-selection problem is formulated as a **Quadratic Unconstrained Binary Optimization (QUBO)** problem, which maps naturally to quantum hardware -- either quantum annealing (D-Wave) or gate-based QAOA (IBM, etc.).

This places QBoost at the intersection of three fields:
1. **Ensemble learning** (boosting, bagging, stacking)
2. **Combinatorial optimization** (QUBO, Ising models)
3. **Quantum computing** (QAOA, quantum annealing)

The promise: while classical boosting algorithms like AdaBoost select classifiers greedily (one at a time), QBoost searches over all 2^N possible subsets simultaneously via quantum superposition, potentially finding a globally optimal ensemble that greedy methods miss.

---

## 2. Mathematical Foundation

### 2.1 Ensemble Learning and Weak Classifiers

**Setup.** We have a training set of S labeled samples {(x_s, y_s)}_{s=1}^S where x_s in R^d is a feature vector and y_s in {-1, +1} is the binary label. Note we use the +/-1 convention (not 0/1) for labels, which is standard in boosting theory.

We train N weak classifiers h_1, h_2, ..., h_N on this data. Each h_i: R^d -> {-1, +1} is individually mediocre (accuracy slightly above 50%), but collectively they contain enough information to classify well.

**The ensemble.** We seek a strong classifier of the form:

```
H(x) = sign( sum_{i=1}^{N} w_i h_i(x) )
```

where w = (w_1, ..., w_N) in {0, 1}^N is a binary weight vector. Here w_i = 1 means "include classifier i in the ensemble" and w_i = 0 means "exclude it."

This is the key difference from AdaBoost, which uses real-valued weights. QBoost restricts to binary selection, making the problem combinatorial and amenable to QUBO formulation.

### 2.2 The QBoost Objective Function

We want the ensemble to match the training labels as closely as possible while keeping the ensemble small (for generalization). The QBoost objective is:

```
min_{w in {0,1}^N}  L(w) = sum_{s=1}^{S} ( sum_{i=1}^{N} w_i h_i(x_s) - y_s )^2  +  lambda sum_{i=1}^{N} w_i
```

The first term is the **training loss**: the squared error between the ensemble's raw output (before sign) and the true labels. The second term is an **L0 regularizer** (since w_i is binary, sum w_i counts the number of selected classifiers), weighted by the hyperparameter lambda >= 0.

**Expanding the quadratic.** Let us define the prediction matrix:

```
P_{si} = h_i(x_s)    (S x N matrix)
```

Then the training loss becomes:

```
sum_s ( sum_i w_i P_{si} - y_s )^2 = sum_s ( sum_i sum_j w_i w_j P_{si} P_{sj} - 2 y_s sum_i w_i P_{si} + y_s^2 )
```

Since w_i in {0,1} implies w_i^2 = w_i, we can write this in matrix form:

```
L(w) = w^T Q w + q^T w + const
```

where:

```
Q_{ij} = sum_{s=1}^{S} h_i(x_s) h_j(x_s)  = (P^T P)_{ij}     for i != j

Q_{ii} = sum_{s=1}^{S} h_i(x_s)^2 - 2 sum_{s=1}^{S} y_s h_i(x_s) + lambda
       = S - 2 sum_{s=1}^{S} y_s h_i(x_s) + lambda
```

Note: since h_i(x_s) in {-1,+1}, we have h_i(x_s)^2 = 1, so the diagonal of P^T P is S (the number of training samples). The off-diagonal terms capture correlations between classifiers.

More explicitly, the full QUBO matrix is:

```
Q_{ij} = sum_{s=1}^{S} h_i(x_s) h_j(x_s)              (off-diagonal, i != j)
Q_{ii} = sum_{s=1}^{S} h_i(x_s)^2 - 2 sum_s y_s h_i(x_s) + lambda   (diagonal)
```

The constant term const = sum_s y_s^2 = S does not affect the optimization.

### 2.3 QUBO to Ising Conversion

To solve on a quantum computer, we convert the QUBO to an Ising Hamiltonian using the standard substitution:

```
w_i = (1 - Z_i) / 2
```

where Z_i is the Pauli-Z operator on qubit i with eigenvalues +/-1. When Z_i = +1 (qubit in |0>), w_i = 0 (classifier excluded). When Z_i = -1 (qubit in |1>), w_i = 1 (classifier included).

Substituting into the QUBO:

```
w_i w_j = (1 - Z_i)(1 - Z_j) / 4  = (1 - Z_i - Z_j + Z_i Z_j) / 4
```

```
w_i = (1 - Z_i) / 2
```

The objective becomes:

```
L(Z) = sum_{i,j} Q_{ij} (1 - Z_i - Z_j + Z_i Z_j) / 4  +  sum_i q_i (1 - Z_i) / 2  +  const
```

Expanding and collecting terms:

```
H_Ising = sum_{i<j} J_{ij} Z_i Z_j  +  sum_i h_i Z_i  +  E_0
```

where:

```
J_{ij} = Q_{ij} / 4                             (ZZ coupling)

h_i = (-sum_j Q_{ij} - q_i) / 2    (not to be confused with classifiers h_i)
    = (-sum_j Q_{ij}) / 4 - q_i / 2     (local field)

E_0 = (sum_{ij} Q_{ij} + 2 sum_i q_i) / 4 + const  (energy offset)
```

**SparsePauliOp construction.** In Qiskit, we build this as:

```python
H = sum_{i<j} J_{ij} * "...Z_i...Z_j..."  +  sum_i h_i * "...Z_i..."  +  E_0 * "II...I"
```

using Qiskit's little-endian convention (qubit 0 is rightmost in the Pauli string).

### 2.4 Solving with QAOA

The Ising Hamiltonian H_Ising is a diagonal operator in the computational basis, exactly the type of cost Hamiltonian that QAOA (algorithm 02) is designed to minimize.

**QAOA procedure:**

1. **Prepare** the uniform superposition |+>^N (N qubits, one per classifier).

2. **Apply p layers** of alternating unitaries:
   ```
   |gamma, beta> = U_M(beta_p) U_C(gamma_p) ... U_M(beta_1) U_C(gamma_1) |+>^N
   ```
   where:
   - U_C(gamma) = exp(-i gamma H_Ising) applies phases based on the QUBO cost
   - U_M(beta) = exp(-i beta sum_i X_i) is the standard transverse-field mixer

3. **Optimize** the 2p parameters (gamma_1,...,gamma_p, beta_1,...,beta_p) using a classical optimizer (COBYLA, SPSA, etc.) to minimize <H_Ising>.

4. **Measure** the final state. The most probable bitstring w* = (w_1*,...,w_N*) gives the selected classifiers.

**Key point:** Since QAOA minimizes the Hamiltonian, and our QUBO is already a minimization problem, we use H_Ising directly (no negation needed, unlike the MaxCut formulation in algorithm 02 which maximizes). However, in practice with Qiskit's QAOA implementation, we negate because Qiskit's compute_minimum_eigenvalue seeks the minimum eigenvalue -- and we want to minimize the QUBO.

**Circuit complexity for QBoost:**
- N qubits (one per weak classifier)
- Each QAOA layer has O(N^2) ZZ gates (from the dense QUBO matrix) + N RX gates
- Total: O(p * N^2) two-qubit gates

### 2.5 Comparison with Classical Boosting

| Property | AdaBoost | QBoost |
|----------|----------|--------|
| Weight type | Real-valued | Binary {0,1} |
| Selection strategy | Greedy sequential | Global optimization |
| Search space explored | N per round (T rounds) | All 2^N subsets simultaneously |
| Objective | Exponential loss | Squared loss + L0 regularizer |
| Correlation handling | Implicit (reweighting) | Explicit (Q matrix encodes correlations) |
| Overfitting control | Early stopping | Regularization parameter lambda |
| Hardware | Classical CPU | Quantum processor or quantum annealer |

**AdaBoost** works iteratively: at round t, it reweights training samples to focus on misclassified ones, then selects the best classifier for the current weights. This is a greedy approach -- optimal at each step, but not globally optimal.

**QBoost** directly optimizes over all 2^N possible binary selections. The QUBO matrix Q captures all pairwise correlations between classifiers. Two classifiers that are highly correlated (similar predictions) will have a large Q_{ij}, penalizing their simultaneous selection. This naturally promotes diversity in the ensemble -- a property that classical boosting achieves only heuristically through sample reweighting.

---

## 3. Detailed Example

### 3.1 Setup

Consider a binary classification task on the `make_moons` dataset (200 samples, noise=0.3). We train N = 8 decision stumps (decision trees of depth 1) as weak classifiers.

Each decision stump partitions the feature space with a single threshold on one feature:
```
h_i(x) = +1 if x_{f_i} > theta_i, else -1
```

### 3.2 QUBO Construction

With 8 classifiers and ~160 training samples (after 80/20 split):

1. Compute the prediction matrix P (160 x 8), where P_{si} = h_i(x_s) in {-1, +1}.

2. Build Q = P^T P (8 x 8 matrix). The diagonal Q_{ii} = 160 (number of training samples, since h_i^2 = 1). The off-diagonals Q_{ij} = sum_s h_i(x_s) h_j(x_s) measure agreement between classifiers (positive = agree often, negative = disagree often).

3. Modify diagonal: Q_{ii} -> Q_{ii} - 2 sum_s y_s h_i(x_s) + lambda. The term -2 sum_s y_s h_i(x_s) favors classifiers that agree with the true labels. The lambda term penalizes including too many classifiers.

### 3.3 QAOA Solution

The QUBO requires 8 qubits. QAOA with p = 2 layers uses 4 variational parameters and a circuit with O(8^2) = 64 ZZ interactions per layer.

The ground state bitstring, say w* = (1, 0, 1, 0, 1, 1, 0, 0), means: select classifiers h_1, h_3, h_5, h_6. The final ensemble is:

```
H(x) = sign( h_1(x) + h_3(x) + h_5(x) + h_6(x) )
```

and classification is by majority vote of the selected classifiers.

---

## 4. Complexity Analysis

### 4.1 QUBO Size

- **Variables:** N (one binary variable per weak classifier)
- **Quadratic terms:** N(N-1)/2 (fully connected QUBO)
- **Matrix construction:** O(S * N^2) to compute P^T P

### 4.2 Quantum Resources

- **Qubits:** N (one per classifier)
- **QAOA circuit depth per layer:** O(N^2) for the fully-connected ZZ interactions + O(N) for the mixer
- **Total gates:** O(p * N^2) two-qubit gates
- **Practical limit:** N <= ~20 on current NISQ hardware (limited by qubit count, connectivity, and noise)

### 4.3 Scaling Considerations

For large N (many classifiers), several strategies can reduce the quantum resource requirements:

1. **QUBO sparsification:** Zero out small Q_{ij} entries (|Q_{ij}| < threshold), reducing the number of ZZ gates.
2. **Classifier pre-selection:** Use classical methods (correlation filtering, feature importance) to reduce N before quantum optimization.
3. **Recursive QBoost:** Apply QBoost recursively on blocks of classifiers, similar to divide-and-conquer.

---

## 5. References

1. Neven, H., Denchev, V. S., Drew-Brook, M., Zhang, J., Macready, W. G., & Rose, G. "NIPS 2008 Demonstration: Binary Classification using Hardware Implementation of Quantum Annealing." (2008).
2. Neven, H., Denchev, V. S., Rose, G., & Macready, W. G. "QBoost: Large Scale Classifier Training with Adiabatic Quantum Optimization." Proceedings of the Asian Conference on Machine Learning, PMLR 25:333-348 (2012).
3. Boyda, E., Basu, S., Ganguly, S., Michaelis, A., Mukhopadhyay, S., & Nemani, R. R. "Deploying a quantum annealing processor to detect tree cover in aerial imagery of California." PLoS ONE 12(2): e0172505 (2017).
4. Mucke, S., Heese, R., Muller, S., Wolter, M., & Piatkowski, N. "Large-Scale Quantum Hybrid Ensemble Learning." arXiv:2303.11428 (2023).
5. Farhi, E., Goldstone, J., & Gutmann, S. "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028 (2014).
