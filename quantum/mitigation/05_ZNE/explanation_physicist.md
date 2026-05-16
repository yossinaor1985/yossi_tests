# Zero-Noise Extrapolation (ZNE) - Physicist's Deep Dive

## 1. Overview

Zero-Noise Extrapolation (ZNE) is an error mitigation technique that estimates the noiseless expectation value by running a circuit at multiple controlled noise levels and extrapolating to the zero-noise limit. It requires no knowledge of the noise model -- only the ability to controllably amplify noise.

ZNE is one of the most widely used error mitigation methods due to its simplicity and generality.

---

## 2. Core Principle

### 2.1 The Extrapolation Idea

Let E(lambda) be the expectation value of an observable at noise level lambda:

```
E(lambda) = E_ideal + c_1 * lambda + c_2 * lambda^2 + ...
```

where:
- lambda = 1 is the physical (hardware) noise level
- E(lambda=0) = E_ideal is the noiseless result we want
- c_1, c_2, ... are unknown noise coefficients

By measuring E at multiple noise levels lambda_1 < lambda_2 < ..., we fit a model and extrapolate to lambda = 0.

### 2.2 Noise Amplification Methods

To vary lambda, we need to controllably increase the noise:

**Gate Folding**: Replace each gate G with G . G^dag . G (which equals G ideally but triples the noise):
```
lambda = 1:  ...G...
lambda = 3:  ...G.G^dag.G...
lambda = 5:  ...G.G^dag.G.G^dag.G...
```

Each folding step adds a factor of 2 to the noise (lambda = 1, 3, 5, 7, ...).

**Partial Folding**: Fold only a fraction of the gates for intermediate noise levels:
```
lambda = 1 + 2k/N   (folding k out of N gates)
```

**Pulse Stretching**: On pulse-level access hardware, stretch the gate pulses by a factor of lambda. Longer pulses experience more decoherence.

---

## 3. Extrapolation Methods

### 3.1 Linear Extrapolation

Assume E(lambda) = a + b * lambda:

```
E_ZNE = E(lambda_1) - (E(lambda_2) - E(lambda_1)) * lambda_1 / (lambda_2 - lambda_1)
```

**Pros**: Simple, robust with only 2 noise levels.
**Cons**: Ignores higher-order terms, biased if noise is nonlinear.

### 3.2 Polynomial Extrapolation

Fit E(lambda) = a_0 + a_1 * lambda + a_2 * lambda^2 + ... + a_d * lambda^d:

Requires d+1 noise levels. Extrapolated value: E_ZNE = a_0.

**Pros**: Can capture nonlinear noise behavior.
**Cons**: Higher-degree fits are numerically unstable (Runge phenomenon).

### 3.3 Exponential Extrapolation

Assume E(lambda) = A * exp(-B * lambda) + C:

```
E_ZNE = A + C   (lambda -> 0 limit)
```

**Motivation**: For depolarizing noise with error rate p per gate and N gates:
```
E(lambda) approx E_ideal * (1 - 2p)^(lambda * N) = E_ideal * exp(-2p * lambda * N)
```

This is naturally exponential in lambda.

**Pros**: Physically motivated, often gives best results.
**Cons**: Requires 3+ noise levels, can be sensitive to outliers.

### 3.4 Richardson Extrapolation

The most systematic approach. Given noise levels {lambda_i} for i = 1,...,M:

```
E_ZNE = sum_i w_i * E(lambda_i)
```

where the weights satisfy:

```
sum_i w_i = 1                   (zeroth order)
sum_i w_i * lambda_i^k = 0     (for k = 1, ..., M-1)
```

This cancels the first M-1 terms in the Taylor expansion.

For two noise levels (lambda_1 = 1, lambda_2 = c):

```
w_1 = c / (c - 1)
w_2 = -1 / (c - 1)
E_ZNE = [c * E(1) - E(c)] / (c - 1)
```

---

## 4. Gate Folding in Detail

### 4.1 Global Gate Folding

Fold the entire circuit: C -> C . C^dag . C

The folded circuit implements the same ideal unitary but with 3x the noise.

For noise factor lambda = 2k + 1 (k folds):
```
C_folded = C . (C^dag . C)^k
```

### 4.2 Local Gate Folding

Fold individual gates: G -> G . G^dag . G

This allows finer control over noise levels by folding only a subset of gates.

For a circuit with N gates and target noise factor lambda = 1 + 2f:
```
n_folded = f * N   (number of gates to fold once)
```

### 4.3 Noise Scaling Analysis

Under depolarizing noise with per-gate error rate p:

- Without folding (lambda=1): E(1) = E_ideal * (1-2p)^N
- With folding (lambda=k): E(k) = E_ideal * (1-2p)^(k*N)

So E(lambda) = E_ideal * exp(-gamma * lambda) where gamma = -N * ln(1-2p).

---

## 5. Bias-Variance Tradeoff

### 5.1 Bias

ZNE bias comes from the truncation of higher-order terms:

```
Bias = |E_ZNE - E_ideal| ~ O(lambda_max^(M+1))
```

where M is the extrapolation order. Higher-order extrapolation reduces bias but...

### 5.2 Variance

...increases variance. The variance of the ZNE estimate:

```
Var(E_ZNE) = sum_i w_i^2 * Var(E(lambda_i))
```

Richardson weights grow with order, amplifying statistical noise. For M noise levels:

```
Var(E_ZNE) / Var(E_raw) ~ Product_i (lambda_i + 1) / (lambda_i - lambda_j)^2
```

### 5.3 Optimal Strategy

- **Shallow circuits / low noise**: Linear extrapolation often suffices.
- **Deep circuits / high noise**: Exponential fit is more robust.
- **Shot budget**: Allocate more shots to higher noise levels (which have worse signal-to-noise).

---

## 6. Practical Considerations

### 6.1 Noise Model Assumptions

ZNE assumes noise scales uniformly with lambda. This holds approximately for:
- Depolarizing noise (scales as p -> lambda * p)
- Amplitude damping (scales approximately)

It may fail if:
- Different noise processes scale differently with gate count
- Noise has strong non-Markovian components

### 6.2 Observable Dependence

ZNE mitigates expectation values, not full distributions. Different observables may require different extrapolation models.

### 6.3 Combination with Other Techniques

- **ZNE + TREX**: TREX handles readout, ZNE handles gate noise
- **ZNE + Pauli Twirling**: Twirling simplifies noise model, making ZNE more reliable
- **ZNE + PEA**: PEA provides fine-grained noise amplification for ZNE

---

## 7. Error Bounds

### 7.1 Worst-Case Bound

Without assumptions on the noise model, ZNE provides no guaranteed error bound. The extrapolated value could be arbitrarily wrong if the true E(lambda) curve differs from the fitted model at lambda=0.

### 7.2 With Noise Model Assumptions

If the noise is depolarizing and the exponential model is correct:

```
|E_ZNE - E_ideal| <= C * Var(E)^{1/2} * (noise amplification factor)
```

The "noise amplification factor" is the cost of mitigation.

### 7.3 Sampling Overhead

The effective number of shots is reduced by the variance amplification:

```
N_effective = N_total / gamma^2
```

where gamma = sqrt(sum w_i^2) is the ZNE cost factor.

---

## 8. Implementation in Qiskit

### 8.1 Using Estimator with ZNE

In Qiskit Runtime, ZNE is available via resilience options:

```python
options.resilience_level = 2  # Enables ZNE
options.resilience.zne_mitigation = True
options.resilience.zne.noise_factors = [1, 3, 5]
options.resilience.zne.extrapolator = "exponential"
```

### 8.2 Manual Implementation

For local simulation:
1. Build folded circuits at each noise level
2. Run each circuit
3. Fit extrapolation model to (lambda, E) data
4. Evaluate at lambda=0

---

## 9. References

1. Temme, K., Bravyi, S., & Gambetta, J. M. (2017). "Error mitigation for short-depth quantum circuits." Physical Review Letters, 119(18), 180509.
2. Li, Y., & Benjamin, S. C. (2017). "Efficient variational quantum simulator incorporating active error minimization." Physical Review X, 7(2), 021050.
3. Giurgica-Tiron, T., et al. (2020). "Digital zero noise extrapolation for quantum error mitigation." IEEE International Conference on Quantum Computing and Engineering (QCE).
4. He, A., et al. (2020). "Zero-noise extrapolation for quantum-gate error mitigation with identity insertions." Physical Review A, 102(1), 012426.
5. Kim, Y., et al. (2023). "Evidence for the utility of quantum computing before fault tolerance." Nature, 618, 500-505.
6. Qiskit documentation: Zero-noise extrapolation - https://docs.quantum.ibm.com/
