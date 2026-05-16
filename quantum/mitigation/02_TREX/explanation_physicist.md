# TREX (Twirled Readout Error eXtinction) - Physicist's Deep Dive

## 1. Overview

TREX is a measurement error mitigation technique that **randomizes** readout errors by applying random X gates before measurement, then classically post-processing to undo the randomization. This converts arbitrary asymmetric readout errors into a simple symmetric (depolarizing-like) form that can be corrected by a single rescaling factor per qubit.

The key advantage over direct calibration (M3): TREX requires no separate calibration circuits and is self-calibrating from the experiment data itself.

---

## 2. The Problem with Asymmetric Readout Errors

### 2.1 Asymmetric Error Model

On superconducting qubits, readout errors are typically asymmetric:

```
P(measure 1 | state 0) = e_0   (typically small, ~1-2%)
P(measure 0 | state 1) = e_1   (typically larger, ~3-8%, due to T1 relaxation)
```

The asymmetry means that the error depends on the state being measured. This makes correction state-dependent and more complex.

### 2.2 Impact on Expectation Values

For a Pauli Z measurement on qubit k:

```
<Z>_measured = (1 - e_0 - e_1) * <Z>_ideal + (e_0 - e_1)
```

The offset term (e_0 - e_1) introduces a systematic bias that shifts the expectation value.

---

## 3. The TREX Protocol

### 3.1 Randomization Step

For each shot of the experiment:

1. Generate a random bit string r = (r_1, r_2, ..., r_n) where each r_k is 0 or 1 with equal probability.
2. Before measurement, apply X gate to qubit k if r_k = 1.
3. Measure all qubits, obtaining outcome string m = (m_1, ..., m_n).
4. Classical post-processing: the "de-twirled" outcome is s_k = m_k XOR r_k.

### 3.2 Effect on Readout Errors

Without twirling, for qubit k in state |b> (b = 0 or 1):

```
P(measure m | state b) = A[m, b]   (from assignment matrix)
```

With twirling (applying X if r=1):
- If r=0: state stays |b>, measure normally
- If r=1: state becomes |1-b> (X applied), measure, then flip result back

The effective error probability becomes:

```
P(s != b) = (1/2)(e_0 + e_1) = e_sym
```

regardless of whether b=0 or b=1. The error is now **symmetric**.

### 3.3 Mathematical Proof

The twirled assignment matrix for qubit k:

```
A_twirled = (1/2)(A + X * A * X)
```

where X is the Pauli X matrix. Expanding:

```
A = [[1-e_0, e_1],    X*A*X = [[1-e_1, e_0],
     [e_0, 1-e_1]]             [e_1,   1-e_0]]
```

```
A_twirled = (1/2) * [[2 - e_0 - e_1,  e_0 + e_1],
                      [e_0 + e_1,      2 - e_0 - e_1]]

           = [[(1 - e_sym),  e_sym],
              [e_sym,        (1 - e_sym)]]
```

where e_sym = (e_0 + e_1) / 2. This is a symmetric depolarizing channel.

---

## 4. Correction via Rescaling

### 4.1 Single-Qubit Correction

With symmetric readout errors, the measured expectation value of Z on qubit k:

```
<Z>_measured = (1 - 2 * e_sym) * <Z>_ideal
```

No offset term! The correction is simply:

```
<Z>_corrected = <Z>_measured / (1 - 2 * e_sym)
              = <Z>_measured / (1 - e_0 - e_1)
```

### 4.2 Multi-Qubit Correction for Pauli Strings

For a Pauli string O = P_1 (x) P_2 (x) ... (x) P_n, where each P_k is I or Z:

```
<O>_corrected = <O>_measured / Product_{k: P_k = Z} (1 - 2 * e_sym_k)
```

The correction factor is a product over only those qubits where Z appears (identity qubits contribute factor 1).

### 4.3 Estimating e_sym

The symmetric error rate e_sym can be estimated from the twirled data itself:

1. For each random bit string r, the fraction of de-twirled outcomes that are "flipped" relative to the majority gives an estimate of e_sym.
2. Alternatively, use a subset of shots with known preparation (like calibration).

A self-consistent approach: from the twirled measurements, the probability of any bitstring is a noisy version of the ideal. The noise factor can be estimated from the variance structure.

---

## 5. Comparison with Direct Calibration

| Property                  | Direct Calibration (M3) | TREX                    |
|---------------------------|-------------------------|-------------------------|
| Separate calibration      | Yes (2n circuits)       | No (self-calibrating)   |
| Handles asymmetry         | Directly                | Symmetrizes first       |
| Correction complexity     | Matrix inversion        | Simple rescaling        |
| Shot overhead             | Calibration shots       | ~2x per-shot overhead   |
| Correlations              | Can model (CTMP)        | Assumes uncorrelated    |
| Time drift                | Sensitive               | Robust (real-time cal.) |

---

## 6. Combining TREX with Other Techniques

### 6.1 TREX + ZNE

TREX handles readout errors while ZNE handles gate errors. They are complementary:
1. Apply TREX to symmetrize readout errors
2. Run circuits at multiple noise levels for ZNE
3. Correct readout via TREX rescaling
4. Extrapolate to zero gate noise via ZNE

### 6.2 TREX + Pauli Twirling

Pauli twirling converts gate noise to Pauli channels, while TREX converts readout noise to symmetric form. Together, they simplify the entire noise model to a tractable form.

---

## 7. Limitations

1. **Assumes uncorrelated readout errors**: TREX symmetrizes each qubit independently. Correlated readout errors (crosstalk) are not fully addressed.

2. **Overhead in shots**: Each shot requires generating a random bit string and applying conditional X gates. This effectively doubles the circuit depth by 1 gate layer.

3. **Variance amplification**: The rescaling factor 1/(1 - 2*e_sym) amplifies statistical noise. For large e_sym, more shots are needed to maintain precision.

4. **Only corrects readout errors**: TREX does not address gate errors or state preparation errors.

---

## 8. Implementation Notes

### 8.1 Efficient Randomization

Rather than generating per-shot random strings, batch the shots:
- Group shots by random string r
- Pre-compile one circuit per unique r (or a representative subset)
- Classical post-processing combines results from all groups

### 8.2 Qiskit Integration

In Qiskit Runtime, TREX is available via the resilience options. When using SamplerV2 or EstimatorV2:

```python
options.resilience.measure_mitigation = True
options.resilience.measure_noise_learning.num_randomizations = 32
```

The runtime automatically handles the randomization and post-processing.

---

## 9. References

1. van den Berg, E., Minev, Z. K., & Temme, K. (2022). "Model-free readout-error mitigation for quantum expectation values." Physical Review A, 105(3), 032620.
2. Wallman, J. J., & Emerson, J. (2016). "Noise tailoring for scalable quantum computation via randomized compiling." Physical Review A, 94(5), 052325.
3. Kandala, A., et al. (2019). "Error mitigation extends the computational reach of a noisy quantum processor." Nature, 567(7749), 491-495.
4. Qiskit documentation: Readout error mitigation - https://docs.quantum.ibm.com/
