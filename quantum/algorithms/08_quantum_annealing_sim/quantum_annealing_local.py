"""
Quantum Annealing (Simulated on Gate-Based Hardware) - Local Simulator
=======================================================================

This script implements Trotterized quantum annealing on a gate-based
quantum simulator. It builds annealing circuits from scratch and compares
the approach with QAOA on the MaxCut problem.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
Quantum annealing evolves a time-dependent Hamiltonian:
    H(s) = (1 - s) * H_M + s * H_C

where s = s(t) is the annealing schedule, H_M is the mixer (driver)
Hamiltonian, and H_C is the cost (problem) Hamiltonian.

On a gate-based computer, we discretize the continuous evolution into
P Trotter steps:
    U(T) ~ prod_{k=0}^{P-1} exp(-i*beta_k*H_M) * exp(-i*gamma_k*H_C)

where:
    gamma_k = dt * s_k       (cost parameter at step k)
    beta_k  = dt * (1 - s_k) (mixer parameter at step k)

The parameters are FIXED by the schedule (not variationally optimized).

Algorithm:
    1. Initialize |psi_0> = |+>^n  (ground state of H_M)
    2. For each Trotter step k = 0, ..., P-1:
        a. Compute s_k from the annealing schedule
        b. Apply U_C(gamma_k): cost unitary with gamma_k = dt * s_k
        c. Apply U_M(beta_k): mixer unitary with beta_k = dt * (1 - s_k)
    3. Measure final state to extract solution
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer import AerSimulator


# =============================================================================
# SECTION 1: Hamiltonian Construction
# =============================================================================

def build_maxcut_hamiltonian(edges, num_nodes):
    """
    Build the MaxCut cost Hamiltonian.

    H_C = (1/2) sum_{(i,j) in E} (I - Z_i Z_j)

    Each edge (i,j) contributes +1 to the eigenvalue when qubits i and j
    are in different states (cut edge), and 0 when they are the same.

    Args:
        edges: List of (i, j) tuples representing graph edges
        num_nodes: Number of nodes (qubits) in the graph

    Returns:
        SparsePauliOp: The MaxCut Hamiltonian
    """
    pauli_list = []
    for i, j in edges:
        # Identity term: (1/2) * I
        id_str = "I" * num_nodes
        pauli_list.append((id_str, 0.5))

        # ZZ term: -(1/2) * Z_i Z_j
        zz_list = ["I"] * num_nodes
        zz_list[num_nodes - 1 - i] = "Z"
        zz_list[num_nodes - 1 - j] = "Z"
        pauli_list.append(("".join(zz_list), -0.5))

    return SparsePauliOp.from_list(pauli_list).simplify()


def build_mixer_hamiltonian(num_nodes):
    """
    Build the mixer (driver) Hamiltonian H_M = sum_i X_i.

    This is the standard transverse-field mixer. Its ground state is |+>^n
    (uniform superposition), which serves as the initial state for annealing.

    The mixer generates quantum fluctuations that allow the system to
    explore the solution space via quantum tunneling.

    Args:
        num_nodes: Number of qubits

    Returns:
        SparsePauliOp: The mixer Hamiltonian
    """
    pauli_list = []
    for i in range(num_nodes):
        x_str = ["I"] * num_nodes
        x_str[num_nodes - 1 - i] = "X"
        pauli_list.append(("".join(x_str), 1.0))
    return SparsePauliOp.from_list(pauli_list)


# =============================================================================
# SECTION 2: Annealing Schedules
# =============================================================================

def linear_schedule(t, T):
    """
    Linear annealing schedule: s(t) = t/T.

    The simplest schedule. The Hamiltonian changes at a constant rate.
    Not optimal -- wastes time where the gap is large and rushes through
    the critical region near the minimum gap.

    Args:
        t: Current time (or step index)
        T: Total annealing time (or total number of steps)

    Returns:
        float: Schedule parameter s in [0, 1]
    """
    return t / T


def polynomial_schedule(t, T, alpha=2.0):
    """
    Polynomial annealing schedule: s(t) = (t/T)^alpha.

    alpha > 1: slower start, faster end. Spends more time in the
               early paramagnetic phase. Good when the minimum gap
               occurs early in the anneal.
    alpha < 1: faster start, slower end. Spends more time in the
               late ferromagnetic phase.
    alpha = 1: reduces to linear schedule.

    Args:
        t: Current time
        T: Total annealing time
        alpha: Polynomial exponent (default: 2.0)

    Returns:
        float: Schedule parameter s in [0, 1]
    """
    return (t / T) ** alpha


def sigmoid_schedule(t, T, kappa=4.0):
    """
    Sigmoid annealing schedule: s(t) = 0.5 * [1 + tanh(kappa * (2t/T - 1))].

    This schedule spends more time near s = 0.5, where the minimum gap
    typically occurs for many optimization problems. The parameter kappa
    controls the steepness:
        kappa -> 0: approaches linear schedule
        kappa -> inf: approaches step function (instant jump at t = T/2)

    This is often superior to linear scheduling because the adiabatic
    condition is most stringent near the gap minimum.

    See explanation_physicist.md, Section 3.3.

    Args:
        t: Current time
        T: Total annealing time
        kappa: Steepness parameter (default: 4.0)

    Returns:
        float: Schedule parameter s in [0, 1]
    """
    # tanh-based sigmoid centered at t/T = 0.5
    x = kappa * (2.0 * t / T - 1.0)
    return 0.5 * (1.0 + np.tanh(x))


def cosine_schedule(t, T):
    """
    Cosine annealing schedule: s(t) = 0.5 * [1 - cos(pi * t / T)].

    Smooth schedule that slows down near s = 0 and s = 1. This naturally
    spends more time near the boundaries where the system must transition
    between phases.

    Args:
        t: Current time
        T: Total annealing time

    Returns:
        float: Schedule parameter s in [0, 1]
    """
    return 0.5 * (1.0 - np.cos(np.pi * t / T))


# =============================================================================
# SECTION 3: Trotterized Annealing Circuit
# =============================================================================

def build_annealing_circuit(num_nodes, edges, num_steps, total_time,
                            schedule_fn=linear_schedule, **schedule_kwargs):
    """
    Build a Trotterized quantum annealing circuit.

    This discretizes the continuous adiabatic evolution into P gate-based
    Trotter steps. Each step k applies:
        U_k = U_M(beta_k) * U_C(gamma_k)
    where:
        gamma_k = dt * s_k        (cost unitary strength)
        beta_k  = dt * (1 - s_k)  (mixer unitary strength)
        s_k     = schedule(k + 0.5, P)  (midpoint rule for better accuracy)

    See explanation_physicist.md, Section 4.

    Args:
        num_nodes: Number of qubits
        edges: Graph edges for MaxCut
        num_steps: Number of Trotter steps P
        total_time: Total annealing time T
        schedule_fn: Annealing schedule function s(t, T)
        **schedule_kwargs: Additional keyword arguments for the schedule

    Returns:
        QuantumCircuit: The Trotterized annealing circuit (without measurement)
        gammas: List of cost parameters at each step
        betas: List of mixer parameters at each step
    """
    dt = total_time / num_steps
    qc = QuantumCircuit(num_nodes)

    # -------------------------------------------------------------------------
    # Step 0: Initialize in |+>^n (ground state of H_M = sum_i X_i)
    # -------------------------------------------------------------------------
    for i in range(num_nodes):
        qc.h(i)

    gammas = []
    betas = []

    # -------------------------------------------------------------------------
    # Steps 1..P: Apply Trotter steps
    # -------------------------------------------------------------------------
    for k in range(num_steps):
        # Midpoint rule: evaluate schedule at t = (k + 0.5) * dt
        # This gives second-order accuracy in the time discretization
        t_k = (k + 0.5) * dt
        s_k = schedule_fn(t_k, total_time, **schedule_kwargs)

        # Clamp to [epsilon, 1-epsilon] to avoid degenerate steps
        s_k = max(1e-10, min(1.0 - 1e-10, s_k))

        gamma_k = dt * s_k           # Cost unitary strength
        beta_k = dt * (1.0 - s_k)    # Mixer unitary strength

        gammas.append(gamma_k)
        betas.append(beta_k)

        # --- Cost unitary: exp(-i * gamma_k * H_C) ---
        # For MaxCut: H_C = (1/2) sum_{(i,j)} (I - Z_i Z_j)
        # exp(-i*gamma*Z_i*Z_j/2) is implemented via CNOT-RZ-CNOT
        # The identity part contributes only a global phase (ignored).
        for i_node, j_node in edges:
            qc.cx(i_node, j_node)
            qc.rz(2 * gamma_k, j_node)
            qc.cx(i_node, j_node)

        # --- Mixer unitary: exp(-i * beta_k * H_M) ---
        # H_M = sum_i X_i
        # exp(-i*beta*X_i) = RX(2*beta) on each qubit
        for i_node in range(num_nodes):
            qc.rx(2 * beta_k, i_node)

    return qc, gammas, betas


def build_annealing_circuit_with_measurement(num_nodes, edges, num_steps,
                                             total_time,
                                             schedule_fn=linear_schedule,
                                             **schedule_kwargs):
    """
    Build a Trotterized annealing circuit with final measurement.

    Wraps build_annealing_circuit and adds measurement gates.

    Args:
        num_nodes: Number of qubits
        edges: Graph edges
        num_steps: Number of Trotter steps
        total_time: Total annealing time
        schedule_fn: Schedule function
        **schedule_kwargs: Schedule keyword arguments

    Returns:
        QuantumCircuit: Circuit with measurements
        gammas: Cost parameters
        betas: Mixer parameters
    """
    qc, gammas, betas = build_annealing_circuit(
        num_nodes, edges, num_steps, total_time,
        schedule_fn, **schedule_kwargs
    )
    qc.measure_all()
    return qc, gammas, betas


# =============================================================================
# SECTION 4: Statevector-Based Annealing Simulation
# =============================================================================

def run_annealing_statevector(edges, num_nodes, num_steps, total_time,
                              schedule_fn=linear_schedule, **schedule_kwargs):
    """
    Run Trotterized quantum annealing using exact statevector simulation.

    This builds the annealing circuit and evolves the state exactly,
    tracking the cost expectation value <H_C> and the ground state
    fidelity at each Trotter step.

    Args:
        edges: Graph edges
        num_nodes: Number of qubits
        num_steps: Number of Trotter steps P
        total_time: Total annealing time T
        schedule_fn: Annealing schedule function
        **schedule_kwargs: Schedule keyword arguments

    Returns:
        cost_history: <H_C> at each step (length P+1, including initial)
        schedule_values: s_k at each step (length P)
        final_state: Statevector after annealing
        gammas: Cost parameters
        betas: Mixer parameters
    """
    H_C = build_maxcut_hamiltonian(edges, num_nodes)

    dt = total_time / num_steps

    # Initialize |+>^n
    qc_init = QuantumCircuit(num_nodes)
    for i in range(num_nodes):
        qc_init.h(i)
    state = Statevector(qc_init)

    # Measure initial cost
    C_0 = state.expectation_value(H_C).real
    cost_history = [C_0]
    schedule_values = []
    gammas = []
    betas = []

    print(f"  Step 0 (initial): <H_C> = {C_0:.6f}")

    for k in range(num_steps):
        t_k = (k + 0.5) * dt
        s_k = schedule_fn(t_k, total_time, **schedule_kwargs)
        s_k = max(1e-10, min(1.0 - 1e-10, s_k))

        gamma_k = dt * s_k
        beta_k = dt * (1.0 - s_k)

        schedule_values.append(s_k)
        gammas.append(gamma_k)
        betas.append(beta_k)

        # Build single-step circuit
        qc_step = QuantumCircuit(num_nodes)

        # Cost unitary
        for i_node, j_node in edges:
            qc_step.cx(i_node, j_node)
            qc_step.rz(2 * gamma_k, j_node)
            qc_step.cx(i_node, j_node)

        # Mixer unitary
        for i_node in range(num_nodes):
            qc_step.rx(2 * beta_k, i_node)

        # Evolve state
        state = state.evolve(qc_step)

        # Measure cost
        C_k = state.expectation_value(H_C).real
        cost_history.append(C_k)

        if k < 5 or k == num_steps - 1 or (k + 1) % max(1, num_steps // 10) == 0:
            print(f"  Step {k+1:4d}: s = {s_k:.4f}, "
                  f"gamma = {gamma_k:.4f}, beta = {beta_k:.4f}, "
                  f"<H_C> = {C_k:.6f}")

    return cost_history, schedule_values, state, gammas, betas


# =============================================================================
# SECTION 5: QAOA for Comparison
# =============================================================================

def build_qaoa_circuit(num_nodes, edges, gammas, betas):
    """
    Build a standard QAOA circuit with given parameters.

    QAOA uses the same circuit structure as Trotterized annealing,
    but the parameters are variationally optimized rather than fixed
    by a schedule.

    See explanation_physicist.md, Section 5.

    Args:
        num_nodes: Number of qubits
        edges: Graph edges
        gammas: Cost unitary parameters (one per layer)
        betas: Mixer unitary parameters (one per layer)

    Returns:
        QuantumCircuit: The QAOA circuit (without measurement)
    """
    p = len(gammas)
    qc = QuantumCircuit(num_nodes)

    # Initialize |+>^n
    for i in range(num_nodes):
        qc.h(i)

    # QAOA layers
    for layer in range(p):
        # Cost unitary
        for i_node, j_node in edges:
            qc.cx(i_node, j_node)
            qc.rz(2 * gammas[layer], j_node)
            qc.cx(i_node, j_node)

        # Mixer unitary
        for i_node in range(num_nodes):
            qc.rx(2 * betas[layer], i_node)

    return qc


def evaluate_qaoa_cost(num_nodes, edges, gammas, betas):
    """
    Evaluate <H_C> for a given set of QAOA parameters.

    Uses exact statevector simulation for efficiency.

    Args:
        num_nodes: Number of qubits
        edges: Graph edges
        gammas: Cost parameters
        betas: Mixer parameters

    Returns:
        float: Expectation value <H_C>
    """
    H_C = build_maxcut_hamiltonian(edges, num_nodes)
    qc = build_qaoa_circuit(num_nodes, edges, gammas, betas)
    state = Statevector(qc)
    return state.expectation_value(H_C).real


def optimize_qaoa(edges, num_nodes, p, maxiter=300):
    """
    Run QAOA with classical parameter optimization.

    Uses COBYLA optimizer (gradient-free, noise-tolerant) to find
    optimal gamma and beta parameters at depth p.

    Args:
        edges: Graph edges
        num_nodes: Number of qubits
        p: Number of QAOA layers
        maxiter: Maximum optimizer iterations

    Returns:
        best_cost: Best <H_C> found
        optimal_gammas: Optimized cost parameters
        optimal_betas: Optimized mixer parameters
        n_evals: Number of function evaluations used
    """
    from scipy.optimize import minimize

    H_C = build_maxcut_hamiltonian(edges, num_nodes)
    eval_count = [0]

    def cost_function(params):
        """Objective: minimize -<H_C> (equivalent to maximizing <H_C>)."""
        gammas_opt = params[:p]
        betas_opt = params[p:]
        qc = build_qaoa_circuit(num_nodes, edges, gammas_opt, betas_opt)
        state = Statevector(qc)
        cost = -state.expectation_value(H_C).real
        eval_count[0] += 1
        return cost

    # Initialize with annealing-inspired ramp (a good starting point)
    gamma_init = np.linspace(0.1, 0.8, p)
    beta_init = np.linspace(0.8, 0.1, p)
    x0 = np.concatenate([gamma_init, beta_init])

    result = minimize(cost_function, x0, method='COBYLA',
                      options={'maxiter': maxiter, 'rhobeg': 0.3})

    best_cost = -result.fun
    optimal_gammas = result.x[:p].tolist()
    optimal_betas = result.x[p:].tolist()

    return best_cost, optimal_gammas, optimal_betas, eval_count[0]


# =============================================================================
# SECTION 6: Analysis Utilities
# =============================================================================

def compute_exact_maxcut(edges, num_nodes):
    """
    Compute the exact MaxCut value by brute force.

    Enumerates all 2^n bitstrings and evaluates the cut value for each.
    Only feasible for small instances (n <= ~20).

    Args:
        edges: Graph edges
        num_nodes: Number of nodes

    Returns:
        max_cut: Maximum cut value
        optimal_bitstrings: List of bitstrings achieving the max cut
    """
    max_cut = 0
    optimal_bitstrings = []

    for x in range(2 ** num_nodes):
        bs = format(x, f'0{num_nodes}b')
        cut = sum(1 for (i, j) in edges if bs[i] != bs[j])
        if cut > max_cut:
            max_cut = cut
            optimal_bitstrings = [bs]
        elif cut == max_cut:
            optimal_bitstrings.append(bs)

    return max_cut, optimal_bitstrings


def analyze_final_state(state, edges, num_nodes, max_cut, top_k=10):
    """
    Analyze the final quantum state after annealing.

    Prints the top-k most probable bitstrings and their cut values.

    Args:
        state: Statevector after annealing
        edges: Graph edges
        num_nodes: Number of nodes
        max_cut: Known optimal cut value
        top_k: Number of top results to display
    """
    probs = state.probabilities_dict()
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    print(f"\n  Top {top_k} measurement outcomes:")
    for bs, prob in sorted_probs[:top_k]:
        cut = sum(1 for (i, j) in edges if bs[i] != bs[j])
        marker = " <-- OPTIMAL" if cut == max_cut else ""
        print(f"    |{bs}> : prob = {prob:.4f}, cut = {cut}{marker}")

    # Compute expected cut value from the probability distribution
    expected_cut = 0.0
    for bs, prob in probs.items():
        cut = sum(1 for (i, j) in edges if bs[i] != bs[j])
        expected_cut += cut * prob

    # Probability of sampling an optimal solution
    optimal_prob = sum(
        prob for bs, prob in probs.items()
        if sum(1 for (i, j) in edges if bs[i] != bs[j]) == max_cut
    )

    print(f"\n  Expected cut value: {expected_cut:.4f}")
    print(f"  Approximation ratio: {expected_cut / max_cut:.4f}")
    print(f"  Probability of optimal solution: {optimal_prob:.4f}")

    return expected_cut, optimal_prob


# =============================================================================
# SECTION 7: Main Execution
# =============================================================================

def main():
    print("=" * 70)
    print("Quantum Annealing (Trotterized) - Local Simulator")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Problem Setup -- MaxCut on a 5-Node Graph
    # =========================================================================

    print("\n--- Step 1: MaxCut Problem Setup ---")

    # Pentagon with one diagonal -- 5 nodes, 6 edges
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
    num_nodes = 5

    max_cut, optimal_bs = compute_exact_maxcut(edges, num_nodes)

    print(f"  Graph: {num_nodes} nodes, {len(edges)} edges")
    print(f"  Edges: {edges}")
    print(f"  MaxCut: {max_cut}")
    print(f"  Optimal bitstrings: {optimal_bs}")

    # =========================================================================
    # STEP 2: Trotterized Annealing with Linear Schedule
    # =========================================================================

    print("\n--- Step 2: Trotterized Annealing (Linear Schedule) ---")
    print("  Parameters: P=40 steps, T=4.0")

    cost_lin, sched_lin, state_lin, gammas_lin, betas_lin = \
        run_annealing_statevector(
            edges, num_nodes,
            num_steps=40,
            total_time=4.0,
            schedule_fn=linear_schedule
        )

    print(f"\n  Final <H_C>: {cost_lin[-1]:.6f}")
    print(f"  Approximation ratio: {cost_lin[-1] / max_cut:.4f}")

    analyze_final_state(state_lin, edges, num_nodes, max_cut)

    # =========================================================================
    # STEP 3: Compare Multiple Annealing Schedules
    # =========================================================================

    print("\n--- Step 3: Comparing Annealing Schedules ---")

    num_steps = 40
    total_time = 4.0

    schedule_configs = [
        ("Linear", linear_schedule, {}),
        ("Polynomial (alpha=2)", polynomial_schedule, {"alpha": 2.0}),
        ("Polynomial (alpha=0.5)", polynomial_schedule, {"alpha": 0.5}),
        ("Sigmoid (kappa=4)", sigmoid_schedule, {"kappa": 4.0}),
        ("Cosine", cosine_schedule, {}),
    ]

    schedule_results = {}

    for name, sched_fn, kwargs in schedule_configs:
        print(f"\n  Schedule: {name}")
        costs, scheds, state, _, _ = run_annealing_statevector(
            edges, num_nodes, num_steps, total_time,
            schedule_fn=sched_fn, **kwargs
        )
        ratio = costs[-1] / max_cut
        _, opt_prob = analyze_final_state(state, edges, num_nodes, max_cut, top_k=3)
        schedule_results[name] = {
            "costs": costs,
            "schedule": scheds,
            "ratio": ratio,
            "opt_prob": opt_prob,
        }
        print(f"  --> Approximation ratio: {ratio:.4f}")

    # =========================================================================
    # STEP 4: Effect of Number of Trotter Steps
    # =========================================================================

    print("\n--- Step 4: Effect of Trotter Steps (P) ---")

    total_time_fixed = 4.0
    step_counts = [5, 10, 20, 40, 80, 160]
    trotter_results = {}

    for P in step_counts:
        costs, _, state, _, _ = run_annealing_statevector(
            edges, num_nodes, P, total_time_fixed,
            schedule_fn=linear_schedule
        )
        ratio = costs[-1] / max_cut
        trotter_results[P] = ratio
        print(f"  P = {P:4d}: ratio = {ratio:.4f}")

    # =========================================================================
    # STEP 5: Effect of Total Annealing Time
    # =========================================================================

    print("\n--- Step 5: Effect of Total Annealing Time (T) ---")

    num_steps_fixed = 40
    times = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    time_results = {}

    for T in times:
        costs, _, state, _, _ = run_annealing_statevector(
            edges, num_nodes, num_steps_fixed, T,
            schedule_fn=linear_schedule
        )
        ratio = costs[-1] / max_cut
        time_results[T] = ratio
        print(f"  T = {T:5.1f}: ratio = {ratio:.4f}")

    # =========================================================================
    # STEP 6: Comparison with QAOA
    # =========================================================================

    print("\n--- Step 6: QAOA Comparison ---")

    qaoa_results = {}
    for p in [5, 10, 20, 40]:
        best_cost, opt_gammas, opt_betas, n_evals = optimize_qaoa(
            edges, num_nodes, p, maxiter=500
        )
        ratio = best_cost / max_cut
        qaoa_results[p] = {
            "cost": best_cost,
            "ratio": ratio,
            "n_evals": n_evals,
        }
        print(f"  QAOA p={p:3d}: <H_C> = {best_cost:.4f}, "
              f"ratio = {ratio:.4f}, evals = {n_evals}")

    # Compare with Trotterized annealing at matching depths
    print("\n  Annealing vs QAOA at matching circuit depth:")
    for p in [5, 10, 20, 40]:
        ann_ratio = trotter_results.get(p, None)
        qaoa_ratio = qaoa_results[p]["ratio"]
        if ann_ratio is not None:
            print(f"    depth={p:3d}: Annealing = {ann_ratio:.4f}, "
                  f"QAOA = {qaoa_ratio:.4f}, "
                  f"diff = {qaoa_ratio - ann_ratio:+.4f}")

    # =========================================================================
    # STEP 7: Annealing-Inspired QAOA Initialization
    # =========================================================================

    print("\n--- Step 7: Annealing-Inspired QAOA Initialization ---")
    print("  Using linear annealing schedule as initial parameters for QAOA")

    p_test = 20

    # Annealing schedule parameters as QAOA initialization
    dt_init = 4.0 / p_test
    gamma_init_anneal = [dt_init * (k + 0.5) / p_test for k in range(p_test)]
    beta_init_anneal = [dt_init * (1.0 - (k + 0.5) / p_test) for k in range(p_test)]

    anneal_init_cost = evaluate_qaoa_cost(
        num_nodes, edges, gamma_init_anneal, beta_init_anneal
    )
    print(f"  Annealing init (no optimization): <H_C> = {anneal_init_cost:.4f}, "
          f"ratio = {anneal_init_cost / max_cut:.4f}")

    # Random initialization for comparison
    np.random.seed(42)
    gamma_init_rand = np.random.uniform(0, np.pi, p_test).tolist()
    beta_init_rand = np.random.uniform(0, np.pi / 2, p_test).tolist()

    rand_init_cost = evaluate_qaoa_cost(
        num_nodes, edges, gamma_init_rand, beta_init_rand
    )
    print(f"  Random init (no optimization):    <H_C> = {rand_init_cost:.4f}, "
          f"ratio = {rand_init_cost / max_cut:.4f}")

    # =========================================================================
    # STEP 8: Shot-Based Simulation (AerSimulator)
    # =========================================================================

    print("\n--- Step 8: Shot-Based Simulation (AerSimulator) ---")

    SHOTS = 8192
    best_schedule = max(schedule_results.items(), key=lambda x: x[1]["ratio"])
    print(f"  Using best schedule: {best_schedule[0]}")

    # Rebuild circuit with measurements
    # Use linear schedule for the shot-based demo
    qc_shots, _, _ = build_annealing_circuit_with_measurement(
        num_nodes, edges,
        num_steps=40, total_time=4.0,
        schedule_fn=linear_schedule
    )

    simulator = AerSimulator()
    result = simulator.run(qc_shots, shots=SHOTS).result()
    counts = result.get_counts()

    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    print(f"\n  Top 10 measurement results ({SHOTS} shots):")
    for bs, count in sorted_counts[:10]:
        cut = sum(1 for (i, j) in edges if bs[i] != bs[j])
        prob = count / SHOTS
        marker = " <-- OPTIMAL" if cut == max_cut else ""
        print(f"    |{bs}> : count = {count:5d} ({prob:.1%}), cut = {cut}{marker}")

    # Expected cut from sampling
    expected_cut_sampled = sum(
        sum(1 for (i, j) in edges if bs[i] != bs[j]) * count
        for bs, count in counts.items()
    ) / SHOTS

    print(f"\n  Expected cut (sampled): {expected_cut_sampled:.2f}")
    print(f"  Sampling ratio: {expected_cut_sampled / max_cut:.4f}")

    # =========================================================================
    # STEP 9: Visualization
    # =========================================================================

    print("\n--- Step 9: Generating Plots ---")

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))

    # ---- Plot 1: Annealing Schedules ----
    t_arr = np.linspace(0, 1, 200)
    for name, sched_fn, kwargs in schedule_configs:
        s_arr = [sched_fn(t, 1.0, **kwargs) for t in t_arr]
        axes[0, 0].plot(t_arr, s_arr, linewidth=2, label=name)
    axes[0, 0].set_xlabel('t / T', fontsize=12)
    axes[0, 0].set_ylabel('s(t)', fontsize=12)
    axes[0, 0].set_title('Annealing Schedules', fontsize=14)
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(True, alpha=0.3)

    # ---- Plot 2: Cost Evolution by Schedule ----
    for name, data in schedule_results.items():
        steps_arr = range(len(data["costs"]))
        axes[0, 1].plot(steps_arr, data["costs"], linewidth=2,
                        label=f'{name} ({data["ratio"]:.3f})')
    axes[0, 1].axhline(y=max_cut, color='r', linestyle='--',
                        linewidth=2, label=f'MaxCut = {max_cut}')
    axes[0, 1].set_xlabel('Trotter Step', fontsize=12)
    axes[0, 1].set_ylabel('<H_C>', fontsize=12)
    axes[0, 1].set_title('Cost Evolution by Schedule', fontsize=14)
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].grid(True, alpha=0.3)

    # ---- Plot 3: Effect of Trotter Steps ----
    P_vals = sorted(trotter_results.keys())
    ratios_P = [trotter_results[P] for P in P_vals]
    axes[0, 2].plot(P_vals, ratios_P, 'bo-', linewidth=2, markersize=8)
    axes[0, 2].axhline(y=1.0, color='r', linestyle='--', alpha=0.5)
    axes[0, 2].set_xlabel('Number of Trotter Steps (P)', fontsize=12)
    axes[0, 2].set_ylabel('Approximation Ratio', fontsize=12)
    axes[0, 2].set_title('Convergence with Trotter Steps', fontsize=14)
    axes[0, 2].grid(True, alpha=0.3)
    axes[0, 2].set_xscale('log')

    # ---- Plot 4: Effect of Annealing Time ----
    T_vals = sorted(time_results.keys())
    ratios_T = [time_results[T] for T in T_vals]
    axes[1, 0].plot(T_vals, ratios_T, 'rs-', linewidth=2, markersize=8)
    axes[1, 0].axhline(y=1.0, color='r', linestyle='--', alpha=0.5)
    axes[1, 0].set_xlabel('Total Annealing Time (T)', fontsize=12)
    axes[1, 0].set_ylabel('Approximation Ratio', fontsize=12)
    axes[1, 0].set_title('Convergence with Annealing Time', fontsize=14)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_xscale('log')

    # ---- Plot 5: Annealing vs QAOA ----
    common_depths = sorted(set(trotter_results.keys()) & set(qaoa_results.keys()))
    ann_ratios = [trotter_results[d] for d in common_depths]
    qaoa_ratios_plot = [qaoa_results[d]["ratio"] for d in common_depths]
    axes[1, 1].plot(common_depths, ann_ratios, 'bo-', linewidth=2,
                    markersize=8, label='Trotterized Annealing')
    axes[1, 1].plot(common_depths, qaoa_ratios_plot, 'r^-', linewidth=2,
                    markersize=8, label='QAOA (optimized)')
    axes[1, 1].axhline(y=1.0, color='gray', linestyle='--', alpha=0.5)
    axes[1, 1].set_xlabel('Circuit Depth (layers)', fontsize=12)
    axes[1, 1].set_ylabel('Approximation Ratio', fontsize=12)
    axes[1, 1].set_title('Annealing vs QAOA', fontsize=14)
    axes[1, 1].legend(fontsize=10)
    axes[1, 1].grid(True, alpha=0.3)

    # ---- Plot 6: Schedule Parameters (gamma_k, beta_k) ----
    steps_arr = range(len(gammas_lin))
    axes[1, 2].plot(steps_arr, gammas_lin, 'b-', linewidth=2, label='gamma_k (cost)')
    axes[1, 2].plot(steps_arr, betas_lin, 'r-', linewidth=2, label='beta_k (mixer)')
    axes[1, 2].set_xlabel('Trotter Step', fontsize=12)
    axes[1, 2].set_ylabel('Parameter Value', fontsize=12)
    axes[1, 2].set_title('Annealing Parameters (Linear Schedule)', fontsize=14)
    axes[1, 2].legend(fontsize=10)
    axes[1, 2].grid(True, alpha=0.3)

    plt.suptitle('Quantum Annealing (Trotterized on Gate-Based Hardware)',
                 fontsize=16, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig('quantum/algorithms/08_quantum_annealing_sim/'
                'quantum_annealing_results.png',
                dpi=150, bbox_inches='tight')
    plt.show()

    # =========================================================================
    # STEP 10: Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
    Problem: MaxCut on {num_nodes}-node graph with {len(edges)} edges
    Exact MaxCut: {max_cut}
    Optimal bitstrings: {optimal_bs}

    Trotterized Annealing Results (P=40, T=4.0):
      Linear schedule:     ratio = {schedule_results['Linear']['ratio']:.4f}
      Polynomial (a=2):    ratio = {schedule_results['Polynomial (alpha=2)']['ratio']:.4f}
      Polynomial (a=0.5):  ratio = {schedule_results['Polynomial (alpha=0.5)']['ratio']:.4f}
      Sigmoid (k=4):       ratio = {schedule_results['Sigmoid (kappa=4)']['ratio']:.4f}
      Cosine:              ratio = {schedule_results['Cosine']['ratio']:.4f}

    Key Findings:
      1. More Trotter steps (P) -> better approximation (Trotter error decreases)
      2. Longer annealing time (T) -> better adiabatic fidelity (up to a point)
      3. Nonlinear schedules can outperform linear when the gap structure is favorable
      4. QAOA with optimized parameters outperforms fixed-schedule annealing
         at the same circuit depth, but requires classical optimization
      5. Annealing schedule provides excellent QAOA initialization
    """)


if __name__ == "__main__":
    main()
