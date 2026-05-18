# 3-Qubit Phase-Flip Code - Physicist's Deep Dive

## 1. Overview

The 3-qubit phase-flip code protects a single logical qubit against a single phase-flip (Z) error. It is the exact dual of the 3-qubit bit-flip code, obtained by conjugating the entire encoding/decoding procedure with Hadamard gates. This duality makes phase-flip correction conceptually transparent: transform to the Hadamard basis, apply the bit-flip code, then transform back.

Code parameters: [[3, 1, 1]] (3 physical qubits, 1 logical qubit, distance 1 for general errors but corrects 1 phase-flip)
The fix is by using a Phase flip gate (Z) on the physical qubit.


How it works - just like bit flip but in the |+>, |-> space
First use CNOT gates to 
|psi_L> = alpha|0_L> + beta|1_L> -> CNOT(1,2) -> CNOT(1,3) -> alpha|000> + beta|111>
Then use the Hadamard gate to 
alpha|000> + beta|111> -> H(1) -> H(2) -> H(3) -> alpha|+++> + beta|--->
where 
H|0> = |+>
H|1> = |->
Then statistics. Same problems as for bit flip
---

## 2. Motivation: Why Phase Flips Matter

### 2.1 The Phase-Flip Error

A phase-flip (Z) error does not change the computational-basis populations. It only affects the relative phase between |0> and |1>:

```
Z|0> = |0>
Z|1> = -|1>
```

So Z acting on alpha|0> + beta|1> gives alpha|0> - beta|1>. The probabilities of measuring 0 or 1 are unchanged, but interference patterns are destroyed. This is a purely quantum error with no classical analog.

### 2.2 Why the Bit-Flip Code Fails for Phase Errors

The bit-flip code encodes |0> -> |000>, |1> -> |111>. The stabilizers Z_1Z_2 and Z_2Z_3 measure bit-parity in the Z basis. A phase-flip Z_i commutes with all Z operators, so Z_1Z_2 and Z_2Z_3 cannot detect it:

```
[Z_i, Z_jZ_k] = 0   for all i, j, k
```

A Z error is completely invisible to the bit-flip syndrome. We need a different code.

---

## 3. Key Insight: Hadamard Conjugation

### 3.1 Hadamard Converts Z to X

The Hadamard gate H satisfies:

```
HZH = X
HXH = Z
```

This means: if we work in the Hadamard-transformed (|+>, |->) basis, a Z error looks like an X error, and we can use the bit-flip code machinery.

### 3.2 The Strategy

1. Apply H to each qubit (move to Hadamard basis)
2. In this basis, Z errors become X errors
3. Apply the bit-flip encoding (CNOT chain)
4. Apply H to each qubit again (return to computational basis)

The full encoding circuit is: H^{otimes 3} -> CNOT chain -> H^{otimes 3}

---

## 4. Encoding

### 4.1 Logical States

```
|0_L> = |+++> = (|0>+|1>)/sqrt(2) tensor (|0>+|1>)/sqrt(2) tensor (|0>+|1>)/sqrt(2)
      = (1/2sqrt(2)) (|000> + |001> + |010> + |011> + |100> + |101> + |110> + |111>)

|1_L> = |---> = (|0>-|1>)/sqrt(2) tensor (|0>-|1>)/sqrt(2) tensor (|0>-|1>)/sqrt(2)
      = (1/2sqrt(2)) (|000> - |001> - |010> + |011> - |100> + |101> + |110> - |111>)
```

General logical state:
```
|psi_L> = alpha|0_L> + beta|1_L> = alpha|+++> + beta|--->
```

### 4.2 Verification of Logical States

Notice that |+> = H|0> and |-> = H|1>. So:

```
|0_L> = H^{otimes 3} |000>
|1_L> = H^{otimes 3} |111>
```

The phase-flip code is literally the bit-flip code with every qubit Hadamard-rotated.

### 4.3 Encoding Circuit

Starting from |psi> = alpha|0> + beta|1> on qubit 0, with qubits 1,2 initialized to |0>:

```
Step 1: H on q0          -> alpha|+> + beta|-> on q0 (ancillas still |0>)
Step 2: CNOT(0,1)         -> alpha|+0> + beta|-> XOR mapping in comp basis
Step 3: CNOT(0,2)         -> entangle all three
Step 4: H on q0, q1, q2   -> return to computational basis
```

More precisely, the full circuit acts as:

```
|psi>|0>|0> -> H_0 -> CNOT(0,1) -> CNOT(0,2) -> H_0 H_1 H_2 -> alpha|+++> + beta|--->
```

Circuit diagram:
```
q0: --|psi>--H--*-----*--H--
                |     |
q1: --|0>-------X-----|--H--
                      |
q2: --|0>-------------X--H--
```

### 4.4 Proof of Correct Encoding

Start: (alpha|0> + beta|1>) |0> |0>

After H on q0:
```
(alpha|+> + beta|->) |0>|0>
= (alpha (|0>+|1>)/sqrt(2) + beta (|0>-|1>)/sqrt(2)) |00>
```

After CNOT(0,1):
```
alpha (|00>+|11>)/sqrt(2) |0> + beta (|00>-|11>)/sqrt(2) |0>
= alpha (|000>+|110>)/sqrt(2) + beta (|000>-|110>)/sqrt(2)
```

Wait -- let us be more careful. After CNOT(0,1) on the first two qubits:

```
alpha (|0>+|1>)/sqrt(2) |0> -> alpha (|00>+|11>)/sqrt(2)
beta (|0>-|1>)/sqrt(2) |0>  -> beta (|00>-|11>)/sqrt(2)
```

After CNOT(0,2) (control q0, target q2, with q2 = |0>):

```
alpha: (|00>+|11>)/sqrt(2) |0> -> (|000>+|111>)/sqrt(2)
beta:  (|00>-|11>)/sqrt(2) |0> -> (|000>-|111>)/sqrt(2)
```

State before final Hadamards:
```
alpha (|000>+|111>)/sqrt(2) + beta (|000>-|111>)/sqrt(2)
```

This is (alpha + beta)|000>/sqrt(2) + (alpha - beta)|111>/sqrt(2) -- a GHZ state. Now apply H^{otimes 3}:

```
H^{otimes 3} |000> = |+++>
H^{otimes 3} |111> = |--->
```

Final state:
```
alpha (|+++> + |--->) / sqrt(2) + beta (|+++> - |--->) / sqrt(2)
```

Hmm, this does not simplify to alpha|+++> + beta|---> directly. Let us redo this more carefully using the shortcut:

The bit-flip code encodes |0> -> |000>, |1> -> |111>. Conjugating by H^{otimes 3}:

```
(H^3)(encode)(|psi> |0> |0>)
= H^3 (alpha|000> + beta|111>)
= alpha|+++> + beta|--->
```

But we want to build the circuit as: H_0, CNOT, CNOT, H_all. The correct decomposition is:

```
Encode_phase = H^{otimes 3} . Encode_bit . H_0^{-1}
```

Wait, the standard presentation is simpler. We want:

```
|psi> |0>|0> -> alpha|+++> + beta|--->
```

Circuit: first apply CNOT(0,1), CNOT(0,2) to get alpha|000> + beta|111>, then apply H to all three:

```
q0: --|psi>--*-----*--H--
             |     |
q1: --|0>----X-----|--H--
                   |
q2: --|0>----------X--H--
```

Check: alpha|000> + beta|111> -> H^3 -> alpha|+++> + beta|---> . Correct!

So the encoding circuit is: CNOT chain followed by Hadamard on all qubits.

### 4.5 Summary of Encoding

```
Encoding circuit: CNOT(0,1) -> CNOT(0,2) -> H_0 -> H_1 -> H_2

|0> -> |000> -> |+++> = |0_L>
|1> -> |111> -> |---> = |1_L>
```

---

## 5. Error Model: Dephasing Channel

### 5.1 Single-Qubit Phase-Flip Channel

The dephasing channel on qubit i with probability p:

```
E(rho) = (1-p) rho + p Z_i rho Z_i
```

Kraus operators: K_0 = sqrt(1-p) I, K_1 = sqrt(p) Z

### 5.2 Independent Errors on 3 Qubits

With independent phase-flip probability p on each qubit:

```
rho_err = sum_{i,j,k in {0,1}} p_i p_j p_k (Z_1^i Z_2^j Z_3^k) rho (Z_1^i Z_2^j Z_3^k)
```

where p_0 = 1-p, p_1 = p.

Probability of 0 errors: (1-p)^3
Probability of exactly 1 error: 3p(1-p)^2
Probability of 2+ errors: 3p^2(1-p) + p^3

---

## 6. Syndrome Measurement

### 6.1 Stabilizer Generators

The phase-flip code is stabilized by:

```
S_1 = X_1 X_2  (checks relative phase-parity of qubits 1,2)
S_2 = X_2 X_3  (checks relative phase-parity of qubits 2,3)
```

These are obtained from the bit-flip stabilizers Z_1Z_2, Z_2Z_3 by Hadamard conjugation:

```
H^{otimes 3} (Z_i Z_j) H^{otimes 3} = X_i X_j
```

The stabilizers commute with each other and with the logical operators:
- Z_L = Z_1 Z_2 Z_3 (logical Z)
- X_L = X_1 (or X_2 or X_3) (logical X)

### 6.2 Why X-Stabilizers Detect Z-Errors

Z errors anti-commute with X:

```
{Z_i, X_i} = 0   (anti-commute)
[Z_i, X_j] = 0   for i != j  (commute)
```

So a Z error on qubit i flips the eigenvalue of any stabilizer containing X_i:

```
S_1 (Z_1 |psi_L>) = Z_1 (-S_1) |psi_L> = -Z_1 S_1 |psi_L>
```

The stabilizer eigenvalue changes from +1 to -1, producing a detectable syndrome.

### 6.3 Syndrome Table

| Error    | S_1 = X_1X_2 | S_2 = X_2X_3 | Syndrome |
|----------|-------------|-------------|----------|
| None (I) | +1          | +1          | (0, 0)   |
| Z_1      | -1          | +1          | (1, 0)   |
| Z_2      | -1          | -1          | (1, 1)   |
| Z_3      | +1          | -1          | (0, 1)   |

The syndrome uniquely identifies which qubit suffered a phase flip.

### 6.4 Syndrome Measurement Circuit

To measure X_1X_2 and X_2X_3, we need to measure in the X basis. The trick: apply H before and after CNOT-based parity checks.

```
q0: --H---*---------H--
          |
q1: --H---|---*--*--H--
          |   |  |
q2: --H---|---|--|---*--H--
          |   |  |   |
a0: ------Z---Z--|---|---> Measure (S1)
                 |   |
a1: -------------Z---Z---> Measure (S2)
```

Equivalently, using the Hadamard-basis approach:
1. Apply H to all data qubits (transform to |0>/|1> basis)
2. Use standard CNOT-based parity measurement (same as bit-flip syndrome)
3. Apply H to all data qubits (return to |+>/|-> basis)

This is exactly the bit-flip syndrome circuit conjugated by H^{otimes 3}.

---

## 7. Error Correction

Given syndrome (s1, s2):
- (0, 0): no correction needed
- (1, 0): apply Z_1 (phase flip on qubit 1)
- (1, 1): apply Z_2 (phase flip on qubit 2)
- (0, 1): apply Z_3 (phase flip on qubit 3)

### 7.1 Logical Error Rate

The code fails when 2 or more qubits suffer phase flips. The logical error probability is:

```
p_L = 3p^2(1-p) + p^3 = 3p^2 - 2p^3
```

This is identical to the bit-flip code formula, because the code structure is the same (only the basis is different).

For the uncoded qubit under dephasing: p_uncoded = p

The code helps when p_L < p:
```
3p^2 - 2p^3 < p  =>  p < 1/2
```

### 7.2 Error Suppression

For small p: p_L approx 3p^2 (quadratic suppression)

Example: if p = 0.01, then p_L approx 0.0003 (30x improvement)

---

## 8. Duality with the Bit-Flip Code

### 8.1 Hadamard Conjugation

Every element of the phase-flip code is the Hadamard conjugate of the corresponding bit-flip code element:

| Bit-Flip Code          | Phase-Flip Code                |
|------------------------|-------------------------------|
| \|0_L> = \|000>        | \|0_L> = \|+++>               |
| \|1_L> = \|111>        | \|1_L> = \|--->               |
| Error: X               | Error: Z                      |
| Stabilizers: Z_iZ_j    | Stabilizers: X_iX_j           |
| Correction: X_i        | Correction: Z_i               |
| Encodes in Z-basis     | Encodes in X-basis            |

### 8.2 Formal Statement

If U_encode is the bit-flip encoding unitary, then the phase-flip encoding is:

```
U_phase = H^{otimes 3} . U_bit
```

And if E_bit is correctable by the bit-flip code, then H E_bit H is correctable by the phase-flip code.

### 8.3 Why This Duality Matters

This Hadamard duality is the seed of the Shor 9-qubit code: concatenate the bit-flip code (inner) with the phase-flip code (outer) to correct both X and Z errors. It also foreshadows CSS codes, which systematically combine X-error and Z-error correcting codes.

---

## 9. Limitations

1. **Only corrects phase-flip (Z) errors:** Cannot correct bit-flip (X) or general errors
2. **No protection against Y errors:** Y = iXZ, which is a simultaneous bit and phase flip
3. **Overhead:** 3 physical qubits per logical qubit (3:1 ratio)
4. **Not a general quantum code:** Does not satisfy the quantum error correction conditions for arbitrary single-qubit errors
5. **Complementary weakness:** The bit-flip code corrects X but not Z; the phase-flip code corrects Z but not X. Neither alone is sufficient.

---

## 10. Path Forward: Combining Both Codes

The Shor code (Section 03) resolves the complementary weakness by concatenation:

1. First encode against phase flips: |0> -> |+++>, |1> -> |--->
2. Then encode each physical qubit against bit flips: |+> -> (|000>+|111>)/sqrt(2), |-> -> (|000>-|111>)/sqrt(2)

Result: 9-qubit code that corrects arbitrary single-qubit errors.

---

## 11. References

1. Nielsen, M. A. & Chuang, I. L. "Quantum Computation and Quantum Information." Cambridge University Press (2010), Section 10.1.
2. Gottesman, D. "An Introduction to Quantum Error Correction and Fault-Tolerant Quantum Computation." arXiv:0904.2557 (2009).
3. Preskill, J. "Quantum Computing in the NISQ Era and Beyond." Quantum 2, 79 (2018).
4. Shor, P. W. "Scheme for reducing decoherence in quantum computer memory." Physical Review A, 52(4), R2493 (1995).
