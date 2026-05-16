# Variational Quantum Regressor (VQR) - Physicist's Deep Dive

## 1. Overview

The Variational Quantum Regressor (VQR) extends the variational quantum classifier (VQC, Topic 12) from discrete classification to continuous-valued regression. Instead of predicting class labels, VQR predicts a real-valued output y in R for each input x.

The core idea: a parameterized quantum circuit maps input features x to a quantum state |psi(x, theta)>, and the expectation value of an observable O provides the regression prediction:

```
f(x; theta) = <psi(x, theta)| O |psi(x, theta)>
```

This is trained by minimizing the mean squared error between predictions and targets.

---

## 2. Mathematical Framework

### 2.1 VQR Circuit

The complete VQR unitary is identical in structure to VQC:

```
|psi(x, theta)> = U(theta) U_phi(x) |0>^n
```

where:
- U_phi(x): feature map encoding classical input x into quantum state
- U(theta): variational ansatz with trainable parameters theta

The key difference from VQC is the output interpretation:
- VQC: class label from measurement probabilities
- VQR: continuous value from expectation value <O>

### 2.2 Output Function

The regression function is:

```
f(x; theta) = <psi(x, theta)| O |psi(x, theta)>
            = <0|^n U_phi(x)^dag U(theta)^dag O U(theta) U_phi(x) |0>^n
```

For a single-qubit observable O = Z_0 (Pauli-Z on qubit 0):
```
f(x; theta) in [-1, 1]
```

For multi-output regression with K outputs, use K observables {O_1, ..., O_K}:
```
f_k(x; theta) = <psi(x, theta)| O_k |psi(x, theta)>
```

### 2.3 Output Scaling

Since expectation values are bounded (e.g., <Z> in [-1, 1]), we typically need an affine rescaling:

```
y_pred = a * f(x; theta) + b
```

where a and b are determined by the target range. For targets in [y_min, y_max]:
```
a = (y_max - y_min) / 2
b = (y_max + y_min) / 2
```

Alternatively, normalize targets to [-1, 1] before training.

### 2.4 Loss Function

The standard loss is mean squared error (MSE):

```
L(theta) = (1/N) sum_{i=1}^{N} (y_i - f(x_i; theta))^2
```

For the VQR class in Qiskit, the loss can also be:
- L1 loss: (1/N) sum |y_i - f(x_i; theta)|
- Huber loss: combination of L1 and L2 (robust to outliers)

---

## 3. Feature Map Encoding

### 3.1 Encoding Strategies for Regression

The feature map U_phi(x) determines how input data influences the quantum state. For regression, the encoding directly determines which functions f(x; theta) the model can represent.

**ZZFeatureMap** (standard choice):
```
U_ZZ(x) = prod_l [H^n * prod_i exp(i x_i Z_i) * prod_{i<j} exp(i (pi-x_i)(pi-x_j) Z_i Z_j)]
```

**Data re-uploading** (enhanced expressivity):
```
U(x, theta) = V_L(theta_L) W(x) ... V_1(theta_1) W(x)
```

With data re-uploading, the output is a truncated Fourier series in x (Schuld et al., 2021):
```
f(x; theta) = sum_{k=-L}^{L} c_k(theta) * exp(i k omega x)
```

This is particularly powerful for 1D regression: L re-uploading layers gives a 2L+1 term Fourier series.

### 3.2 Expressivity for Regression

**Theorem (Schuld et al., 2021):** A quantum model with data-encoding gates R(x omega) repeated L times generates functions of the form:

```
f(x) = sum_{omega in Omega} c_omega * exp(i omega x)
```

where Omega is the set of frequencies determined by the encoding gate spectrum and L controls the truncation.

For R_Y(x) encoding: Omega = {-L, -L+1, ..., L-1, L}
For R_Z(x) encoding: same frequency spectrum

**Consequence:** The number of re-uploading layers directly controls the function complexity the model can represent. More layers = higher-frequency components = more complex functions.

---

## 4. Ansatz Design for Regression

### 4.1 RealAmplitudes

```
U(theta) = prod_l [CNOT_chain * prod_i R_Y(theta_{l,i})]
```

Sufficient for many regression tasks. The R_Y rotations produce real-valued amplitudes, and the CNOT chain creates entanglement for multi-feature correlations.

### 4.2 EfficientSU2

```
U(theta) = prod_l [CNOT_chain * prod_i R_Z(theta_{l,i,2}) R_Y(theta_{l,i,1})]
```

Full SU(2) rotations per qubit. More expressive but more parameters (2n per layer vs n for RealAmplitudes).

### 4.3 Depth Considerations

For regression, the ansatz depth controls the "resolution" of the approximation:
- Shallow (reps=1): smooth, low-complexity functions
- Deep (reps=3+): complex, high-frequency functions
- Too deep: barren plateaus and overfitting

Rule of thumb: reps = O(log n) to avoid barren plateaus while maintaining expressivity.

---

## 5. Gradient Computation

### 5.1 Parameter Shift Rule

Identical to VQC (Topic 12, Section 3.1). For each parameter theta_j:

```
dL/d(theta_j) = (1/N) sum_i 2(f(x_i) - y_i) * df(x_i)/d(theta_j)
```

where:
```
df/d(theta_j) = (1/2)[f(theta_j + pi/2) - f(theta_j - pi/2)]
```

### 5.2 Gradient Cost for Regression

Per training step with N data points and p parameters:
- Function evaluations: 2 * p * N (parameter shift for each sample)
- Shots per evaluation: S
- Total shots: 2pNS

This is more expensive than classification because every training sample contributes to the gradient through the MSE loss.

---

## 6. Connection to Classical Methods

### 6.1 Quantum Kernel Regression

VQR can be viewed as a kernel regression model. The quantum kernel:
```
K(x, x') = |<phi(x)|phi(x')>|^2
```

defines an RKHS in which the optimal regressor is:
```
f*(x) = sum_i alpha_i K(x_i, x)
```

VQR implicitly solves this with the variational ansatz providing the coefficients alpha_i through its parameters theta.

### 6.2 Comparison with Classical Regression

| Aspect | VQR | Linear Regression | Neural Network |
|--------|-----|-------------------|----------------|
| Model | <psi\|O\|psi> | w^T x + b | g(Wx + b) |
| Feature space | 2^n dimensional | d dimensional | arbitrary |
| Parameters | O(nL) | O(d) | O(d * width * depth) |
| Training | gradient-free/shift | closed form | backpropagation |
| Expressivity | Fourier series | linear | universal approx |

---

## 7. Multi-Output Regression

For K-dimensional output y in R^K, use K observables:

```
O_k = Z_k (Pauli-Z on qubit k), k = 1, ..., K
```

The loss becomes:
```
L(theta) = (1/N) sum_i sum_k (y_{i,k} - f_k(x_i; theta))^2
```

This requires K <= n (outputs bounded by qubit count) and a single circuit evaluation yields all K outputs simultaneously.

---

## 8. Convergence and Generalization

### 8.1 Generalization Bound

For a VQR with p parameters trained on N samples:
```
E[L_test] <= L_train + O(sqrt(p * log(N) / N))
```

This scales like classical regression with p effective degrees of freedom.

### 8.2 Overfitting

VQR can overfit when:
- Too many parameters relative to training data
- Feature map creates too-expressive embedding
- Insufficient regularization

Mitigation: L2 regularization on parameters, early stopping, cross-validation.

---

## 9. References

1. Mitarai, K., et al. "Quantum circuit learning." Physical Review A 98, 032309 (2018).
2. Schuld, M., Sweke, R., & Meyer, J. K. "Effect of data encoding on the expressive power of variational quantum-machine-learning models." Physical Review A 103, 032430 (2021).
3. Cerezo, M., et al. "Variational quantum algorithms." Nature Reviews Physics 3, 625-644 (2021).
4. Perez-Salinas, A., et al. "Data re-uploading for a universal quantum classifier." Quantum 4, 226 (2020).
5. Abbas, A., et al. "The power of quantum neural networks." Nature Computational Science 1, 403-409 (2021).
6. Qiskit Machine Learning documentation: https://qiskit-community.github.io/qiskit-machine-learning/