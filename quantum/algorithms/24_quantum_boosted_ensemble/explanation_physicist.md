# Quantum Boosted Ensemble (PQC Weak Learners + Classical AdaBoost) - Physicist's Deep Dive

## 1. Overview

Algorithms 23 (QBoost) and 24 (this topic) both combine quantum computing with ensemble methods, but in opposite directions:

| Aspect | QBoost (Topic 23) | Quantum Boosted Ensemble (This Topic) |
|--------|-------------------|--------------------------------------|
| Weak learners | Classical (decision stumps) | **Quantum** (shallow PQCs) |
| Ensemble method | Quantum (QUBO selection) | **Classical** (AdaBoost) |
| Quantum role | Optimize which classifiers to keep | Act as the classifiers themselves |
| Hardware needs | Quantum annealer / QAOA | Gate-based NISQ device |

**Core idea:** Instead of using quantum optimization to SELECT classical classifiers (QBoost), here we use quantum circuits AS the weak learners themselves, combined via the classical AdaBoost algorithm. Each weak learner is a shallow parameterized quantum circuit (PQC) that classifies only slightly better than random. The ensemble of many such weak quantum classifiers, weighted by their performance, can achieve strong classification accuracy.

This approach is fundamentally NISQ-friendly: shallow circuits (1-2 qubits, 1 repetition layer) have low gate errors, and the boosting framework compensates for individual weakness through composition.

---

## 2. Mathematical Foundation

### 2.1 The AdaBoost Algorithm

AdaBoost (Adaptive Boosting) was introduced by Freund & Schapire (1997). It builds a strong classifier from a sequence of weak classifiers, where each successive weak learner focuses on the samples that previous learners misclassified.

**Setup:** Training data {(x_i, y_i)}_{i=1}^{m} with x_i in R^d, y_i in {-1, +1}.

**Algorithm:**

1. **Initialize** uniform sample weights:
```
D_1(i) = 1/m    for i = 1, ..., m
```

2. **For** t = 1, ..., T (boosting rounds):

   (a) Train weak learner h_t: D^d -> {-1, +1} on weighted data (D_t, X, y).

   (b) Compute weighted error:
   ```
   epsilon_t = sum_{i=1}^{m} D_t(i) * I[h_t(x_i) != y_i]
   ```
   where I[.] is the indicator function.

   (c) Compute learner weight:
   ```
   alpha_t = (1/2) * ln((1 - epsilon_t) / epsilon_t)
   ```
   Note: alpha_t > 0 when epsilon_t < 1/2 (better than random), and alpha_t increases as epsilon_t decreases (better classifiers get louder votes).

   (d) Update sample weights:
   ```
   D_{t+1}(i) = D_t(i) * exp(-alpha_t * y_i * h_t(x_i)) / Z_t
   ```
   where Z_t is a normalization constant ensuring sum_i D_{t+1}(i) = 1.

   **Key insight:** When h_t(x_i) = y_i (correct prediction), the exponent is negative, so D_{t+1}(i) < D_t(i) -- the weight decreases. When h_t(x_i) != y_i (misclassification), the exponent is positive, so D_{t+1}(i) > D_t(i) -- the weight increases. This forces the next learner to focus on hard examples.

3. **Final classifier** (weighted majority vote):
```
H(x) = sign(sum_{t=1}^{T} alpha_t * h_t(x))
```

**Convergence guarantee:** The training error of H(x) satisfies:
```
err_train(H) <= exp(-2 * sum_{t=1}^{T} gamma_t^2)
```
where gamma_t = 1/2 - epsilon_t is the "edge" of the t-th weak learner over random guessing. As long as each gamma_t > 0 (each learner is slightly better than random), the training error decreases exponentially with the number of boosting rounds T.

---

### 2.2 Parameterized Quantum Circuits as Weak Learners

A PQC weak learner is a shallow quantum circuit that maps a classical input x to a binary prediction {-1, +1}.

**Architecture:**

```
|0>^n --[Feature Map S(x)]--[Ansatz V(theta)]--[Measure Z_0]
```

**Feature Map S(x):** Encodes the classical input x into the quantum state. We use ZFeatureMap:
```
S(x) = prod_{j=1}^{n} exp(i * x_j * Z_j)
```
This applies single-qubit Z-rotations parameterized by the input features. For n=2 qubits with reps=1, this is a simple, shallow encoding.

**Ansatz V(theta):** A trainable circuit with parameters theta. We use RealAmplitudes:
```
V(theta) = prod_{l=1}^{L} [CNOT layer] * prod_{j=1}^{n} R_Y(theta_{l,j})
```
For reps=1 with linear entanglement on 2 qubits, this gives:
```
V(theta) = CNOT(0,1) * R_Y(theta_3) tensor R_Y(theta_4) * R_Y(theta_1) tensor R_Y(theta_2)
```

Wait -- let us be precise about the parameter count. RealAmplitudes(2, reps=1, entanglement='linear') has:
- Initial layer: 2 R_Y gates (theta_0, theta_1)
- CNOT layer: 1 CNOT gate (qubit 0 -> qubit 1)
- Final layer: 2 R_Y gates (theta_2, theta_3)
- Total trainable parameters: 4

**Measurement and prediction:**

After applying S(x) and V(theta), we measure the expectation value of Z on qubit 0:
```
f_theta(x) = <0| V^dag(theta) S^dag(x) (Z_0 tensor I_{rest}) S(x) V(theta) |0>
```

The prediction is:
```
h(x) = sign(f_theta(x)) = sign(<Z_0>)
```
If <Z_0> > 0, predict +1; otherwise predict -1.

**Why are these "weak" learners?**

A shallow PQC with 2 qubits and 1 repetition layer has limited expressibility. The set of functions {f_theta : theta in R^p} that it can represent is a strict subset of all binary classifiers. This limited hypothesis class means:
- It cannot perfectly classify arbitrary training sets
- It typically achieves accuracy only slightly above 50%
- This is exactly the "weak learner" requirement for AdaBoost: epsilon_t < 1/2

The shallow depth is a feature, not a bug: it ensures the circuit is "weak" enough for boosting to be effective, AND it minimizes gate errors on NISQ hardware.

---

### 2.3 Training Weighted Quantum Classifiers

In standard PQC training, we minimize the unweighted loss. In AdaBoost, each round requires training on weighted data. We modify the loss function to incorporate the sample weights D_t.

**Weighted loss function:**

For a PQC with parameters theta at boosting round t, the weighted misclassification-proxy loss is:
```
L(theta) = sum_{i=1}^{m} D_t(i) * ell(y_i, f_theta(x_i))
```

We use the weighted hinge-like loss:
```
ell(y_i, f_theta(x_i)) = (1 - y_i * f_theta(x_i)) / 2
```

This loss equals 0 when f_theta(x_i) = y_i (correct with full confidence) and equals 1 when f_theta(x_i) = -y_i (wrong with full confidence).

So the total weighted loss is:
```
L(theta) = sum_{i=1}^{m} D_t(i) * (1 - y_i * <Z_0>_i) / 2
```

**Optimization:** We minimize L(theta) using COBYLA (Constrained Optimization BY Linear Approximation), a derivative-free optimizer well-suited for noisy quantum landscapes:
- Derivative-free: does not require gradient computation through the quantum circuit
- Bounded: converges in a controlled number of function evaluations
- Noise-tolerant: works reasonably well with stochastic loss functions

**Warm-starting:** In practice, the optimal parameters theta*_t from round t can be used as the initial point for round t+1, since the weighted data distributions D_t and D_{t+1} are related (they differ only by a reweighting). This can speed up convergence.

---

### 2.4 Expressibility vs Ensemble Size Trade-off

There is a fundamental trade-off between the expressibility of individual weak learners and the number of boosting rounds needed:

**Shallow PQC (low expressibility) + many boosting rounds:**
- Each h_t can only represent simple decision boundaries (roughly linear or slightly curved)
- Need many rounds T to approximate a complex boundary
- Each circuit is cheap (few gates, low error)
- Total cost: T * (cost per shallow circuit)

**Deep PQC (high expressibility) + single model:**
- A single deep circuit can represent complex decision boundaries
- Only one model, no boosting needed
- Each circuit is expensive (many gates, high error accumulation)
- Total cost: 1 * (cost per deep circuit)

**The ensemble advantage:** Consider a target decision boundary B that requires expressibility E to represent. A shallow PQC with expressibility e << E cannot represent B directly. However, the boosted ensemble:
```
H(x) = sign(sum_{t=1}^{T} alpha_t * h_t(x))
```
is a weighted sum of simple functions. By the universal approximation properties of boosted ensembles, as T -> infinity, H(x) can approximate arbitrarily complex boundaries, even though each h_t is simple.

**Formal statement:** If the weak learner hypothesis class H_weak has VC dimension d, the boosted ensemble after T rounds has effective VC dimension O(T * d). So boosting with T=10 shallow PQCs (d=4 each) gives effective VC dimension ~40, comparable to a single deep circuit with 40 parameters.

**Practical implication for NISQ:** On current hardware with ~0.1-1% two-qubit gate error rates:
- A circuit with 20 CNOT gates accumulates ~2-20% error
- A circuit with 2 CNOT gates accumulates ~0.2-2% error
- 10 shallow circuits (2 CNOTs each) executed independently have max individual error ~2%, and boosting naturally handles noisy predictions through its weighting mechanism

---

### 2.5 Advantage for NISQ

**Gate error mitigation through shallowness:**

On NISQ devices, the fidelity of a quantum circuit decreases approximately exponentially with circuit depth:
```
F(circuit) ~ prod_{gates} (1 - p_gate) ~ exp(-N_gates * p_avg)
```

For a single deep VQC with depth D and N_gates gates:
```
F_deep ~ exp(-N_gates_deep * p_avg)
```

For a shallow PQC in the boosted ensemble (depth d << D):
```
F_shallow ~ exp(-N_gates_shallow * p_avg) >> F_deep
```

**Parallelizability:**

Each weak learner h_t at boosting round t depends on the sample weights D_t, which depend on the performance of h_{t-1}. So the boosting rounds are inherently sequential. However:
- Within each round, the evaluation of h_t(x_i) for different samples i can be parallelized across multiple QPUs
- The training optimization (COBYLA iterations) involves independent circuit evaluations that can be batched

**Shot allocation as sample weighting:**

An elegant alternative to modifying the loss function: instead of weighting samples in the loss, allocate shots proportional to sample weights. Samples with higher D_t(i) get more shots, effectively reducing measurement noise for the samples that matter most.

---

## 3. Detailed Example

**Setup:** 150 samples from make_moons (sklearn), a nonlinear 2D classification task. Features scaled to [0, pi]. Labels in {-1, +1}. Split 70/30 train/test.

**Weak PQC architecture:**
- 2 qubits
- ZFeatureMap(2, reps=1): 2 feature parameters
- RealAmplitudes(2, reps=1, entanglement='linear'): 4 trainable parameters
- Measurement: Z on qubit 0
- Total circuit depth: ~6 layers (very shallow)

**Boosting with T=5 rounds:**

| Round t | epsilon_t | alpha_t | Interpretation |
|---------|-----------|---------|----------------|
| 1 | ~0.35 | ~0.31 | First PQC on uniform weights; modest accuracy |
| 2 | ~0.38 | ~0.25 | Focuses on round-1 mistakes; still weak |
| 3 | ~0.33 | ~0.35 | Better edge on hard samples |
| 4 | ~0.40 | ~0.20 | Diminishing returns; small alpha |
| 5 | ~0.36 | ~0.29 | Another weak but useful classifier |

Each individual PQC achieves only 60-67% accuracy. But the boosted ensemble H(x) = sign(sum alpha_t h_t(x)) can reach 75-85% accuracy on make_moons.

**Comparison with a single deep VQC:**
- RealAmplitudes(2, reps=3): 8 trainable parameters, ~14 layers
- Trained on unweighted data with COBYLA
- Achieves ~70-80% accuracy

The boosted ensemble of 5 shallow PQCs often matches or exceeds the single deep VQC, while using circuits that are individually much shallower and more hardware-friendly.

---

## 4. Comparison

| Criterion | Boosted Shallow PQCs | Single Deep VQC | Classical AdaBoost |
|-----------|---------------------|-----------------|-------------------|
| **Circuit depth** | Very shallow (reps=1) | Deep (reps=3+) | N/A |
| **Total parameters** | T*p (e.g., 5*4=20) | p_deep (e.g., 8) | N/A |
| **Gate errors (NISQ)** | Low per circuit | High (error accumulation) | N/A |
| **Training** | T sequential rounds, each cheap | Single optimization, expensive | T sequential rounds, very cheap |
| **Expressibility** | Low per learner, high in ensemble | High (single model) | Depends on base learner |
| **Parallelism** | Evaluation parallelizable | Single circuit | Trivially parallelizable |
| **make_moons accuracy** | ~75-85% | ~70-80% | ~90-95% (with trees) |
| **Hardware requirement** | NISQ-ready (shallow) | NISQ but noisy | Classical only |
| **Theoretical grounding** | Boosting theory guarantees | Variational (heuristic) | Well-established |

**Key takeaway:** Boosted shallow PQCs offer a principled way to get ensemble-level accuracy from NISQ-friendly circuits. Classical AdaBoost with decision trees will likely outperform both quantum approaches on small datasets, but the quantum approach becomes interesting when the quantum feature encoding captures structure that classical features miss.

---

## 5. References

1. **Freund, Y. & Schapire, R. E.** (1997). "A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting." *Journal of Computer and System Sciences*, 55(1), 119-139. [The original AdaBoost algorithm.]

2. **Schuld, M., Sweke, R., & Meyer, J. K.** (2021). "Effect of data encoding on the expressive power of variational quantum machine learning models." *Physical Review A*, 103(3), 032430. [Analysis of expressibility of quantum feature maps and ansatze.]

3. **Abbas, A., Sutter, D., Zoufal, C., Lucchi, A., Figalli, A., & Woerner, S.** (2021). "The power of quantum neural networks." *Nature Computational Science*, 1(6), 403-409. [Effective dimension and expressibility of PQCs.]

4. **Havlicek, V., Corcoles, A. D., Temme, K., Harrow, A. W., Kandala, A., Chow, J. M., & Gambetta, J. M.** (2019). "Supervised learning with quantum-enhanced feature spaces." *Nature*, 567(7747), 209-212. [Experimental demonstration of quantum classification.]

5. **Macaluso, A., Clissa, L., Lodi, S., & Sartori, C.** (2020). "Quantum ensemble for classification." *arXiv:2007.01028*. [Ensemble methods with quantum weak learners.]
