"""
Variational Quantum Eigensolver (VQE) - Local Simulator Implementation
========================================================================

This script demonstrates VQE on a local Aer simulator to find the ground-state
energy of a 2-qubit Hamiltonian representing the H2 molecule (simplified).

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
VQE exploits the variational principle:
    E_0 <= <psi(theta)| H |psi(theta)>

We prepare |psi(theta)> using a parameterized quantum circuit (ansatz),
measure <H> on the quantum computer, and use a classical optimizer to
minimize the energy w.r.t. theta.

The Hamiltonian is decomposed into Pauli strings:
    H = sum_i alpha_i P_i

Each <P_i> is measured independently, and <H> = sum_i alpha_i <P_i>.

Algorithm Steps:
    1. Define the Hamiltonian as a sum of Pauli operators
    2. Choose an ansatz (parameterized quantum circuit)
    3. Initialize parameters theta
    4. Loop:
        a. Prepare |psi(theta)> on the quantum computer
        b. Measure <H> = sum_i alpha_i <psi(theta)|P_i|psi(theta)>
        c. Use classical optimizer to update theta
        d. Check convergence
    5. Return the minimum energy found
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import COBYLA, SPSA, L_BFGS_B
from qiskit_aer.primitives import EstimatorV2 as AerEstimator


def main():
    print("=" * 70)
    print("VQE - Variational Quantum Eigensolver (Local Simulator)")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Define the Hamiltonian
    # =========================================================================
    # We construct a 2-qubit Hamiltonian representing a simplified H2 molecule.
    #
    # H = g0*II + g1*ZI + g2*IZ + g3*ZZ + g4*XX + g5*YY
    #
    # These coefficients correspond to H2 at equilibrium bond length (~0.735 A)
    # in the STO-3G basis after qubit reduction via symmetry tapering.
    #
    # See explanation_physicist.md, Section 6: Worked Example
    # =========================================================================

    print("\n--- Step 1: Hamiltonian Definition ---")

    hamiltonian = SparsePauliOp.from_list([
        ("II", -0.8105),   # g0: constant energy offset (nuclear repulsion + core)
        ("ZI",  0.1721),   # g1: one-body term (qubit 0 in Z basis)
        ("IZ", -0.2257),   # g2: one-body term (qubit 1 in Z basis)
        ("ZZ",  0.1721),   # g3: two-body interaction in Z basis
        ("XX",  0.0454),   # g4: exchange interaction (X-X coupling)
        ("YY",  0.0454),   # g5: exchange interaction (Y-Y coupling)
    ])

    print(f"Hamiltonian:\n{hamiltonian}")
    print(f"Number of Pauli terms: {len(hamiltonian)}")
    print(f"Number of qubits: {hamiltonian.num_qubits}")

    # =========================================================================
    # STEP 2: Choose the Ansatz
    # =========================================================================
    # We use EfficientSU2, a hardware-efficient ansatz from Qiskit.
    #
    # Structure (see explanation_physicist.md, Section 3.3):
    #   Each layer applies R_Y and R_Z rotations to every qubit,
    #   followed by an entangling layer (CNOT gates).
    #
    #   |psi(theta)> = [prod_l U_ent * prod_q R_Z(theta) R_Y(theta)] |00...0>
    #
    # For 2 qubits with 1 repetition (reps=1):
    #   - Layer 0: R_Y(t0) R_Z(t1) on q0, R_Y(t2) R_Z(t3) on q1
    #   - CNOT(q0, q1)
    #   - Layer 1: R_Y(t4) R_Z(t5) on q0, R_Y(t6) R_Z(t7) on q1
    #   Total: 8 parameters
    # =========================================================================

    print("\n--- Step 2: Ansatz Selection ---")

    ansatz = EfficientSU2(
        num_qubits=2,
        reps=1,                      # Number of repetition layers
        entanglement="linear",       # CNOT connectivity pattern
        insert_barriers=True         # Visual clarity in circuit drawing
    )

    print(f"Ansatz: EfficientSU2")
    print(f"Number of parameters: {ansatz.num_parameters}")
    print(f"Circuit depth: {ansatz.depth()}")
    print(f"\nCircuit diagram:")
    print(ansatz.draw(output="text"))

    # =========================================================================
    # STEP 3: Configure the Estimator (Quantum Backend)
    # =========================================================================
    # The Estimator primitive computes <psi(theta)|H|psi(theta)> for us.
    # On a real device, this involves:
    #   1. Preparing |psi(theta)> by running the ansatz circuit
    #   2. Rotating qubits to measure each Pauli term P_i
    #   3. Accumulating statistics from many shots
    #   4. Computing <H> = sum_i alpha_i <P_i>
    #
    # Here we use the Aer simulator's EstimatorV2 for noiseless simulation.
    # =========================================================================

    print("\n--- Step 3: Estimator Configuration ---")

    estimator = AerEstimator()
    print("Using: AerEstimator (noiseless local simulator)")

    # =========================================================================
    # STEP 4: Configure the Classical Optimizer
    # =========================================================================
    # COBYLA (Constrained Optimization BY Linear Approximation):
    #   - Gradient-free optimizer
    #   - Does not require computing dC/d(theta_j)
    #   - Robust to noise in the cost function
    #   - Good choice for NISQ devices where gradients are noisy
    #
    # See explanation_physicist.md, Section 4.1: Gradient-Free Methods
    # =========================================================================

    print("\n--- Step 4: Optimizer Configuration ---")

    # Track the energy at each iteration for plotting
    energy_history = []

    def callback(eval_count, parameters, value, metadata):
        """
        Callback function called at each VQE iteration.
        Records the energy for convergence analysis.
        """
        energy_history.append(value)
        if eval_count % 10 == 0:
            print(f"  Iteration {eval_count:4d}: Energy = {value:.6f} Ha")

    optimizer = COBYLA(maxiter=200)
    print(f"Optimizer: COBYLA (gradient-free)")
    print(f"Max iterations: 200")

    # =========================================================================
    # STEP 5: Run VQE
    # =========================================================================
    # The VQE algorithm:
    #   1. Starts with random initial parameters theta_0
    #   2. Evaluates E(theta_0) = <psi(theta_0)|H|psi(theta_0)> via Estimator
    #   3. COBYLA proposes new theta_1 based on E(theta_0)
    #   4. Repeats until convergence (|E_{k+1} - E_k| < tol)
    #
    # The variational principle guarantees E(theta*) >= E_0 (true ground state).
    # =========================================================================

    print("\n--- Step 5: Running VQE ---")
    print("Optimizing parameters to minimize <psi(theta)|H|psi(theta)>...\n")

    vqe = VQE(
        estimator=estimator,
        ansatz=ansatz,
        optimizer=optimizer,
        callback=callback
    )

    # Set initial point (starting parameters)
    # Starting near zero means the initial state is close to |00>
    initial_point = np.zeros(ansatz.num_parameters)
    vqe.initial_point = initial_point

    result = vqe.compute_minimum_eigenvalue(hamiltonian)

    # =========================================================================
    # STEP 6: Analyze Results
    # =========================================================================
    # The VQE result contains:
    #   - eigenvalue: the minimum energy found (upper bound to E_0)
    #   - optimal_parameters: the theta* that achieves this minimum
    #   - optimizer_evals: number of function evaluations
    #
    # For H2 at equilibrium, the exact ground-state energy is about -1.137 Ha.
    # =========================================================================

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    # Exact ground-state energy for comparison
    # Computed by diagonalizing the Hamiltonian matrix
    exact_energy = min(np.linalg.eigvalsh(hamiltonian.to_matrix()))

    print(f"\nVQE ground-state energy:  {result.eigenvalue:.8f} Ha")
    print(f"Exact ground-state energy: {exact_energy:.8f} Ha")
    print(f"Error (VQE - exact):       {abs(result.eigenvalue - exact_energy):.2e} Ha")
    print(f"Chemical accuracy (1.6e-3 Ha = 1 kcal/mol): "
          f"{'ACHIEVED' if abs(result.eigenvalue - exact_energy) < 1.6e-3 else 'NOT ACHIEVED'}")
    print(f"\nOptimal parameters: {result.optimal_parameters}")
    print(f"Number of optimizer evaluations: {result.cost_function_evals}")

    # =========================================================================
    # STEP 7: Exact Energy Landscape (for 2-qubit visualization)
    # =========================================================================
    # Since our ansatz has 8 parameters, we cannot visualize the full landscape.
    # Instead, we scan along one parameter while keeping others at optimal values
    # to show the variational principle at work.
    # =========================================================================

    print("\n--- Step 7: Energy Landscape Visualization ---")

    # Scan one parameter (first R_Y rotation angle) while fixing the rest
    optimal_params = list(result.optimal_parameters.values())
    param_range = np.linspace(0, 2 * np.pi, 100)
    energies_scan = []

    for val in param_range:
        # Create a copy with one parameter varied
        test_params = optimal_params.copy()
        test_params[0] = val  # Vary the first parameter

        # Bind parameters and compute energy classically (exact for visualization)
        bound_circuit = ansatz.assign_parameters(test_params)
        from qiskit.quantum_info import Statevector
        state = Statevector(bound_circuit)
        energy_val = state.expectation_value(hamiltonian).real
        energies_scan.append(energy_val)

    # =========================================================================
    # STEP 8: Plot Results
    # =========================================================================

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Convergence history
    axes[0].plot(range(len(energy_history)), energy_history, 'b-', linewidth=1.5)
    axes[0].axhline(y=exact_energy, color='r', linestyle='--', label=f'Exact E_0 = {exact_energy:.4f} Ha')
    axes[0].set_xlabel('Iteration', fontsize=12)
    axes[0].set_ylabel('Energy (Ha)', fontsize=12)
    axes[0].set_title('VQE Convergence', fontsize=14)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Energy landscape (1D slice)
    axes[1].plot(param_range, energies_scan, 'g-', linewidth=1.5, label='E(theta_0)')
    axes[1].axhline(y=exact_energy, color='r', linestyle='--', label=f'Exact E_0 = {exact_energy:.4f} Ha')
    axes[1].axvline(x=optimal_params[0], color='k', linestyle=':', label=f'Optimal theta_0 = {optimal_params[0]:.2f}')
    axes[1].set_xlabel('theta_0 (first parameter)', fontsize=12)
    axes[1].set_ylabel('Energy (Ha)', fontsize=12)
    axes[1].set_title('Energy Landscape (1D slice)', fontsize=14)
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/01_VQE/vqe_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/01_VQE/vqe_results.png")

    # =========================================================================
    # STEP 9: Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    VQE successfully found the ground-state energy of the H2 Hamiltonian.

    Key concepts demonstrated:
    1. Hamiltonian decomposition into Pauli strings (SparsePauliOp)
    2. Hardware-efficient ansatz (EfficientSU2)
    3. Estimator primitive for computing <H>
    4. Classical optimization loop (COBYLA)
    5. Variational principle: VQE energy >= exact energy

    The error between VQE and exact diagonalization quantifies
    the quality of the ansatz + optimizer combination.
    """)


if __name__ == "__main__":
    main()
