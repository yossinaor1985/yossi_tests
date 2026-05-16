# Repetition Codes - Physicist's Deep Dive

## 1. Overview

The repetition code is the generalization of the 3-qubit bit-flip code to an arbitrary number of qubits d. It encodes a single logical qubit into d physical qubits, correcting up to floor((d-1)/2) bit-flip (X) errors. While it only protects against one type of error, it is the foundational model for understanding key concepts in quantum error correction: code distance, error thresholds, and the tradeoff between overhead and protection.

Code parameters: [[d, 1, d]] (d physical qubits, 1 logical qubit, distance d for bit-flip errors only)

---

## 2. Encoding

### 2.1 Logical States

For a d-qubit repetition code:

```
|0_L> = |00...0>  (d zeros)
|1_L> = |11...1>  (d ones)
```

General logical state:
```
|psi_L> = alpha|0_L> + beta|1_L> = alpha|00...0> + beta|11...1>
```

This is a d-qubit GHZ-type state.

### 2.2 Encoding Circuit

Starting from |psi> = alpha|0> + beta|1> on qubit 1, with qubits 2, ..., d initialized to |0>:

```
|psi>|0>...|0> -> CNOT(1,2) -> CNOT(1,3) -> ... -> CNOT(1,d) -> alpha|00...0> + beta|11...1>
```

Circuit for d = 5 (example):
```
q0: --|psi>--*-----*-----*-----*--
             |     |     |     |
q1: --|0>----X-----|-----|-----|--
                   |     |     |
q2: --|0>----------X-----|-----|--
                         |     |
q3: --|0>----------------X-----|--
                               |
q4: --|0>----------------------X--
```

The encoding circuit has depth 1 (all CNOTs can be parallelized if connectivity allows) and uses d-1 CNOT gates.

### 2.3 Proof of Correct Encoding

By induction. After CNOT(1, k) for k = 2, ..., j:
```
alpha|00...0> + beta|11...1>  (on qubits 1, ..., j)
```

Base case (j=1): trivially alpha|0> + beta|1>.

Inductive step: if we have alpha|00...0> + beta|11...1> on qubits 1,...,j, then CNOT(1, j+1) acting on qubit j+1 (in state |0>) gives:
```
alpha|00...0>|0> + beta|11...1>|1> = alpha|00...0> + beta|11...1>  (on qubits 1,...,j+1)
```

since CNOT flips the target when the control is |1>.

---

## 3. Stabilizer Structure

### 3.1 Stabilizer Generators

The d-qubit repetition code has d-1 independent stabilizer generators:

```
S_i = Z_i Z_{i+1}    for i = 1, 2, ..., d-1
```

These measure the parity between neighboring qubits. The full stabilizer group has 2^{d-1} elements (all products of generators).

### 3.2 Codespace Characterization

The codespace is the simultaneous +1 eigenspace of all stabilizers:

```
S_i |psi_L> = +|psi_L>    for all i = 1, ..., d-1
```

This means: all neighboring pairs of qubits have the same Z-parity, which forces all qubits to be in the same state. The only two states satisfying this are |00...0> and |11...1>, giving a 2-dimensional codespace (1 logical qubit).

### 3.3 Logical Operators

```
Z_L = Z_1  (or Z_i for any i, since all are equivalent modulo stabilizers)
X_L = X_1 X_2 ... X_d  (flip all d qubits)
```

The minimum-weight logical X operator has weight d, confirming the code distance is d.

### 3.4 Why Z_L = Z_1 Works

Since S_i = Z_i Z_{i+1} is in the stabilizer group, we have Z_i ~ Z_{i+1} (equivalent modulo stabilizers). By transitivity: Z_1 ~ Z_2 ~ ... ~ Z_d. So any single Z_i acts as the logical Z.

---

## 4. Error Model and Syndrome Decoding

### 4.1 Independent Bit-Flip Errors

Each qubit independently experiences an X error with probability p:

```
E_i(rho) = (1-p) rho + p X_i rho X_i
```

The total error channel on d qubits:
```
E(rho) = sum_{E in {I,X}^d} Pr(E) * E rho E^dag
```

where Pr(E) = p^{wt(E)} (1-p)^{d-wt(E)} and wt(E) is the number of X operators in E.

### 4.2 Syndrome Measurement

Each stabilizer S_i = Z_i Z_{i+1} has eigenvalue +1 (no boundary between qubits i and i+1) or -1 (boundary detected). The syndrome is a binary vector of length d-1:

```
s = (s_1, s_2, ..., s_{d-1})    where s_i in {0, 1}
```

s_i = 0 means Z_i Z_{i+1} = +1 (qubits i, i+1 agree)
s_i = 1 means Z_i Z_{i+1} = -1 (qubits i, i+1 disagree)

The syndrome detects the boundaries of error regions: if qubits j through k are flipped, the syndrome has s_{j-1} = 1 and s_k = 1 (if those indices exist), with all other entries 0.

### 4.3 Syndrome Table (d = 5 Example)

| Error Pattern | Syndrome (s1,s2,s3,s4) | Weight |
|---------------|------------------------|--------|
| IIIII | (0,0,0,0) | 0 |
| XIIII | (1,0,0,0) | 1 |
| IXIII | (1,1,0,0) | 1 |
| IIXII | (0,1,1,0) | 1 |
| IIIXI | (0,0,1,1) | 1 |
| IIIIX | (0,0,0,1) | 1 |
| XXIII | (0,1,0,0) | 2 |
| IXXII | (1,0,1,0) | 2 |
| IIXXI | (0,1,0,1) | 2 |
| IIIXX | (0,0,1,0) | 2 |

Note: errors of weight 1 and weight d-1 share syndromes (e.g., XIIII and IXXXX both give syndrome (1,0,0,0) for d=5). This is why the code can only correct up to floor((d-1)/2) errors.

### 4.4 Syndrome Measurement Circuit

```
q0: ----*-----------------------
        |
q1: ----|----*---*--------------
        |    |   |
q2: ----|----|---|----*---*-----
        |    |   |    |   |
q3: ----|----|---|----|----|---*---*--
        |    |   |    |   |   |   |
q4: ----|----|---|----|----|---|---|--
        |    |   |    |   |   |   |
a0: ----Z----Z---|----|----|---|---|-->  Measure (S1 = Z1Z2)
                 |    |   |   |   |
a1: -------------Z----Z---|---|---|-->  Measure (S2 = Z2Z3)
                          |   |   |
a2: ----------------------Z---Z---|-->  Measure (S3 = Z3Z4)
                                  |
a3: ------------------------------Z-->  Measure (S4 = Z4Z5)
```

(The last ancilla a3 needs one more CNOT from q4.)

---

## 5. Minimum Weight Decoding

### 5.1 Decoding Strategy

Given syndrome s, the decoder finds the minimum-weight error E consistent with s. For the repetition code, this is equivalent to majority vote:

1. The syndrome identifies the boundaries between "flipped" and "unflipped" regions
2. Each consistent error pattern corresponds to choosing which side of each boundary to flip
3. The minimum-weight decoder chooses the side with fewer qubits

### 5.2 Equivalence to Majority Vote

For the d-qubit repetition code, minimum-weight decoding is exactly majority vote: count the number of 0s and 1s. If the majority matches |0_L>, decode to |0_L>; otherwise decode to |1_L>.

Formally: if k qubits are flipped (k errors), correction succeeds iff k <= floor((d-1)/2), i.e., the flipped qubits are in the minority.

### 5.3 Connection to Classical Majority Vote

The quantum repetition code syndrome decoding is isomorphic to the classical repetition code with majority-vote decoding:

| | Classical | Quantum |
|---|---|---|
| Codewords | 000...0, 111...1 | |0_L> = |00...0>, |1_L> = |11...1> |
| Error detection | Read all bits, majority vote | Measure stabilizers Z_i Z_{i+1} |
| Information extracted | Full state (destructive) | Parity differences only (non-destructive) |
| Superposition | Not applicable | Preserved during syndrome measurement |

---

## 6. Error Rate Analysis

### 6.1 Logical Error Probability

The code fails when more than floor((d-1)/2) qubits are flipped. The logical error probability is:

```
p_L = sum_{k=ceil(d/2)}^{d} C(d,k) * p^k * (1-p)^{d-k}
```

where C(d,k) is the binomial coefficient "d choose k".

### 6.2 Leading-Order Approximation

For small p (p << 1), the dominant term is the lowest-order one:

```
p_L ~ C(d, ceil(d/2)) * p^{ceil(d/2)} * (1-p)^{floor(d/2)}
    ~ C(d, ceil(d/2)) * p^{ceil(d/2)}    for p << 1
```

This is a key result: the logical error rate scales as p^{ceil(d/2)}, giving polynomial suppression.

### 6.3 Error Rate Comparison for Small p

| Distance d | Leading term | Coefficient | Scaling |
|------------|-------------|-------------|---------|
| d = 3 | C(3,2) p^2 = 3p^2 | 3 | Quadratic |
| d = 5 | C(5,3) p^3 = 10p^3 | 10 | Cubic |
| d = 7 | C(7,4) p^4 = 35p^4 | 35 | Quartic |
| d = 9 | C(9,5) p^5 = 126p^5 | 126 | Quintic |

Numerical examples (p = 0.01):

| Distance | p_L (approx) | Improvement factor p/p_L |
|----------|-------------|------------------------|
| d = 3 | 3 * 10^{-4} | ~33x |
| d = 5 | 10 * 10^{-6} | ~10,000x |
| d = 7 | 35 * 10^{-8} | ~286,000x |
| d = 9 | 126 * 10^{-10} | ~7.9 * 10^7 x |

Each increase in d by 2 gains roughly two more orders of magnitude of error suppression (at p = 0.01).

### 6.4 Exact Formulas

For the three most common cases:

d = 3:
```
p_L = 3p^2(1-p) + p^3 = 3p^2 - 2p^3
```

d = 5:
```
p_L = C(5,3)p^3(1-p)^2 + C(5,4)p^4(1-p) + p^5
    = 10p^3 - 15p^4 + 6p^5
```

d = 7:
```
p_L = C(7,4)p^4(1-p)^3 + C(7,5)p^5(1-p)^2 + C(7,6)p^6(1-p) + p^7
    = 35p^4 - 84p^5 + 70p^6 - 20p^7
```

---

## 7. Threshold Concept

### 7.1 When Does the Code Help?

The code provides a benefit when the logical error rate is lower than the physical error rate:

```
p_L < p
```

For the d-qubit repetition code, this condition is satisfied when p < p_threshold.

### 7.2 Threshold for Repetition Code

The threshold is p_th = 1/2.

Proof: At p = 1/2, each qubit is equally likely to be flipped or not. Majority vote succeeds with probability exactly 1/2 (by symmetry), so p_L = 1/2 = p. For p < 1/2, the majority is more likely correct, so p_L < p. For p > 1/2, majority vote is worse than random.

Formal derivation for d = 3:
```
p_L < p
3p^2 - 2p^3 < p
3p^2 - 2p^3 - p < 0
p(3p - 2p^2 - 1) < 0
-p(2p^2 - 3p + 1) < 0
-p(2p - 1)(p - 1) < 0
```

For 0 < p < 1: this simplifies to (2p - 1) > 0 being false, i.e., p < 1/2.

### 7.3 Threshold Behavior

Below threshold (p < 1/2):
- Increasing d always reduces p_L
- In the limit d -> infinity, p_L -> 0 (perfect correction)

At threshold (p = 1/2):
- p_L = 1/2 for all d (no benefit from adding qubits)

Above threshold (p > 1/2):
- Increasing d makes things worse (p_L -> 1)
- The majority vote is systematically wrong

### 7.4 Exponential Suppression Below Threshold

For p < 1/2 and large d, the logical error rate decreases exponentially:

```
p_L ~ exp(-d * D_KL(1/2 || p))
```

where D_KL(1/2 || p) = (1/2) ln(1/(2p)) + (1/2) ln(1/(2(1-p))) is the Kullback-Leibler divergence. This is a consequence of the Chernoff bound applied to the binomial distribution.

---

## 8. Overhead Analysis

### 8.1 Resource Cost

| Distance d | Physical qubits | Ancilla qubits | Total qubits | CNOT gates (encoding) | Correctable errors |
|------------|----------------|-----------------|---------------|----------------------|-------------------|
| 3 | 3 | 2 | 5 | 2 | 1 |
| 5 | 5 | 4 | 9 | 4 | 2 |
| 7 | 7 | 6 | 13 | 6 | 3 |
| 9 | 9 | 8 | 17 | 8 | 4 |
| d | d | d-1 | 2d-1 | d-1 | floor((d-1)/2) |

### 8.2 Rate

The code rate R = k/n = 1/d decreases with increasing distance. This is the fundamental tradeoff: more protection requires more overhead.

---

## 9. Limitations

1. **Only corrects bit-flip (X) errors:** The repetition code provides zero protection against phase-flip (Z) errors or general errors. A single Z error on any qubit is an undetectable logical error (since Z_i acts as Z_L).

2. **Not a true quantum code:** The code distance for general errors is only 1, making it a [[d, 1, 1]] code in the general sense. It is effectively a classical repetition code embedded in quantum hardware.

3. **Phase errors are fatal:** Z_i commutes with all stabilizers (since Z_i commutes with Z_j Z_{j+1}), so phase errors produce no syndrome and cannot be detected.

4. **Not scalable alone:** To correct both bit-flip and phase-flip errors simultaneously requires more sophisticated codes (Shor code, surface codes, etc.).

5. **Why study it then?** Despite its limitations, the repetition code is invaluable because:
   - It demonstrates all key QEC concepts in the simplest setting
   - It is the building block of the surface code (a 2D version)
   - It is experimentally achievable and has been demonstrated on real hardware
   - The threshold and scaling concepts generalize directly to practical codes

---

## 10. Connection to Surface Codes

The surface code can be viewed as two interleaved repetition codes:
- One repetition code in the X-basis (correcting Z errors)
- One repetition code in the Z-basis (correcting X errors)

The 2D structure allows both types of errors to be corrected simultaneously. This connection makes the repetition code the essential pedagogical stepping stone to understanding surface codes.

---

## 11. References

1. Nielsen, M. A. & Chuang, I. L. "Quantum Computation and Quantum Information." Cambridge University Press (2010), Section 10.1.
2. Gottesman, D. "An Introduction to Quantum Error Correction and Fault-Tolerant Quantum Computation." arXiv:0904.2557 (2009).
3. Devitt, S. J., Munro, W. J. & Nemoto, K. "Quantum Error Correction for Beginners." Rep. Prog. Phys. 76, 076001 (2013).
4. Google Quantum AI. "Exponential suppression of bit or phase errors with cyclic error correction." Nature 595, 383-387 (2021).
5. Dennis, E., Kitaev, A., Landahl, A. & Preskill, J. "Topological quantum memory." J. Math. Phys. 43, 4452-4505 (2002).
