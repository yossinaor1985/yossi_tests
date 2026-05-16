"""
FALQON - IBM Production-Ready Implementation
==============================================

Production FALQON for MaxCut on IBM Quantum hardware.

Qiskit Version: 2.4.1

Production Considerations:
    - FALQON requires measuring <i[H_C, H_M]> between layers
    - On real hardware, this is done via mid-circuit measurement
      or by pre-computing beta values on a simulator
    - The growing circuit depth is the main limitation on NISQ devices
    - Hybrid approach: use simulator for feedback, hardware for final state
"""

import json
import os
from datetime import datetime

import numpy as np
from scipy.linalg import expm
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session


def build_maxcut_hamiltonian(edges, num_nodes):
    """Build MaxCut cost Hamiltonian."""
    pauli_list = []
    for i, j in edges:
        id_str = "I" * num_nodes
        pauli_list.append((id_str, 0.5))
        zz = ["I"] * num_nodes
        zz[num_nodes - 1 - i] = "Z"
        zz[num_nodes - 1 - j] = "Z"
        pauli_list.append(("".join(zz), -0.5))
    return SparsePauliOp.from_list(pauli_list).simplify()


def build_mixer_hamiltonian(num_nodes):
    """Build mixer H_M = sum_i X_i."""
    pauli_list = []
    for i in range(num_nodes):
        x = ["I"] * num_nodes
        x[num_nodes - 1 - i] = "X"
        pauli_list.append(("".join(x), 1.0))
    return SparsePauliOp.from_list(pauli_list)


def precompute_falqon_parameters(edges, num_nodes, num_layers, dt_gamma, dt_beta):
    """
    Pre-compute FALQON beta parameters using statevector simulation.

    Production strategy: Run FALQON on a classical simulator to determine
    the feedback parameters, then construct the full circuit for execution
    on real hardware. This avoids mid-circuit measurements.

    This is valid because:
    - For small instances (n <= ~25), classical simulation is feasible
    - The computed beta values are deterministic (no randomness)
    - The final circuit with known parameters can then be executed on hardware
      to sample solutions with real quantum effects

    Args:
        edges: Graph edges
        num_nodes: Number of qubits
        num_layers: Number of FALQON layers
        dt_gamma: Cost step size
        dt_beta: Mixer step size

    Returns:
        betas: List of pre-computed mixer parameters
        gammas: List of cost parameters (all equal to dt_gamma)
        cost_history: Cost values at each layer
    """
    H_C = build_maxcut_hamiltonian(edges, num_nodes)
    H_M = build_mixer_hamiltonian(num_nodes)

    HC_mat = H_C.to_matrix()
    HM_mat = H_M.to_matrix()

    # Commutator: i[H_C, H_M]
    comm_mat = 1j * (HC_mat @ HM_mat - HM_mat @ HC_mat)
    comm_op = SparsePauliOp.from_operator(comm_mat)

    # Initialize
    n = 2**num_nodes
    qc = QuantumCircuit(num_nodes)
    for i in range(num_nodes):
        qc.h(i)
    state = Statevector(qc)

    betas = []
    gammas = []
    cost_history = [state.expectation_value(H_C).real]

    for k in range(num_layers):
        # Cost unitary
        U_C = expm(-1j * dt_gamma * HC_mat)
        state_prime = Statevector(U_C @ state.data)

        # Feedback measurement
        a_k = state_prime.expectation_value(comm_op).real
        beta_k = -dt_beta * a_k

        # Mixer unitary
        U_M = expm(-1j * beta_k * HM_mat)
        state = Statevector(U_M @ state_prime.data)

        betas.append(beta_k)
        gammas.append(dt_gamma)
        cost_history.append(state.expectation_value(H_C).real)

    return betas, gammas, cost_history


def build_falqon_circuit(num_nodes, edges, gammas, betas):
    """
    Build the full FALQON circuit with pre-computed parameters.

    This circuit can be transpiled and executed on real hardware.

    Args:
        num_nodes: Number of qubits
        edges: Graph edges
        gammas: Cost unitary parameters (one per layer)
        betas: Mixer parameters (pre-computed via feedback law)

    Returns:
        QuantumCircuit: The complete FALQON circuit with measurements
    """
    qc = QuantumCircuit(num_nodes, num_nodes)

    # Initialize in |+>^n
    for i in range(num_nodes):
        qc.h(i)
    qc.barrier()

    # Apply FALQON layers
    for layer, (gamma, beta) in enumerate(zip(gammas, betas)):
        # Cost unitary: exp(-i * gamma * H_C)
        # For MaxCut: ZZ interactions on each edge
        for i, j in edges:
            qc.cx(i, j)
            qc.rz(2 * gamma, j)
            qc.cx(i, j)
        qc.barrier()

        # Mixer unitary: exp(-i * beta * H_M)
        # H_M = sum_i X_i -> product of R_X(2*beta) on each qubit
        for i in range(num_nodes):
            qc.rx(2 * beta, i)
        qc.barrier()

    # Measure
    qc.measure(range(num_nodes), range(num_nodes))
    return qc


def evaluate_solutions(counts, edges):
    """Evaluate MaxCut for measurement results."""
    results = {}
    for bitstring, count in counts.items():
        cut = sum(1 for (i, j) in edges if bitstring[i] != bitstring[j])
        results[bitstring] = {'cut': cut, 'count': count}
    return results


def run_production():
    print("=" * 70)
    print("FALQON - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # Configuration
    # =========================================================================

    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2)]
    num_nodes = 5
    NUM_LAYERS = 30
    DT_GAMMA = 0.1
    DT_BETA = 0.5
    SHOTS = 8192

    # Exact MaxCut
    max_cut = max(
        sum(1 for (i, j) in edges if format(x, f'0{num_nodes}b')[i] != format(x, f'0{num_nodes}b')[j])
        for x in range(2**num_nodes)
    )

    print(f"\nGraph: {num_nodes} nodes, {len(edges)} edges")
    print(f"MaxCut: {max_cut}")
    print(f"Layers: {NUM_LAYERS}, dt_gamma={DT_GAMMA}, dt_beta={DT_BETA}")

    # =========================================================================
    # STEP 1: Pre-compute Parameters
    # =========================================================================

    print("\n--- Step 1: Pre-computing FALQON Parameters (simulator) ---")

    betas, gammas, cost_history = precompute_falqon_parameters(
        edges, num_nodes, NUM_LAYERS, DT_GAMMA, DT_BETA
    )

    print(f"Pre-computed {len(betas)} beta parameters")
    print(f"Final expected cost: {cost_history[-1]:.4f}")
    print(f"Approximation ratio: {cost_history[-1]/max_cut:.4f}")

    # =========================================================================
    # STEP 2: Build Circuit
    # =========================================================================

    print("\n--- Step 2: Building FALQON Circuit ---")

    qc = build_falqon_circuit(num_nodes, edges, gammas, betas)
    print(f"Circuit depth: {qc.depth()}")
    print(f"Gate count: {dict(qc.count_ops())}")
    print(f"Total gates: {sum(qc.count_ops().values())}")

    # =========================================================================
    # STEP 3: Execute on Simulator (or Hardware)
    # =========================================================================

    print("\n--- Step 3: Execution ---")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR_TOKEN")
    # backend = service.least_busy(simulator=False, min_num_qubits=num_nodes)
    #
    # pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
    # transpiled_qc = pm.run(qc)
    # print(f"Transpiled depth: {transpiled_qc.depth()}")
    #
    # with Session(service=service, backend=backend) as session:
    #     sampler = SamplerV2(session=session)
    #     job = sampler.run([transpiled_qc], shots=SHOTS)
    #     result = job.result()
    # -------------------------------------------------------------------------

    simulator = AerSimulator()
    result = simulator.run(qc, shots=SHOTS).result()
    counts = result.get_counts()

    # =========================================================================
    # STEP 4: Analyze Results
    # =========================================================================

    print("\n--- Step 4: Results ---")

    solutions = evaluate_solutions(counts, edges)
    sorted_solutions = sorted(solutions.items(), key=lambda x: x[1]['cut'], reverse=True)

    print(f"\nTop 10 solutions from {SHOTS} shots:")
    for bs, info in sorted_solutions[:10]:
        prob = info['count'] / SHOTS
        marker = " <-- OPTIMAL" if info['cut'] == max_cut else ""
        print(f"  |{bs}> : cut = {info['cut']}, count = {info['count']} "
              f"({prob:.1%}){marker}")

    # Expected cut value from sampling
    expected_cut = sum(info['cut'] * info['count'] for _, info in solutions.items()) / SHOTS
    best_sampled_cut = max(info['cut'] for _, info in solutions.items())

    print(f"\n  Expected cut (from sampling): {expected_cut:.2f}")
    print(f"  Best sampled cut: {best_sampled_cut}")
    print(f"  Sampling ratio: {expected_cut/max_cut:.4f}")

    # =========================================================================
    # STEP 5: Save Results
    # =========================================================================

    output_dir = "quantum/algorithms/06_FALQON/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "FALQON",
        "qiskit_version": "2.4.1",
        "config": {
            "num_layers": NUM_LAYERS,
            "dt_gamma": DT_GAMMA,
            "dt_beta": DT_BETA,
            "shots": SHOTS,
        },
        "problem": {
            "num_nodes": num_nodes,
            "edges": edges,
            "exact_maxcut": max_cut,
        },
        "results": {
            "final_cost": float(cost_history[-1]),
            "approx_ratio": float(cost_history[-1] / max_cut),
            "expected_cut_sampling": float(expected_cut),
            "best_sampled_cut": int(best_sampled_cut),
            "circuit_depth": qc.depth(),
        },
        "precomputed_betas": [float(b) for b in betas],
    }

    filepath = os.path.join(output_dir, "falqon_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"\nResults saved to {filepath}")

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print(f"""
    FALQON on IBM Hardware:

    1. Pre-computation Strategy:
       - Compute beta parameters on classical simulator
       - Build full circuit with fixed parameters
       - Execute on quantum hardware for sampling
       - Valid for n <= ~25 qubits (classical sim feasible)

    2. Circuit Depth Concern:
       - {NUM_LAYERS} layers -> depth {qc.depth()}
       - IBM backends: useful depth ~100-300 for 2-qubit gates
       - May need to reduce layers on noisy hardware

    3. Depth Budget:
       - Each FALQON layer: ~{len(edges)} CNOT + {num_nodes} RX gates
       - Total 2-qubit gates: ~{len(edges) * NUM_LAYERS}
       - Transpiled: may increase due to routing

    4. When to Use FALQON over QAOA:
       - When classical optimization is the bottleneck
       - When monotonic convergence is needed
       - When circuit depth is not the limiting factor
       - Best combined with error mitigation (ZNE, PEC)
    """)


if __name__ == "__main__":
    run_production()
