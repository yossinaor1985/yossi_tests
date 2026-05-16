# Probabilistic Error Cancellation (PEC) - Physicist's Deep Dive

## 1. Overview

Probabilistic Error Cancellation (PEC) is an error mitigation technique that achieves **exact** (unbiased) correction of expectation values by representing the ideal gate as a quasi-probability distribution over noisy implementable operations. Unlike ZNE which is approximate, PEC is exact in expectation -- the price is exponential sampling overhead.

---

## 2. Core Idea

### 2.1 The Decomposition

The ideal (noiseless) gate G_ideal can be expressed as:

```
G_ideal = sum_i eta_i * G_noisy_i
```

where:
- {G_noisy_i} are noisy operations that can be physically implemented
- {eta_i} are **real coefficients** (quasi-probabilities) that can be negative
- sum_i eta_i = 1 (normalization in the operator sense)

The set {G_noisy_i} typically includes the noisy gate followed by Pauli corrections.

### 2.2 Quasi-Probability Distribution

Define:
```
p_i = |eta_i| / gamma
sign_i = sgn(eta_i) = +1 or -1
gamma = sum_i |eta_i|   (one-norm of the quasi-probability vector)
```

Then {p_i} forms a valid probability distribution (p_i >= 0, sum p_i = 1), and:

```
G_ideal = gamma * sum_i sign_i * p_i * G_noisy_i
```

### 2.3 Monte Carlo Estimation

To estimate <O> for the ideal circuit:

1. For each gate in the circuit, sample a noisy variant according to {p_i}
2. Run the modified circuit, measure O, obtain outcome o
3. The PEC estimate is: o_corrected = gamma_total * sign_total * o
   where gamma_total = product of all gate gammas, sign_total = product of all sampled signs

The expectation:
```
E[o_corrected] = <O>_ideal   (exact in expectation!)
```

---

## 3. Constructing the Decomposition

### 3.1 For a Pauli Noise Channel

If the noise channel after gate G is a Pauli channel:

```
E(rho) = (1-p) * rho + sum_k p_k * P_k * rho * P_k^dag
```

Then the inverse channel (which "undoes" the noise) is:

```
E^{-1}(rho) = sum_k eta_k * P_k * rho * P_k^dag
```

where the quasi-probabilities {eta_k} are obtained by inverting the Pauli probability vector.

### 3.2 Explicit Construction for Depolarizing Noise

For single-qubit depolarizing noise with error rate p:

```
E(rho) = (1-p) rho + (p/3)(X rho X + Y rho Y + Z rho Z)
```

The inverse:
```
E^{-1}(rho) = (1 + 3p/(3-4p)) rho - (p/(3-4p))(X rho X + Y rho Y + Z rho Z)
```

The quasi-probabilities:
```
eta_I = (3 - 3p) / (3 - 4p)
eta_X = eta_Y = eta_Z = -p / (3 - 4p)
```

The gamma factor:
```
gamma = |eta_I| + |eta_X| + |eta_Y| + |eta_Z| = (3 + 2p) / (3 - 4p) > 1
```

For small p: gamma approx 1 + (10/3)*p + O(p^2).

### 3.3 General Construction via Noise Tomography

For an arbitrary noise channel E:

1. Perform process tomography or Pauli twirling to characterize E
2. Compute the Pauli Transfer Matrix (PTM) Lambda of E
3. Invert: Lambda^{-1} gives the PTM of E^{-1}
4. Decompose E^{-1} into a quasi-probability mixture of Pauli operations
5. The decomposition coefficients are the eta_i

---

## 4. Sampling Overhead (The Cost of PEC)

### 4.1 Single-Gate Cost

The variance of the PEC estimator for a single gate:

```
Var(o_corrected) = gamma^2 * Var(o)
```

The variance is amplified by gamma^2. Effective number of useful shots:

```
N_effective = N_total / gamma^2
```

### 4.2 Multi-Gate Cost

For a circuit with L gates, each with gamma factor gamma_l:

```
gamma_total = Product_{l=1}^L gamma_l
```

The sampling overhead:
```
N_total / N_effective = gamma_total^2 = Product_l gamma_l^2
```

For depolarizing noise with per-gate gamma approx 1 + (10/3)*p:

```
gamma_total^2 approx exp(20*p*L/3)
```

This is **exponential** in the circuit volume (p * L). For p = 0.01 and L = 100:
```
gamma_total^2 approx exp(0.67) approx 1.95
```
About 2x overhead -- manageable.

For p = 0.01 and L = 1000:
```
gamma_total^2 approx exp(6.7) approx 812
```
Need ~800x more shots -- expensive but potentially feasible.

### 4.3 Comparison with ZNE

| Property         | ZNE              | PEC               |
|------------------|------------------|--------------------|
| Bias             | Non-zero (model) | Zero (exact)       |
| Variance         | Moderate         | High (gamma^2)     |
| Noise knowledge  | None required    | Full characterization |
| Scaling          | Moderate         | Exponential in pL  |

---

## 5. Sparse Pauli-Lindblad Noise Model

### 5.1 Scalable Noise Learning

Full process tomography is exponentially expensive. The Sparse Pauli-Lindblad (SPL) model provides a scalable alternative:

```
E(rho) = exp(L)(rho)
```

where L is a Lindblad generator with sparse Pauli terms:

```
L(rho) = sum_k lambda_k (P_k rho P_k^dag - rho)
```

Only O(n) or O(n^2) Pauli terms (local and 2-local) are needed, not O(4^n).

### 5.2 Learning the SPL Model

The Pauli-Lindblad rates {lambda_k} can be estimated from:
1. Prepare random Pauli eigenstates
2. Apply the noisy layer
3. Measure in the Pauli basis
4. Fit the decay rates

This requires O(n^2) circuits, not O(4^n).

---

## 6. Implementation Details

### 6.1 Circuit Execution

For each PEC sample:
1. For each gate layer l:
   a. Sample index i_l from distribution {p_i^(l)}
   b. Record sign: s_l = sign(eta_{i_l}^(l))
   c. Apply the sampled noisy operation G_{i_l}^(l)
2. Measure the observable O, getting outcome o
3. Compute: o_PEC = gamma_total * (product s_l) * o

### 6.2 Number of Samples

To estimate <O> to precision epsilon with confidence 1-delta:

```
N_samples >= gamma_total^2 * ||O||^2 * ln(2/delta) / (2 * epsilon^2)
```

### 6.3 Practical Approximations

**Truncated PEC**: Only correct the most significant error terms, accepting small bias in exchange for reduced gamma.

**Layered PEC**: Apply PEC layer-by-layer rather than gate-by-gate, reducing the number of independent samples needed.

---

## 7. Limitations

1. **Exponential sampling overhead**: gamma_total^2 grows exponentially with circuit volume pL.
2. **Requires noise characterization**: Full Pauli channel knowledge needed for each gate.
3. **Noise drift**: If noise changes between characterization and experiment, PEC is biased.
4. **Observable dependent**: PEC corrects expectation values, not full state/distribution.
5. **Classical overhead**: Post-processing with sign corrections can be complex.

---

## 8. Qiskit Implementation

In Qiskit Runtime, PEC is available via:

```python
options.resilience_level = 3  # Enables PEC
# Runtime automatically performs noise learning and PEC correction
```

The runtime handles noise learning (Sparse Pauli-Lindblad), quasi-probability decomposition, and Monte Carlo sampling.

---

## 9. References

1. Temme, K., Bravyi, S., & Gambetta, J. M. (2017). "Error mitigation for short-depth quantum circuits." Physical Review Letters, 119(18), 180509.
2. van den Berg, E., Minev, Z. K., Kandala, A., & Temme, K. (2023). "Probabilistic error cancellation with sparse Pauli-Lindblad models on noisy quantum processors." Nature Physics, 19, 1116-1121.
3. Endo, S., Benjamin, S. C., & Li, Y. (2018). "Practical quantum error mitigation for near-future applications." Physical Review X, 8(3), 031027.
4. Strikis, A., et al. (2021). "Learning-based quantum error mitigation." PRX Quantum, 2(4), 040330.
5. Kim, Y., et al. (2023). "Evidence for the utility of quantum computing before fault tolerance." Nature, 618, 500-505.
6. Qiskit documentation: Probabilistic error cancellation - https://docs.quantum.ibm.com/
