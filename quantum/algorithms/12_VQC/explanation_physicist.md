# Variational Quantum Classifier (VQC) - Physicist's Deep Dive

## 1. Overview

The Variational Quantum Classifier (VQC) is a supervised quantum machine learning algorithm that classifies classical data by encoding it into quantum states, processing it through a parameterized quantum circuit, and extracting predictions via measurement. VQC belongs to the family of variational quantum algorithms where a classical optimizer tunes circuit parameters to minimize a classification loss function.

The VQC pipeline consists of three stages:
1. **Feature map (data encoding):** Map classical input x to a quantum state via U_phi(x)|0>
2. **Variational ansatz:** Apply a trainable unitary U(theta) to learn decision boundaries
3. **Measurement:** Extract class probabilities from the output state

This structure is analogous to a classical neural network: the feature map is the input layer, the ansatz is the hidden layer(s), and the measurement is the output layer. The crucial difference is that VQC operates in an exponentially large Hilbert space, potentially enabling richer feature representations.

---

## 2. Mathematical Framework

### 2.1 Full VQC Circuit

The complete VQC unitary acting on n qubits is:

```
U_VQC(x, theta) = U(theta) * U_phi(x)
```

The output state is:

```
|psi(x, theta)> = U(theta) * U_phi(x) |0>^n
```

Classification is performed by measuring the expectation value of an observable O (typically Z on the first qubit):

```
f(x, theta) = <psi(x, theta)| O |psi(x, theta)>
```

For binary classification:
- If f(x, theta) >= 0: predict class 0
- If f(x, theta) < 0: predict class 1

Or equivalently, the probability of measuring |0> on the readout qubit:

```
p(class = 0 | x) = |<0| Tr_{rest}(|psi><psi|) |0>|
```

### 2.2 Feature Map: U_phi(x)

The feature map encodes a classical data vector x = (x_1, ..., x_d) into a quantum state. The encoding strategy critically determines the model's expressivity.

**ZZFeatureMap** (second-order Pauli encoding):

```
U_phi(x) = [prod_{l=1}^{r} U_ZZ(x) * H^{tensor n}]
```

where:

```
U_ZZ(x) = exp(i * sum_{i} x_i Z_i + i * sum_{i<j} (pi - x_i)(pi - x_j) Z_i Z_j)
```

The ZZ interaction terms create entanglement that depends on data features, making the encoding nonlinear. This is essential: without nonlinear encoding, the quantum model reduces to a linear classifier in the original feature space.

The feature map defines an implicit kernel:

```
kappa(x, x') = |<0^n| U_phi(x')^dag U_phi(x) |0^n>|^2
```

This is the same kernel used in QSVC (Topic 11). VQC can be viewed as a kernel method where the kernel is implicitly defined but the classifier is parameterized rather than computed via a support vector formulation.

**Data re-uploading:** Repeating the feature map r times increases the effective nonlinearity of the encoding. Each repetition applies the data-dependent unitary again, creating higher-order functions of the input features:

```
U_phi^{(r)}(x) = [U_phi(x)]^r
```

This is analogous to using higher-degree polynomial features in classical ML.

### 2.3 Variational Ansatz: U(theta)

The ansatz is a parameterized circuit with trainable parameters theta = (theta_1, ..., theta_p). Common choices:

**RealAmplitudes:**

```
U(theta) = prod_{l=1}^{L} [ENT_l * prod_{i=1}^{n} R_Y(theta_{l,i})]
```

This produces states with real-valued amplitudes only (no complex phases). Despite this restriction, it is sufficient for many classification tasks.

- Parameters per layer: n
- Total parameters: n(L + 1) (including final rotation layer)
- Entangling gates per layer: n - 1 (linear CNOT chain)

**EfficientSU2:**

```
U(theta) = prod_{l=1}^{L} [ENT_l * prod_{i=1}^{n} R_Z(theta_{l,i,2}) R_Y(theta_{l,i,1})]
```

Full SU(2) rotations per qubit, more expressive but more parameters.

The ansatz depth L controls the trade-off between expressibility and trainability (see Section 5).

### 2.4 Loss Function

For binary classification with labels y in {0, 1}, the cross-entropy loss is:

```
L(theta) = -(1/N) * sum_{i=1}^{N} [y_i * log(p_i) + (1 - y_i) * log(1 - p_i)]
```

where p_i = p(class = 1 | x_i, theta) is the predicted probability for sample x_i.

In practice, VQC implementations often use a simpler squared-error loss:

```
L(theta) = (1/N) * sum_{i=1}^{N} (y_i - f(x_i, theta))^2
```

where f(x_i, theta) = <psi(x_i, theta)| Z_0 |psi(x_i, theta)> is the expectation value.

For multi-class classification (K classes), use K readout qubits and the softmax cross-entropy:

```
L(theta) = -(1/N) * sum_{i=1}^{N} sum_{k=1}^{K} y_{i,k} * log(p_{i,k})
```

where p_{i,k} is the probability of measuring |1> on the k-th readout qubit.

---

## 3. Parameter Shift Rule for Gradients

### 3.1 The Fundamental Result

For a parameterized gate of the form exp(-i theta_j G / 2) where G is a generator with eigenvalues +/-1 (e.g., Pauli operators), the gradient of the expectation value with respect to theta_j is:

```
d<O>/d(theta_j) = (1/2) [<O>_{theta_j + pi/2} - <O>_{theta_j - pi/2}]
```

This is **exact** (not a finite-difference approximation). It requires only two circuit evaluations per parameter.

### 3.2 Derivation

Consider a cost function C(theta) = <0| U(theta)^dag O U(theta) |0> where U(theta) contains a gate R_j(theta_j) = exp(-i theta_j G_j / 2).

We can write U(theta) = V * R_j(theta_j) * W where V and W are the parts of the circuit after and before the j-th gate respectively.

Then:

```
C(theta) = <phi| R_j(theta_j)^dag M R_j(theta_j) |phi>
```

where |phi> = W|0> and M = V^dag O V.

Differentiating:

```
dC/d(theta_j) = <phi| (i/2)[G_j, R_j^dag M R_j] |phi>
```

Using the fact that for G_j with eigenvalues +/-1:

```
R_j(theta_j +/- pi/2) = (1/sqrt(2))(I -/+ i G_j) R_j(theta_j)
```

After algebraic manipulation:

```
dC/d(theta_j) = (1/2)[C(theta_j + pi/2) - C(theta_j - pi/2)]
```

### 3.3 Gradient Cost

For a VQC with p parameters, computing the full gradient requires 2p circuit evaluations. Each evaluation requires O(S) shots for statistical accuracy, where S is the number of shots.

Total measurement budget per gradient step: 2pS

With p ~ O(nL) parameters and S ~ O(1/epsilon^2) shots for precision epsilon:

```
Total shots per step ~ O(nL / epsilon^2)
```

### 3.4 Natural Gradient

The natural gradient uses the quantum Fisher information matrix F to precondition the gradient:

```
theta_{t+1} = theta_t - eta * F(theta_t)^{-1} * grad L(theta_t)
```

The quantum Fisher information matrix elements are:

```
F_{ij} = Re[<d_i psi | d_j psi>] - <d_i psi|psi><psi|d_j psi>
```

where |d_j psi> = d|psi>/d(theta_j).

Natural gradient converges faster but requires O(p^2) additional circuit evaluations to estimate F.

---

## 4. Expressibility of VQC Models

### 4.1 Universal Approximation

A VQC with sufficient depth can approximate any classification function to arbitrary accuracy (universal approximation theorem for quantum models). Formally:

For any continuous function g: R^d -> R and any epsilon > 0, there exist circuit parameters theta* such that:

```
sup_{x in X} |f(x, theta*) - g(x)| < epsilon
```

provided the feature map is sufficiently nonlinear and the ansatz has enough layers.

### 4.2 Effective Dimension

The expressibility of a VQC is quantified by its effective dimension, which measures the volume of the function space the model can access:

```
d_eff = 2 * log(det(I + (n_data / (2*pi*ln(2))) * F_hat)) / log(n_data / (2*pi*ln(2)))
```

where F_hat is the normalized Fisher information matrix averaged over the parameter space.

Higher effective dimension means the model can represent a richer set of decision boundaries.

### 4.3 Feature Map Expressivity vs Ansatz Expressivity

The total model expressivity depends on BOTH components:

1. **Feature map expressivity:** Determines the "data geometry" in Hilbert space. A more complex feature map creates more nonlinear embeddings, enabling separation of more complex data distributions.

2. **Ansatz expressivity:** Determines the "decision boundary flexibility." A more expressive ansatz can draw more complex boundaries in the Hilbert space feature representation.

Critical insight: an overly expressive feature map with a simple ansatz can outperform a simple feature map with an expressive ansatz. The data encoding matters at least as much as the variational parameters.

### 4.4 Encoding Capacity

The encoding capacity C of a feature map with n qubits and d-dimensional input is bounded by:

```
C <= min(2^n, d_eff)
```

For the ZZFeatureMap with d features on n = d qubits:
- First-order terms: d parameters
- Second-order terms: d(d-1)/2 parameters
- Total encoding parameters: d + d(d-1)/2 = d(d+1)/2

This quadratic scaling in the number of features provides implicit nonlinear feature engineering.

---

## 5. Connection to Classical Neural Networks

### 5.1 Structural Analogy

| VQC Component | Neural Network Analog |
|---|---|
| Feature map U_phi(x) | Input layer / feature extraction |
| Variational ansatz U(theta) | Hidden layers |
| Measurement <O> | Output layer / activation |
| Parameter shift rule | Backpropagation |
| Cross-entropy loss | Cross-entropy loss |
| Qubits | Neurons (exponential state space) |
| Entangling gates | Skip connections / attention |

### 5.2 Kernel Interpretation

The VQC decision function can be rewritten as:

```
f(x, theta) = <0| U_phi(x)^dag U(theta)^dag Z_0 U(theta) U_phi(x) |0>
            = sum_{alpha, beta} c_{alpha,beta}(theta) * <0| U_phi(x)^dag |alpha><beta| U_phi(x) |0>
```

where the sum runs over computational basis states |alpha>, |beta>.

This shows that VQC computes a weighted combination of transition amplitudes, which is equivalent to a kernel model with a learned kernel:

```
f(x, theta) = sum_k w_k(theta) * phi_k(x)
```

where phi_k(x) are features in the quantum Hilbert space. The key difference from QSVC is that VQC learns the weights w_k implicitly through the variational parameters rather than via support vectors.

### 5.3 Barren Plateaus and Vanishing Gradients

The barren plateau problem in VQC is analogous to the vanishing gradient problem in deep neural networks:

```
Var[dL/d(theta_j)] <= F(n) * 2^{-n}
```

Mitigation strategies (see also Topic 9, Section 6):
1. Use problem-aware feature maps with limited depth
2. Keep ansatz depth O(log(n))
3. Use local cost functions (measure individual qubits, not global observables)
4. Initialize parameters near zero
5. Use layer-wise training (pre-train each layer before adding the next)
6. Implement warm-starting from classically pre-trained parameters

### 5.4 Advantages Over Classical Models

Potential quantum advantages in classification:
1. **Exponential feature space:** n qubits provide a 2^n-dimensional Hilbert space. Encoding into this space is analogous to mapping to a 2^n-dimensional feature space, which would require exponential resources classically.
2. **Entanglement-based correlations:** Entangling gates create feature interactions that have no efficient classical analog for certain data distributions.
3. **Quantum kernels:** The implicit kernel kappa(x, x') can be hard to compute classically for certain feature maps, potentially providing a computational advantage.

Caveat: Proven quantum advantage for classification on practical datasets remains an open question. Current results suggest advantages primarily for data with quantum-native structure.

---

## 6. Training Dynamics

### 6.1 Optimization Landscape

The VQC loss landscape L(theta) is generally non-convex with:
- Multiple local minima
- Saddle points
- Barren plateaus (for deep circuits)
- Narrow ravines (for overparameterized circuits)

However, for overparameterized VQCs (more parameters than training samples), the loss landscape becomes more favorable:
- Local minima are closer to global minima
- The optimization landscape resembles that of overparameterized neural networks

### 6.2 Optimizer Selection

| Optimizer | Type | VQC suitability | Notes |
|---|---|---|---|
| COBYLA | Gradient-free | Good for noisy hardware | No gradient computation needed |
| SPSA | Stochastic gradient | Good for noisy gradients | Only 2 evaluations per step |
| L-BFGS-B | Quasi-Newton | Best for simulators | Requires exact gradients |
| Adam | Gradient descent | Good general-purpose | Works with parameter shift |
| QN-SPSA | Natural gradient | Best convergence | Higher per-step cost |

### 6.3 Convergence Guarantees

For a VQC with p parameters trained on N samples with cross-entropy loss:

Generalization bound:
```
L_test <= L_train + O(sqrt(p * log(N) / N))
```

This is analogous to the VC-dimension bound in classical learning theory, with the effective VC dimension scaling as O(p) where p is the number of variational parameters.

---

## 7. Multi-class Extension

### 7.1 One-vs-All Approach

For K classes, train K binary VQC classifiers:
- Classifier k: distinguishes class k from all other classes
- Prediction: argmax_k f_k(x, theta_k)
- Cost: K times the single-classifier cost

### 7.2 Multi-qubit Readout

Use K readout qubits, one per class:

```
p(class = k | x) = <psi(x,theta)| (I - Z_k)/2 |psi(x,theta)>
```

Normalize via softmax: p_k = exp(f_k) / sum_j exp(f_j)

This approach requires only a single circuit execution per prediction.

---

## 8. References

1. Havlicek, V., et al. "Supervised learning with quantum-enhanced feature spaces." Nature 567, 209-212 (2019).
2. Schuld, M. & Killoran, N. "Quantum Machine Learning in Feature Hilbert Spaces." Physical Review Letters 122, 040504 (2019).
3. Mitarai, K., et al. "Quantum circuit learning." Physical Review A 98, 032309 (2018).
4. Schuld, M., Sweke, R., & Meyer, J. K. "Effect of data encoding on the expressive power of variational quantum-machine-learning models." Physical Review A 103, 032430 (2021).
5. Abbas, A., et al. "The power of quantum neural networks." Nature Computational Science 1, 403-409 (2021).
6. Cerezo, M., et al. "Variational quantum algorithms." Nature Reviews Physics 3, 625-644 (2021).
7. Perez-Salinas, A., et al. "Data re-uploading for a universal quantum classifier." Quantum 4, 226 (2020).
8. Benedetti, M., et al. "Parameterized quantum circuits as machine learning models." Quantum Science and Technology 4, 043001 (2019).
