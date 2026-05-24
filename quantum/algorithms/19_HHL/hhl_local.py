"""
HHL Algorithm (Harrow-Hassidim-Lloyd) - Local Simulator Implementation
========================================================================

This script demonstrates the HHL algorithm on a local Aer simulator to solve
a 2x2 linear system Ax = b.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
The HHL algorithm solves Ax = b by:
    1. Encoding |b> into a quantum state
    2. Using QPE to extract eigenvalues of A into a clock register
    3. Inverting eigenvalues via controlled rotations on an ancilla
    4. Uncomputing QPE (inverse QPE)
    5. Post-selecting on the ancilla qubit being |1>

The result is a quantum state proportional to A^{-1}|b>.

For our 2x2 system:
    A = [[1, -1/3], [-1/3, 1]]
    b = [1, 0]
    Eigenvalues: lambda_1 = 2/3, lambda_2 = 4/3
    Condition number: kappa = 2
    Classical solution: x = [9/8, 3/8] = [1.125, 0.375]

QPE parameter: t_0 = 3*pi/4 maps eigenvalues to exact binary fractions:
    phi_1 = lambda_1 * t_0 / (2*pi) = 1/4 --> clock |01> (k=1)
    phi_2 = lambda_2 * t_0 / (2*pi) = 1/2 --> clock |10> (k=2)

Registers (4 qubits total):
    q0 = ancilla (for eigenvalue inversion + post-selection)
    q1 = clock_0 (LSB of clock register)
    q2 = clock_1 (MSB of clock register)
    q3 = state qubit (encodes |b>)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, Operator
from qiskit_aer import AerSimulator


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_matrix_exponential(A, t):
    """
    Compute e^{iAt} via eigendecomposition.

    A = V Lambda V^T  =>  e^{iAt} = V diag(e^{i lambda_j t}) V^T

    Parameters
    ----------
    A : numpy.ndarray
        Hermitian matrix.
    t : float
        Evolution time.

    Returns
    -------
    numpy.ndarray
        The unitary matrix e^{iAt}.
    """
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    exp_diag = np.diag(np.exp(1j * eigenvalues * t))
    U = eigenvectors @ exp_diag @ eigenvectors.conj().T
    return U


def build_hhl_circuit(A, b, n_clock=2):
    """
    Build the full HHL circuit for a 2x2 linear system.

    Parameters
    ----------
    A : numpy.ndarray
        2x2 Hermitian matrix.
    b : numpy.ndarray
        2-element vector (must be a valid quantum state or normalizable).
    n_clock : int
        Number of clock qubits for QPE (minimum 2 for this problem).

    Returns
    -------
    QuantumCircuit
        The complete HHL circuit (without measurements, for statevector sim).
    dict
        Metadata: eigenvalues, t0, C, rotation angles.
    """
    # ---- Eigendecomposition of A ----
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    lambda_min = np.min(np.abs(eigenvalues))
    lambda_max = np.max(np.abs(eigenvalues))

    # ---- Choose t_0 so that eigenphases are exact binary fractions ----
    # For n_clock=2: We want phi_1 = lambda_1 * t0 / (2*pi) = 1/4
    #                          phi_2 = lambda_2 * t0 / (2*pi) = 1/2
    # => t0 = 2*pi*(1/4) / lambda_1 = pi/2 / (2/3) = 3*pi/4
    t0 = 3.0 * np.pi / 4.0

    # ---- Normalization constant for eigenvalue inversion ----
    C = lambda_min  # C = 2/3

    # ---- Compute rotation angles for each eigenvalue clock state ----
    # For clock state |k>, the eigenvalue is lambda = 2*pi*k / (2^n_clock * t0)
    # But we use the actual eigenvalue mapping:
    #   k=1 -> lambda_1 = 2/3, k=2 -> lambda_2 = 4/3
    rotation_angles = {}
    eigenvalue_map = {}

    for j, lam in enumerate(sorted(np.abs(eigenvalues))):
        # Phase: phi = lam * t0 / (2*pi)
        phi = lam * t0 / (2.0 * np.pi)
        k = int(round(phi * (2**n_clock)))
        if k > 0:
            theta = 2.0 * np.arcsin(min(C / lam, 1.0))
            rotation_angles[k] = theta
            eigenvalue_map[k] = lam

    # ---- Create registers ----
    ancilla = QuantumRegister(1, name="ancilla")
    clock = QuantumRegister(n_clock, name="clock")
    state = QuantumRegister(1, name="state")
    qc = QuantumCircuit(ancilla, clock, state, name="HHL")

    # ---- STEP 1: State preparation (|b> = |0>, trivially prepared) ----
    # Normalize b and prepare state if needed
    b_norm = b / np.linalg.norm(b)
    # For b = [1, 0], the state qubit is already |0>, no gates needed.
    # For general b, we would need amplitude encoding.
    if abs(b_norm[1]) > 1e-10:
        # General state preparation for 1 qubit
        theta_b = 2.0 * np.arccos(np.real(b_norm[0]))
        qc.ry(theta_b, state[0])

    qc.barrier()

    # ---- STEP 2: QPE ----
    # 2a. Hadamard on all clock qubits
    for i in range(n_clock):
        qc.h(clock[i])

    # 2b. Controlled-U^{2^k} applications
    # clock[0] is LSB, clock[n_clock-1] is MSB
    # clock[k] controls U^{2^k}
    for k in range(n_clock):
        power = 2**k
        t_eff = t0 * power
        U_power = compute_matrix_exponential(A, t_eff)

        # Create controlled unitary
        U_op = Operator(U_power)
        U_gate = U_op.to_instruction()
        U_gate.name = f"U^{power}"
        ctrl_U = U_gate.control(1)

        # Apply: control=clock[k], target=state[0]
        qc.append(ctrl_U, [clock[k], state[0]])

    qc.barrier()

    # 2c. Inverse QFT on clock register
    # For 2 qubits: iQFT = SWAP, then H-ctrl-S_dag-H pattern
    # Standard inverse QFT for n_clock qubits
    _apply_inverse_qft(qc, clock, n_clock)

    qc.barrier()

    # ---- STEP 3: Eigenvalue inversion (controlled Ry on ancilla) ----
    for k, theta in rotation_angles.items():
        # Apply Ry(theta) on ancilla, controlled by clock = |k>
        # Convert k to binary and apply X gates for 0-controls
        _apply_controlled_ry_on_clock_state(qc, ancilla[0], clock, n_clock, k, theta)

    qc.barrier()

    # ---- STEP 4: Inverse QPE (reverse of Step 2) ----
    # 4a. Forward QFT (inverse of inverse QFT)
    _apply_forward_qft(qc, clock, n_clock)

    qc.barrier()

    # 4b. Inverse controlled-U^{2^k} applications (in reverse order)
    for k in range(n_clock - 1, -1, -1):
        power = 2**k
        t_eff = t0 * power
        U_power = compute_matrix_exponential(A, t_eff)
        U_inv = np.conj(U_power).T  # U^dagger

        U_inv_op = Operator(U_inv)
        U_inv_gate = U_inv_op.to_instruction()
        U_inv_gate.name = f"U^-{power}"
        ctrl_U_inv = U_inv_gate.control(1)

        qc.append(ctrl_U_inv, [clock[k], state[0]])

    # 4c. Hadamard on clock qubits (reverse of step 2a)
    for i in range(n_clock):
        qc.h(clock[i])

    qc.barrier()

    metadata = {
        "eigenvalues": eigenvalues.tolist(),
        "t0": t0,
        "C": C,
        "rotation_angles": rotation_angles,
        "eigenvalue_map": eigenvalue_map,
        "n_clock": n_clock,
        "n_qubits": 1 + n_clock + 1,
    }

    return qc, metadata


def _apply_inverse_qft(qc, clock, n):
    """Apply inverse QFT on the clock register."""
    # Swap qubits to reverse order
    for i in range(n // 2):
        qc.swap(clock[i], clock[n - 1 - i])

    # Apply inverse QFT gates
    for j in range(n):
        for k in range(j):
            angle = -np.pi / (2 ** (j - k))
            qc.cp(angle, clock[k], clock[j])
        qc.h(clock[j])


def _apply_forward_qft(qc, clock, n):
    """Apply forward QFT on the clock register (inverse of inverse QFT)."""
    for j in range(n - 1, -1, -1):
        qc.h(clock[j])
        for k in range(j - 1, -1, -1):
            angle = np.pi / (2 ** (j - k))
            qc.cp(angle, clock[k], clock[j])

    for i in range(n // 2):
        qc.swap(clock[i], clock[n - 1 - i])


def _apply_controlled_ry_on_clock_state(qc, ancilla_qubit, clock, n_clock, k, theta):
    """
    Apply Ry(theta) on the ancilla qubit, controlled by the clock register
    being in state |k>.

    Uses the standard trick: apply X gates to flip 0-controls to 1-controls,
    then apply multi-controlled Ry, then unflip.

    Parameters
    ----------
    qc : QuantumCircuit
    ancilla_qubit : Qubit
    clock : QuantumRegister
    n_clock : int
    k : int
        The clock state (as integer) that triggers the rotation.
    theta : float
        The Ry rotation angle.
    """
    # Determine which clock qubits should be |0> (need X gate)
    binary_k = format(k, f"0{n_clock}b")[::-1]  # LSB first

    # Apply X to qubits that should be |0> in |k>
    for i in range(n_clock):
        if binary_k[i] == "0":
            qc.x(clock[i])

    # Multi-controlled Ry
    # Build the multi-controlled Ry gate
    ry_gate = QuantumCircuit(1, name=f"Ry({theta:.3f})")
    ry_gate.ry(theta, 0)
    ry_instruction = ry_gate.to_gate()
    mcry = ry_instruction.control(n_clock)

    # Apply: controls = clock qubits, target = ancilla
    control_qubits = [clock[i] for i in range(n_clock)]
    qc.append(mcry, control_qubits + [ancilla_qubit])

    # Unflip X gates
    for i in range(n_clock):
        if binary_k[i] == "0":
            qc.x(clock[i])


def postselect_ancilla(statevector, n_total, ancilla_index=0):
    """
    Post-select on ancilla qubit being |1>.

    Parameters
    ----------
    statevector : numpy.ndarray
        Full statevector of the circuit (2^n_total amplitudes).
    n_total : int
        Total number of qubits.
    ancilla_index : int
        Index of the ancilla qubit (0 = first qubit in Qiskit ordering).

    Returns
    -------
    numpy.ndarray
        Amplitudes of the state qubit conditioned on ancilla=|1>.
    float
        Post-selection probability.
    """
    n = n_total
    amplitudes = np.array(statevector)

    # In Qiskit's ordering, qubit 0 is the LEAST significant bit
    # ancilla is qubit 0 (index 0)
    # We want states where bit 0 (ancilla) = 1
    selected_indices = []
    for i in range(2**n):
        if (i >> ancilla_index) & 1 == 1:
            selected_indices.append(i)

    selected_amplitudes = amplitudes[selected_indices]
    prob = np.sum(np.abs(selected_amplitudes) ** 2)

    if prob > 1e-12:
        selected_amplitudes /= np.sqrt(prob)

    return selected_amplitudes, prob


def extract_state_qubit_amplitudes(postselected_amps, n_total, ancilla_index=0,
                                    state_index=None, n_clock=2):
    """
    After post-selection on ancilla=|1>, extract the amplitudes for the state
    qubit, tracing out the clock register (which should be |00...0>).

    Parameters
    ----------
    postselected_amps : numpy.ndarray
        Post-selected amplitudes (2^{n_total-1} elements).
    n_total : int
        Total number of qubits.
    ancilla_index : int
        Index of ancilla qubit.
    state_index : int or None
        Index of state qubit. If None, assumed to be the last qubit.
    n_clock : int
        Number of clock qubits.

    Returns
    -------
    numpy.ndarray
        2-element array: amplitudes for state qubit |0> and |1>.
    """
    # After removing ancilla, we have n_total-1 qubits
    # Ordering: clock_0, clock_1, ..., clock_{n-1}, state
    # In Qiskit bit ordering (LSB = first qubit), the post-selected indices
    # remove the ancilla bit.
    # We want clock = |00...0> and extract the state qubit amplitudes.

    n_remaining = n_total - 1
    state_amp_0 = 0.0 + 0.0j
    state_amp_1 = 0.0 + 0.0j

    for idx in range(len(postselected_amps)):
        # idx represents the remaining qubits (clock + state) after ancilla removal
        # clock bits: bits 0 to n_clock-1
        # state bit: bit n_clock
        clock_val = idx & ((1 << n_clock) - 1)
        state_val = (idx >> n_clock) & 1

        if clock_val == 0:  # Clock register is |00...0>
            if state_val == 0:
                state_amp_0 = postselected_amps[idx]
            else:
                state_amp_1 = postselected_amps[idx]

    return np.array([state_amp_0, state_amp_1])


# =============================================================================
# PART A: Build and run HHL for the 2x2 system
# =============================================================================

def run_part_a():
    """Run the HHL algorithm for the 2x2 system and compare with classical."""

    print("=" * 70)
    print("PART A: HHL Algorithm for 2x2 Linear System")
    print("=" * 70)

    # ---- Define the problem ----
    A = np.array([[1.0, -1.0 / 3.0], [-1.0 / 3.0, 1.0]])
    b = np.array([1.0, 0.0])

    print("\nProblem: Ax = b")
    print(f"A = {A.tolist()}")
    print(f"b = {b.tolist()}")

    # ---- Classical solution ----
    x_classical = np.linalg.solve(A, b)
    print(f"\nClassical solution (numpy.linalg.solve):")
    print(f"  x = {x_classical}")
    print(f"  x = [{x_classical[0]:.6f}, {x_classical[1]:.6f}]")

    # ---- Eigendecomposition ----
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    kappa = max(abs(eigenvalues)) / min(abs(eigenvalues))
    print(f"\nEigenvalues: {eigenvalues}")
    print(f"Eigenvectors:\n{eigenvectors}")
    print(f"Condition number kappa = {kappa:.4f}")

    # ---- Build HHL circuit ----
    n_clock = 2
    qc, metadata = build_hhl_circuit(A, b, n_clock=n_clock)
    n_total = metadata["n_qubits"]

    print(f"\nCircuit details:")
    print(f"  Total qubits: {n_total}")
    print(f"  Clock qubits: {n_clock}")
    print(f"  t_0 = {metadata['t0']:.6f} = 3*pi/4")
    print(f"  C = {metadata['C']:.6f}")
    print(f"  Rotation angles: {metadata['rotation_angles']}")
    print(f"  Eigenvalue map: {metadata['eigenvalue_map']}")
    print(f"  Circuit depth: {qc.depth()}")

    # ---- Statevector simulation ----
    print("\nRunning statevector simulation...")
    sv = Statevector.from_instruction(qc)
    sv_array = np.array(sv)

    # ---- Post-selection on ancilla = |1> ----
    postselected, post_prob = postselect_ancilla(sv_array, n_total, ancilla_index=0)
    print(f"Post-selection probability: {post_prob:.6f}")

    # ---- Extract state qubit amplitudes ----
    state_amps = extract_state_qubit_amplitudes(postselected, n_total, n_clock=n_clock)
    print(f"State qubit amplitudes (post-selected): {state_amps}")

    # ---- Compare with classical solution ----
    # The quantum state is proportional to x_classical (normalized)
    x_classical_norm = x_classical / np.linalg.norm(x_classical)
    quantum_state_norm = state_amps / np.linalg.norm(state_amps)

    # Ensure consistent global phase
    if np.abs(quantum_state_norm[0]) > 1e-10:
        phase = np.angle(quantum_state_norm[0]) - np.angle(x_classical_norm[0])
        quantum_state_norm *= np.exp(-1j * phase)

    print(f"\nComparison (normalized states):")
    print(f"  Classical (normalized):  {np.real(x_classical_norm)}")
    print(f"  Quantum (normalized):    {np.real(quantum_state_norm)}")

    # Fidelity
    fidelity = np.abs(np.dot(np.conj(x_classical_norm), quantum_state_norm)) ** 2
    print(f"  Fidelity: {fidelity:.8f}")

    # Reconstruct x from quantum amplitudes
    # Scale quantum state to match classical solution norm
    if np.abs(quantum_state_norm[0]) > 1e-10:
        scale = x_classical[0] / np.real(quantum_state_norm[0])
    else:
        scale = np.linalg.norm(x_classical) / np.linalg.norm(quantum_state_norm)

    x_quantum = np.real(quantum_state_norm) * scale
    print(f"\n  Classical x = [{x_classical[0]:.6f}, {x_classical[1]:.6f}]")
    print(f"  Quantum x  = [{x_quantum[0]:.6f}, {x_quantum[1]:.6f}]")
    print(f"  Ratio x[0]/x[1] (classical) = {x_classical[0]/x_classical[1]:.6f}")
    if abs(np.real(quantum_state_norm[1])) > 1e-10:
        ratio_q = np.real(quantum_state_norm[0]) / np.real(quantum_state_norm[1])
        print(f"  Ratio x[0]/x[1] (quantum)   = {ratio_q:.6f}")

    return {
        "A": A,
        "b": b,
        "x_classical": x_classical,
        "quantum_state": quantum_state_norm,
        "fidelity": fidelity,
        "post_prob": post_prob,
        "circuit": qc,
        "metadata": metadata,
    }


# =============================================================================
# PART B: Vary n_clock and study fidelity
# =============================================================================

def run_part_b(A, b, x_classical):
    """Run HHL with different numbers of clock qubits."""

    print("\n" + "=" * 70)
    print("PART B: Effect of Clock Qubit Count on Fidelity")
    print("=" * 70)

    n_clock_values = [2, 3, 4]
    fidelities = []
    post_probs = []
    depths = []

    x_classical_norm = x_classical / np.linalg.norm(x_classical)

    for nc in n_clock_values:
        print(f"\n--- n_clock = {nc} ---")

        qc, metadata = build_hhl_circuit(A, b, n_clock=nc)
        n_total = metadata["n_qubits"]

        sv = Statevector.from_instruction(qc)
        sv_array = np.array(sv)

        postselected, post_prob = postselect_ancilla(sv_array, n_total, ancilla_index=0)

        state_amps = extract_state_qubit_amplitudes(postselected, n_total, n_clock=nc)
        quantum_norm = state_amps / np.linalg.norm(state_amps)

        # Fix global phase
        if np.abs(quantum_norm[0]) > 1e-10:
            phase = np.angle(quantum_norm[0]) - np.angle(x_classical_norm[0])
            quantum_norm *= np.exp(-1j * phase)

        fidelity = np.abs(np.dot(np.conj(x_classical_norm), quantum_norm)) ** 2

        fidelities.append(fidelity)
        post_probs.append(post_prob)
        depths.append(qc.depth())

        print(f"  Total qubits: {n_total}")
        print(f"  Circuit depth: {qc.depth()}")
        print(f"  Post-selection probability: {post_prob:.6f}")
        print(f"  Fidelity: {fidelity:.8f}")
        print(f"  Quantum state (normalized): {np.real(quantum_norm)}")

    print(f"\n{'n_clock':>8} {'Fidelity':>12} {'P(post-sel)':>14} {'Depth':>8}")
    print("-" * 44)
    for i, nc in enumerate(n_clock_values):
        print(f"{nc:>8} {fidelities[i]:>12.8f} {post_probs[i]:>14.6f} {depths[i]:>8}")

    return {
        "n_clock_values": n_clock_values,
        "fidelities": fidelities,
        "post_probs": post_probs,
        "depths": depths,
    }


# =============================================================================
# PART C: Visualization
# =============================================================================

def run_part_c(part_a_results, part_b_results):
    """Create visualizations of HHL results."""

    print("\n" + "=" * 70)
    print("PART C: Visualization")
    print("=" * 70)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # ---- Plot 1: Quantum vs Classical solution ----
    ax1 = axes[0]
    x_classical = part_a_results["x_classical"]
    quantum_state = np.real(part_a_results["quantum_state"])
    x_classical_norm = x_classical / np.linalg.norm(x_classical)

    x_pos = np.arange(2)
    width = 0.35

    bars1 = ax1.bar(x_pos - width / 2, np.real(x_classical_norm), width,
                     label="Classical (normalized)", color="#2196F3", alpha=0.8)
    bars2 = ax1.bar(x_pos + width / 2, quantum_state, width,
                     label="Quantum (normalized)", color="#FF5722", alpha=0.8)

    ax1.set_xlabel("Component")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("HHL: Quantum vs Classical Solution")
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(["x[0]", "x[1]"])
    ax1.legend()
    ax1.grid(axis="y", alpha=0.3)

    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.annotate(f"{height:.4f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        ax1.annotate(f"{height:.4f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)

    # ---- Plot 2: Fidelity vs n_clock ----
    ax2 = axes[1]
    n_clocks = part_b_results["n_clock_values"]
    fids = part_b_results["fidelities"]

    ax2.plot(n_clocks, fids, "o-", color="#4CAF50", linewidth=2, markersize=10)
    ax2.set_xlabel("Number of Clock Qubits")
    ax2.set_ylabel("Fidelity")
    ax2.set_title("Fidelity vs Clock Qubits")
    ax2.set_xticks(n_clocks)
    ax2.set_ylim([0.9 * min(fids), 1.02])
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=1.0, color="gray", linestyle="--", alpha=0.5, label="Perfect fidelity")
    ax2.legend()

    for i, (nc, f) in enumerate(zip(n_clocks, fids)):
        ax2.annotate(f"{f:.6f}", xy=(nc, f), xytext=(5, 10),
                     textcoords="offset points", fontsize=9)

    # ---- Plot 3: Post-selection probability and circuit depth ----
    ax3 = axes[2]
    post_probs = part_b_results["post_probs"]
    depths = part_b_results["depths"]

    color1 = "#9C27B0"
    color2 = "#FF9800"

    ln1 = ax3.plot(n_clocks, post_probs, "s-", color=color1, linewidth=2,
                    markersize=10, label="Post-selection prob.")
    ax3.set_xlabel("Number of Clock Qubits")
    ax3.set_ylabel("Post-selection Probability", color=color1)
    ax3.tick_params(axis="y", labelcolor=color1)
    ax3.set_xticks(n_clocks)

    ax3_twin = ax3.twinx()
    ln2 = ax3_twin.plot(n_clocks, depths, "D-", color=color2, linewidth=2,
                         markersize=10, label="Circuit depth")
    ax3_twin.set_ylabel("Circuit Depth", color=color2)
    ax3_twin.tick_params(axis="y", labelcolor=color2)

    lines = ln1 + ln2
    labels = [l.get_label() for l in lines]
    ax3.legend(lines, labels, loc="center right")
    ax3.set_title("Resource Scaling")
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()

    # ---- Save figure ----
    save_path = "quantum/algorithms/19_HHL/hhl_results.png"
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    print(f"\nPlot saved to: {save_path}")
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "#" * 70)
    print("#" + " " * 18 + "HHL ALGORITHM (Local Simulator)" + " " * 19 + "#")
    print("#" + " " * 18 + "Solving Ax = b on a Quantum Computer" + " " * 14 + "#")
    print("#" * 70)

    # ---- Part A ----
    part_a_results = run_part_a()

    # ---- Part B ----
    part_b_results = run_part_b(
        part_a_results["A"],
        part_a_results["b"],
        part_a_results["x_classical"],
    )

    # ---- Part C ----
    run_part_c(part_a_results, part_b_results)

    # ---- SUMMARY ----
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"""
Problem: Ax = b
  A = [[1, -1/3], [-1/3, 1]]
  b = [1, 0]

Classical solution:
  x = [1.125, 0.375]

Eigenvalues of A:
  lambda_1 = 2/3 = 0.6667
  lambda_2 = 4/3 = 1.3333
  Condition number kappa = 2

HHL Parameters:
  t_0 = 3*pi/4 (maps eigenvalues to exact binary phases)
  C = lambda_min = 2/3

QPE Phase Mapping:
  lambda_1 = 2/3 -> phi = 1/4 -> clock |01>
  lambda_2 = 4/3 -> phi = 1/2 -> clock |10>

Results (n_clock=2):
  Fidelity with classical solution: {part_a_results['fidelity']:.8f}
  Post-selection probability: {part_a_results['post_prob']:.6f}

Fidelity scaling with clock qubits:""")

    for i, nc in enumerate(part_b_results["n_clock_values"]):
        print(f"  n_clock={nc}: fidelity={part_b_results['fidelities'][i]:.8f}, "
              f"depth={part_b_results['depths'][i]}")

    print(f"""
Key Observations:
  1. The HHL algorithm correctly recovers the solution ratio x[0]/x[1] = 3
  2. Post-selection probability = {part_a_results['post_prob']:.4f} (theoretical: 5/8 = 0.625)
  3. For this 2x2 system with exact binary phases, n_clock=2 achieves perfect fidelity
  4. Additional clock qubits do not improve fidelity (phases are already exact)
     but they increase circuit depth

Plot saved to: quantum/algorithms/19_HHL/hhl_results.png
""")


if __name__ == "__main__":
    main()
