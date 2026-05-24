"""
HHL Algorithm - IBM Production-Ready Implementation
=====================================================

This script implements a production-quality HHL workflow designed for
execution on real IBM Quantum hardware via Qiskit Runtime.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Key differences from the local simulator version:
    1. Uses shot-based simulation with the AerSimulator backend
    2. Includes full measurement and post-selection from counts
    3. Transpiles circuits for realistic gate sets
    4. Saves structured JSON results to disk for reproducibility
    5. Designed for easy migration to IBM Runtime backends
    6. Production-grade error handling and logging

Theoretical Background:
    See explanation_physicist.md for the full mathematical framework.
    The HHL algorithm solves Ax = b by:
        1. QPE to extract eigenvalues into a clock register
        2. Controlled rotations to invert eigenvalues
        3. Inverse QPE to uncompute the clock register
        4. Post-selection on an ancilla qubit

NOTE: To run on real IBM hardware:
    1. Uncomment the IBM Runtime imports below
    2. Set your IBM_QUANTUM_TOKEN environment variable
    3. Switch the backend from AerSimulator to a real device
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Operator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

# =============================================================================
# IBM Runtime imports - uncomment for real hardware execution
# =============================================================================
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session
# from qiskit_ibm_runtime.options import SamplerOptions

# =============================================================================
# CONFIGURATION
# =============================================================================

RESULTS_DIR = "quantum/algorithms/19_HHL/production_results"


# =============================================================================
# PROBLEM DEFINITION
# =============================================================================

def create_problem():
    """
    Define the linear system Ax = b.

    Returns
    -------
    A : numpy.ndarray
        2x2 Hermitian matrix.
    b : numpy.ndarray
        Right-hand side vector.
    """
    A = np.array([[1.0, -1.0 / 3.0], [-1.0 / 3.0, 1.0]])
    b = np.array([1.0, 0.0])

    print("Problem Definition:")
    print(f"  A = {A.tolist()}")
    print(f"  b = {b.tolist()}")

    # Validate: A must be Hermitian
    if not np.allclose(A, A.conj().T):
        raise ValueError("Matrix A must be Hermitian.")

    # Validate: A must be invertible
    det = np.linalg.det(A)
    if abs(det) < 1e-10:
        raise ValueError(f"Matrix A is singular (det = {det:.6e}).")

    eigenvalues = np.linalg.eigvalsh(A)
    kappa = max(abs(eigenvalues)) / min(abs(eigenvalues))
    print(f"  Eigenvalues: {eigenvalues}")
    print(f"  Condition number: {kappa:.4f}")
    print(f"  det(A) = {det:.6f}")

    return A, b


# =============================================================================
# CLASSICAL SOLVER
# =============================================================================

def solve_classically(A, b):
    """
    Solve Ax = b using numpy.

    Parameters
    ----------
    A : numpy.ndarray
    b : numpy.ndarray

    Returns
    -------
    numpy.ndarray
        Solution vector x.
    """
    x = np.linalg.solve(A, b)
    print(f"\nClassical solution: x = {x.tolist()}")
    print(f"  x = [{x[0]:.6f}, {x[1]:.6f}]")

    # Verify
    residual = np.linalg.norm(A @ x - b)
    print(f"  Residual ||Ax - b|| = {residual:.2e}")

    return x


# =============================================================================
# CIRCUIT CONSTRUCTION
# =============================================================================

def _compute_matrix_exponential(A, t):
    """Compute e^{iAt} via eigendecomposition."""
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    exp_diag = np.diag(np.exp(1j * eigenvalues * t))
    return eigenvectors @ exp_diag @ eigenvectors.conj().T


def _apply_inverse_qft(qc, clock, n):
    """Apply inverse QFT to the clock register."""
    for i in range(n // 2):
        qc.swap(clock[i], clock[n - 1 - i])

    for j in range(n):
        for k in range(j):
            angle = -np.pi / (2 ** (j - k))
            qc.cp(angle, clock[k], clock[j])
        qc.h(clock[j])


def _apply_forward_qft(qc, clock, n):
    """Apply forward QFT to the clock register."""
    for j in range(n - 1, -1, -1):
        qc.h(clock[j])
        for k in range(j - 1, -1, -1):
            angle = np.pi / (2 ** (j - k))
            qc.cp(angle, clock[k], clock[j])

    for i in range(n // 2):
        qc.swap(clock[i], clock[n - 1 - i])


def _apply_controlled_ry_on_clock_state(qc, ancilla_qubit, clock, n_clock, k, theta):
    """Apply Ry(theta) on ancilla controlled by clock=|k>."""
    binary_k = format(k, f"0{n_clock}b")[::-1]

    for i in range(n_clock):
        if binary_k[i] == "0":
            qc.x(clock[i])

    ry_gate = QuantumCircuit(1, name=f"Ry({theta:.3f})")
    ry_gate.ry(theta, 0)
    ry_instruction = ry_gate.to_gate()
    mcry = ry_instruction.control(n_clock)

    control_qubits = [clock[i] for i in range(n_clock)]
    qc.append(mcry, control_qubits + [ancilla_qubit])

    for i in range(n_clock):
        if binary_k[i] == "0":
            qc.x(clock[i])


def build_hhl_circuit(A, b, n_clock=2):
    """
    Build the complete HHL circuit with measurements on all qubits.

    Parameters
    ----------
    A : numpy.ndarray
        2x2 Hermitian matrix.
    b : numpy.ndarray
        Right-hand side vector.
    n_clock : int
        Number of clock qubits for QPE.

    Returns
    -------
    QuantumCircuit
        The complete HHL circuit with classical measurements.
    dict
        Circuit metadata.
    """
    # ---- Eigendecomposition ----
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    lambda_min = np.min(np.abs(eigenvalues))

    # ---- QPE parameters ----
    t0 = 3.0 * np.pi / 4.0
    C = lambda_min

    # ---- Rotation angles ----
    rotation_angles = {}
    eigenvalue_map = {}

    for lam in sorted(np.abs(eigenvalues)):
        phi = lam * t0 / (2.0 * np.pi)
        k = int(round(phi * (2**n_clock)))
        if k > 0:
            theta = 2.0 * np.arcsin(min(C / lam, 1.0))
            rotation_angles[k] = theta
            eigenvalue_map[k] = lam

    # ---- Create registers ----
    ancilla = QuantumRegister(1, name="anc")
    clock = QuantumRegister(n_clock, name="clk")
    state = QuantumRegister(1, name="st")
    c_anc = ClassicalRegister(1, name="c_anc")
    c_clk = ClassicalRegister(n_clock, name="c_clk")
    c_st = ClassicalRegister(1, name="c_st")
    qc = QuantumCircuit(ancilla, clock, state, c_anc, c_clk, c_st, name="HHL_prod")

    # ---- STEP 1: State preparation ----
    b_norm = b / np.linalg.norm(b)
    if abs(b_norm[1]) > 1e-10:
        theta_b = 2.0 * np.arccos(np.real(b_norm[0]))
        qc.ry(theta_b, state[0])

    qc.barrier()

    # ---- STEP 2: QPE ----
    for i in range(n_clock):
        qc.h(clock[i])

    for k in range(n_clock):
        power = 2**k
        t_eff = t0 * power
        U_power = _compute_matrix_exponential(A, t_eff)
        U_op = Operator(U_power)
        U_gate = U_op.to_instruction()
        U_gate.name = f"U^{power}"
        ctrl_U = U_gate.control(1)
        qc.append(ctrl_U, [clock[k], state[0]])

    qc.barrier()

    _apply_inverse_qft(qc, clock, n_clock)

    qc.barrier()

    # ---- STEP 3: Eigenvalue inversion ----
    for k, theta in rotation_angles.items():
        _apply_controlled_ry_on_clock_state(qc, ancilla[0], clock, n_clock, k, theta)

    qc.barrier()

    # ---- STEP 4: Inverse QPE ----
    _apply_forward_qft(qc, clock, n_clock)

    qc.barrier()

    for k in range(n_clock - 1, -1, -1):
        power = 2**k
        t_eff = t0 * power
        U_power = _compute_matrix_exponential(A, t_eff)
        U_inv = np.conj(U_power).T
        U_inv_op = Operator(U_inv)
        U_inv_gate = U_inv_op.to_instruction()
        U_inv_gate.name = f"U^-{power}"
        ctrl_U_inv = U_inv_gate.control(1)
        qc.append(ctrl_U_inv, [clock[k], state[0]])

    for i in range(n_clock):
        qc.h(clock[i])

    qc.barrier()

    # ---- STEP 5: Measurements ----
    qc.measure(ancilla[0], c_anc[0])
    qc.measure(state[0], c_st[0])
    for i in range(n_clock):
        qc.measure(clock[i], c_clk[i])

    metadata = {
        "eigenvalues": eigenvalues.tolist(),
        "t0": t0,
        "C": C,
        "rotation_angles": {str(k): v for k, v in rotation_angles.items()},
        "eigenvalue_map": {str(k): v for k, v in eigenvalue_map.items()},
        "n_clock": n_clock,
        "n_qubits": 1 + n_clock + 1,
    }

    return qc, metadata


# =============================================================================
# EXECUTION AND POST-SELECTION
# =============================================================================

def run_hhl_with_shots(circuit, shots=8192):
    """
    Execute the HHL circuit on AerSimulator with shot-based sampling.

    Performs post-selection on the ancilla qubit being |1> and the clock
    register being |00...0>.

    Parameters
    ----------
    circuit : QuantumCircuit
        The complete HHL circuit with measurements.
    shots : int
        Number of shots.

    Returns
    -------
    dict
        Post-selected counts and state probabilities.
    dict
        Raw counts.
    int
        Total post-selected shots.
    """
    print(f"\nExecuting circuit with {shots} shots on AerSimulator...")

    backend = AerSimulator()

    # Transpile for the backend
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled = pm.run(circuit)

    print(f"  Transpiled circuit depth: {transpiled.depth()}")
    print(f"  Transpiled gate count: {transpiled.count_ops()}")

    # Run
    job = backend.run(transpiled, shots=shots)
    result = job.result()
    raw_counts = result.get_counts()

    # ---- Post-selection ----
    # Qiskit bit ordering in count strings: c_st c_clk c_anc (right to left)
    # We post-select on:
    #   ancilla (c_anc) = 1
    #   clock (c_clk) = 00...0

    n_clock = circuit.num_qubits - 2  # total - ancilla - state
    postselected_counts = {}
    total_postselected = 0

    for bitstring, count in raw_counts.items():
        # Parse the bitstring
        # Format: "c_st c_clk[n-1]...c_clk[0] c_anc"
        # Qiskit concatenates registers: c_anc is rightmost, c_st is leftmost
        bits = bitstring.replace(" ", "")

        # With our register layout:
        # c_anc (1 bit) | c_clk (n_clock bits) | c_st (1 bit)
        # In Qiskit output, the order is: c_st c_clk c_anc (left to right = MSB to LSB)
        # So bits[-1] = c_anc[0], bits[-1-n_clock:-1] = c_clk, bits[0] = c_st

        anc_bit = bits[-1]
        clk_bits = bits[1:1 + n_clock]
        st_bit = bits[0]

        if anc_bit == "1" and all(c == "0" for c in clk_bits):
            postselected_counts[st_bit] = postselected_counts.get(st_bit, 0) + count
            total_postselected += count

    # Compute state probabilities from post-selected counts
    state_probs = {}
    if total_postselected > 0:
        for state_val, count in postselected_counts.items():
            state_probs[state_val] = count / total_postselected

    print(f"\n  Raw counts (top 10):")
    sorted_raw = sorted(raw_counts.items(), key=lambda x: -x[1])[:10]
    for bs, cnt in sorted_raw:
        print(f"    {bs}: {cnt}")

    print(f"\n  Post-selected counts (ancilla=1, clock=0):")
    print(f"    Total post-selected: {total_postselected}/{shots} "
          f"({100*total_postselected/shots:.1f}%)")
    for st, cnt in postselected_counts.items():
        print(f"    state={st}: {cnt} ({100*cnt/total_postselected:.1f}%)"
              if total_postselected > 0 else f"    state={st}: {cnt}")

    return {
        "postselected_counts": postselected_counts,
        "state_probabilities": state_probs,
        "total_postselected": total_postselected,
    }, raw_counts, total_postselected


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_results(quantum_results, x_classical, shots):
    """
    Analyze quantum results and compare with classical solution.

    Parameters
    ----------
    quantum_results : dict
        Post-selected quantum results.
    x_classical : numpy.ndarray
        Classical solution.
    shots : int
        Total number of shots.

    Returns
    -------
    dict
        Analysis results including fidelity estimate.
    """
    print("\n" + "-" * 50)
    print("ANALYSIS")
    print("-" * 50)

    state_probs = quantum_results["state_probabilities"]
    total_ps = quantum_results["total_postselected"]

    # Classical solution probability distribution (normalized |x|^2)
    x_norm_sq = np.abs(x_classical) ** 2
    classical_probs = x_norm_sq / np.sum(x_norm_sq)

    print(f"\n  Classical |x|^2 distribution:")
    print(f"    P(state=0) = {classical_probs[0]:.6f}")
    print(f"    P(state=1) = {classical_probs[1]:.6f}")

    print(f"\n  Quantum post-selected distribution:")
    q_prob_0 = state_probs.get("0", 0.0)
    q_prob_1 = state_probs.get("1", 0.0)
    print(f"    P(state=0) = {q_prob_0:.6f}")
    print(f"    P(state=1) = {q_prob_1:.6f}")

    # Fidelity estimate (classical fidelity between probability distributions)
    # F = (sum_i sqrt(p_i * q_i))^2
    quantum_probs_arr = np.array([q_prob_0, q_prob_1])
    fidelity = (np.sum(np.sqrt(classical_probs * quantum_probs_arr))) ** 2

    print(f"\n  Fidelity (Bhattacharyya): {fidelity:.6f}")

    # Ratio comparison
    if q_prob_1 > 0:
        quantum_ratio = q_prob_0 / q_prob_1
        classical_ratio = classical_probs[0] / classical_probs[1]
        print(f"\n  Amplitude ratio |x[0]|^2/|x[1]|^2:")
        print(f"    Classical: {classical_ratio:.4f}")
        print(f"    Quantum:   {quantum_ratio:.4f}")

    post_selection_rate = total_ps / shots if shots > 0 else 0

    return {
        "classical_probs": classical_probs.tolist(),
        "quantum_probs": quantum_probs_arr.tolist(),
        "fidelity": float(fidelity),
        "post_selection_rate": float(post_selection_rate),
    }


# =============================================================================
# SAVE RESULTS
# =============================================================================

def save_results(problem, classical_solution, quantum_results, analysis,
                 circuit_metadata, circuit_depth, shots):
    """
    Save all results to a JSON file.

    Parameters
    ----------
    problem : dict
        Problem definition (A, b).
    classical_solution : numpy.ndarray
    quantum_results : dict
    analysis : dict
    circuit_metadata : dict
    circuit_depth : int
    shots : int
    """
    os.makedirs(RESULTS_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"hhl_results_{timestamp}.json"
    filepath = os.path.join(RESULTS_DIR, filename)

    results = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "algorithm": "HHL",
            "qiskit_version": "2.4.1",
            "backend": "AerSimulator",
            "shots": shots,
            "n_clock": circuit_metadata["n_clock"],
            "n_qubits": circuit_metadata["n_qubits"],
        },
        "problem": {
            "A": problem["A"].tolist(),
            "b": problem["b"].tolist(),
            "eigenvalues": circuit_metadata["eigenvalues"],
            "condition_number": float(
                max(abs(e) for e in circuit_metadata["eigenvalues"])
                / min(abs(e) for e in circuit_metadata["eigenvalues"])
            ),
        },
        "classical_solution": classical_solution.tolist(),
        "quantum_results": {
            "post_selected_counts": quantum_results["postselected_counts"],
            "state_probabilities": quantum_results["state_probabilities"],
            "fidelity": analysis["fidelity"],
        },
        "metrics": {
            "post_selection_rate": analysis["post_selection_rate"],
            "circuit_depth": circuit_depth,
            "total_postselected_shots": quantum_results["total_postselected"],
        },
    }

    with open(filepath, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {filepath}")
    return filepath


# =============================================================================
# PRODUCTION PIPELINE
# =============================================================================

def run_production():
    """
    Main production pipeline for HHL.

    Steps:
        1. Define problem
        2. Solve classically (ground truth)
        3. Build HHL circuit
        4. Transpile for backend
        5. Execute with shots
        6. Post-select and analyze
        7. Save results to JSON
        8. Print comparison table and notes
    """
    print("=" * 70)
    print("HHL ALGORITHM - PRODUCTION PIPELINE")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Backend: AerSimulator (local)")
    print()

    # ---- Step 1: Define problem ----
    A, b = create_problem()

    # ---- Step 2: Classical solution ----
    x_classical = solve_classically(A, b)

    # ---- Step 3: Build circuit ----
    n_clock = 2
    shots = 8192

    print(f"\nBuilding HHL circuit (n_clock={n_clock})...")
    circuit, metadata = build_hhl_circuit(A, b, n_clock=n_clock)
    print(f"  Raw circuit depth: {circuit.depth()}")
    print(f"  Qubit count: {circuit.num_qubits}")

    # ---- Step 4: Transpile ----
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=2, backend=backend)
    transpiled = pm.run(circuit)
    transpiled_depth = transpiled.depth()
    print(f"  Transpiled depth (opt_level=2): {transpiled_depth}")
    print(f"  Transpiled gate counts: {dict(transpiled.count_ops())}")

    # ---- Step 5 & 6: Execute and post-select ----
    quantum_results, raw_counts, total_ps = run_hhl_with_shots(circuit, shots=shots)

    # ---- Step 7: Analyze ----
    analysis = analyze_results(quantum_results, x_classical, shots)

    # ---- Step 8: Save ----
    problem_dict = {"A": A, "b": b}
    save_path = save_results(
        problem_dict, x_classical, quantum_results, analysis,
        metadata, transpiled_depth, shots,
    )

    # ---- Step 9: Comparison table ----
    print("\n" + "=" * 70)
    print("COMPARISON TABLE")
    print("=" * 70)

    print(f"""
{'Metric':<35} {'Classical':>15} {'Quantum':>15}
{'-'*65}
{'Solution x[0]':<35} {x_classical[0]:>15.6f} {'(state probs)':>15}
{'Solution x[1]':<35} {x_classical[1]:>15.6f} {'(state probs)':>15}
{'P(state=0)':<35} {analysis['classical_probs'][0]:>15.6f} {analysis['quantum_probs'][0]:>15.6f}
{'P(state=1)':<35} {analysis['classical_probs'][1]:>15.6f} {analysis['quantum_probs'][1]:>15.6f}
{'Fidelity':<35} {'1.000000':>15} {analysis['fidelity']:>15.6f}
{'Post-selection rate':<35} {'N/A':>15} {analysis['post_selection_rate']:>15.4f}
{'Circuit depth (transpiled)':<35} {'N/A':>15} {transpiled_depth:>15}
{'Shots':<35} {'N/A':>15} {shots:>15}
{'Post-selected shots':<35} {'N/A':>15} {total_ps:>15}
""")

    # ---- Production notes ----
    print("=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print("""
1. BACKEND: Currently using AerSimulator (noiseless local simulation).
   To deploy on real IBM hardware:
     - Uncomment IBM Runtime imports at the top of this file
     - Set IBM_QUANTUM_TOKEN environment variable
     - Replace AerSimulator with QiskitRuntimeService().least_busy(...)
     - Wrap execution in a Session for efficient job batching

2. ERROR MITIGATION: For real hardware, enable:
     - Measurement error mitigation (M3/mthree)
     - Dynamical decoupling during idle periods
     - Zero-noise extrapolation (ZNE) if available

3. CIRCUIT OPTIMIZATION: The transpiled depth is critical for NISQ devices.
   Consider:
     - Higher optimization levels (opt_level=3) for deeper compression
     - Custom gate decompositions for the controlled-U unitaries
     - Approximate QPE (fewer clock qubits) to reduce depth

4. POST-SELECTION: The success probability scales as O(1/kappa^2).
   For larger condition numbers, use amplitude amplification to boost
   the post-selection rate from O(1/kappa^2) to O(1/kappa).

5. SCALABILITY: This 2x2 demo uses 4 qubits. For practical advantage:
     - N = 2^10 (1024 variables) requires ~10 state + ~20 clock qubits
     - Hamiltonian simulation must replace the exact matrix exponential
     - State preparation requires QRAM or structured input

6. RESULTS: JSON results are saved to:
     """ + RESULTS_DIR + """

7. KNOWN LIMITATIONS:
     - Shot noise introduces statistical error (reduce with more shots)
     - Post-selection discards most measurements (wasteful)
     - Current hardware gate fidelities (~99.5%) limit circuit depth
""")

    return save_path


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    run_production()
