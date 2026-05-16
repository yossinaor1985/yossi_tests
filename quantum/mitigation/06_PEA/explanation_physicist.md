# Probabilistic Error Amplification (PEA) - Physicist's Deep Dive

## 1. Overview

Probabilistic Error Amplification (PEA) is a technique for controlled noise amplification, designed to be used with Zero-Noise Extrapolation (ZNE). While gate folding (the standard noise amplification for ZNE) is simple, it amplifies ALL noise sources equally and only allows integer (or coarse fractional) noise scaling. PEA provides **fine-grained, continuous** control over the noise level by probabilistically injecting Pauli errors.

---

## 2. Motivation

### 2.1 Limitations of Gate Folding

Gate folding (G -> G G^dag G) has limitations:
1. **Discrete noise levels**: Lambda = 1, 3, 5, ... (or fractional via partial folding)
2. **Uniform amplification**: All noise sources are amplified equally
3. **Circuit depth increase**: Each fold triples the gate count
4. **Inconsistent noise model**: Folded circuits may not accurately model scaled-up noise

### 2.2 PEA Advantages

PEA addresses these by:
1. **Continuous lambda**: Any noise factor lambda >= 1 is achievable
2. **Targeted amplification**: Can amplify specific noise types
3. **Minimal circuit overhead**: Only adds single-qubit Pauli gates
4. **Accurate noise scaling**: Directly scales the effective error rate

---

## 3. Theory

### 3.1 Noise Channel Model

Assume the noisy implementation of a gate G is:

```
E_G(rho) = (1-p) * G rho G^dag + p * sum_k q_k * P_k G rho G^dag P_k^dag
```

where p is the total error probability and {q_k} are the relative Pauli error probabilities (sum q_k = 1).

The noise channel (after removing the ideal gate) is:

```
Lambda(rho) = (1-p) rho + p * sum_k q_k P_k rho P_k^dag
```

### 3.2 PEA Amplification

To amplify the noise by factor lambda, PEA modifies the channel to:

```
Lambda_amp(rho) = (1 - lambda*p) rho + lambda*p * sum_k q_k P_k rho P_k^dag
```

This is achieved by inserting Pauli errors with probability (lambda-1)*p / (1 - p) after each gate:

```
P_amplify = (lambda - 1) * p * q_k / (1 - p)
```

for each Pauli P_k.

### 3.3 Proof of Correctness

The total error probability after PEA injection:

```
p_total = p + (1-p) * P_amplify_total
        = p + (1-p) * (lambda-1)*p / (1-p)
        = p + (lambda-1)*p
        = lambda * p
```

So the effective error rate is exactly lambda * p.

### 3.4 Constraint: lambda * p <= 1

For the amplified channel to be valid (probabilities non-negative):

```
lambda * p <= 1  =>  lambda <= 1/p
```

If the base error rate is p = 0.01, the maximum amplification is lambda = 100.

---

## 4. Noise Learning

### 4.1 Why We Need Noise Characterization

PEA requires knowledge of the noise channel (the Pauli error probabilities {p * q_k}). This is obtained through **noise learning** -- characterizing the Pauli error channel for each gate.

### 4.2 Methods for Noise Learning

**Randomized Benchmarking (RB)**: Measures the average gate error rate p.

**Interleaved RB**: Measures the error rate of a specific gate.

**Cycle Benchmarking**: Characterizes the full Pauli error channel for a cycle of gates.

**Noise Reconstruction from Twirling**: After Pauli twirling, the noise is a Pauli channel. Its parameters can be estimated from the twirled measurement statistics.

### 4.3 Practical Noise Learning

For each gate layer:
1. Apply Pauli twirling to convert noise to a Pauli channel
2. Run circuits with known preparations and measurements
3. Estimate per-Pauli error rates from the statistics

---

## 5. PEA + ZNE Pipeline

### 5.1 Full Protocol

1. **Noise Learning**: Characterize Pauli error rates for each gate layer
2. **PEA Circuits**: For each target noise factor lambda_i:
   a. Compute injection probabilities for each gate
   b. For each shot, randomly insert Pauli errors with computed probabilities
   c. Run circuit and record result
3. **ZNE Extrapolation**: Fit E(lambda) and extrapolate to lambda = 0

### 5.2 Advantages over Gate Folding + ZNE

| Property                  | Gate Folding + ZNE    | PEA + ZNE              |
|---------------------------|-----------------------|------------------------|
| Lambda values             | Discrete (1,3,5,...)  | Continuous             |
| Circuit depth             | Increases 3x per fold | Constant (+ 1Q gates) |
| Noise model fidelity      | Approximate           | Exact (if noise known) |
| Requires noise learning   | No                    | Yes                    |
| Shot overhead             | None                  | Per-shot randomization |

### 5.3 Optimal Noise Factor Selection

For PEA + ZNE, choose noise factors to minimize the variance of the extrapolated estimate:

- For linear extrapolation: lambda_1 = 1, lambda_2 = 1 + delta (small delta for low variance but high bias)
- For exponential: lambda_1 = 1, lambda_2, lambda_3 spread over range [1, 1/p]

---

## 6. Implementation Details

### 6.1 Per-Shot Randomization

For each shot at noise factor lambda:
1. For each gate in the circuit:
   a. Compute injection probability: p_inject = (lambda - 1) * p_gate / (1 - p_gate)
   b. With probability p_inject, insert a random Pauli error (weighted by {q_k})
   c. Otherwise, do nothing
2. Run the modified circuit
3. Record the measurement outcome

### 6.2 Batching for Efficiency

Rather than modifying per-shot, batch the shots:
- Generate N random circuit instances for noise factor lambda
- Each instance has Pauli errors inserted at random positions
- Run all instances and average the results

### 6.3 Sign Correction

When Pauli errors are inserted, some observables acquire a sign flip. The measurement outcome must be multiplied by the appropriate sign:

```
<O>_corrected = (1/N) * sum_i sign_i * outcome_i
```

where sign_i = +1 or -1 depending on which Paulis were inserted.

---

## 7. Limitations

1. **Requires noise characterization**: PEA needs knowledge of the Pauli error rates, which may be expensive to obtain and can drift over time.
2. **Pauli noise assumption**: Works best when the actual noise is well-approximated by a Pauli channel (use Pauli twirling first).
3. **Maximum amplification**: Lambda is bounded by 1/p. For very low noise gates, this allows large amplification; for noisy gates, the range is limited.
4. **Shot overhead**: Each noise factor requires its own set of shots with per-shot randomization.

---

## 8. References

1. Temme, K., Bravyi, S., & Gambetta, J. M. (2017). "Error mitigation for short-depth quantum circuits." Physical Review Letters, 119(18), 180509.
2. Kim, Y., et al. (2023). "Evidence for the utility of quantum computing before fault tolerance." Nature, 618, 500-505.
3. van den Berg, E., Minev, Z. K., Kandala, A., & Temme, K. (2023). "Probabilistic error cancellation with sparse Pauli-Lindblad models on noisy quantum processors." Nature Physics, 19, 1116-1121.
4. Cai, Z., et al. (2023). "Quantum error mitigation." Reviews of Modern Physics, 95(4), 045005.
5. Qiskit documentation: Error mitigation - https://docs.quantum.ibm.com/
