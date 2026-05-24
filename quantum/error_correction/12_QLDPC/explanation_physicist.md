# Quantum Low-Density Parity-Check (QLDPC) Codes - Physicist's Deep Dive

4. Quantum LDPC (qLDPC) Codes (The Future King)
Quantum Low-Density Parity-Check (qLDPC) codes are the hot topic in quantum computing and are widely considered the architecture that will eventually replace the surface code.
The Physics: Surface codes are limited because a qubit can only talk to its immediate physical neighbors on a flat plane. qLDPC codes break this 2D constraint using long-range connectors (like optical links or 3D via-stacking) to weave complex, non-local network connections between qubits.
The Superpower (Killing the Overhead): Remember how a surface code requires thousands of physical qubits for one logical qubit? qLDPC codes can pack dozens of logical qubits into the same physical footprint. IBM demonstrated that a qLDPC architecture could achieve fault tolerance using roughly 10 to 20 times fewer physical qubits than a surface code [The IBM Quantum team, Nature, 2024].
The Catch: The hardware routing is an engineering nightmare. You cannot easily build these complex crossing connections on a standard 2D chip without causing wiring bottlenecks.





## 1. Overview

Quantum Low-Density Parity-Check (QLDPC) codes are a family of quantum error-correcting codes with sparse stabilizer generators — each stabilizer acts on only O(1) qubits (constant weight), and each qubit participates in only O(1) stabilizers. This sparsity is the quantum analog of classical LDPC codes, which revolutionized classical communications (Wi-Fi, 5G, satellite).

QLDPC codes represent the cutting edge of fault-tolerant quantum computing: they achieve the same error protection as surface codes with **asymptotically fewer physical qubits** — potentially reducing overhead by 10x or more. IBM demonstrated a [[144, 12, 12]] bivariate bicycle QLDPC code in 2024, and Panteleev & Kalachev (2022) proved the existence of asymptotically good QLDPC codes with constant rate and linear distance.

---

## 2. Classical LDPC Codes Recap

### 2.1 Parity-Check Matrix

A classical LDPC code is defined by a sparse parity-check matrix H in F_2^{m x n}:

```
Codewords: {x in F_2^n : Hx = 0 (mod 2)}
```

"Low-density" means:
- Each row of H has at most w_r ones (row weight)
- Each column of H has at most w_c ones (column weight)
- w_r, w_c = O(1) as n -> infinity

### 2.2 Tanner Graph

The parity-check matrix H defines a bipartite graph:
- **Variable nodes:** one per codeword bit (n nodes)
- **Check nodes:** one per parity check (m nodes)
- **Edges:** H_{ij} = 1 means check i is connected to variable j

This graph structure enables efficient decoding via **belief propagation** (BP): local messages are passed along edges iteratively until convergence.

### 2.3 Performance

Classical LDPC codes achieve capacity (Shannon limit) with polynomial-time decoding. The key: sparsity enables local message-passing that converges to the global optimum.

---

## 3. From Classical to Quantum LDPC

### 3.1 CSS-LDPC Construction

A CSS quantum code from classical codes C_1 and C_2 with C_2^perp subset C_1:

```
[[n, k, d]] quantum code
X-stabilizers from rows of H_2 (parity check of C_2)
Z-stabilizers from rows of H_1 (parity check of C_1)
```

A **QLDPC code** requires both H_1 and H_2 to be sparse (low-density).

### 3.2 The Commutativity Constraint

For a valid CSS code: H_1 H_2^T = 0 (mod 2)

This makes QLDPC construction much harder than classical LDPC:
- Classical: just find a sparse H
- Quantum: find two sparse matrices H_1, H_2 with H_1 H_2^T = 0

This interplay between X and Z stabilizers is the fundamental challenge. Naively enforcing commutativity tends to destroy the sparsity or the distance.

### 3.3 Code Parameters

A QLDPC code is characterized by:
- **n:** number of physical qubits
- **k:** number of logical qubits (encoding rate r = k/n)
- **d:** code distance (minimum weight of a logical operator)
- **w:** maximum stabilizer weight (the "low density" parameter)

The goal: maximize k and d while keeping w = O(1) and n as small as possible.

---

## 4. Key QLDPC Code Families

### 4.1 Hypergraph Product Codes (Tillich & Zémor, 2014)

Given classical codes C_1 = [n_1, k_1, d_1] and C_2 = [n_2, k_2, d_2]:

```
Hypergraph product: [[n, k, d]] where
    n = n_1 * r_2 + r_1 * n_2
    k = k_1 * k_2
    d >= min(d_1, d_2)
```

where r_i = n_i - k_i. Stabilizer weight w <= w_1 + w_2.

Properties:
- Always satisfies commutativity (by construction)
- Encoding rate k/n -> constant as n -> infinity
- Distance d = O(sqrt(n)) typically

**Construction:**
- X-stabilizer parity check: H_X = [H_1 tensor I_{r_2} | I_{r_1} tensor H_2^T]
- Z-stabilizer parity check: H_Z = [I_{n_1} tensor H_2 | H_1^T tensor I_{n_2}]

**Commutativity proof:**
```
H_X * H_Z^T = H_1 tensor H_2^T + H_1 tensor H_2^T = 0 (mod 2)
```

### 4.2 Lifted Product Codes (Panteleev & Kalachev, 2022)

Generalization using group algebra over F_2[G] for a group G (often cyclic Z_L):
- Replace scalar entries in H with group elements (L x L permutation matrices)
- "Lift" the base code by the group action

**Breakthrough result:** First family achieving **asymptotically good** QLDPC codes:
- k = Theta(n) (constant rate)
- d = Theta(n) (linear distance)
- w = O(1) (constant weight)

This matches the Gilbert-Varshamov bound — the theoretical optimum.

### 4.3 Balanced Product Codes (Breuckmann & Eberhardt, 2021)

Interpolate between hypergraph product and lifted product:
- Use group actions on the Tanner graph
- Balance the structure for better distance while maintaining sparsity

### 4.4 Bivariate Bicycle Codes (IBM, 2024)

Specific QLDPC codes used in IBM's experimental demonstrations:
- Defined by two polynomials a(x,y) and b(x,y) over Z_l x Z_m
- Compact algebraic representation, hardware-friendly layout
- [[144, 12, 12]] code demonstrated experimentally
- 12x fewer qubits than equivalent surface code
- Stabilizer weight 6 (vs 4 for surface code)

### 4.5 Quantum Tanner Codes (Leverrier & Zémor, 2022)

Based on Cayley graphs of groups with local codes on vertices:
- Also achieve constant rate + linear distance
- Provide an alternative construction to lifted products
- Connected to expander graph theory

---

## 5. Decoding QLDPC Codes

### 5.1 Belief Propagation (BP)

Standard LDPC decoder adapted for quantum:

```
For each check-variable edge, iterate:
    mu_{c->v}(x) = sum_{x' : check satisfied} prod_{v' != v} mu_{v'->c}(x')
    mu_{v->c}(x) = channel_info(x) * prod_{c' != c} mu_{c'->v}(x)
```

For QLDPC: run BP independently for X and Z syndromes.

**Problem:** BP often fails for QLDPC due to:
1. Short cycles in the Tanner graph (induced by commutativity constraint)
2. Quantum degeneracy: multiple errors with same syndrome are equivalent
3. Correlations between X and Z errors (for non-CSS codes)

### 5.2 BP + Ordered Statistics Decoding (BP-OSD)

After BP converges (possibly incorrectly):
1. Use BP soft information to order bits by reliability
2. Apply OSD on the most unreliable bits
3. Search over low-weight corrections

BP-OSD is currently the most practical decoder for general QLDPC codes.

### 5.3 Union-Find Decoder

Near-linear time complexity, works well for topological codes. Extended to QLDPC via:
- Clustering syndrome defects
- Growing clusters until they merge or reach a boundary
- Peeling decoder on the resulting structure

### 5.4 Minimum Weight Perfect Matching (MWPM)

Optimal for surface codes but harder to apply to QLDPC:
- Requires defining a distance metric between syndrome defects
- Non-local stabilizers make the metric computation more complex

---

## 6. Comparison with Surface Codes

| Property | Surface Code | QLDPC (Bivariate Bicycle) |
|----------|-------------|--------------------------|
| Parameters | [[d^2, 1, d]] | [[n, k, d]] with k/n = const |
| Qubits per logical | d^2 | ~n/k (10x fewer) |
| Stabilizer weight | 4 | ~6 |
| Decoding | MWPM (fast, well-studied) | BP-OSD (still developing) |
| Gate implementation | Transversal CNOT | More complex (flag FT) |
| Connectivity | 2D nearest-neighbor | Non-local (needs routing) |
| Threshold | ~1% | ~0.5-0.8% (decoder-dependent) |
| Maturity | Widely demonstrated | Early experiments (IBM 2024) |

**Key tradeoff:** QLDPC saves qubits but requires non-local connectivity and more complex decoding.

---

## 7. Worked Example: Hypergraph Product from Repetition Code

### 7.1 Input

Take C_1 = C_2 = [3, 1, 3] repetition code with parity check:
```
H = [[1, 1, 0],
     [0, 1, 1]]
```

Here n = 3, k = 1, r = n - k = 2.

### 7.2 Hypergraph Product

Physical qubits: n_total = 3*2 + 2*3 = 12
But we also have check qubits, so the full code lives on n_1*n_2 + r_1*r_2 = 9 + 4 = 13 qubits.

X-stabilizer matrix:
```
H_X = [H tensor I_2 | I_2 tensor H^T]
```

This gives a [[13, 1, 3]] QLDPC code with stabilizer weight <= 4.

### 7.3 Comparison

- Shor code: [[9, 1, 3]] but weight-6 stabilizers
- Surface code (d=3): [[9, 1, 3]] with weight-4 stabilizers
- Hypergraph product: [[13, 1, 3]] with weight-4 stabilizers (more qubits but structured)

For larger codes, QLDPC wins decisively on the rate k/n.

---

## 8. The Quantum Singleton and Hamming Bounds

### 8.1 Quantum Singleton Bound

For any [[n, k, d]] code:
```
k <= n - 2(d - 1)
```

### 8.2 Quantum Hamming Bound

For non-degenerate [[n, k, d]] codes:
```
sum_{j=0}^{floor((d-1)/2)} C(n, j) * 3^j <= 2^{n-k}
```

### 8.3 Achieving the Bounds

Asymptotically good QLDPC codes (Panteleev-Kalachev) approach the quantum Gilbert-Varshamov bound:
```
k/n >= 1 - H_2(d/n) - d/n * log_2(3)
```
where H_2 is the binary entropy function. This is the best known achievable rate-distance tradeoff.

---

## 9. Hardware Considerations

### 9.1 Connectivity Requirements

QLDPC stabilizers connect non-neighboring qubits, requiring:
- Long-range qubit coupling (trapped ions, neutral atoms)
- SWAP routing on nearest-neighbor hardware (superconducting)
- Modular architectures with inter-module links

### 9.2 IBM's Approach

IBM's bivariate bicycle codes use:
- Connectivity graph designed for heavy-hex lattice
- Flag fault tolerance for weight-6 stabilizers
- Real-time BP-OSD decoding on classical co-processor

### 9.3 Syndrome Extraction

For weight-w stabilizers:
- Need w CNOT gates per stabilizer measurement
- Flag qubits detect "hook" errors from CNOT propagation
- Measurement circuit depth: O(w) per round

---

## 10. Open Problems

1. **Practical threshold:** Determining exact thresholds for specific QLDPC families under realistic noise
2. **Fast decoding:** Achieving real-time BP-OSD for large codes (microsecond timescale)
3. **Logical gates:** Implementing universal gate sets fault-tolerantly within QLDPC codes
4. **Hardware co-design:** Optimizing QLDPC codes for specific hardware connectivity graphs
5. **Concatenation:** Combining QLDPC with other codes for better performance

---

## 11. References

1. Breuckmann, N. P. & Eberhardt, J. N. "Balanced Product Quantum Codes." IEEE Trans. Inf. Theory 67, 6653-6674 (2021).
2. Panteleev, P. & Kalachev, G. "Asymptotically Good Quantum and Locally Testable Classical LDPC Codes." STOC 2022.
3. Tillich, J.-P. & Zémor, G. "Quantum LDPC Codes With Positive Rate and Minimum Distance Proportional to sqrt(n)." IEEE Trans. Inf. Theory 60, 1193-1202 (2014).
4. Bravyi, S., et al. "High-threshold and low-overhead fault-tolerant quantum memory." Nature 627, 778-782 (2024).
5. Leverrier, A. & Zémor, G. "Quantum Tanner codes." FOCS 2022.
6. Panteleev, P. & Kalachev, G. "Quantum LDPC Codes with Almost Linear Minimum Distance." IEEE Trans. Inf. Theory 68, 213-229 (2022).
7. Gallager, R. G. "Low-Density Parity-Check Codes." MIT Press (1963).
8. Roffe, J. "Quantum Error Correction: An Introductory Guide." Contemporary Physics 60, 226-245 (2019).
9. Roffe, J. "LDPC: Belief Propagation and Ordered Statistics Decoding." GitHub: quantumgizmos/bp_osd.
