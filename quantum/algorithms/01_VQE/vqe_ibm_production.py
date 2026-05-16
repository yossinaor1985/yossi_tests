"""
Variational Quantum Eigensolver (VQE) - IBM Production-Ready Implementation
=============================================================================

This script demonstrates a production-quality VQE workflow designed for
execution on real IBM Quantum hardware via Qiskit Runtime.

Qiskit Version: 2.4.1

Key differences from the local simulator version:
    1. Uses QiskitRuntimeService to connect to IBM Quantum backends
    2. Transpiles circuits for the target backend's topology & gate set
    3. Uses Sessions for efficient job batching
    4. Includes error mitigation (resilience level)
    5. Saves results to disk for reproducibility
    6. Handles real-world concerns: timeouts, retries, backend selection

NOTE: This code is NOT actually deployed. The IBM token and backend
selection are configured but the execution is commented out by default.
To run on real hardware:
    1. Set your IBM Quantum API token
    2. Uncomment the real-backend execution section
    3. Ensure you have IBM Quantum access (free or premium plan)

Theoretical Background:
    See explanation_physicist.md for the full mathematical framework.
    This implementation applies the same VQE algorithm but accounts for
    hardware constraints: limited qubit connectivity, gate errors,
    readout errors, and decoherence.
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SPSA

# =============================================================================
# IBM Runtime imports - these connect to real quantum hardware
# =============================================================================
# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Session
# from qiskit_ibm_runtime.options import EstimatorOptions


def build_hamiltonian():
    """
    Construct the H2 molecule Hamiltonian as a SparsePauliOp.

    This is the same Hamiltonian used in the local simulator version.
    On real hardware, the measurement of each Pauli term involves:
        1. Basis rotation gates (H for X-basis, S^dag H for Y-basis)
        2. Computational basis measurement
        3. Classical post-processing to compute <P_i>
        4. Weighted sum: <H> = sum_i alpha_i <P_i>

    Returns:
        SparsePauliOp: The 2-qubit H2 Hamiltonian
    """
    return SparsePauliOp.from_list([
        ("II", -0.8105),
        ("ZI",  0.1721),
        ("IZ", -0.2257),
        ("ZZ",  0.1721),
        ("XX",  0.0454),
        ("YY",  0.0454),
    ])


def build_ansatz(num_qubits=2, reps=2):
    """
    Build the parameterized ansatz circuit.

    For production use, we increase the number of repetitions (reps=2)
    compared to the local version (reps=1) to improve expressibility.
    More layers = more parameters = better approximation capability,
    but also deeper circuits that accumulate more hardware errors.

    Trade-off (see explanation_physicist.md, Section 3.1):
        - Deeper circuits: better variational flexibility
        - But: more noise, risk of barren plateaus
        - Production choice: reps=2 is a good balance for 2 qubits

    Args:
        num_qubits: Number of qubits in the circuit
        reps: Number of ansatz repetition layers

    Returns:
        QuantumCircuit: The parameterized ansatz
    """
    ansatz = EfficientSU2(
        num_qubits=num_qubits,
        reps=reps,
        entanglement="linear",
    )
    return ansatz


def transpile_for_backend(ansatz, backend):
    """
    Transpile the ansatz circuit for the target backend.

    Production transpilation involves:
        1. Mapping logical qubits to physical qubits (Layout)
        2. Routing gates through the backend's connectivity (Routing)
        3. Decomposing gates into the backend's native gate set
        4. Optimizing the circuit (gate cancellation, commutation)

    Qiskit uses VF2Layout for initial placement and SabreSwap for routing.
    optimization_level=3 enables the most aggressive optimizations.

    Args:
        ansatz: The parameterized quantum circuit
        backend: The IBM Quantum backend object

    Returns:
        QuantumCircuit: Transpiled circuit ready for the backend
    """
    pass_manager = generate_preset_pass_manager(
        optimization_level=3,   # Maximum optimization
        backend=backend
    )
    transpiled = pass_manager.run(ansatz)
    return transpiled


def configure_estimator_options():
    """
    Configure the Estimator with error mitigation for production use.

    Error mitigation levels (see mitigation/ folder for details):
        Level 0: No mitigation (raw results)
        Level 1: TREX - Twirled Readout Error eXtinction
                 Mitigates measurement (readout) errors
        Level 2: TREX + ZNE - Zero Noise Extrapolation
                 Also mitigates gate errors by extrapolating to zero noise

    For VQE, Level 1 is typically sufficient because:
        - VQE is variational: systematic errors shift the landscape but
          the optimizer can still find the minimum
        - Level 2 (ZNE) adds significant overhead (3-5x more circuits)
        - But for final production results, Level 2 is recommended

    Returns:
        dict: Configuration dictionary for EstimatorOptions
    """
    options_config = {
        "resilience_level": 1,              # TREX for readout mitigation
        "default_shots": 8192,              # Shots per circuit evaluation
        "dynamical_decoupling": {
            "enable": True,                 # Insert DD sequences on idle qubits
            "sequence_type": "XpXm",        # X - delay - X^dag sequence
        },
        "twirling": {
            "enable_gates": True,           # Pauli twirling on 2-qubit gates
            "num_randomizations": 32,       # Number of random twirls
        },
    }
    return options_config


def save_results(result, hamiltonian, config, output_dir):
    """
    Save VQE results to disk for reproducibility.

    Production practice: always save raw results, metadata, and configuration
    so experiments can be reproduced and audited later.

    Args:
        result: VQE result object
        hamiltonian: The Hamiltonian operator
        config: Run configuration dictionary
        output_dir: Directory to save results
    """
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "VQE",
        "qiskit_version": "2.4.1",
        "hamiltonian": {
            "pauli_terms": [(str(label), float(coeff.real))
                           for label, coeff in zip(hamiltonian.paulis.to_labels(),
                                                    hamiltonian.coeffs)],
            "num_qubits": int(hamiltonian.num_qubits),
        },
        "config": config,
        "results": {
            "ground_state_energy": float(result.eigenvalue.real)
                                  if hasattr(result.eigenvalue, 'real')
                                  else float(result.eigenvalue),
            "optimal_parameters": {str(k): float(v)
                                   for k, v in result.optimal_parameters.items()},
            "num_evaluations": int(result.cost_function_evals),
        },
    }

    filepath = os.path.join(output_dir, "vqe_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"Results saved to {filepath}")


def run_vqe_production():
    """
    Full production VQE pipeline.

    This function demonstrates the complete workflow for running VQE
    on IBM Quantum hardware, including:
        1. Service initialization and backend selection
        2. Hamiltonian and ansatz construction
        3. Circuit transpilation
        4. Estimator configuration with error mitigation
        5. VQE execution with SPSA optimizer
        6. Result analysis and saving
    """
    print("=" * 70)
    print("VQE - Production IBM Quantum Implementation")
    print("=" * 70)

    # =========================================================================
    # STEP 1: IBM Quantum Service Connection
    # =========================================================================
    # In production, you authenticate with your IBM Quantum API token.
    # The service provides access to real quantum hardware.
    #
    # To get a token:
    #   1. Create an account at https://quantum.ibm.com
    #   2. Copy your API token from the dashboard
    #   3. Save it: QiskitRuntimeService.save_account(channel="ibm_quantum",
    #                                                  token="YOUR_TOKEN")
    # =========================================================================

    print("\n--- Step 1: IBM Quantum Service ---")
    print("NOTE: Using local simulation for demonstration.")
    print("To run on real hardware, uncomment the IBM Runtime section below.\n")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE EXECUTION:
    # -------------------------------------------------------------------------
    # service = QiskitRuntimeService(
    #     channel="ibm_quantum",
    #     token="YOUR_IBM_QUANTUM_API_TOKEN"  # Replace with your token
    # )
    #
    # # Select the least busy backend with >= 2 qubits
    # backend = service.least_busy(
    #     simulator=False,
    #     min_num_qubits=2,
    #     operational=True
    # )
    # print(f"Selected backend: {backend.name}")
    # print(f"Number of qubits: {backend.num_qubits}")
    # print(f"Processor type: {backend.processor_type}")
    # -------------------------------------------------------------------------

    # =========================================================================
    # STEP 2: Build Hamiltonian and Ansatz
    # =========================================================================

    print("--- Step 2: Hamiltonian and Ansatz ---")

    hamiltonian = build_hamiltonian()
    ansatz = build_ansatz(num_qubits=2, reps=2)

    print(f"Hamiltonian: {len(hamiltonian)} Pauli terms")
    print(f"Ansatz: EfficientSU2, {ansatz.num_parameters} parameters")

    # =========================================================================
    # STEP 3: Transpilation (for real backend)
    # =========================================================================
    # On real hardware, the circuit must be compiled for:
    #   - The backend's native gate set (e.g., ECR, RZ, SX, X)
    #   - The backend's qubit connectivity (coupling map)
    #   - Minimizing circuit depth to reduce decoherence errors
    #
    # For local simulation, we skip transpilation as the simulator
    # supports all gates natively.
    # =========================================================================

    print("\n--- Step 3: Transpilation ---")
    print("Transpilation would be performed for real hardware.")
    print("Backend native gates: ECR, RZ, SX, X (typical IBM backends)")

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # transpiled_ansatz = transpile_for_backend(ansatz, backend)
    # print(f"Original depth: {ansatz.depth()}")
    # print(f"Transpiled depth: {transpiled_ansatz.depth()}")
    # print(f"Transpiled gate count: {dict(transpiled_ansatz.count_ops())}")
    # -------------------------------------------------------------------------

    # =========================================================================
    # STEP 4: Configure Estimator with Error Mitigation
    # =========================================================================

    print("\n--- Step 4: Error Mitigation Configuration ---")

    mitigation_config = configure_estimator_options()
    print(f"Resilience level: {mitigation_config['resilience_level']}")
    print(f"Shots per evaluation: {mitigation_config['default_shots']}")
    print(f"Dynamical decoupling: {mitigation_config['dynamical_decoupling']['enable']}")
    print(f"Pauli twirling: {mitigation_config['twirling']['enable_gates']}")

    # =========================================================================
    # STEP 5: Run VQE
    # =========================================================================
    # For production, we use SPSA (Simultaneous Perturbation Stochastic
    # Approximation) as the optimizer because:
    #
    #   1. It only requires 2 circuit evaluations per iteration
    #      (regardless of the number of parameters)
    #   2. It's designed for noisy cost functions
    #   3. It handles stochastic gradient estimation naturally
    #
    # See explanation_physicist.md, Section 4.1
    #
    # SPSA hyperparameters:
    #   - maxiter: max optimization steps
    #   - learning_rate / perturbation: step size schedules
    #     (auto-calibrated by default in Qiskit)
    # =========================================================================

    print("\n--- Step 5: Running VQE ---")

    # For demonstration, use Aer simulator
    from qiskit_aer.primitives import EstimatorV2 as AerEstimator
    estimator = AerEstimator()

    # -------------------------------------------------------------------------
    # UNCOMMENT FOR REAL HARDWARE:
    # with Session(service=service, backend=backend) as session:
    #     estimator = EstimatorV2(session=session)
    #
    #     # Apply error mitigation options
    #     estimator.options.resilience_level = mitigation_config["resilience_level"]
    #     estimator.options.default_shots = mitigation_config["default_shots"]
    #     estimator.options.dynamical_decoupling.enable = True
    #     estimator.options.dynamical_decoupling.sequence_type = "XpXm"
    #     estimator.options.twirling.enable_gates = True
    #     estimator.options.twirling.num_randomizations = 32
    # -------------------------------------------------------------------------

    energy_history = []
    param_history = []

    def callback(eval_count, parameters, value, metadata):
        """Track optimization progress."""
        energy_history.append(value)
        param_history.append(parameters.copy())
        if eval_count % 20 == 0:
            print(f"  Eval {eval_count:4d}: E = {value:.6f} Ha")

    # SPSA optimizer for noisy environments
    optimizer = SPSA(
        maxiter=300,        # More iterations for noisy optimization
    )

    vqe = VQE(
        estimator=estimator,
        ansatz=ansatz,
        optimizer=optimizer,
        callback=callback,
    )

    # Initialize near zero for reproducibility
    initial_point = np.random.default_rng(42).uniform(-0.1, 0.1, ansatz.num_parameters)
    vqe.initial_point = initial_point

    print(f"Optimizer: SPSA (stochastic, 2 evals/iteration)")
    print(f"Max iterations: 300")
    print(f"Initial parameters: random near zero (seed=42)")
    print(f"\nOptimizing...\n")

    result = vqe.compute_minimum_eigenvalue(hamiltonian)

    # =========================================================================
    # STEP 6: Results Analysis
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION RESULTS")
    print("=" * 70)

    exact_energy = min(np.linalg.eigvalsh(hamiltonian.to_matrix()))

    print(f"\nVQE ground-state energy:  {result.eigenvalue:.8f} Ha")
    print(f"Exact ground-state energy: {exact_energy:.8f} Ha")
    print(f"Absolute error:            {abs(result.eigenvalue - exact_energy):.2e} Ha")
    print(f"Relative error:            {abs(result.eigenvalue - exact_energy) / abs(exact_energy) * 100:.4f}%")

    chemical_accuracy = 1.6e-3  # 1 kcal/mol in Hartree
    if abs(result.eigenvalue - exact_energy) < chemical_accuracy:
        print(f"\nChemical accuracy ACHIEVED (error < {chemical_accuracy} Ha)")
    else:
        print(f"\nChemical accuracy NOT achieved (error >= {chemical_accuracy} Ha)")
        print("On real hardware, consider: more shots, better ansatz, or error mitigation")

    # =========================================================================
    # STEP 7: Save Results
    # =========================================================================

    config = {
        "backend": "aer_simulator (demo)",
        "optimizer": "SPSA",
        "max_iterations": 300,
        "ansatz": "EfficientSU2",
        "ansatz_reps": 2,
        "num_parameters": ansatz.num_parameters,
        "mitigation": mitigation_config,
        "initial_point_seed": 42,
    }

    save_results(
        result=result,
        hamiltonian=hamiltonian,
        config=config,
        output_dir="quantum/algorithms/01_VQE/results"
    )

    # =========================================================================
    # STEP 8: Production Checklist Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION DEPLOYMENT CHECKLIST")
    print("=" * 70)
    print("""
    Before running on real IBM Quantum hardware:

    [ ] 1. Set IBM Quantum API token
           QiskitRuntimeService.save_account(
               channel="ibm_quantum", token="YOUR_TOKEN"
           )

    [ ] 2. Select appropriate backend
           - Check qubit count, connectivity, error rates
           - Use service.least_busy() or specify by name

    [ ] 3. Transpile for target backend
           - optimization_level=3 for best gate reduction
           - Check transpiled circuit depth vs T1/T2 times

    [ ] 4. Configure error mitigation
           - Minimum: resilience_level=1 (TREX)
           - Recommended: resilience_level=2 (TREX + ZNE)
           - Add dynamical decoupling and Pauli twirling

    [ ] 5. Set appropriate shot count
           - More shots = less statistical noise
           - Typical: 4096-32768 per circuit evaluation

    [ ] 6. Use Sessions for efficiency
           - Groups related jobs on the same backend
           - Reduces queue wait times

    [ ] 7. Save all results with full metadata
           - Timestamp, backend info, configuration
           - Enables reproducibility and post-analysis
    """)


if __name__ == "__main__":
    run_vqe_production()
