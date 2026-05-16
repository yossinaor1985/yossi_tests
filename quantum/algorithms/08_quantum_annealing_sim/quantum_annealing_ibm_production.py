"""
Quantum Annealing (Trotterized) - IBM Production-Ready Implementation
======================================================================

Production implementation of Trotterized quantum annealing for MaxCut
on IBM Quantum hardware.

Qiskit Version: 2.4.1

Production Considerations:
    - Parameters are fixed by the annealing schedule (no optimization loop)
    - Circuit depth grows linearly with Trotter steps P
    - On NISQ hardware, P is limited by decoherence (~10-30 steps practical)
    - Error mitigation (ZNE, Twirled Readout) is essential for noisy backends
    - Transpilation at optimization_level=3 reduces gate count significantly
    - Results are saved to JSON for reproducibility and post-processing

Strategy:
    1. Compute annealing schedule parameters classically (trivial)
    2. Build the full Trotterized circuit with gate-based decomposition
    3. Transpile for target backend
    4. Execute with error mitigation
    5. Post-process and save results
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session


# =============================================================================
# SECTION 1: Hamiltonian Construction
# =============================================================================

def build_maxcut_hamiltonian(edges, num_nodes):
    """Build MaxCut cost Hamiltonian H_C = (1/2) sum_{(i,j)} (I - Z_i Z_j)."""
    pauli_list = []
    for i, j in edges:
        id_str = "I" * num_nodes
        pauli_list.append((id_str, 0.5))
        zz = ["I"] * num_nodes
        zz[num_nodes - 1 - i] = "Z"
        zz[num_nodes - 1 - j] = "Z"
        pauli_list.append(("".join(zz), -0.5))
    return SparsePauliOp.from_list(pauli_list).simplify()


# =============================================================================
# SECTION 2: Annealing Schedules
# =============================================================================

def linear_schedule(t, T):
    """Linear schedule: s(t) = t/T."""
    return t / T


def sigmoid_schedule(t, T, kappa=4.0):
    """Sigmoid schedule: s(t) = 0.5 * [1 + tanh(kappa * (2t/T - 1))]."""
    x = kappa * (2.0 * t / T - 1.0)
    return 0.5 * (1.0 + np.tanh(x))


def polynomial_schedule(t, T, alpha=2.0):
    """Polynomial schedule: s(t) = (t/T)^alpha."""
    return (t / T) ** alpha


# =============================================================================
# SECTION 3: Circuit Construction
# =============================================================================

def compute_schedule_parameters(num_steps, total_time,
                                schedule_fn=linear_schedule,
                                **schedule_kwargs):
    """
    Compute annealing schedule parameters for all Trotter steps.

    Unlike variational algorithms, these parameters are deterministic
    and computed classically -- no quantum resources needed.

    Uses the midpoint rule for better accuracy: s_k = s((k+0.5)*dt, T).

    Args:
        num_steps: Number of Trotter steps P
        total_time: Total annealing time T
        schedule_fn: Annealing schedule function
        **schedule_kwargs: Additional schedule parameters

    Returns:
        gammas: Cost parameters [dt * s_k for each step]
        betas: Mixer parameters [dt * (1 - s_k) for each step]
        schedule_values: Schedule parameter s_k at each step
    """
    dt = total_time / num_steps
    gammas = []
    betas = []
    schedule_values = []

    for k in range(num_steps):
        t_k = (k + 0.5) * dt
        s_k = schedule_fn(t_k, total_time, **schedule_kwargs)
        s_k = max(1e-10, min(1.0 - 1e-10, s_k))

        gammas.append(dt * s_k)
        betas.append(dt * (1.0 - s_k))
        schedule_values.append(s_k)

    return gammas, betas, schedule_values


def build_annealing_circuit(num_nodes, edges, gammas, betas):
    """
    Build the full Trotterized annealing circuit with measurements.

    Each Trotter step k applies:
        U_M(beta_k) * U_C(gamma_k)

    where:
        U_C(gamma) = prod_{(i,j)} exp(-i*gamma*Z_i*Z_j/2)
                   = prod_{(i,j)} CNOT(i,j) RZ(2*gamma, j) CNOT(i,j)

        U_M(beta)  = prod_i exp(-i*beta*X_i) = prod_i RX(2*beta, i)

    Args:
        num_nodes: Number of qubits
        edges: Graph edges
        gammas: Cost parameters (one per step)
        betas: Mixer parameters (one per step)

    Returns:
        QuantumCircuit: The complete circuit with measurements
    """
    num_steps = len(gammas)
    qc = QuantumCircuit(num_nodes, num_nodes)

    # Initialize |+>^n (ground state of H_M)
    for i in range(num_nodes):
        qc.h(i)
    qc.barrier()

    # Trotter steps
    for step in range(num_steps):
        gamma_k = gammas[step]
        beta_k = betas[step]

        # Cost unitary: exp(-i * gamma_k * H_C)
        for i_node, j_node in edges:
            qc.cx(i_node, j_node)
            qc.rz(2 * gamma_k, j_node)
            qc.cx(i_node, j_node)

        # Mixer unitary: exp(-i * beta_k * H_M)
        for i_node in range(num_nodes):
            qc.rx(2 * beta_k, i_node)

        # Add barrier between steps for clarity
        if step < num_steps - 1:
            qc.barrier()

    qc.barrier()

    # Final measurement
    qc.measure(range(num_nodes), range(num_nodes))

    return qc


# =============================================================================
# SECTION 4: Statevector Pre-Validation
# =============================================================================

def prevalidate_with_statevector(num_nodes, edges, gammas, betas):
    """
    Pre-validate the annealing circuit using exact statevector simulation.

    This serves as a reference to compare against noisy hardware results.
    Run this BEFORE submitting to real hardware to verify the schedule
    produces good results.

    Args:
        num_nodes: Number of qubits
        edges: Graph edges
        gammas: Cost parameters
        betas: Mixer parameters

    Returns:
        expected_cost: Exact <H_C> from statevector
        optimal_prob: Probability of sampling the optimal solution
        top_bitstrings: List of (bitstring, probability, cut_value) tuples
    """
    H_C = build_maxcut_hamiltonian(edges, num_nodes)

    # Build circuit without measurements for statevector
    qc = QuantumCircuit(num_nodes)
    for i in range(num_nodes):
        qc.h(i)

    for step in range(len(gammas)):
        for i_node, j_node in edges:
            qc.cx(i_node, j_node)
            qc.rz(2 * gammas[step], j_node)
            qc.cx(i_node, j_node)
        for i_node in range(num_nodes):
            qc.rx(2 * betas[step], i_node)

    state = Statevector(qc)
    expected_cost = state.expectation_value(H_C).real

    probs = state.probabilities_dict()
    top_bitstrings = []
    for bs, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True)[:20]:
        cut = sum(1 for (i, j) in edges if bs[i] != bs[j])
        top_bitstrings.append((bs, float(prob), int(cut)))

    max_cut = max(cut for _, _, cut in top_bitstrings) if top_bitstrings else 0
    optimal_prob = sum(
        prob for _, prob, cut in top_bitstrings if cut == max_cut
    )

    return float(expected_cost), float(optimal_prob), top_bitstrings


# =============================================================================
# SECTION 5: Result Analysis
# =============================================================================

def evaluate_solutions(counts, edges):
    """
    Evaluate MaxCut value for each sampled bitstring.

    Args:
        counts: Dictionary of {bitstring: count} from measurement
        edges: Graph edges

    Returns:
        Dictionary of {bitstring: {'cut': int, 'count': int}}
    """
    results = {}
    for bitstring, count in counts.items():
        cut = sum(1 for (i, j) in edges if bitstring[i] != bitstring[j])
        results[bitstring] = {'cut': cut, 'count': count}
    return results


# =============================================================================
# SECTION 6: Production Execution
# =============================================================================

def run_production():
    print("=" * 70)
    print("Quantum Annealing (Trotterized) - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # Configuration
    # =========================================================================

    # Problem: MaxCut on pentagon + diagonal
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
    num_nodes = 5

    # Annealing parameters
    # On real hardware, keep NUM_STEPS modest (10-30) to limit circuit depth.
    # The total time T controls the adiabaticity: larger T -> closer to
    # ground state, but more susceptible to decoherence.
    NUM_STEPS = 20
    TOTAL_TIME = 3.0
    SCHEDULE = "sigmoid"
    SCHEDULE_KWARGS = {"kappa": 4.0}
    SHOTS = 8192

    # Select schedule function
    schedule_fns = {
        "linear": linear_schedule,
        "sigmoid": sigmoid_schedule,
        "polynomial": polynomial_schedule,
    }
    schedule_fn = schedule_fns[SCHEDULE]

    # Exact MaxCut for reference
    max_cut = max(
        sum(1 for (i, j) in edges
            if format(x, f'0{num_nodes}b')[i] != format(x, f'0{num_nodes}b')[j])
        for x in range(2 ** num_nodes)
    )

    print(f"\n  Graph: {num_nodes} nodes, {len(edges)} edges")
    print(f"  MaxCut: {max_cut}")
    print(f"  Trotter steps: {NUM_STEPS}")
    print(f"  Annealing time: {TOTAL_TIME}")
    print(f"  Schedule: {SCHEDULE} ({SCHEDULE_KWARGS})")
    print(f"  Shots: {SHOTS}")

    # =========================================================================
    # STEP 1: Compute Schedule Parameters
    # =========================================================================

    print("\n--- Step 1: Computing Annealing Schedule ---")

    gammas, betas, schedule_values = compute_schedule_parameters(
        NUM_STEPS, TOTAL_TIME,
        schedule_fn=schedule_fn,
        **SCHEDULE_KWARGS
    )

    print(f"  Computed {NUM_STEPS} parameter pairs (gamma_k, beta_k)")
    print(f"  gamma range: [{min(gammas):.4f}, {max(gammas):.4f}]")
    print(f"  beta range:  [{min(betas):.4f}, {max(betas):.4f}]")

    # =========================================================================
    # STEP 2: Pre-Validate with Statevector
    # =========================================================================

    print("\n--- Step 2: Statevector Pre-Validation ---")

    sv_cost, sv_opt_prob, sv_top = prevalidate_with_statevector(
        num_nodes, edges, gammas, betas
    )

    print(f"  Expected <H_C> (exact): {sv_cost:.4f}")
    print(f"  Approximation ratio:    {sv_cost / max_cut:.4f}")
    print(f"  P(optimal solution):    {sv_opt_prob:.4f}")
    print(f"\n  Top 5 bitstrings (exact):")
    for bs, prob, cut in sv_top[:5]:
        marker = " <-- OPTIMAL" if cut == max_cut else ""
        print(f"    |{bs}> : prob = {prob:.4f}, cut = {cut}{marker}")

    # =========================================================================
    # STEP 3: Build Circuit
    # =========================================================================

    print("\n--- Step 3: Building Annealing Circuit ---")

    qc = build_annealing_circuit(num_nodes, edges, gammas, betas)

    print(f"  Circuit qubits: {qc.num_qubits}")
    print(f"  Circuit depth:  {qc.depth()}")
    print(f"  Gate counts:    {dict(qc.count_ops())}")
    print(f"  Total gates:    {sum(qc.count_ops().values())}")

    # =========================================================================
    # STEP 4: Execute
    # =========================================================================

    print("\n--- Step 4: Execution ---")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    #
    # service = QiskitRuntimeService(
    #     channel="ibm_quantum",
    #     token="YOUR_IBM_QUANTUM_TOKEN"
    # )
    # backend = service.least_busy(simulator=False, min_num_qubits=num_nodes)
    # print(f"  Backend: {backend.name}")
    #
    # # Transpile with high optimization for hardware
    # pm = generate_preset_pass_manager(
    #     optimization_level=3,
    #     backend=backend
    # )
    # transpiled_qc = pm.run(qc)
    # print(f"  Transpiled depth: {transpiled_qc.depth()}")
    # print(f"  Transpiled gates: {dict(transpiled_qc.count_ops())}")
    #
    # # Execute with error mitigation
    # # Option A: Resilience level 1 (Twirled Readout Error Extinction)
    # # Option B: Resilience level 2 (Zero Noise Extrapolation)
    # with Session(service=service, backend=backend) as session:
    #     sampler = SamplerV2(
    #         session=session,
    #         options={
    #             "resilience_level": 1,
    #             "execution": {
    #                 "shots": SHOTS,
    #             },
    #         }
    #     )
    #     job = sampler.run([transpiled_qc])
    #     print(f"  Job ID: {job.job_id()}")
    #     result = job.result()
    #
    # # Extract counts from SamplerV2 result
    # pub_result = result[0]
    # counts = pub_result.data.meas.get_counts()
    # -------------------------------------------------------------------------

    # Local simulator execution
    print("  Running on AerSimulator (local)...")
    simulator = AerSimulator()
    result = simulator.run(qc, shots=SHOTS).result()
    counts = result.get_counts()
    print(f"  Completed: {sum(counts.values())} shots")

    # =========================================================================
    # STEP 5: Analyze Results
    # =========================================================================

    print("\n--- Step 5: Results Analysis ---")

    solutions = evaluate_solutions(counts, edges)
    sorted_solutions = sorted(
        solutions.items(), key=lambda x: x[1]['cut'], reverse=True
    )

    print(f"\n  Top 10 solutions from {SHOTS} shots:")
    for bs, info in sorted_solutions[:10]:
        prob = info['count'] / SHOTS
        marker = " <-- OPTIMAL" if info['cut'] == max_cut else ""
        print(f"    |{bs}> : cut = {info['cut']}, count = {info['count']} "
              f"({prob:.1%}){marker}")

    # Compute aggregate metrics
    expected_cut = sum(
        info['cut'] * info['count'] for _, info in solutions.items()
    ) / SHOTS
    best_sampled_cut = max(info['cut'] for _, info in solutions.items())
    optimal_count = sum(
        info['count'] for _, info in solutions.items()
        if info['cut'] == max_cut
    )

    print(f"\n  Expected cut (sampled):  {expected_cut:.2f}")
    print(f"  Best sampled cut:        {best_sampled_cut}")
    print(f"  Sampling approx ratio:   {expected_cut / max_cut:.4f}")
    print(f"  Optimal solutions found: {optimal_count} / {SHOTS} "
          f"({optimal_count / SHOTS:.1%})")

    # Compare with statevector pre-validation
    print(f"\n  Statevector vs Sampled:")
    print(f"    SV expected <H_C>:  {sv_cost:.4f}")
    print(f"    Sampled <cut>:      {expected_cut:.4f}")
    print(f"    Difference:         {abs(sv_cost - expected_cut):.4f}")

    # =========================================================================
    # STEP 6: Save Results
    # =========================================================================

    output_dir = "quantum/algorithms/08_quantum_annealing_sim/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "Trotterized Quantum Annealing",
        "qiskit_version": "2.4.1",
        "config": {
            "num_steps": NUM_STEPS,
            "total_time": TOTAL_TIME,
            "schedule": SCHEDULE,
            "schedule_kwargs": SCHEDULE_KWARGS,
            "shots": SHOTS,
        },
        "problem": {
            "type": "MaxCut",
            "num_nodes": num_nodes,
            "edges": edges,
            "exact_maxcut": max_cut,
        },
        "schedule_parameters": {
            "gammas": [float(g) for g in gammas],
            "betas": [float(b) for b in betas],
            "schedule_values": [float(s) for s in schedule_values],
        },
        "statevector_validation": {
            "expected_cost": sv_cost,
            "approx_ratio": sv_cost / max_cut,
            "optimal_probability": sv_opt_prob,
        },
        "sampled_results": {
            "expected_cut": float(expected_cut),
            "best_sampled_cut": int(best_sampled_cut),
            "sampling_ratio": float(expected_cut / max_cut),
            "optimal_count": int(optimal_count),
            "optimal_fraction": float(optimal_count / SHOTS),
        },
        "circuit_info": {
            "depth": qc.depth(),
            "gate_counts": dict(qc.count_ops()),
            "total_gates": sum(qc.count_ops().values()),
        },
        "top_solutions": [
            {
                "bitstring": bs,
                "cut": info['cut'],
                "count": info['count'],
                "probability": info['count'] / SHOTS,
            }
            for bs, info in sorted_solutions[:20]
        ],
    }

    filepath = os.path.join(output_dir, "quantum_annealing_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"\n  Results saved to {filepath}")

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print(f"""
    Trotterized Quantum Annealing on IBM Hardware:

    1. Circuit Depth Budget:
       - {NUM_STEPS} Trotter steps -> circuit depth {qc.depth()}
       - Each step: {len(edges)} CNOT pairs + {num_nodes} RX gates
       - Total 2-qubit gates: ~{2 * len(edges) * NUM_STEPS}
       - IBM backends: useful depth ~100-300 (after transpilation)
       - Reduce NUM_STEPS if transpiled depth exceeds backend limit

    2. Annealing Time vs. Decoherence:
       - Larger T -> better adiabatic fidelity
       - But larger T -> larger gate angles -> more accumulated gate error
       - Optimal T balances adiabatic error and hardware noise
       - Start with T = 2-5 and scan

    3. Schedule Selection:
       - Sigmoid often outperforms linear for structured problems
       - The minimum gap location determines the optimal schedule
       - For unknown gap structure, start with linear

    4. Error Mitigation:
       - Resilience level 1 (TREX): corrects readout errors, minimal overhead
       - Resilience level 2 (ZNE): extrapolates to zero noise, 3x shot cost
       - For deep annealing circuits, ZNE is recommended

    5. Advantages over QAOA on Hardware:
       - No classical optimization loop (no repeated circuit executions)
       - Parameters computed classically in O(P) time
       - Single circuit submission (lower latency)
       - Disadvantage: fixed schedule may be suboptimal vs. QAOA at same depth

    6. Scaling Considerations:
       - For n > 20 qubits: increase P proportionally
       - For dense graphs: circuit depth per step grows as O(|E|)
       - Consider graph coloring for parallel ZZ gate execution
    """)


if __name__ == "__main__":
    run_production()
