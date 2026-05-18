# 3-Qubit Bit-Flip Code - Physicist's Deep Dive

## 1. Overview

The 3-qubit bit-flip code is the simplest quantum error correcting code. It protects a single logical qubit against a single bit-flip (X) error by encoding it into 3 physical qubits using a quantum repetition strategy.

Code parameters: [[3, 1, 1]] (3 physical qubits, 1 logical qubit, distance 1 for general errors but corrects 1 bit-flip)
The fix is by using a Bit flip gate (X) on the physical qubit.

---

## 2. Encoding

### 2.1 Logical States

```
|0_L> = |000>
|1_L> = |111>
```

General logical state:
```
|psi_L> = alpha|0_L> + beta|1_L> = alpha|000> + beta|111>
```

### 2.2 Encoding Circuit

Starting from |psi> = alpha|0> + beta|1> on qubit 1, with qubits 2,3 initialized to |0>:

```
|psi>|0>|0> -> CNOT(1,2) -> CNOT(1,3) -> alpha|000> + beta|111>
CNOT|10>=|11>
CNOT|110> = |111>
CNOT|000> = |000>
This is why 
alpha|0_L> + beta|1_L> -> CNOT(1,2) -> CNOT(1,3) -> alpha|000> + beta|111>
```

Circuit:
```
q0: --|psi>--*-----*--
             |     |
q1: --|0>----X-----|--
                   |
q2: --|0>----------X--
```

### 2.3 Proof of Correct Encoding

CNOT(1,2) acting on alpha|0>|0> + beta|1>|0>:
```
= alpha|00> + beta|11>  (on qubits 1,2)
```

CNOT(1,3):
```
= alpha|000> + beta|111>  (on qubits 1,2,3)
```

This is the GHZ-type encoding.

---

## 3. Error Model: Bit-Flip Channel

### 3.1 Single-Qubit Bit-Flip

The bit-flip channel on qubit i with probability p:

```
E(rho) = (1-p) rho + p X_i rho X_i
```

Kraus operators: K_0 = sqrt(1-p) I, K_1 = sqrt(p) X

### 3.2 Independent Errors on 3 Qubits

With independent bit-flip probability p on each qubit, the state after errors is:

```
rho_err = sum_{i,j,k in {0,1}} p_i p_j p_k (X_1^i X_2^j X_3^k) rho (X_1^i X_2^j X_3^k)
```

where p_0 = 1-p, p_1 = p.

Probability of 0 errors: (1-p)^3
Probability of exactly 1 error: 3p(1-p)^2
Probability of 2+ errors: 3p^2(1-p) + p^3

---

## 4. Syndrome Measurement

### 4.1 Stabilizer Generators

The code is stabilized by two operators:

```
S_1 = Z_1 Z_2  (measures parity of qubits 1,2)
S_2 = Z_2 Z_3  (measures parity of qubits 2,3)
```

These commute with each other and with the logical operators X_L = X_1 X_2 X_3 and Z_L = Z_1 (or Z_2 or Z_3).

### 4.2 Syndrome Table

| Error | S_1 = Z_1Z_2 | S_2 = Z_2Z_3 | Syndrome |
|-------|-------------|-------------|----------|
| None (I) | +1 | +1 | (0, 0) |
| X_1 | -1 | +1 | (1, 0) |
| X_2 | -1 | -1 | (1, 1) |
| X_3 | +1 | -1 | (0, 1) |

The syndrome uniquely identifies which qubit was flipped.

### 4.3 Syndrome Measurement Circuit

```
q0: ----*-----------
        |
q1: ----|----*---*--
        |    |   |
q2: ----|----|---|----*--
        |    |   |    |
a0: ----Z----Z---|----|--> Measure (S1)
                 |    |
a1: -------------Z----Z--> Measure (S2)
```

Using CNOT gates (Z-basis parity measurement):
```
a0 = q0 XOR q1  (syndrome bit 1)
a1 = q1 XOR q2  (syndrome bit 2)
```

---

## 5. Error Correction

Given syndrome (s1, s2):
- (0, 0): no correction
- (1, 0): apply X_1
- (1, 1): apply X_2
- (0, 1): apply X_3

### 5.1 Logical Error Rate

The code fails when 2 or more qubits are flipped. The logical error probability is:

```
p_L = 3p^2(1-p) + p^3 = 3p^2 - 2p^3
```

For the uncoded qubit: p_uncoded = p

The code helps when p_L < p:
```
3p^2 - 2p^3 < p  =>  p(3p - 2p^2 - 1) < 0  =>  p < 1/2
```

So the bit-flip code improves reliability when p < 1/2 (break-even point).

### 5.2 Error Suppression

For small p: p_L ≈ 3p^2 (quadratic suppression)

Example: if p = 0.01, then p_L ≈ 0.0003 (30x improvement)

---

## 6. Limitations

1. **Only corrects bit-flip (X) errors:** Cannot correct phase-flip (Z) or general errors
2. **No protection against Y errors:** Y = iXZ, which is a simultaneous bit and phase flip
3. **Overhead:** 3 physical qubits per logical qubit (3:1 ratio)
4. **Not a general quantum code:** Does not satisfy the quantum error correction conditions for arbitrary errors

---

## 7. Connection to Classical Repetition Code

The 3-qubit bit-flip code is the quantum analog of the classical [3,1,3] repetition code:
- Classical: 0 -> 000, 1 -> 111 (majority vote for decoding)
- Quantum: |0> -> |000>, |1> -> |111> (syndrome measurement for error identification)

Key difference: in quantum, we cannot simply "read" the qubits (that would collapse the superposition). Instead, we use ancilla-based syndrome measurement that extracts error information without disturbing the encoded state.

---

## 8. References

1. Nielsen, M. A. & Chuang, I. L. "Quantum Computation and Quantum Information." Cambridge University Press (2010), Section 10.1.
2. Gottesman, D. "An Introduction to Quantum Error Correction and Fault-Tolerant Quantum Computation." arXiv:0904.2557 (2009).
3. Preskill, J. "Quantum Computing in the NISQ Era and Beyond." Quantum 2, 79 (2018).


## 9. what happens in bit flip if one of the ancillas has changed?
If an ancilla qubit changes before the syndrome measurement, it breaks the error detection system and can cause the code to accidentally ruin perfectly good data.
In a 3-qubit bit-flip code, you use two extra ancilla qubits to measure the relationships (Z_1Z_2 and Z_2Z_3) between the three data qubits.

Here is exactly what happens if an ancilla flips or encounters an error:

### Scenario 1: The Ancilla Flips During the Measurement Circuit
If an ancilla flips due to hardware noise right before it is measured, it reports a faulty error syndrome (a false positive).
- The Result: The system thinks a data qubit has flipped when it actually hasn't.
- The Consequence: The recovery step will apply an unnecessary gate to a healthy data qubit, introducing a real error into your data.

### Scenario 2: The Ancilla Flips Before the Entangling CNOT Gates
If an ancilla flips at the very beginning of the circuit (before interacting with the data qubits via CNOT gates), it will actively propagate errors backward into your data.
- The Result: Because CNOT gates can propagate phase errors backward and bit-flips forward, a corrupted ancilla can spread errors to multiple data qubits simultaneously.
- The Consequence: The code can only handle one data qubit error. If a bad ancilla corrupts two data qubits, the majority-vote logic fails completely, and the logical state is permanently destroyed.

### How Quantum Computers Fix This
Because ancillas are just as fragile as data qubits, real quantum systems do not rely on a single, unprotected ancilla measurement. They use Fault-Tolerant Quantum Error Correction:
Repeated Measurements: They measure the ancillas multiple times. A single flipped ancilla will show up as a temporary glitch (e.g., reporting syndromes 0 -> 1 -> 0), which the software filters out.
Flag Qubits: They add extra "flag" qubits to watch the ancillas. If an ancilla misbehaves, the flag qubit triggers a warning to ignore that specific measurement.
