# Grover Adaptive Search (GAS) for Optimization - Physicist's Deep Dive

## 1. Overview

Grover Adaptive Search (GAS) applies Grover's quantum search algorithm iteratively to solve combinatorial optimization problems. Unlike QAOA (which finds approximate solutions variationally), GAS provably finds the exact optimal solution with quadratic speedup over classical brute-force search.

The key idea: use Grover's algorithm to search for solutions that are better than the current best known solution, progressively tightening the threshold until the optimum is found.

**Original references:**
- Grover, L. K. "A fast quantum mechanical algorithm for database search." (1996)
- Durr, C. & Hoyer, P. "A quantum algorithm for finding the minimum." (1996)
- Gilliam, A., Woerner, S., & Gonciulea, C. "Grover Adaptive Search for Constrained Polynomial Binary Optimization." (2021)

---

## 2. Mathematical Foundation

### 2.1 Grover's Search Algorithm (Review)

**Problem:** Given a function f: {0,1}^n -> {0,1} (oracle), find x* such that f(x*) = 1.

**Grover's algorithm:**

1. Initialize: |psi_0> = H^{otimes n} |0>^n = (1/sqrt(N)) sum_{x=0}^{N-1} |x>, where N = 2^n

2. Apply the Grover operator G = D * O repeatedly:
   - **Oracle operator** O: flips the phase of marked states
     ```
     O |x> = (-1)^{f(x)} |x>
     ```
   - **Diffusion operator** D = 2|psi_0><psi_0| - I: amplifies the amplitude of marked states (reflection about the mean)

3. After k applications of G, measure to get a marked state with high probability.

**Optimal number of iterations:**

If there are M marked states out of N total:
```
k_opt = floor(pi/(4*theta) - 1/2)
```
where theta = arcsin(sqrt(M/N)).

For M << N: k_opt ≈ (pi/4) * sqrt(N/M)

**Success probability after k iterations:**
```
P(success) = sin^2((2k+1)*theta)
```

### 2.2 Geometric Interpretation

The Hilbert space is spanned by two orthogonal states:
```
|alpha> = (1/sqrt(N-M)) sum_{f(x)=0} |x>    (non-solutions)
|beta>  = (1/sqrt(M))   sum_{f(x)=1} |x>     (solutions)
```

The initial state is:
```
|psi_0> = cos(theta) |alpha> + sin(theta) |beta>
```
where sin(theta) = sqrt(M/N).

Each Grover iteration rotates the state by 2*theta toward |beta>:
```
G^k |psi_0> = cos((2k+1)*theta) |alpha> + sin((2k+1)*theta) |beta>
```

### 2.3 Durr-Hoyer Minimum Finding Algorithm

**Problem:** Given f: {0,1}^n -> R, find x* = argmin f(x).

**Algorithm:**

1. Pick a random x, set threshold y = f(x).
2. Define oracle O_y that marks all x with f(x) < y.
3. Run Grover's search with O_y to find x' with f(x') < y.
4. Update y = f(x') and repeat.
5. After O(sqrt(N)) total Grover iterations, x* is found with high probability.

**Complexity:** O(sqrt(N)) oracle calls, providing a quadratic speedup over the classical O(N).

### 2.4 Grover Adaptive Search for QUBO

**Problem:** Minimize C(x) = x^T Q x + q^T x for x in {0,1}^n.

**Phase oracle construction:**

The oracle must implement:
```
O_y |x>|0> = |x>|C(x) < y>
```

This requires:
1. **Arithmetic circuit:** Compute C(x) into an ancilla register
2. **Comparison circuit:** Compare C(x) with threshold y
3. **Phase kickback:** Use the comparison qubit to flip the phase
4. **Uncomputation:** Reverse the arithmetic to restore ancillae

The cost function C(x) for QUBO can be decomposed as:
```
C(x) = sum_{i<j} Q_{ij} x_i x_j + sum_i (Q_{ii} + q_i) x_i
```

Since x_i in {0,1}, the multiplication x_i * x_j is an AND gate (Toffoli).

---

## 3. Circuit Construction

### 3.1 Oracle Circuit for QUBO

For a QUBO with n binary variables:

1. **Register allocation:**
   - n qubits for the solution x
   - m ancilla qubits for storing C(x) (m = ceil(log2(max C(x))))
   - 1 flag qubit for the comparison result

2. **Compute C(x):**
   - For each term Q_{ij} x_i x_j: use a Toffoli gate controlled on x_i and x_j to add Q_{ij} to the ancilla register
   - For each term (Q_{ii} + q_i) x_i: use a controlled addition on x_i

3. **Compare with threshold:**
   - Subtract y from the ancilla register
   - The sign bit indicates whether C(x) < y

4. **Phase kickback:**
   - Apply a Z gate on the flag qubit to flip the phase of states where C(x) < y

5. **Uncompute:**
   - Reverse all operations in steps 2-3 (except the phase flip)

### 3.2 Grover Diffusion Operator

The standard diffusion operator D = 2|+><+| - I is implemented as:

```
D = H^{otimes n} * (2|0><0| - I) * H^{otimes n}
```

The middle operator (2|0><0| - I) flips the phase of |0...0> and is implemented as:
```
X^{otimes n} * MCZ * X^{otimes n}
```
where MCZ is a multi-controlled Z gate.

---

## 4. Qiskit Implementation: GroverOptimizer

Qiskit's `GroverOptimizer` from `qiskit_optimization` implements GAS for QUBO problems:

1. Converts the QUBO into a quantum oracle circuit
2. Applies Grover iterations with adaptive threshold
3. Returns the optimal solution

The `GroverOptimizer` takes:
- `num_value_qubits`: Number of qubits for encoding C(x)
- `num_iterations`: Maximum Grover iterations per search round
- `converters`: Optional converters (e.g., QuadraticProgramToQubo)

---

## 5. Worked Example: 3-Variable QUBO

### Problem

Minimize C(x) = -x_0 - x_1 + 2*x_0*x_1 + x_2 - x_1*x_2

In matrix form:
```
Q = [[-1,  2,  0],
     [ 0, -1, -1],
     [ 0,  0,  1]]
```

### All solutions (brute force):

| x_0 x_1 x_2 | C(x) |
|:---:|:---:|
| 000 | 0 |
| 001 | 1 |
| 010 | -1 |
| 011 | -1 |
| 100 | -1 |
| 101 | 0 |
| 110 | 0 |
| 111 | 0 |

Minimum: C(x) = -1 at x = {010, 011, 100}

### GAS Execution:

**Round 1:** Pick random x = 000, threshold y = C(000) = 0
- Oracle marks all x with C(x) < 0: {010, 011, 100}
- M/N = 3/8, theta = arcsin(sqrt(3/8)) ≈ 0.6585
- k_opt = floor(pi/(4*0.6585) - 0.5) = floor(0.69) = 0
- Even k=0 has a chance due to initial overlap. After 1 Grover iteration, probability of finding a marked state ≈ 94.5%
- Suppose we find x = 010, update threshold y = -1

**Round 2:** Threshold y = -1
- Oracle marks all x with C(x) < -1: {} (empty set)
- No solutions found → algorithm terminates
- Output: x* = 010, C(x*) = -1

---

## 6. Complexity Analysis

- **Classical brute force:** O(2^n) evaluations
- **Grover Adaptive Search:** O(sqrt(2^n)) = O(2^{n/2}) evaluations
- **Quadratic speedup** is provably optimal for unstructured search (BBBV theorem)

**Gate complexity per oracle call:**
- O(n^2) for quadratic terms (Toffoli gates)
- O(m * n) for arithmetic accumulation
- O(m) for comparison
- Total: O(n^2 + m*n) gates per oracle evaluation

**Practical limitation:** The oracle circuit for real QUBO problems can be very deep, making GAS impractical on NISQ devices. It is primarily of interest for fault-tolerant quantum computers.

---

## 7. References

1. Grover, L. K. "A fast quantum mechanical algorithm for database search." Proc. STOC 1996, pp. 212-219.
2. Durr, C. & Hoyer, P. "A quantum algorithm for finding the minimum." arXiv:quant-ph/9607014 (1996).
3. Gilliam, A., Woerner, S., & Gonciulea, C. "Grover Adaptive Search for Constrained Polynomial Binary Optimization." Quantum Science and Technology 6, 034010 (2021).
4. Boyer, M., Brassard, G., Hoyer, P., & Tapp, A. "Tight bounds on quantum searching." Fortschritte der Physik 46, 493-505 (1998).
