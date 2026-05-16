# Quantum Neural Networks (QNN) - Physicist's Deep Dive

## 1. Overview

Quantum Neural Networks (QNNs) are parameterized quantum circuits used as machine learning models, analogous to classical neural networks. In Qiskit, two main QNN implementations exist:

- **EstimatorQNN:** Outputs expectation values of observables <psi(x,theta)|O|psi(x,theta)>
- **SamplerQNN:** Outputs quasi-probabilities from sampling the circuit output

QNNs serve as the quantum equivalent of a classical function approximator f(x; theta), where x is input data and theta are trainable parameters.

---

## 2. Mathematical Framework

### 2.1 QNN as a Function

A QNN implements a function:
```
f(x; theta) = <0^n| U^dag(x, theta) O U(x, theta) |0^n>
```

where:
- x in R^d is the classical input data
- theta in R^p are the trainable parameters
- U(x, theta) = V(theta) W(x) is the quantum circuit
- W(x) is the feature map (data encoding)
- V(theta) is the variational ansatz (trainable)
- O is the observable (measurement operator)

### 2.2 EstimatorQNN

EstimatorQNN uses the Estimator primitive to compute expectation values.

**Output:** For a single observable O:
```
f_est(x; theta) = <psi(x, theta)| O |psi(x, theta)>
```

For multiple observables {O_1, ..., O_m}:
```
f_est(x; theta) = [<O_1>, <O_2>, ..., <O_m>]
```

This provides a continuous output in [-1, 1] per observable (for Pauli observables).

**Gradient computation:**
Using the parameter shift rule (see VQE physicist.md):
```
d f / d theta_j = (f(theta_j + pi/2) - f(theta_j - pi/2)) / 2
```

### 2.3 SamplerQNN

SamplerQNN uses the Sampler primitive to compute output probabilities.

**Output:** The probability distribution over measurement outcomes:
```
f_samp(x; theta) = [P(0|x,theta), P(1|x,theta), ..., P(2^n - 1|x,theta)]
```

Or with a custom interpret function g that maps bitstrings to labels:
```
f_samp(x; theta) = [P(g(z) = 0), P(g(z) = 1), ...]
```

For binary classification with parity:
```
g(z) = z_0 XOR z_1 XOR ... XOR z_{n-1}
```

### 2.4 Loss Functions

**For classification (cross-entropy):**
```
L(theta) = -(1/N) sum_i [y_i log(f(x_i; theta)) + (1-y_i) log(1 - f(x_i; theta))]
```

**For regression (MSE):**
```
L(theta) = (1/N) sum_i (y_i - f(x_i; theta))^2
```

### 2.5 Forward and Backward Pass

**Forward pass:**
1. Encode data: |psi_0> = W(x)|0>
2. Apply ansatz: |psi> = V(theta)|psi_0>
3. Measure observable: output = <psi|O|psi> (or sample distribution)

**Backward pass (gradient):**
1. For each parameter theta_j, compute two shifted circuits
2. Forward pass each shifted circuit
3. Gradient = (output_+ - output_-) / 2
4. Total: 2p circuit evaluations per gradient step

---

## 3. QNN Architecture Choices

### 3.1 Data Encoding Strategies

**Amplitude encoding:**
```
|x> = (1/||x||) sum_i x_i |i>
```
Encodes d-dimensional data in log2(d) qubits. Very efficient but requires deep circuits.

**Angle encoding:**
```
|phi(x)> = tensor_i R_Y(x_i) |0>
```
Encodes d-dimensional data in d qubits. Simple but limited expressiveness.

**Re-uploading (data re-encoding):**
```
U(x, theta) = V_L(theta_L) W(x) V_{L-1}(theta_{L-1}) W(x) ... V_1(theta_1) W(x)
```
Interleaves data encoding with trainable layers. Provably universal for function approximation (Perez-Salinas et al., 2020).

### 3.2 Observable Selection

**Single Pauli-Z:** Binary output in [-1, 1]
```
O = Z_0
```

**Magnetization:** Average Z over all qubits
```
O = (1/n) sum_i Z_i
```

**Custom observables:** Weighted Pauli strings for multi-class output

### 3.3 Output Interpretation

For classification with c classes and n qubits:
- **Method 1:** Use c observables, one per class -> f in R^c
- **Method 2:** Use SamplerQNN with interpret function -> P(class_k)
- **Method 3:** Use single observable, threshold at 0 -> binary

---

## 4. Training QNNs

### 4.1 Optimization Landscape

QNN loss landscapes can be:
- **Smooth:** When the circuit is shallow and the problem is simple
- **Rugged:** With many local minima for complex problems
- **Flat:** Barren plateaus for deep or random circuits

### 4.2 Optimizers for QNNs

**Gradient-based:**
- SPSA: Stochastic, only 2 evaluations per step
- Adam: Requires accurate gradients (parameter shift)
- L-BFGS-B: Second-order, fast convergence when gradients are accurate

**Gradient-free:**
- COBYLA: Robust to noise
- Nelder-Mead: Good for few parameters

### 4.3 Regularization

- **Early stopping:** Monitor validation loss
- **Parameter norm penalty:** L2 regularization on theta
- **Dropout-inspired:** Randomly skip gates during training (not standard in Qiskit)

---

## 5. Universality and Expressiveness

### 5.1 Universal Approximation Theorem for QNNs

A QNN with data re-uploading (encoding x multiple times) can approximate any continuous function f: R^d -> R to arbitrary precision (given sufficient circuit depth and parameters).

**Theorem (Perez-Salinas et al., 2020):**
A single-qubit QNN with L layers of alternating data encoding and parameterized rotations:
```
U(x, theta) = prod_{l=1}^{L} R_Z(theta_{l,3}) R_Y(theta_{l,2}) R_Z(theta_{l,1}) R_Y(x)
```
can approximate any function f: [0, 2*pi] -> [-1, 1] using a Fourier series with L terms.

### 5.2 Fourier Analysis of QNNs

The output of a QNN can be written as a truncated Fourier series:
```
f(x; theta) = sum_{k=-L}^{L} c_k(theta) exp(i k x)
```

where the accessible frequencies {k} are determined by the circuit architecture, and the Fourier coefficients c_k(theta) are determined by the trainable parameters.

---

## 6. Comparison: EstimatorQNN vs SamplerQNN

| Property | EstimatorQNN | SamplerQNN |
|----------|-------------|------------|
| Output | Expectation values <O> | Probabilities P(z) |
| Range | [-1, 1] per observable | [0, 1] (probabilities) |
| Multi-output | Multiple observables | Multiple bitstring classes |
| Gradient | Parameter shift rule | Parameter shift rule |
| Use case | Regression, binary classif. | Multi-class classification |
| Noise sensitivity | Moderate | Higher (probabilities are noisier) |

---

## 7. References

1. Schuld, M. & Petruccione, F. "Machine Learning with Quantum Computers." 2nd ed. Springer (2021).
2. Perez-Salinas, A., et al. "Data re-uploading for a universal quantum classifier." Quantum 4, 226 (2020).
3. Schuld, M., Sweke, R., & Meyer, J. K. "Effect of data encoding on the expressive power of variational quantum-machine-learning models." PRA 103, 032430 (2021).
4. Abbas, A., et al. "The power of quantum neural networks." Nature Computational Science 1, 403-409 (2021).
