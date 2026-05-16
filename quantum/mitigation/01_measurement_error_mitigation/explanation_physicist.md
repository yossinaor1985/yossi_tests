# Measurement Error Mitigation (M3) - Physicist's Deep Dive

## 1. Overview

Measurement (readout) errors are among the most significant noise sources on current quantum hardware. Unlike gate errors which corrupt the quantum state during computation, readout errors occur at the very end -- when we extract classical information from quantum states. On typical superconducting hardware, readout error rates range from 0.5% to 5%, substantially higher than single-qubit gate error rates.

Measurement Error Mitigation corrects for these readout errors in classical post-processing, without modifying the quantum circuit itself. The most scalable modern approach is **M3 (Matrix-free Measurement Mitigation)**, which avoids constructing the full confusion matrix.

---

## 2. The Readout Error Model

### 2.1 Single-Qubit Readout Errors

For a single qubit, readout errors are characterized by two conditional probabilities:

```
P(measure 1 | prepared 0) = e_0  (false positive / excitation during readout)
P(measure 0 | prepared 1) = e_1  (false negative / relaxation during readout)
```

These are typically asymmetric: e_1 > e_0 on superconducting qubits because T1 relaxation during measurement drives |1> -> |0>.

### 2.2 The Assignment Matrix (Confusion Matrix)

For a single qubit, the **assignment matrix** A relates measured probabilities to ideal probabilities:

```
P_measured = A * P_ideal
```

where:

```
A = | 1 - e_0    e_1   |
    |   e_0    1 - e_1  |
```

Each column j of A is the conditional probability distribution P(measured outcome | prepared state j).

### 2.3 Multi-Qubit Assignment Matrix

For n qubits with 2^n basis states, the full assignment matrix is 2^n x 2^n:

```
A[i,j] = P(measure bitstring i | prepared bitstring j)
```

If readout errors are **uncorrelated** across qubits, A factors as a tensor product:

```
A = A_1 (x) A_2 (x) ... (x) A_n
```

where A_k is the 2x2 assignment matrix for qubit k, and (x) denotes the Kronecker product.

This tensor product structure is crucial for scalability -- storing and inverting the full 2^n x 2^n matrix is intractable for n > ~15 qubits.

---

## 3. Calibration Procedure

### 3.1 Full Calibration (Exponential Cost)

To determine the full assignment matrix, prepare each of the 2^n computational basis states and measure:

```
For each basis state |j> (j = 0, 1, ..., 2^n - 1):
    1. Prepare |j> on the quantum hardware
    2. Measure many shots to estimate P(i|j) for all outcomes i
    3. Column j of A = measured probability distribution
```

This requires 2^n separate circuits, each with many shots -- exponentially expensive.

### 3.2 Tensor Product Calibration (Linear Cost)

Under the tensor product noise model, we only need to calibrate each qubit independently:

```
For each qubit k (k = 1, ..., n):
    1. Prepare |0> on qubit k, measure -> get P(0|0)_k, P(1|0)_k
    2. Prepare |1> on qubit k, measure -> get P(0|1)_k, P(1|1)_k
    3. Construct A_k = [[1-e_0, e_1], [e_0, 1-e_1]]
```

Total circuits needed: 2n (linear in number of qubits).

### 3.3 Correlated Calibration (CTMP Model)

Some qubits exhibit correlated readout errors (e.g., due to crosstalk in readout resonators). The **Continuous Time Markov Process (CTMP)** model captures nearest-neighbor correlations:

```
A = exp(G)
```

where G is a sparse generator matrix with non-zero elements only between bitstrings differing in correlated qubit pairs.

---

## 4. Correction Methods

### 4.1 Matrix Inversion

The simplest correction:

```
P_ideal = A^{-1} * P_measured
```

**Problem**: A^{-1} can produce negative "probabilities" since it is not a stochastic matrix. These must be handled by:
- Clipping negative values to zero and renormalizing
- Constrained least-squares: minimize ||A * P - P_measured||^2 subject to P >= 0, sum(P) = 1

### 4.2 Iterative Methods

For large systems where storing/inverting A is infeasible:

**Iterative Bayesian Unfolding**:
```
P^{(k+1)}_j = P^{(k)}_j * sum_i [ A[i,j] * P_measured[i] / (A * P^{(k)})_i ]
```

This converges to the maximum likelihood solution and naturally produces non-negative probabilities.

### 4.3 Least-Squares with Constraints

Minimize:

```
chi^2 = sum_i (P_measured[i] - sum_j A[i,j] * P_ideal[j])^2
```

subject to:
```
P_ideal[j] >= 0  for all j
sum_j P_ideal[j] = 1
```

This is a quadratic program solvable with standard convex optimization.

---

## 5. M3: Matrix-free Measurement Mitigation

### 5.1 Key Insight

M3 avoids constructing the full 2^n x 2^n matrix. Instead, it works only with the **reduced set** of bitstrings that actually appear in the measurement output.

If k distinct bitstrings are observed (k << 2^n for large n), M3 constructs and inverts only a k x k submatrix.

### 5.2 Algorithm

1. **Calibration**: Measure per-qubit readout error rates (e_0, e_1) for each qubit. Only 2n circuits needed.

2. **Collect raw counts**: Run the target circuit, obtain raw measurement counts {c_i} for observed bitstrings {b_i}.

3. **Build reduced assignment matrix**: For the k observed bitstrings, compute the k x k matrix:
   ```
   A_reduced[i,j] = Product_{m=1}^{n} A_m[b_i[m], b_j[m]]
   ```
   where b_i[m] is the m-th bit of bitstring b_i.

4. **Solve reduced system**:
   ```
   P_reduced = A_reduced^{-1} * C_reduced / total_shots
   ```
   with non-negativity constraints.

5. **Output corrected counts**.

### 5.3 Complexity Analysis

- Calibration: O(n) circuits
- Correction: O(k^2 * n) for building A_reduced + O(k^3) for inversion
- Since k << 2^n (typically k ~ poly(n) for structured circuits), this is efficient

### 5.4 Error Propagation

The statistical uncertainty in the corrected probabilities:

```
Var(P_corrected) = A^{-1} * diag(P_measured / N_shots) * (A^{-1})^T
```

M3 computes these error bars automatically by propagating shot noise through the correction.

---

## 6. Comparison of Methods

| Method                    | Calibration Cost | Memory    | Accuracy        | Scalability |
|---------------------------|------------------|-----------|-----------------|-------------|
| Full matrix inversion     | O(2^n)           | O(4^n)    | Exact (if A exact) | n < 15   |
| Tensor product inversion  | O(n)             | O(n)      | Good (if uncorr.)  | Any n    |
| M3 (matrix-free)          | O(n)             | O(k^2)    | Good               | Any n    |
| Iterative Bayesian        | O(2^n) or O(n)   | O(k)      | Good               | Any n    |
| CTMP                      | O(n)             | O(n^2)    | Better (corr.)     | Any n    |

---

## 7. Practical Considerations

### 7.1 Calibration Drift

Readout error rates drift over time due to fluctuations in qubit frequencies, resonator properties, and amplifier settings. Recalibrate at least every few hours or before critical runs.

### 7.2 State-Dependent Readout Errors

The simple model assumes readout errors depend only on the measured qubit state. In practice, errors can depend on the states of neighboring qubits (crosstalk). The CTMP model partially addresses this.

### 7.3 Shot Budget

Mitigation amplifies statistical noise by a factor related to the condition number of A:

```
Effective shots = N_shots / kappa(A)^2
```

Highly noisy readout (large e_0, e_1) leads to poorly conditioned A and requires more shots.

### 7.4 Mitigation vs Correction

Measurement error mitigation is post-processing -- it cannot recover information lost due to fundamental information-theoretic limits. If readout errors are too severe (approaching 50%), no amount of mitigation can help.

---

## 8. Qiskit Implementation Notes

### 8.1 mthree Package

The `mthree` (M3) package provides the canonical implementation:

```python
import mthree
mit = mthree.M3Mitigation(backend)
mit.cals_from_system(qubits=[0, 1, 2])  # Calibrate
quasi_dist = mit.apply_correction(raw_counts, qubits=[0, 1, 2])
```

### 8.2 Qiskit Aer Noise Model

For local simulation with readout errors:

```python
from qiskit_aer.noise import NoiseModel, ReadoutError
noise_model = NoiseModel()
p0_given1 = 0.05  # P(read 0 | state 1)
p1_given0 = 0.02  # P(read 1 | state 0)
re = ReadoutError([[1-p1_given0, p1_given0], [p0_given1, 1-p0_given1]])
noise_model.add_readout_error(re, [qubit_index])
```

### 8.3 Integration with Estimator / Sampler

In Qiskit Runtime, measurement error mitigation is available as a resilience option:

```python
# SamplerV2 with resilience
options.resilience.measure_mitigation = True
```

---

## 9. Mathematical Details

### 9.1 Positive Operator-Valued Measure (POVM) Formulation

Ideal measurement: POVM elements M_i = |i><i| (projectors onto computational basis states).

Noisy measurement: POVM elements:

```
M_i^noisy = sum_j A[i,j] |j><j|
```

The measured probability of outcome i for state rho:

```
P(i) = Tr(M_i^noisy * rho) = sum_j A[i,j] <j|rho|j>
```

### 9.2 Twirled Readout vs Direct Calibration

An alternative approach (TREX, covered in Topic 02) randomizes readout errors by inserting random X gates before measurement. The advantage is that it converts asymmetric readout errors to a symmetric form, simplifiable to a single-parameter model per qubit.

### 9.3 Confidence Intervals

Using the delta method, the variance of the corrected probability for outcome j:

```
Var(p_j^corr) approx sum_k (A^{-1}[j,k])^2 * p_k^raw * (1 - p_k^raw) / N
```

where N is the total number of shots.

---

## 10. References

1. Bravyi, S., Sheldon, S., Kandala, A., Mckay, D. C., & Gambetta, J. M. (2021). "Mitigating measurement errors in multiqubit experiments." Physical Review A, 103(4), 042605.
2. Nation, P. D., Kang, H., Sundaresan, N., & Gambetta, J. M. (2021). "Scalable mitigation of measurement errors on quantum computers." PRX Quantum, 2(4), 040326.
3. Maciejewski, F. B., Zimboras, Z., & Oszmaniec, M. (2020). "Mitigation of readout noise in near-term quantum devices by classical post-processing based on detector tomography." Quantum, 4, 257.
4. Smolin, J. A., Gambetta, J. M., & Smith, G. (2012). "Efficient method for computing the maximum-likelihood quantum state from measurements with additive Gaussian noise." Physical Review Letters, 108(7), 070502.
5. Qiskit documentation: Measurement error mitigation - https://docs.quantum.ibm.com/
