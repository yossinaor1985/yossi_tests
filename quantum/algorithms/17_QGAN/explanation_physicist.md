# Quantum Generative Adversarial Networks (QGAN) - Physicist's Deep Dive

## 1. Overview

Quantum GANs adapt the classical GAN framework to quantum computing. The most practical near-term architecture uses a quantum generator (parameterized circuit) and a classical discriminator (neural network). The generator produces samples from a quantum Born distribution, and the discriminator distinguishes real data from generated samples.

---

## 2. Classical GAN Recap

### 2.1 Minimax Game

A GAN consists of a generator G and discriminator D playing a minimax game:

```
min_G max_D V(D, G) = E_{x~p_data}[log D(x)] + E_{z~p_z}[log(1 - D(G(z)))]
```

At the Nash equilibrium: G perfectly generates the data distribution, and D outputs 1/2 everywhere.

### 2.2 Training

Alternating optimization:
1. Fix G, update D to better distinguish real vs fake
2. Fix D, update G to better fool D

---

## 3. QGAN Architectures

### 3.1 Quantum Generator + Classical Discriminator (Most Practical)

```
z (random) -> Quantum Circuit G(theta) -> Measurement -> x_fake
                                                         |
                                                         v
x_real -------> Classical NN D(phi) --------> real/fake
x_fake -------> Classical NN D(phi) --------> real/fake
```

The quantum generator G(theta)|0>^n produces a state whose measurement distribution approximates the target data distribution.

### 3.2 Born Machine Interpretation

The quantum generator naturally defines a Born machine:

```
P_G(x) = |<x|G(theta)|0>^n|^2
```

This is the probability of measuring bitstring x when preparing G(theta)|0> and measuring in the computational basis.

**Key advantage:** Born machines can efficiently represent certain distributions that require exponentially many parameters classically (e.g., distributions with long-range correlations).

### 3.3 Continuous Output via Post-Processing

For continuous data (e.g., financial time series), the discrete samples from the quantum circuit are mapped to continuous values:

```
x_continuous = f_decode(bitstring) = sum_k 2^{-k} * bit_k * (x_max - x_min) + x_min
```

This maps n-bit strings to 2^n uniformly spaced values in [x_min, x_max].

---

## 4. Training Dynamics

### 4.1 Generator Loss

The generator minimizes:
```
L_G(theta) = E_{z}[log(1 - D(G(theta, z)))]
```

or equivalently (non-saturating form):
```
L_G(theta) = -E_{z}[log D(G(theta, z))]
```

### 4.2 Discriminator Loss

The discriminator maximizes (or minimizes the negative):
```
L_D(phi) = -E_{x~real}[log D(x; phi)] - E_{x~fake}[log(1 - D(x; phi))]
```

### 4.3 Gradient for Quantum Generator

The parameter shift rule computes exact gradients for the generator:
```
dL_G/d(theta_j) = (1/2)[L_G(theta_j + pi/2) - L_G(theta_j - pi/2)]
```

Each gradient evaluation requires 2 circuit executions (shifted parameters), plus forward passes through the discriminator.

### 4.4 Training Stability

QGANs suffer from similar instabilities as classical GANs:
- Mode collapse (generator ignores part of the distribution)
- Vanishing gradients when discriminator is too strong
- Oscillation between generator and discriminator

Mitigation: careful learning rate scheduling, label smoothing, spectral normalization.

---

## 5. Applications

### 5.1 Loading Probability Distributions

QGANs can load arbitrary probability distributions onto quantum states, useful for quantum finance (option pricing), quantum chemistry (state preparation), and quantum simulation.

### 5.2 Synthetic Data Generation

Generate synthetic samples that match the statistical properties of real data while preserving privacy.

### 5.3 Quantum State Tomography

The adversarial framework can learn to generate a target quantum state without full tomography.

---

## 6. Expressivity

### 6.1 Born Machine Expressivity

**Theorem (Coyle et al., 2020):** A parameterized quantum circuit with n qubits and polynomial depth can represent distributions that require exponential classical resources.

Specifically, if the circuit generates a distribution corresponding to the output of a quantum computation in IQP (Instantaneous Quantum Polynomial) or BosonSampling, then no polynomial-size classical circuit can sample from the same distribution (under standard complexity assumptions).

### 6.2 Barren Plateaus in QGANs

The generator gradient can exhibit barren plateaus when:
- The circuit is too deep (hardware-efficient ansatz with random initialization)
- Global cost functions are used

Mitigation: shallow circuits, local cost functions, structured initialization.

---

## 7. References

1. Lloyd, S. & Weedbrook, C. "Quantum generative adversarial learning." Physical Review Letters 121, 040502 (2018).
2. Dallaire-Demers, P.-L. & Killoran, N. "Quantum generative adversarial networks." Physical Review A 98, 012324 (2018).
3. Zoufal, C., Lucchi, A., & Woerner, S. "Quantum Generative Adversarial Networks for learning and loading random distributions." npj Quantum Information 5, 103 (2019).
4. Coyle, B., et al. "The Born supremacy: quantum advantage and training of an Ising Born machine." npj Quantum Information 6, 60 (2020).
5. Goodfellow, I., et al. "Generative Adversarial Nets." NeurIPS 2014.