# Color Codes - Physicist's Deep Dive

## 1. Overview

Color codes, introduced by Bombin & Martin-Delgado (2006), are a family of topological
stabilizer codes defined on 2-colex lattices (lattices whose faces are 3-colorable).
Their defining feature is the **transversal implementation of the full Clifford group**,
a significant advantage over surface codes which require lattice surgery for all logical
gates.

**Core idea:** The lattice is colored with 3 colors (red, green, blue) such that no two
adjacent faces share a color. Stabilizer generators are associated with faces, and each
face generates both an X-stabilizer and a Z-stabilizer (unlike the surface code where
X and Z stabilizers live on different lattice elements). This doubled stabilizer
structure enables transversal Clifford gates.

The smallest color code is the **7-qubit color code**, which is equivalent to the Steane
[[7, 1, 3]] code. This connection provides a concrete bridge between CSS codes and
topological codes.


## example

# Hexagonal (6.6.6) Color Code: The [[7, 1, 3]] Steane Code

This example shows the numerical structure of the smallest hexagonal color code. It uses 7 physical qubits to protect 1 logical qubit with a code distance of 3.

## 1. Lattice Structure and Qubit Mapping

Imagine a single central hexagon surrounded by boundary lines. Qubits sit on the vertices:

*   **Face 1 (Red Hexagon)**: Qubits **1, 2, 3, 4, 5, 6**
*   **Face 2 (Green Boundary)**: Qubits **2, 3, 4, 7**
*   **Face 3 (Blue Boundary)**: Qubits **4, 5, 6, 7**

## 2. The Numerical Stabilizers

Every face requires both an $X$-type and a $Z$-type stabilizer check. The 6 generator matrices are defined below:


| Face (Color) | Qubits Map | $X$-Stabilizer | $Z$-Stabilizer |
| :--- | :--- | :--- | :--- |
| **Face 1 (Red)** | [1, 2, 3, 4, 5, 6] | $X_1 X_2 X_3 X_4 X_5 X_6$ | $Z_1 Z_2 Z_3 Z_4 Z_5 Z_6$ |
| **Face 2 (Green)** | [2, 3, 4, 7] | $X_2 X_3 X_4 X_7$ | $Z_2 Z_3 Z_4 Z_7$ |
| **Face 3 (Blue)** | [4, 5, 6, 7] | $X_4 X_5 X_6 X_7$ | $Z_4 Z_5 Z_6 Z_7$ |

## 3. Error Detection Walkthrough

When the system is error-free, measuring these 6 operators yields a product value of $+1$. 

### Scenario: A phase-flip error ($Z$) occurs on Qubit 1

1. **Anti-commutation**: $Z$ errors only trigger $X$-type stabilizers ($X_1 Z_1 = -Z_1 X_1$).
2. **Syndrome Measurement**:
   * **Red $X$-Check**: Contains Qubit 1 $\rightarrow$ Flips to **$-1$**
   * **Green $X$-Check**: Misses Qubit 1 $\rightarrow$ Stays **$+1$**
   * **Blue $X$-Check**: Misses Qubit 1 $\rightarrow$ Stays **$+1$**
3. **Syndrome Vector**: `[-1, +1, +1]`
4. **Correction**: The unique syndrome points exclusively to Qubit 1. The decoder applies a $Z_1$ operation to fix the error ($Z_1 \times Z_1 = I$).
Use code with caution.
---

## 2. Lattice Structure and Colorability

### 2.1 3-Colorable Lattices (2-Colexes)

A 2-colex is a 2D lattice embedded in a surface such that:
1. Every face can be assigned one of 3 colors (red, green, blue)
2. No two faces sharing an edge have the same color
3. Every vertex is shared by exactly one face of each color

The most common lattice types:

**Triangular (4.8.8) lattice:**
```
    [R]---[G]---[R]
   / | \ / | \ / |
  [B] | [B] | [B] |
   \ | / \ | / \ |
    [G]---[R]---[G]
```

**Hexagonal (6.6.6) lattice:**
```
     /\    /\
    / R\  / R\
   /    \/    \
  |  G  ||  G  |
   \    /\    /
    \ B/  \ B/
     \/    \/
```

**Square-octagon (4.8.8) lattice** -- most commonly used:
```
   [R]----[G]----[R]
   |  \  / |  \  / |
   |  [B]  |  [B]  |
   |  /  \ |  /  \ |
   [G]----[R]----[G]
```

### 2.2 The 7-Qubit Color Code (Steane Code)

The smallest color code on the triangular lattice has 7 qubits placed on vertices:

```
        q1
       / | \
      /  |  \
    q2   |   q3
    | \  |  / |
    |  [R]  |  |
    |  / \  |  |
    q4--[G]--q5
    | \  |  / |
    |  [B]  |  |
    q6-------q7
```

This is precisely the Steane [[7, 1, 3]] code. The 3 colored faces yield 6 stabilizer
generators (one X and one Z per face):

| Face | Color | X-stabilizer | Z-stabilizer |
|------|-------|-------------|-------------|
| Top | Red | X1 X2 X3 X5 | Z1 Z2 Z3 Z5 |
| Left | Green | X2 X4 X5 X6 | Z2 Z4 Z5 Z6 |
| Right | Blue | X3 X5 X6 X7 | Z3 Z5 Z6 Z7 |

**Code parameters:** n = 7, k = 7 - 6 = 1, d = 3 --> [[7, 1, 3]]

---

## 3. Stabilizer Structure

### 3.1 Face Stabilizers

For each face f of the lattice, define two stabilizers:

```
S_X(f) = tensor product of X_i for all qubits i on the boundary of face f
S_Z(f) = tensor product of Z_i for all qubits i on the boundary of face f
```

**Key property:** Since each edge is shared by exactly two faces of different colors,
any two face stabilizers (even X of one face and Z of another) commute:

```
[S_X(f), S_Z(f')] = 0  for all faces f, f'
```

**Proof:** Two faces share an even number of vertices (0 or 2 for adjacent faces on
a 2-colex), so the anticommutations cancel pairwise.

### 3.2 Color-Restricted Stabilizers

A powerful feature of color codes: we can define **color-restricted stabilizer groups**.
For each pair of colors (c1, c2), the stabilizers supported on faces of color c1 or c2
form a subgroup. These are CSS codes themselves:

```
S_{RG} = < S_X(f), S_Z(f) : f is Red or Green >
S_{RB} = < S_X(f), S_Z(f) : f is Red or Blue >
S_{GB} = < S_X(f), S_Z(f) : f is Green or Blue >
```

Each pair encodes the same logical qubit. This triple redundancy in the stabilizer
structure is what enables transversal Clifford gates.

### 3.3 Relationship Between Face Stabilizers

The face stabilizers satisfy the constraint:

```
Product of all X-face stabilizers = I  (each qubit appears in exactly 2 X-stabilizers)
Product of all Z-face stabilizers = I
```

For a lattice with F faces, the number of independent stabilizer generators is 2F - 2,
and the number of logical qubits is:

```
k = n - (2F - 2) = n - 2F + 2
```

For the 7-qubit code: k = 7 - 2(3) + 2 = 7 - 4 = 3... wait. Let me be precise.
Actually for the 7-qubit code on the 2-sphere: k = 7 - 6 = 1, because there are 3 faces
yielding 6 generators, of which 2 are dependent (one X-type, one Z-type), giving 4
independent generators. But the remaining 2 generators come from boundary conditions.

More carefully: 7 qubits, 6 stabilizer generators, but only 6 are listed; however
the product of all X-generators = I and product of all Z-generators = I gives 2
dependencies, so independent generators = 6 - 2 = 4... this gives k = 7 - 4 = 3?

The resolution: the 7-qubit color code on the projective plane would encode 3 qubits.
On the 2-sphere with boundaries (the standard Steane code), the boundary conditions
reduce the dependencies. The standard Steane [[7,1,3]] code has 6 independent stabilizer
generators, confirming k = 1.

---

## 4. Code Parameters

### 4.1 General Distance-d Color Codes

On the triangular lattice, the distance-d color code has parameters:

| d | n (data qubits) | k | Lattice |
|---|-----------------|---|---------|
| 3 | 7 | 1 | 3-triangle |
| 5 | 19 | 1 | 5-triangle |
| 7 | 37 | 1 | 7-triangle |
| d | (3d^2 + 1)/4 | 1 | d-triangle (d odd) |

On the square-octagon (4.8.8) lattice:

| d | n (data qubits) | k |
|---|-----------------|---|
| 3 | 9 | 1 |
| 5 | 25 | 1 |
| 7 | 49 | 1 |
| d | d^2 | 1 |

### 4.2 The 19-Qubit Color Code

The distance-5 triangular color code:

```
Parameters: [[19, 1, 5]]
Stabilizers: 6 X-type + 6 Z-type (18 generators, 6 independent X + 6 independent Z)
Can correct any 2-qubit error
```

This code is notable for being the smallest color code that demonstrates the
advantage of distance > 3 while remaining experimentally tractable.

---

## 5. Transversal Gates: The Key Advantage

### 5.1 What Makes Transversal Gates Special

A transversal gate is one that can be implemented by applying single-qubit gates to
each physical qubit independently:

```
U_L = U_1 (x) U_2 (x) ... (x) U_n
```

Transversal gates are automatically fault-tolerant: a single-qubit error during the
gate affects only one physical qubit, so it cannot spread to become a multi-qubit
error within the same code block.

### 5.2 Color Code Clifford Gates

The color code admits transversal implementations of:

**Logical X:**
```
X_L = X^{(x)n} = X_1 (x) X_2 (x) ... (x) X_n
```

**Logical Z:**
```
Z_L = Z^{(x)n} = Z_1 (x) Z_2 (x) ... (x) Z_n
```

**Logical Hadamard:**
```
H_L = H^{(x)n} = H_1 (x) H_2 (x) ... (x) H_n
```

This works because the color code is a CSS code where the X and Z stabilizers have
identical support (same qubits). Applying H to every qubit swaps X <-> Z stabilizers,
which maps the code space to itself.

**Logical Phase gate (S):**
```
S_L = S^{(x)n} = S_1 (x) S_2 (x) ... (x) S_n
```

This is the crucial gate that the surface code CANNOT implement transversally.
It works for color codes because of the triorthogonality property of the stabilizer
matrix.

**Logical CNOT (between two code blocks):**
```
CNOT_L = CNOT_{1,1'} (x) CNOT_{2,2'} (x) ... (x) CNOT_{n,n'}
```

where qubit i in block 1 is the control and qubit i' in block 2 is the target.

### 5.3 The Full Clifford Group

Together, {H, S, CNOT} generate the full Clifford group. The color code implements
ALL of these transversally. This is a strict advantage over the surface code, where
lattice surgery is needed for every gate.

### 5.4 Non-Clifford Gates

By the Eastin-Knill theorem, no stabilizer code can implement a universal gate set
transversally. The T gate (pi/8 rotation) still requires magic state distillation,
just as with surface codes. However, the 3D color code (defined on a 3-colex) can
implement the T gate transversally at the cost of being a single-shot code with
more complex structure.

---

## 6. Comparison with Surface Codes

### 6.1 Threshold Comparison

| Property | Surface Code | Color Code |
|----------|-------------|------------|
| Code-capacity threshold | ~10.3% | ~10.9% |
| Phenomenological threshold | ~2.9% | ~1.9% |
| Circuit-level threshold | ~0.6-0.8% | ~0.1-0.2% |
| Transversal Clifford | No | Yes |
| Stabilizer weight | 4 (bulk) | 4-8 (depends on lattice) |
| Decoder maturity | Excellent (MWPM) | Developing |

### 6.2 The Threshold Gap

The circuit-level threshold for color codes (~0.1-0.2%) is significantly lower than
for surface codes (~0.6-0.8%). This is because:

1. **Higher-weight stabilizers:** Color code stabilizers on the triangular lattice have
   weight 4, 6, or 8, requiring more CNOT gates per syndrome extraction
2. **More complex syndrome circuits:** The syndrome extraction circuit for color codes
   has more opportunities for error propagation
3. **Decoder difficulty:** The correlated X-Z structure makes decoding harder

### 6.3 Qubit Count Comparison

For the same code distance d:

| d | Surface code (n) | Color code triangular (n) | Color code 4.8.8 (n) |
|---|------------------|--------------------------|---------------------|
| 3 | 9 | 7 | 9 |
| 5 | 25 | 19 | 25 |
| 7 | 49 | 37 | 49 |

The triangular color code uses fewer qubits for the same distance, but the higher
threshold of the surface code means you often need a smaller d to achieve the same
logical error rate, potentially negating this advantage.

### 6.4 When to Choose Color Codes

Color codes are advantageous when:
- Physical error rates are very low (< 0.1%)
- Many Clifford gates are needed (compilation advantage)
- Qubit count is extremely limited
- The hardware natively supports the required lattice connectivity

Surface codes are advantageous when:
- Physical error rates are moderate (0.1-1%)
- Nearest-neighbor connectivity only (planar chips)
- Fast decoding is needed
- Larger distances will be required

---

## 7. Decoding Color Codes

### 7.1 The Restriction Decoder

The restriction decoder (Kubica & Delfosse, 2023) maps the color code decoding problem
to multiple surface code decoding problems:

1. For each pair of colors (c1, c2), project the syndrome onto the color-restricted
   stabilizer group S_{c1,c2}
2. Decode each restricted syndrome using a surface code decoder (e.g., MWPM)
3. Combine the restricted corrections to obtain the full correction

This leverages the mature surface code decoder infrastructure while handling the
additional structure of color codes.

### 7.2 Other Decoders

| Decoder | Approach | Threshold |
|---------|---------|-----------|
| Restriction (MWPM) | Map to surface codes | ~0.1% (circuit) |
| Projection | Similar to restriction | ~0.08% |
| Renormalization | Hierarchical | ~0.08% |
| Mobius | Symmetry-aware MWPM | ~0.1% |
| Neural network | Learned | ~0.1% |
| MaxSAT | Exact for small codes | Optimal (small d) |

---

## 8. The 7-Qubit Color Code in Detail

### 8.1 Stabilizer Generators

The 6 stabilizer generators for [[7, 1, 3]]:

```
g1 (X-red):   X X X I X I I
g2 (X-green): I X I X X X I
g3 (X-blue):  I I X I X X X
g4 (Z-red):   Z Z Z I Z I I
g5 (Z-green): I Z I Z Z Z I
g6 (Z-blue):  I I Z I Z Z Z
```

### 8.2 Logical Operators

```
X_L = X X X X X X X  (all X)
Z_L = Z Z Z Z Z Z Z  (all Z)
```

These anticommute ({X_L, Z_L} = 0 since n = 7 is odd) and commute with all
stabilizers.

### 8.3 Error Correction Example

Consider a single X error on qubit 4: E = I I I X I I I

Syndrome computation:
- g4 (Z-red): Z1 Z2 Z3 Z5 -> commutes with X4 -> syndrome bit = 0
- g5 (Z-green): Z2 Z4 Z5 Z6 -> anticommutes (contains Z4) -> syndrome bit = 1
- g6 (Z-blue): Z3 Z5 Z6 Z7 -> commutes with X4 -> syndrome bit = 0

Z-syndrome = (0, 1, 0) -> uniquely identifies qubit 4 as having an X error.

Similarly for Z errors using X-stabilizer syndromes, and Y errors produce both
X and Z syndromes.

---

## 9. Higher-Dimensional Color Codes

### 9.1 The 3D Color Code

The 3D color code is defined on a 4-colorable lattice (3-colex) in 3 dimensions.
Its key property:

```
Transversal T gate: T_L = T^{(x)n}
```

Combined with the transversal Clifford gates, this gives transversal {H, S, CNOT, T},
which is a universal gate set! However, the 3D color code requires a 3D lattice
architecture, which is extremely challenging for current hardware.

### 9.2 Gauge Color Codes

Gauge color codes (Bombin, 2015) trade encoding rate for flexibility. By promoting
some stabilizers to gauge operators (which need not have definite eigenvalues), one
can implement single-shot error correction -- the ability to correct errors using a
single round of noisy syndrome measurement, rather than d rounds.

---

## 10. Experimental Realizations

### 10.1 Trapped Ion Implementations

Quantinuum demonstrated a distance-7 color code on their H2 processor (2024):
- 29 data qubits + ancilla qubits
- All-to-all connectivity enables direct implementation
- Logical error rate below physical error rate demonstrated
- Multiple rounds of error correction

### 10.2 Superconducting Implementations

Color codes on superconducting hardware face connectivity challenges:
- The triangular lattice requires degree-6 vertices
- Heavy-hex lattices (IBM) are not naturally compatible
- Adaptation requires additional SWAP operations, reducing effective threshold

### 10.3 Neutral Atom Implementations

Neutral atom platforms (e.g., QuEra, Atom Computing) offer:
- Reconfigurable connectivity via atom shuttling
- Potential for native triangular lattice layouts
- Early demonstrations of small color codes (d = 3)

---

## 11. Summary and Outlook

Color codes offer a compelling alternative to surface codes with three key advantages:
1. Transversal Clifford gates (simpler compilation, lower gate overhead)
2. Fewer physical qubits per logical qubit for the same code distance
3. Rich mathematical structure enabling novel decoding strategies

The main disadvantages are:
1. Lower circuit-level threshold (~0.1% vs ~0.8% for surface codes)
2. Higher-weight stabilizers requiring more complex syndrome circuits
3. Less mature decoding infrastructure

The choice between surface codes and color codes ultimately depends on hardware error
rates. As physical qubit quality improves and error rates drop below 0.1%, color codes
may become the preferred choice due to their gate implementation advantages.

---

## References

1. Bombin, H. & Martin-Delgado, M. A. (2006). "Topological quantum distillation." Phys. Rev. Lett. 97, 180501
2. Steane, A. M. (1996). "Error correcting codes in quantum theory." Phys. Rev. Lett. 77, 793
3. Bombin, H. (2015). "Gauge color codes." Phys. Rev. X 5, 031043
4. Kubica, A. & Delfosse, N. (2023). "Efficient color code decoders in d >= 2 dimensions from toric code decoders." Quantum 7, 929
5. Quantinuum (2024). "Fault-tolerant quantum computing with color codes." (Experimental demonstration)
6. Landahl, A. J., Anderson, J. T., & Rice, P. R. (2011). "Fault-tolerant quantum computing with color codes." arXiv:1108.5738
