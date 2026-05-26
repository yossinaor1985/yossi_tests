# Federated Quantum Neural Networks - Physicist's Deep Dive

## 1. Overview

Federated Quantum Neural Networks (Federated QNNs) combine **Federated Learning** (FL) with **Parameterized Quantum Circuits** (PQCs) to enable collaborative quantum machine learning without sharing raw data. Multiple clients each hold a private local dataset and train a shared PQC model locally; only the trained **parameter vectors** are communicated to a central server, which aggregates them to produce an updated global model.

This paradigm directly addresses a fundamental tension in quantum machine learning: while quantum data encoding and model expressivity benefit from large, diverse datasets, privacy regulations and practical constraints often prohibit centralizing data. Federated QNNs resolve this by keeping data local and communicating only classical parameter updates.

**Key references:**
- McMahan et al. (2017): introduced the **Federated Averaging (FedAvg)** algorithm for classical neural networks.
- Chen et al. (2021): first systematic study of federated learning applied to variational quantum circuits, demonstrating that FedAvg transfers directly to PQC parameters.
- Li et al. (2021): analysis of convergence properties under non-IID quantum data distributions.
- Sheng and Zhang (2017): early work on distributed quantum computation and privacy-preserving quantum protocols.

**Prerequisite:** The reader should be familiar with algorithm 13 (QNN) and algorithm 09 (PQC Ansatz Design). This material builds on the PQC training framework established there.

---

## 2. Mathematical Foundation

### 2.1 Federated Learning Framework

Consider N clients, each holding a local dataset D_i of size |D_i|. The total dataset size is |D| = sum_{i=1}^{N} |D_i|. The global empirical risk minimization objective is:

```
L(theta) = sum_{i=1}^{N} (|D_i| / |D|) L_i(theta)
```

where L_i(theta) is the local loss function computed on client i's data:

```
L_i(theta) = (1 / |D_i|) sum_{(x, y) in D_i} l(f(x; theta), y)
```

Here l is the per-sample loss function (e.g., mean-squared error or cross-entropy), and f(x; theta) is the model prediction for input x given parameters theta.

**Federated Averaging (FedAvg) protocol (McMahan et al. 2017):**

```
For each communication round t = 0, 1, 2, ..., T-1:
    1. Server broadcasts global parameters theta^t to all N clients
    2. Each client i initializes theta_i^t = theta^t
    3. Each client i performs E epochs of local gradient descent:
           theta_i^{t,e+1} = theta_i^{t,e} - eta * grad L_i(theta_i^{t,e})
       for e = 0, 1, ..., E-1, with theta_i^{t,0} = theta^t
    4. Each client i sends theta_i^{t+1} = theta_i^{t,E} to the server
    5. Server aggregates:
           theta^{t+1} = (1/N) sum_{i=1}^{N} theta_i^{t+1}
       (or weighted: theta^{t+1} = sum_i (|D_i|/|D|) theta_i^{t+1})
```

This is the canonical form. For simplicity and when client datasets are of equal size, the uniform average (1/N) sum_i theta_i is used.

### 2.2 Parameterized Quantum Circuits as Models

The model f(x; theta) is a PQC that maps classical input x to a prediction. The circuit has the form:

```
|psi(x, theta)> = U(x, theta) |0>^n = W(theta) S(x) |0>^n
```

where:
- S(x) is a **feature map** (data encoding circuit) that encodes the classical input x into quantum amplitudes or phases. Common choices include ZZFeatureMap, ZFeatureMap, or angle encoding.
- W(theta) is a **trainable ansatz** (variational layer) parameterized by theta in R^p. Common choices include RealAmplitudes, EfficientSU2, or hardware-efficient ansatze.
- |0>^n is the n-qubit initial state.

The model output is an expectation value of an observable O:

```
f(x; theta) = <0^n| U^dag(x, theta) O U(x, theta) |0^n>
            = <psi(x, theta)| O |psi(x, theta)>
```

For binary classification, a typical choice is O = Z_0 (Pauli-Z on the first qubit), giving output in [-1, 1]. The predicted class is:

```
y_hat = sign(f(x; theta))
```

For a loss function using mean-squared error:

```
l(f(x; theta), y) = (f(x; theta) - y)^2
```

where y in {-1, +1} is the true label.

### 2.3 Local Training via Parameter Shift Rule

Each client trains the shared PQC architecture on its local data. The gradient of the expectation value with respect to a single parameter theta_k is computed using the **parameter shift rule** (valid for gates of the form exp(-i theta_k G / 2) where G^2 = I):

```
partial L / partial theta_k = [L(theta_k + pi/2) - L(theta_k - pi/2)] / 2
```

More explicitly, if the loss for a single sample (x, y) is l = (f(x; theta) - y)^2, then:

```
partial l / partial theta_k = 2(f(x; theta) - y) * partial f / partial theta_k
```

where:

```
partial f / partial theta_k = [f(x; theta_k + pi/2) - f(x; theta_k - pi/2)] / 2
```

This requires two circuit evaluations per parameter per sample. For p parameters and |D_i| samples, client i performs 2p|D_i| circuit evaluations per epoch.

**Gradient descent update:**

```
theta_k^{new} = theta_k^{old} - eta * partial L_i / partial theta_k
```

where eta is the learning rate.

### 2.4 Federated Averaging for Quantum Parameters

The critical insight enabling federated QML is that **PQC parameters are classical floating-point numbers**, even though they parameterize quantum gates. The aggregation step is therefore identical to classical federated learning:

```
theta^{t+1} = (1/N) sum_{i=1}^{N} theta_i^{t+1}
```

This is an element-wise arithmetic mean of N parameter vectors in R^p. No quantum communication channel is required for aggregation; only classical channels are needed.

**Why this works:** The loss landscape L(theta) of a PQC is a smooth function of theta (since expectation values are continuous functions of gate angles). The FedAvg aggregation corresponds to averaging over locally-descended points on this landscape. Under mild conditions (convexity or bounded gradient divergence), this converges to a neighborhood of the global minimum.

**What is NOT shared:**
- Raw data x_i: stays on client i
- Quantum states |psi(x_i, theta)>: never transmitted
- Measurement outcomes: only used locally to compute gradients

**What IS shared:**
- Only the parameter vector theta_i in R^p (a list of real numbers)

### 2.5 Privacy Considerations

Even though raw data is not shared, the parameter updates themselves can leak information about the local data distribution. An adversary observing theta_i^{t+1} - theta^t (the parameter delta) can potentially infer properties of D_i through model inversion attacks.

**Differential Privacy (DP) enhancement:** Add calibrated Gaussian noise to the parameter updates before sharing:

```
theta_i^{t+1, noisy} = theta_i^{t+1} + N(0, sigma^2 I_p)
```

where sigma is calibrated to achieve (epsilon, delta)-differential privacy. The privacy guarantee states that for any two neighboring datasets D_i, D_i' (differing in one sample), the distribution of theta_i^{t+1, noisy} is approximately the same.

The trade-off: larger sigma improves privacy but degrades convergence because the aggregated parameters are noisier. For quantum circuits with a small number of parameters (p ~ 10-50), the noise magnitude needed for DP can significantly impact training quality.

**Secure aggregation** is an alternative: clients encrypt their updates, the server computes the aggregate without seeing individual updates. This provides privacy without adding noise, but requires a more complex cryptographic protocol.

### 2.6 Non-IID Data Challenges

In practice, client data distributions are often **non-IID** (non-independent and identically distributed). For example:
- Client 1 might have mostly class-0 samples
- Client 2 might have mostly class-1 samples
- Client 3 might have a balanced mixture

This causes **client drift**: each client's locally-optimized parameters theta_i^{t+1} move toward different regions of parameter space, and their average may not be a good global model.

**Formally:** Let theta_i^* = argmin L_i(theta) be the local optimum for client i. If the theta_i^* are far apart in parameter space (due to divergent data distributions), then the federated average (1/N) sum_i theta_i^* may be far from the global optimum theta^* = argmin L(theta).

**Mitigation strategies:**
1. **FedProx** (Li et al., 2020): add a proximal term mu/2 ||theta_i - theta^t||^2 to each client's local objective, penalizing drift from the global model.
2. **Increased communication frequency:** more rounds with fewer local epochs (E=1) reduces drift.
3. **Data sharing:** each client shares a small public subset of data (if privacy allows).
4. **Personalization layers:** only federate a subset of parameters; keep some layers local.

---

## 3. Detailed Example

### 3.1 Setup

**Task:** Binary classification on the make_moons dataset (sklearn), using 3 federated clients.

**Circuit architecture:**
- n = 2 qubits
- Feature map: ZZFeatureMap(2, reps=1) - encodes 2D input features
- Ansatz: RealAmplitudes(2, reps=1, entanglement='linear') - trainable variational layer
- Observable: Z_0 (Pauli-Z on qubit 0)
- Total trainable parameters: p = 4 (for RealAmplitudes with 2 qubits, 1 rep, linear entanglement)

**Data preparation:**
1. Generate 150 samples from make_moons with noise=0.15
2. Scale features to [0, pi] for quantum encoding
3. Convert labels from {0, 1} to {-1, +1}
4. Partition into 3 client datasets of 50 samples each (or proportionally)
5. Hold out a test set from each client

### 3.2 The Training Protocol

```
Initialize theta^0 randomly in [0, 2*pi)^p

For t = 0, 1, ..., T-1 (communication rounds):
    For each client i = 1, 2, 3:
        theta_i <- theta^t  (receive global parameters)
        For epoch e = 1, ..., E:
            For each (x, y) in D_i:
                Compute f(x; theta_i) = <psi(x, theta_i)| Z_0 |psi(x, theta_i)>
                For each parameter k = 1, ..., p:
                    grad_k = [f(x; theta_i + pi/2 * e_k) - f(x; theta_i - pi/2 * e_k)] / 2
                    theta_i[k] -= eta * 2 * (f(x; theta_i) - y) * grad_k

    theta^{t+1} = (1/3) * (theta_1 + theta_2 + theta_3)
```

where e_k is the unit vector in the k-th direction.

### 3.3 Expected Behavior

- **Early rounds (t=0-2):** Accuracy improves rapidly as the model learns the basic decision boundary. Client drift is moderate because the model has not yet specialized.
- **Middle rounds (t=3-4):** Convergence slows. If data is IID across clients, accuracy approaches centralized training. If non-IID, a gap may persist.
- **Asymptotic accuracy:** For make_moons with noise=0.15 and a 2-qubit PQC, expect test accuracy in the range 75-90%, depending on the number of rounds and the specific data split.

### 3.4 Comparison: Federated vs. Centralized

| Property | Federated (3 clients) | Centralized |
|---|---|---|
| Data shared | None (only parameters) | All data on one machine |
| Communication rounds | T (e.g., 5) | 0 (all local) |
| Total training epochs | T * E * N | T_centralized |
| Privacy | Strong (data stays local) | None (all data visible) |
| Convergence speed | Slower (parameter drift) | Faster |
| Final accuracy | May be slightly lower | Upper bound |
| Communication cost | O(T * p * N) floats | 0 |
| Robustness | Tolerates client failures | Single point of failure |

---

## 4. Comparison with Centralized Training

### 4.1 Accuracy Trade-off

Centralized training on the union D = D_1 union ... union D_N provides the most informative gradient estimates (lowest variance) because each gradient step uses all available data. Federated training uses local gradients (higher variance due to smaller D_i) and introduces aggregation error.

**Theorem (informal):** Under L-smooth, mu-strongly convex loss, FedAvg with learning rate eta and E local epochs satisfies:

```
L(theta^T) - L(theta^*) <= O(1 / (mu * eta * T * E)) + O(eta^2 * E^2 * sigma_G^2 / N)
```

where sigma_G^2 measures the gradient divergence across clients. The first term decreases with more rounds; the second is a floor set by non-IID-ness.

### 4.2 Communication Efficiency

Each communication round transmits N parameter vectors of dimension p. For a 2-qubit PQC with p=4 parameters and 3 clients:
- Per round: 3 * 4 * 8 bytes = 96 bytes (negligible)
- For T=5 rounds: 480 bytes total

For larger circuits (e.g., 10 qubits, p=100 parameters, 50 clients):
- Per round: 50 * 100 * 8 bytes = 40 KB
- For T=50 rounds: 2 MB total

This is orders of magnitude less than transmitting raw quantum data or classical training data.

---

## 5. Complexity and Communication

### 5.1 Computational Complexity per Client per Round

For p parameters, |D_i| samples, and E local epochs:
- Circuit evaluations for gradient: 2p per sample (parameter shift rule)
- Total per client per round: 2p * |D_i| * E
- Example: p=4, |D_i|=50, E=5 => 2000 circuit evaluations

### 5.2 Communication Complexity

- Per round: O(N * p) real numbers transmitted (each client sends p floats to server, server sends p floats back)
- Total: O(T * N * p) real numbers over the full training
- Bandwidth: typically negligible compared to computation cost

### 5.3 Total Circuit Evaluations (All Clients)

```
Total = 2 * p * |D| * E * T
```

For our example: 2 * 4 * 150 * 5 * 5 = 30,000 circuit evaluations across all clients.

Compare with centralized training (same total epochs = E * T = 25):
```
Total_centralized = 2 * p * |D| * E_total = 2 * 4 * 150 * 25 = 30,000
```

Same total circuit evaluations, but distributed across clients in the federated case.

---

## 6. References

1. McMahan, B., Moore, E., Ramage, D., Hampson, S., & Arcas, B. A. "Communication-Efficient Learning of Deep Networks from Decentralized Data." AISTATS (2017). [FedAvg algorithm]
2. Chen, S., Zhong, W., Yang, L., Huang, P., & Zeng, G. "Federated Quantum Machine Learning." Entropy 23(4), 460 (2021). [First systematic study of federated QML with PQCs]
3. Li, T., Sahu, A. K., Zaheer, M., Sanjabi, M., Talwalkar, A., & Smith, V. "Federated Optimization in Heterogeneous Networks." MLSys (2020). [FedProx for non-IID data]
4. Sheng, Y. B., & Zhang, Q. "Distributed secure quantum machine learning." Science Bulletin 62(14), 1025-1029 (2017). [Early distributed quantum ML]
5. Schuld, M., Bergholm, V., Gogolin, C., Izaac, J., & Killoran, N. "Evaluating analytic gradients on quantum hardware." Physical Review A 99, 032331 (2019). [Parameter shift rule]
6. Li, W., Lu, S., & Deng, D.-L. "Quantum Federated Learning through Blind Quantum Computing." Science China Physics 64, 100312 (2021). [Privacy analysis in quantum FL]
7. Abbas, A., Sutter, D., Zoufal, C., Lucchi, A., Figalli, A., & Woerner, S. "The power of quantum neural networks." Nature Computational Science 1, 403-409 (2021). [PQC expressivity]
