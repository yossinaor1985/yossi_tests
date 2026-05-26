# Quantum Walk Mixers (Generalized QAOA) - Physicist's Deep Dive

## 1. Overview

Quantum walk mixers were introduced by Hadfield et al. (2019) as part of the **Quantum Alternating Operator Ansatz** (QAOAz) — a generalization of Farhi's original QAOA (algorithm 02 in this repository). The key innovation: replace the standard transverse-field mixer with a mixer whose dynamics correspond to a **continuous-time quantum walk on the graph of feasible solutions**, thereby preserving problem constraints by construction.

In standard QAOA, the mixer H_M = sum_i X_i generates transitions across the entire 2^n Hilbert space, including infeasible states. For constrained optimization problems, this wastes quantum amplitude on states that violate constraints and can never be valid solutions. Quantum walk mixers solve this by restricting exploration to the feasible subspace.

**Prerequisite:** The reader should be familiar with algorithm 02 (QAOA). This material extends that framework.

---

## 2. Mathematical Foundation

### 2.1 The Quantum Alternating Operator Ansatz

The generalized QAOA (QAOAz) prepares the state:

```
|gamma, beta> = U_M(beta_p) U_C(gamma_p) ... U_M(beta_1) U_C(gamma_1) |s_0>
```

where:
- |s_0> is an easily preparable **feasible** initial state
- U_C(gamma) = exp(-i gamma H_C) is the cost unitary (same as standard QAOA)
- U_M(beta) = exp(-i beta H_M) is a **constraint-preserving mixer**
- The mixer must satisfy two properties:
  1. **Feasibility preservation:** If |psi> is in the feasible subspace F, then U_M(beta)|psi> is also in F
  2. **Connectivity (ergodicity):** For any two feasible states |x>, |y> in F, there exists some sequence of mixer applications that maps |x> to |y>

Standard QAOA is the special case where F = {0,1}^n (no constraints), |s_0> = |+>^n, and H_M = sum_i X_i.

### 2.2 Constrained Optimization and the Feasible Subspace

Consider optimization problems of the form:

```
max C(z)  subject to z in F subset {0,1}^n
```

where F is a proper subset of all bitstrings. Examples:

| Problem | Constraint | Feasible Set F |
|---------|------------|----------------|
| Max Bisection | Equal partition size | {z : |z| = n/2} |
| Max k-Vertex Cover | Exactly k vertices | {z : |z| = k} |
| Traveling Salesman | Valid permutation | One-hot encoded rows/columns |
| Graph Coloring | No adjacent same-color | Valid colorings |

Here |z| denotes the Hamming weight of z.

For Max Bisection on n = 4 nodes:
```
|F| = C(4, 2) = 6  out of  2^4 = 16  total bitstrings
```

The feasible states are: {|0011>, |0101>, |0110>, |1001>, |1010>, |1100>}.

### 2.3 The XY Mixer Hamiltonian

For **Hamming-weight constraints** (exactly k ones out of n bits), the natural choice is the XY mixer:

```
H_XY = sum_{(i,j) in E_M} (1/2)(X_i X_j + Y_i Y_j)
```

where E_M is the set of qubit pairs in the mixer graph (typically all pairs or nearest neighbors).

Using raising/lowering operators sigma^+ = (X + iY)/2 and sigma^- = (X - iY)/2:

```
(1/2)(X_i X_j + Y_i Y_j) = sigma_i^+ sigma_j^- + sigma_i^- sigma_j^+
```

This is the **hopping operator**: it moves an excitation from qubit j to qubit i (or vice versa) without creating or destroying excitations. In the computational basis:

```
(1/2)(X_i X_j + Y_i Y_j) |...0_i...1_j...> = |...1_i...0_j...>
(1/2)(X_i X_j + Y_i Y_j) |...1_i...0_j...> = |...0_i...1_j...>
(1/2)(X_i X_j + Y_i Y_j) |...0_i...0_j...> = 0
(1/2)(X_i X_j + Y_i Y_j) |...1_i...1_j...> = 0
```

**Proof of Hamming-weight preservation:**

The total magnetization operator is N = sum_i (I - Z_i)/2, which counts the number of |1>s. We need to show [H_XY, N] = 0.

Since N = (n/2)I - (1/2) sum_i Z_i, it suffices to show [H_XY, sum_i Z_i] = 0.

For a single pair (i,j):
```
[sigma_i^+ sigma_j^- + sigma_i^- sigma_j^+, Z_i + Z_j]
= [sigma_i^+ sigma_j^-, Z_i] + [sigma_i^+ sigma_j^-, Z_j]
  + [sigma_i^- sigma_j^+, Z_i] + [sigma_i^- sigma_j^+, Z_j]
= (-2 sigma_i^+ sigma_j^-) + (2 sigma_i^+ sigma_j^-)
  + (2 sigma_i^- sigma_j^+) + (-2 sigma_i^- sigma_j^+)
= 0
```

where we used [sigma^+, Z] = -2 sigma^+ and [sigma^-, Z] = 2 sigma^-.

Therefore H_XY preserves Hamming weight, and exp(-i beta H_XY) maps the weight-k subspace to itself. QED.

### 2.4 Connection to Continuous-Time Quantum Walks

The unitary U_M(beta) = exp(-i beta H_XY) implements a **continuous-time quantum walk** on the "swap graph" G_swap:

- **Nodes:** All feasible solutions (bitstrings with Hamming weight k)
- **Edges:** Two feasible solutions are connected if they differ by a single (i,j)-swap (one bit flipped 0->1, another flipped 1->0)

This is precisely the **Johnson graph** J(n, k), whose nodes are k-element subsets of {1, ..., n} and edges connect subsets that differ in exactly one element.

For n = 4, k = 2, the Johnson graph J(4, 2) has:
- 6 nodes: {0011, 0101, 0110, 1001, 1010, 1100}
- Each node has degree 4 (can swap any of the 2 ones with any of the 2 zeros)
- The graph is vertex-transitive and connected

The adjacency matrix of J(n, k) (restricted to the weight-k subspace) is proportional to H_XY. Thus the quantum walk explores the feasible space through sequences of single-excitation hops.

**Ergodicity:** J(n, k) is connected for all 0 < k < n, ensuring that the XY mixer can reach any feasible state from any other. This guarantees that QAOAz with the XY mixer does not sacrifice optimality.

### 2.5 The Dicke State

The appropriate initial state for the XY mixer is the **Dicke state**:

```
|D_n^k> = (1/sqrt(C(n,k))) sum_{|z|=k} |z>
```

This is the equal-amplitude superposition of all weight-k bitstrings. It is the ground state of H_XY within the weight-k subspace (by analogy, |+>^n is the ground state of sum_i X_i in standard QAOA).

For n = 4, k = 2:
```
|D_4^2> = (1/sqrt(6)) (|0011> + |0101> + |0110> + |1001> + |1010> + |1100>)
```

Dicke states can be prepared in O(kn) gates using the recursive algorithm of Bartschi and Eidenbenz (2019), or via the `initialize()` method in simulation.

### 2.6 The XXPlusYY Gate

Each pair-wise term exp(-i beta (X_i X_j + Y_i Y_j)/2) is implemented using the **XXPlusYY gate**.

The unitary matrix (in the {|00>, |01>, |10>, |11>} basis):

```
XXPlusYYGate(theta) = [[1,        0,            0,        0],
                       [0,   cos(theta/2),  -i*sin(theta/2), 0],
                       [0, -i*sin(theta/2),  cos(theta/2),   0],
                       [0,        0,            0,        1]]
```

This corresponds to:
```
XXPlusYYGate(theta) = exp(-i (theta/2) (|01><10| + |10><01|))
                    = exp(-i (theta/4) (XX + YY))
```

To implement exp(-i beta (XX + YY)/2), we set theta = 2*beta:

```
XXPlusYYGate(2*beta) = exp(-i beta (XX + YY)/2)
```

The full XY mixer unitary is Trotterized as:
```
U_M(beta) = exp(-i beta H_XY) approx prod_{(i,j) in E_M} XXPlusYYGate(2*beta) on (i,j)
```

This is a first-order Trotter approximation. The error is O(beta^2) per layer, which is acceptable for variational optimization since the parameters are optimized anyway.

### 2.7 Why the Cost Unitary Also Preserves Feasibility

The cost Hamiltonian H_C is diagonal in the computational basis:

```
U_C(gamma) |z> = exp(-i gamma C(z)) |z>
```

It applies a phase to each basis state without changing any bits. Therefore U_C(gamma) trivially preserves Hamming weight (and any other bit-string property). Combined with the XY mixer, the **entire QAOAz circuit** preserves feasibility:

```
|s_0> in F  =>  U_M(beta_p) U_C(gamma_p) ... U_M(beta_1) U_C(gamma_1) |s_0> in F
```

---

## 3. Detailed Example: Max Bisection on 4-Node Cycle

### 3.1 Problem Definition

**Max Bisection:** Given a graph G = (V, E), partition V into two sets S and S^c of **equal size** (|S| = |S^c| = n/2) to maximize the number of edges crossing the partition.

This is MaxCut with the additional constraint |S| = n/2.

Graph: 4-node cycle (same as algorithm 02)
```
    0 --- 1
    |     |
    3 --- 2
```
Edges: {(0,1), (1,2), (2,3), (0,3)}

### 3.2 Feasible Solutions

The 6 feasible bitstrings (Hamming weight = 2) and their cut values:

| Bitstring | Partition (S = {i : z_i = 1}) | Cut Value |
|-----------|-------------------------------|-----------|
| 0011 | S = {2, 3} | 2 |
| 0101 | S = {1, 3} | **4** (optimal) |
| 0110 | S = {1, 2} | 2 |
| 1001 | S = {0, 3} | 2 |
| 1010 | S = {0, 2} | **4** (optimal) |
| 1100 | S = {0, 1} | 2 |

Optimal Max Bisection = 4 (cutting all edges), achieved by the alternating partitions |0101> and |1010>.

Note: These are the same optimal solutions as unconstrained MaxCut. However, for other graphs the Max Bisection optimum can be strictly less than the MaxCut optimum.

### 3.3 Cost Hamiltonian

Same as standard MaxCut (see algorithm 02, Section 3.2):

```
H_C = (1/2) sum_{(i,j) in E} (I - Z_i Z_j)
    = 2I - (1/2)(Z_0 Z_1 + Z_1 Z_2 + Z_2 Z_3 + Z_0 Z_3)
```

### 3.4 XY Mixer for This Problem

Using all 6 qubit pairs (complete mixer graph):

```
H_XY = (1/2) sum_{i<j, i,j in {0,1,2,3}} (X_i X_j + Y_i Y_j)
```

This has C(4, 2) = 6 pair terms. In the weight-2 subspace, H_XY acts as the adjacency matrix of J(4, 2), which is the octahedral graph (each of the 6 nodes connected to 4 others).

### 3.5 Why Standard QAOA Fails for Max Bisection

Standard QAOA starts from |+>^4 and uses the transverse-field mixer sum_i X_i. At any depth p:

- The state has nonzero amplitude on **all** 16 basis states
- Only 6/16 = 37.5% of the Hilbert space is feasible
- Infeasible samples are wasted (must be discarded in post-processing)
- The optimizer must "learn" to suppress infeasible amplitudes, wasting optimization budget

The quantum walk mixer eliminates this problem entirely: every sample is guaranteed feasible.

### 3.6 QAOAz Circuit Structure

```
|D_4^2> --[U_C(gamma_1)]--[U_XY(beta_1)]--..--[U_C(gamma_p)]--[U_XY(beta_p)]-- Measure
```

Where:
- |D_4^2> is prepared using initialize() (simulation) or an explicit circuit (hardware)
- U_C(gamma) uses CNOT-RZ-CNOT for each edge (same as standard QAOA)
- U_XY(beta) uses XXPlusYYGate(2*beta) for each qubit pair

---

## 4. Other Quantum Walk Mixers

### 4.1 Swap/Permutation Mixers

For optimization over permutations (TSP, scheduling), the mixer applies partial SWAP operations between adjacent positions. The quantum walk occurs on the Cayley graph of the symmetric group S_n generated by transpositions.

### 4.2 Grover-Style Mixer

```
U_Grover = 2|psi_F><psi_F| - I
```

where |psi_F> is the uniform superposition over feasible states. This is a reflection operator — equivalent to one step of Grover's search within F. It preserves the feasible subspace and is maximally connected (one-step reachability between any two feasible states).

### 4.3 Partition/Coloring Mixers

For graph coloring problems: change one vertex's color at a time, only to colors not used by neighbors. This uses controlled rotations conditioned on neighbor states.

---

## 5. Complexity and Scaling

### 5.1 Circuit Depth

For p layers of QAOAz with complete-graph XY mixer on n qubits:

```
Dicke state preparation: O(kn) gates  [Bartschi-Eidenbenz]
Cost layer (per round):  O(|E|) gates  [same as standard QAOA]
XY mixer layer (per round): O(n^2) gates  [C(n,2) XXPlusYY gates]
Total depth: O(kn + p(|E| + n^2))
```

For a ring-topology mixer (nearest-neighbor pairs only), the XY layer reduces to O(n) gates, but mixing may require more QAOA rounds.

### 5.2 Comparison with Penalty-Based Approach

An alternative to constraint-preserving mixers: add a penalty term to the cost function:

```
H_penalty = H_C + lambda * (sum_i Z_i - target)^2
```

Trade-offs:

| | Quantum Walk Mixer | Penalty Method |
|---|---|---|
| Feasibility | Guaranteed | Approximate (depends on lambda) |
| Parameter tuning | No penalty coefficient | Must tune lambda |
| Search space | Feasible subspace only | Full Hilbert space |
| Circuit complexity | Higher per layer (multi-qubit mixer) | Lower per layer (single-qubit mixer) |
| Scaling | O(n^2) mixer gates per layer | O(n) mixer gates per layer |

### 5.3 Practical Considerations

The main bottleneck on real hardware is the **Dicke state preparation circuit**, which has depth O(kn) and involves many CNOT gates. For n > ~10 qubits on current NISQ devices, the Dicke state fidelity degrades significantly due to gate errors.

---

## 6. References

1. Hadfield, S., Wang, Z., O'Gorman, B., Rieffel, E. G., Venturelli, D., & Biswas, R. "From the Quantum Approximate Optimization Algorithm to a Quantum Alternating Operator Ansatz." Algorithms 12, 34 (2019).
2. Wang, Z., Rubin, N. C., Dominy, J. M., & Rieffel, E. G. "XY mixers: Analytical and numerical results for the quantum alternating operator ansatz." Physical Review A 101, 012320 (2020).
3. Bartschi, A., & Eidenbenz, S. "Deterministic Preparation of Dicke States." Fundamentals of Computation Theory (FCT), 126-139 (2019).
4. Fuchs, F. G., Kolden, H. O., Aase, N. H., & Sartor, G. "Efficient encoding of the weighted MAX k-CUT on a quantum computer using QAOA." SN Computer Science 2, 89 (2021).
5. Cook, J., Eidenbenz, S., & Bartschi, A. "The Quantum Alternating Operator Ansatz on Maximum k-Colorable Subgraphs." arXiv:1907.05386 (2019).
6. Farhi, E., Goldstone, J., & Gutmann, S. "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028 (2014).
