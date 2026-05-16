# Quantum Annealing (Simulated on Gate-Based Hardware) - Physicist's Deep Dive

## 1. Overview

Quantum annealing is a metaheuristic for solving combinatorial optimization problems by exploiting quantum tunneling and adiabatic evolution. Native quantum annealing requires purpose-built hardware (e.g., D-Wave), but the same physics can be **simulated on gate-based quantum computers** via Trotterization of the time-dependent Hamiltonian evolution.

This topic addresses:
- The adiabatic quantum computing (AQC) theorem that guarantees correctness
- How to discretize the continuous adiabatic evolution into quantum gates (Trotterization)
- The deep connection between Trotterized annealing and QAOA
- Practical implementation of simulated annealing schedules on gate-based hardware

**Key insight:** QAOA is a variational discretization of quantum annealing. Trotterized annealing is a *fixed-schedule* discretization. Both approximate the same continuous-time adiabatic process, but with different parameter-setting strategies.

---

## 2. Adiabatic Quantum Computing

### 2.1 The Adiabatic Theorem

**Statement (Born & Fock, 1928):** If a quantum system starts in the ground state of a Hamiltonian H(0) and the Hamiltonian varies sufficiently slowly, the system remains in the instantaneous ground state of H(t) at all times.

More precisely, consider a time-dependent Hamiltonian H(t) for t in [0, T]. Let |E_0(t)> be the instantaneous ground state with energy E_0(t), and |E_1(t)> the first excited state with energy E_1(t). Define the minimum spectral gap:

```
Delta_min = min_{t in [0,T]} [E_1(t) - E_0(t)]
```

The adiabatic condition requires:

```
max_{t in [0,T]} |<E_1(t)| dH/dt |E_0(t)>| << Delta_min^2
```

If this condition is satisfied, the probability of a transition out of the ground state is bounded by:

```
P_transition <= (max_t |<E_1| dH/dt |E_0>|)^2 / Delta_min^4
```

### 2.2 Proof Sketch

Consider the Schrodinger equation in the adiabatic frame. Expand the state in the instantaneous eigenbasis:

```
|psi(t)> = sum_k c_k(t) exp(-i integral_0^t E_k(t') dt') |E_k(t)>
```

Substituting into i*d|psi>/dt = H(t)|psi> and projecting onto |E_m(t)>:

```
dc_m/dt = -sum_{k != m} c_k(t) * <E_m| dH/dt |E_k> / (E_k - E_m) * exp(i * phi_{mk}(t))
```

where phi_{mk}(t) = integral_0^t (E_m(t') - E_k(t')) dt' is the dynamical phase difference.

For slow evolution (large T), the phase factors oscillate rapidly and the transitions average out. The dominant non-adiabatic coupling is to the first excited state, suppressed by 1/Delta_min^2. The total evolution time T must satisfy:

```
T >> max_t |<E_1| dH/dt |E_0>| / Delta_min^2
```

This is the **adiabatic condition**. The harder the problem (smaller gap), the longer the required annealing time.

### 2.3 Computational Complexity and the Gap

The runtime of AQC is determined by the minimum gap:

```
T = O(1 / Delta_min^2)
```

For NP-hard problems, the gap typically closes exponentially with system size n:

```
Delta_min ~ exp(-alpha * n)
```

leading to exponential runtime T ~ exp(2*alpha*n). This does not violate complexity-theoretic beliefs (NP != BQP). However, for specific problem structures, the gap may close only polynomially, yielding quantum speedups.

---

## 3. Time-Dependent Hamiltonian for Quantum Annealing

### 3.1 The Annealing Hamiltonian

The standard quantum annealing Hamiltonian is:

```
H(s) = (1 - s) * H_M + s * H_C
```

where:
- s = s(t) in [0, 1] is the **annealing schedule** parameter
- H_M is the **driver** (mixer) Hamiltonian, typically the transverse-field: H_M = -sum_i X_i
- H_C is the **problem** (cost) Hamiltonian, encoding the optimization problem
- At s = 0: H(0) = H_M, whose ground state |+>^n is easy to prepare
- At s = 1: H(1) = H_C, whose ground state encodes the solution

### 3.2 Linear Schedule

The simplest schedule is linear: s(t) = t/T, giving:

```
H(t) = (1 - t/T) * H_M + (t/T) * H_C
```

The rate of change is dH/dt = (H_C - H_M)/T, which is uniform in time.

### 3.3 Nonlinear Schedules

The adiabatic condition is most stringent near the minimum gap. Nonlinear schedules slow down near the gap minimum to improve fidelity:

**Polynomial schedule:**
```
s(t) = (t/T)^alpha
```
- alpha > 1: slower start, faster end (good when gap minimum is early)
- alpha < 1: faster start, slower end (good when gap minimum is late)

**Sigmoid schedule (gap-adaptive):**
```
s(t) = 1/2 * [1 + tanh(kappa * (2t/T - 1))]
```

This spends more time near s = 0.5 where the gap minimum often occurs.

**Optimal schedule (Rezakhani et al.):**
```
ds/dt proportional to Delta(s)^2
```

This allocates evolution time inversely proportional to the adiabatic vulnerability, spending more time where the gap is smallest.

---

## 4. Trotterization: Gate-Based Simulation of Annealing

### 4.1 The Trotter-Suzuki Decomposition

To simulate H(t) = (1-s)*H_M + s*H_C on a gate-based computer, we discretize time into P steps (Trotter steps):

```
dt = T / P
t_k = k * dt,  s_k = s(t_k),  k = 0, 1, ..., P-1
```

The full evolution operator is:

```
U(T) = T_exp(-i integral_0^T H(t) dt)  [time-ordered exponential]
```

Using the first-order Trotter-Suzuki decomposition:

```
U(T) approx prod_{k=0}^{P-1} exp(-i * dt * [(1-s_k)*H_M + s_k*H_C])
     approx prod_{k=0}^{P-1} exp(-i * dt * (1-s_k) * H_M) * exp(-i * dt * s_k * H_C)
```

The Trotter error per step is O(dt^2 * ||[H_M, H_C]||), and the total error is:

```
||U_exact - U_Trotter|| = O(P * dt^2 * ||[H_M, H_C]||) = O(T^2 / P * ||[H_M, H_C]||)
```

### 4.2 Higher-Order Trotterization

**Second-order (Strang splitting):**
```
U_k = exp(-i * dt/2 * (1-s_k) * H_M) * exp(-i * dt * s_k * H_C) * exp(-i * dt/2 * (1-s_k) * H_M)
```

Error: O(T^3 / P^2 * ||[H_M, [H_M, H_C]]||)

### 4.3 Circuit Implementation

For MaxCut with H_C = (1/2) sum_{(i,j)} (I - Z_i Z_j) and H_M = sum_i X_i:

**Cost unitary** U_C(gamma_k) = exp(-i * gamma_k * H_C) where gamma_k = dt * s_k:
```
For each edge (i,j):
    CNOT(i, j) -> RZ(2*gamma_k, j) -> CNOT(i, j)
```

**Mixer unitary** U_M(beta_k) = exp(-i * beta_k * H_M) where beta_k = dt * (1 - s_k):
```
For each qubit i:
    RX(2*beta_k, i)
```

Each Trotter step contributes:
- |E| CNOT pairs + |E| RZ gates (cost layer)
- n RX gates (mixer layer)

Total circuit depth: O(P * |E|).

### 4.4 The Trotterized Annealing Circuit

The full circuit has the form:

```
|psi> = U_M(beta_{P-1}) U_C(gamma_{P-1}) ... U_M(beta_1) U_C(gamma_1) U_M(beta_0) U_C(gamma_0) |+>^n
```

where:
```
gamma_k = dt * s_k           [cost parameter at step k]
beta_k  = dt * (1 - s_k)     [mixer parameter at step k]
```

Note: these parameters are **fixed by the schedule**, not variationally optimized.

---

## 5. Connection to QAOA

### 5.1 QAOA as Discretized Annealing

QAOA uses the same circuit structure as Trotterized annealing:

```
|gamma, beta> = prod_{k=1}^{p} U_M(beta_k) U_C(gamma_k) |+>^n
```

The critical difference:

| Aspect | Trotterized Annealing | QAOA |
|--------|----------------------|------|
| Parameters | Fixed by schedule s(t) | Variationally optimized |
| Number of steps P/p | Large (100-1000) | Small (1-20) |
| Error control | Trotter error -> 0 as P -> inf | Approximation ratio depends on p |
| Adiabatic limit | Recovers exact solution at P -> inf, T -> inf | Recovers exact solution at p -> inf |
| Classical cost | None (schedule is predetermined) | Optimization loop required |

### 5.2 QAOA Recovers Annealing in the Deep Limit

Farhi, Goldstone, and Gutmann (2014) proved that for any epsilon > 0, there exists p* such that for all p >= p*, QAOA with optimized parameters achieves:

```
<gamma*, beta*| H_C |gamma*, beta*> >= E_0 - epsilon
```

where E_0 is the ground state energy of H_C. The proof works by showing that the optimal QAOA parameters at large p approximate the Trotterized adiabatic schedule.

### 5.3 Annealing-Inspired QAOA Initialization

The Trotterized annealing schedule provides a natural initialization for QAOA parameters:

```
gamma_k^{init} = (k/p) * gamma_max
beta_k^{init}  = (1 - k/p) * beta_max
```

This "linear ramp" initialization has been shown to outperform random initialization (Zhou et al., 2020) and is equivalent to a discretized linear annealing schedule.

---

## 6. The Transverse-Field Ising Model (TFIM)

### 6.1 Definition

The transverse-field Ising model is the canonical model for quantum annealing:

```
H_TFIM(s) = -(1-s) * Gamma * sum_i X_i - s * [sum_{(i,j)} J_{ij} Z_i Z_j + sum_i h_i Z_i]
```

where:
- Gamma is the transverse-field strength
- J_{ij} are the Ising couplings
- h_i are the local fields
- s in [0, 1] is the annealing parameter

### 6.2 Phase Transition and Gap

At a critical value s_c, the system undergoes a quantum phase transition:
- For s < s_c: the ground state is paramagnetic (aligned with X)
- For s > s_c: the ground state is ferromagnetic/frustrated (aligned with Z)

Near s_c, the gap scales as:

```
Delta ~ |s - s_c|^{z*nu}
```

where z is the dynamical critical exponent and nu is the correlation length exponent. For the 1D TFIM: z = nu = 1, giving Delta ~ 1/n (polynomial gap, efficient annealing).

For frustrated systems (e.g., random J_{ij}), the gap can close exponentially, making annealing inefficient.

### 6.3 Connection to Optimization

Any QUBO (Quadratic Unconstrained Binary Optimization) problem can be cast as finding the ground state of an Ising Hamiltonian:

```
min_z sum_{ij} Q_{ij} z_i z_j  <-->  ground state of H_C = sum_{ij} J_{ij} Z_i Z_j + sum_i h_i Z_i
```

via z_i = (1 - Z_i)/2. This makes the TFIM the natural framework for quantum optimization.

---

## 7. Worked Example: 4-Qubit MaxCut via Trotterized Annealing

### 7.1 Problem

Square graph: 4 nodes, edges {(0,1), (1,2), (2,3), (3,0)}. MaxCut = 4 (solutions: |0101>, |1010>).

### 7.2 Hamiltonians

```
H_C = (1/2)[(I - Z_0 Z_1) + (I - Z_1 Z_2) + (I - Z_2 Z_3) + (I - Z_3 Z_0)]
    = 2*I - (1/2)(Z_0 Z_1 + Z_1 Z_2 + Z_2 Z_3 + Z_3 Z_0)

H_M = X_0 + X_1 + X_2 + X_3
```

### 7.3 Linear Schedule with P = 4 Trotter Steps

s_k = (k + 0.5) / P for k = 0, 1, 2, 3 (midpoint rule):

| Step k | s_k   | gamma_k = dt*s_k | beta_k = dt*(1-s_k) |
|--------|-------|-------------------|----------------------|
| 0      | 0.125 | 0.125*dt          | 0.875*dt             |
| 1      | 0.375 | 0.375*dt          | 0.625*dt             |
| 2      | 0.625 | 0.625*dt          | 0.375*dt             |
| 3      | 0.875 | 0.875*dt          | 0.125*dt             |

With total time T = P*dt, the parameters interpolate from strong mixing (large beta) to strong cost (large gamma), mimicking the adiabatic path.

### 7.4 Expected Behavior

- At P = 4 (crude discretization): approximation ratio ~ 0.7-0.8
- At P = 20: approximation ratio ~ 0.9+
- At P = 100: approximation ratio ~ 0.99+ (approaching adiabatic limit)
- Increasing T also helps, but beyond a point only P matters (Trotter error dominates)

### 7.5 Comparison with QAOA at Same Depth

At depth p = 4:
- Trotterized annealing: gamma, beta fixed by schedule (no optimization needed)
- QAOA: gamma, beta optimized variationally (higher cost, potentially better result at fixed p)

QAOA at p = 4 with optimized parameters will generally outperform Trotterized annealing at P = 4, because QAOA has the freedom to choose any parameters, while annealing is constrained to the schedule. However, annealing does not require a classical optimization loop.

---

## 8. Advanced Topics

### 8.1 Quantum Speed Limit and Annealing Time

The quantum speed limit constrains how fast a state can evolve:

```
T >= pi / (2 * Delta E)
```

where Delta E is the energy uncertainty. For annealing, this sets a lower bound on T given the gap structure.

### 8.2 Diabatic Transitions and Quantum Speed-Up

Counterintuitively, slight diabatic transitions (violating the adiabatic condition) can sometimes help. The system tunnels through intermediate excited states and arrives at the ground state via constructive interference. This is the basis for:
- **Diabatic quantum computing** (Crosson & Harrow, 2021)
- **Quantum walks** as an annealing alternative

### 8.3 Simulated Quantum Annealing vs. True Quantum Annealing

On a gate-based simulator, we cannot capture:
- Finite-temperature effects (thermal excitations in D-Wave)
- Open-system dynamics (system-bath coupling)
- Analog control errors (flux noise in superconducting qubits)

What we CAN capture:
- Coherent quantum tunneling through barriers
- Superposition of candidate solutions
- Entanglement between qubits during the anneal
- The effect of different schedules on solution quality

### 8.4 Error Bounds for Trotterized Annealing

The Trotter error for a single step with H = A + B is:

```
||exp(-i*dt*(A+B)) - exp(-i*dt*A)*exp(-i*dt*B)|| <= dt^2/2 * ||[A, B]||
```

For P steps with total time T = P*dt:

```
||U_exact - U_Trotter|| <= T^2 / (2P) * ||[H_M, H_C]||
```

To achieve error epsilon:

```
P >= T^2 * ||[H_M, H_C]|| / (2*epsilon)
```

---

## 9. References

1. Farhi, E., Goldstone, J., Gutmann, S., & Sipser, M. "Quantum Computation by Adiabatic Evolution." arXiv:quant-ph/0001106 (2000).
2. Farhi, E., Goldstone, J., & Gutmann, S. "A Quantum Approximate Optimization Algorithm." arXiv:1411.4028 (2014).
3. Albash, T. & Lidar, D. A. "Adiabatic quantum computation." Reviews of Modern Physics 90, 015002 (2018).
4. Born, M. & Fock, V. "Beweis des Adiabatensatzes." Zeitschrift fur Physik 51, 165-180 (1928).
5. Suzuki, M. "Generalized Trotter's formula and systematic approximants of exponential operators." Communications in Mathematical Physics 51, 183-190 (1976).
6. Zhou, L., Wang, S.-T., Choi, S., Pichler, H., & Lukin, M. D. "Quantum Approximate Optimization Algorithm: Performance, Mechanism, and Implementation on Near-Term Devices." Physical Review X 10, 021067 (2020).
7. Rezakhani, A. T., Kuo, W.-J., Hamma, A., Lidar, D. A., & Zanardi, P. "Quantum Adiabatic Brachistochrone." Physical Review Letters 103, 080502 (2009).
8. Crosson, E. & Harrow, A. W. "Simulated Quantum Annealing Can Be Exponentially Faster Than Classical Simulated Annealing." FOCS 2016, pp. 714-723.
9. Kadowaki, T. & Nishimori, H. "Quantum annealing in the transverse Ising model." Physical Review E 58, 5355 (1998).
10. Hauke, P., Katzgraber, H. G., Lechner, W., Nishimori, H., & Oliver, W. D. "Perspectives of quantum annealing: Methods and implementations." Reports on Progress in Physics 83, 054401 (2020).
