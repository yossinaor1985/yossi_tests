"""
PQC & Ansatz Design - IBM Production-Ready Implementation
===========================================================

Production guide for selecting and transpiling ansatze for IBM hardware.

Qiskit Version: 2.4.1

Key production concerns:
    - Transpiled circuit depth must fit within T1/T2 coherence times
    - Native gate set: ECR, RZ, SX, X (IBM Eagle/Heron processors)
    - Qubit connectivity: heavy-hex topology (not all-to-all)
    - Entanglement pattern must match backend coupling map
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2, RealAmplitudes, TwoLocal
from qiskit.quantum_info import Statevector, SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2 as AerEstimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Session


def analyze_transpiled_ansatz(ansatz, backend=None):
    """
    Analyze how an ansatz looks after transpilation for IBM hardware.

    Key metrics for production:
        - Transpiled depth vs original depth
        - Number of ECR (2-qubit) gates (dominant error source)
        - Physical qubit layout
        - Estimated error per circuit execution

    Args:
        ansatz: The parameterized circuit
        backend: IBM backend (or None for generic analysis)

    Returns:
        dict: Transpilation analysis
    """
    if backend is not None:
        pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
        transpiled = pm.run(ansatz)
    else:
        # Use optimization without specific backend
        transpiled = ansatz

    ops = dict(transpiled.count_ops())
    return {
        'original_depth': ansatz.depth(),
        'transpiled_depth': transpiled.depth(),
        'original_gates': sum(dict(ansatz.count_ops()).values()),
        'transpiled_gates': sum(ops.values()),
        'two_qubit_gates': sum(v for k, v in ops.items()
                               if k in ['ecr', 'cx', 'cz']),
        'ops': ops,
    }


def select_ansatz_for_problem(problem_type, num_qubits, hardware_constraints=None):
    """
    Production ansatz selection logic.

    Selects the best ansatz based on:
        1. Problem type (optimization, chemistry, ML)
        2. Number of qubits
        3. Hardware constraints (max depth, connectivity)

    Args:
        problem_type: "optimization", "chemistry", "classification", "regression"
        num_qubits: Number of qubits
        hardware_constraints: Dict with 'max_depth', 'connectivity'

    Returns:
        QuantumCircuit: Selected ansatz
        str: Name of the selected ansatz
        str: Reason for selection
    """
    max_depth = (hardware_constraints or {}).get('max_depth', 100)

    if problem_type == "optimization":
        # For optimization: EfficientSU2 with moderate depth
        reps = min(2, max_depth // (3 * num_qubits))
        reps = max(1, reps)
        ansatz = EfficientSU2(num_qubits, reps=reps, entanglement='linear')
        name = f"EfficientSU2(reps={reps}, linear)"
        reason = "Linear entanglement matches heavy-hex; SU(2) rotations are expressive"

    elif problem_type == "chemistry":
        # For chemistry: deeper circuit with full connectivity
        reps = min(3, max_depth // (num_qubits * num_qubits))
        reps = max(1, reps)
        ansatz = TwoLocal(num_qubits, ['ry', 'rz'], 'cx',
                         entanglement='full', reps=reps)
        name = f"TwoLocal(ry+rz, cx, full, reps={reps})"
        reason = "Full entanglement captures electron correlations"

    elif problem_type in ("classification", "regression"):
        # For ML: moderate expressibility, avoid barren plateaus
        reps = min(2, max_depth // (2 * num_qubits))
        reps = max(1, reps)
        ansatz = RealAmplitudes(num_qubits, reps=reps, entanglement='circular')
        name = f"RealAmplitudes(reps={reps}, circular)"
        reason = "Real amplitudes sufficient for classification; circular avoids edge effects"

    else:
        ansatz = EfficientSU2(num_qubits, reps=1)
        name = "EfficientSU2(reps=1, default)"
        reason = "Safe default for unknown problem type"

    return ansatz, name, reason


def run_production():
    print("=" * 70)
    print("PQC & Ansatz Design - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Ansatz Selection for Different Problem Types
    # =========================================================================

    print("\n--- Step 1: Problem-Driven Ansatz Selection ---")

    num_qubits = 4
    constraints = {'max_depth': 50, 'connectivity': 'linear'}

    for problem_type in ['optimization', 'chemistry', 'classification']:
        ansatz, name, reason = select_ansatz_for_problem(
            problem_type, num_qubits, constraints
        )
        print(f"\n  Problem: {problem_type}")
        print(f"  Selected: {name}")
        print(f"  Reason: {reason}")
        print(f"  Parameters: {ansatz.num_parameters}, Depth: {ansatz.depth()}")

    # =========================================================================
    # STEP 2: Transpilation Analysis
    # =========================================================================

    print("\n--- Step 2: Transpilation Analysis ---")

    # Compare ansatze before and after transpilation
    test_ansatze = {
        'EfficientSU2 (linear)': EfficientSU2(num_qubits, reps=2, entanglement='linear'),
        'EfficientSU2 (full)': EfficientSU2(num_qubits, reps=2, entanglement='full'),
        'RealAmplitudes': RealAmplitudes(num_qubits, reps=2),
        'TwoLocal ry-cz': TwoLocal(num_qubits, 'ry', 'cz', reps=2),
    }

    for name, ansatz in test_ansatze.items():
        analysis = analyze_transpiled_ansatz(ansatz)
        print(f"\n  {name}:")
        print(f"    Original depth: {analysis['original_depth']}")
        print(f"    Original gates: {analysis['original_gates']}")

    # =========================================================================
    # STEP 3: VQE Benchmark with Different Ansatze
    # =========================================================================

    print("\n--- Step 3: VQE Benchmark ---")

    # Simple 4-qubit Hamiltonian for benchmarking
    hamiltonian = SparsePauliOp.from_list([
        ("IIII", -0.5),
        ("ZZII", 0.3),
        ("IIZZ", 0.3),
        ("ZIZI", -0.2),
        ("XXII", 0.1),
        ("IIXX", 0.1),
    ])

    exact_energy = min(np.linalg.eigvalsh(hamiltonian.to_matrix()))
    print(f"\n  Exact ground-state energy: {exact_energy:.6f}")

    estimator = AerEstimator()

    for name, ansatz in test_ansatze.items():
        vqe = VQE(
            estimator=estimator,
            ansatz=ansatz,
            optimizer=COBYLA(maxiter=200),
        )
        vqe.initial_point = np.zeros(ansatz.num_parameters)

        result = vqe.compute_minimum_eigenvalue(hamiltonian)
        error = abs(result.eigenvalue - exact_energy)
        print(f"\n  {name}:")
        print(f"    Energy: {result.eigenvalue:.6f}")
        print(f"    Error:  {error:.2e}")
        print(f"    Evals:  {result.cost_function_evals}")

    # =========================================================================
    # STEP 4: Save Results
    # =========================================================================

    output_dir = "quantum/algorithms/09_PQC_ansatz_design/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "analysis": "PQC Ansatz Design",
        "qiskit_version": "2.4.1",
        "num_qubits": num_qubits,
        "ansatz_comparison": {
            name: {
                "parameters": ansatz.num_parameters,
                "depth": ansatz.depth(),
            }
            for name, ansatz in test_ansatze.items()
        },
    }

    filepath = os.path.join(output_dir, "pqc_analysis.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"\nResults saved to {filepath}")

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION ANSATZ GUIDELINES")
    print("=" * 70)
    print("""
    IBM Hardware Ansatz Selection:

    1. Gate Budget:
       - IBM Eagle (127 qubits): ~100-200 useful 2-qubit gates
       - IBM Heron (133 qubits): ~200-400 useful 2-qubit gates
       - Rule: Keep total ECR gates < T2/gate_time

    2. Entanglement Pattern:
       - Use 'linear' to match nearest-neighbor connectivity
       - Avoid 'full' for >6 qubits (requires too many SWAPs)
       - 'circular' is a good compromise

    3. Depth Scaling:
       - reps=1: Good for NISQ (depth ~2n)
       - reps=2: Better expressibility (depth ~4n)
       - reps=3+: Only for high-fidelity devices

    4. Barren Plateau Avoidance:
       - Initialize parameters near zero
       - Use problem-specific ansatze when possible
       - Keep reps <= log2(n) as a rule of thumb

    5. Transpilation:
       - Always use optimization_level=3
       - Check transpiled depth fits coherence time
       - Use backend.target for accurate gate durations
    """)


if __name__ == "__main__":
    run_production()
