"""
Parameterized Quantum Circuits & Ansatz Design - Local Simulator
=================================================================

This script explores different PQC architectures available in Qiskit,
analyzing their expressibility, entangling capability, and suitability
for different optimization/ML tasks.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
A PQC has the general form:
    U(theta) = prod_l [ENT_l * ROT_l(theta_l)]

Key properties:
    - Expressibility: how uniformly the PQC covers the Hilbert space
    - Entangling capability: how much entanglement it can generate
    - Trainability: whether gradients vanish (barren plateaus)

We compare: EfficientSU2, RealAmplitudes, TwoLocal, QAOAAnsatz,
            and custom ansatze.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import (
    EfficientSU2,
    RealAmplitudes,
    TwoLocal,
    NLocal,
    ZFeatureMap,
    ZZFeatureMap,
    PauliFeatureMap,
)
from qiskit.quantum_info import Statevector, state_fidelity, partial_trace, DensityMatrix
from qiskit_aer import AerSimulator


def analyze_ansatz(ansatz, name):
    """
    Analyze a given ansatz circuit.

    Reports:
        - Number of parameters
        - Circuit depth
        - Gate count
        - Entangling gate count

    See explanation_physicist.md, Section 3 for architecture details.
    """
    print(f"\n{'='*50}")
    print(f"Ansatz: {name}")
    print(f"{'='*50}")
    print(f"  Qubits: {ansatz.num_qubits}")
    print(f"  Parameters: {ansatz.num_parameters}")
    print(f"  Depth: {ansatz.depth()}")

    ops = dict(ansatz.count_ops())
    total_gates = sum(ops.values())
    two_qubit = sum(v for k, v in ops.items() if k in ['cx', 'cz', 'ecr', 'swap'])
    print(f"  Total gates: {total_gates}")
    print(f"  2-qubit gates: {two_qubit}")
    print(f"  Gate breakdown: {ops}")
    print(f"\n  Circuit diagram:")
    print(ansatz.draw(output="text", fold=80))

    return {
        'name': name,
        'num_params': ansatz.num_parameters,
        'depth': ansatz.depth(),
        'total_gates': total_gates,
        'two_qubit_gates': two_qubit,
    }


def compute_expressibility(ansatz, n_samples=500):
    """
    Estimate expressibility by computing the fidelity distribution
    and comparing with the Haar-random distribution.

    See explanation_physicist.md, Section 4.1.

    For Haar-random states on an n-qubit system, the fidelity distribution is:
        P_Haar(F) = (2^n - 1) * (1 - F)^{2^n - 2}

    We sample random parameter vectors, compute pairwise fidelities,
    and compare the resulting histogram with the Haar distribution.

    Low KL divergence = high expressibility.

    Args:
        ansatz: The PQC to analyze
        n_samples: Number of random parameter samples

    Returns:
        fidelities: Array of pairwise fidelities
        kl_divergence: Approximate KL divergence from Haar distribution
    """
    n = ansatz.num_qubits
    N = 2**n

    fidelities = []
    rng = np.random.default_rng(42)

    for _ in range(n_samples):
        # Generate two random parameter sets
        params1 = rng.uniform(0, 2 * np.pi, ansatz.num_parameters)
        params2 = rng.uniform(0, 2 * np.pi, ansatz.num_parameters)

        # Create states
        qc1 = ansatz.assign_parameters(params1)
        qc2 = ansatz.assign_parameters(params2)

        sv1 = Statevector(qc1)
        sv2 = Statevector(qc2)

        # Compute fidelity F = |<psi1|psi2>|^2
        F = state_fidelity(sv1, sv2)
        fidelities.append(F)

    fidelities = np.array(fidelities)

    # Compute KL divergence from Haar distribution
    # Haar: P(F) = (N-1) * (1-F)^{N-2}
    n_bins = 50
    hist, bin_edges = np.histogram(fidelities, bins=n_bins, range=(0, 1), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Haar reference
    haar_pdf = np.array([(N - 1) * (1 - f)**(N - 2) for f in bin_centers])
    haar_pdf = haar_pdf / (np.sum(haar_pdf) * (bin_edges[1] - bin_edges[0]))

    # KL divergence (with smoothing to avoid log(0))
    eps = 1e-10
    hist_norm = hist / (np.sum(hist) * (bin_edges[1] - bin_edges[0])) + eps
    haar_norm = haar_pdf + eps
    kl_div = np.sum(hist_norm * np.log(hist_norm / haar_norm)) * (bin_edges[1] - bin_edges[0])

    return fidelities, kl_div


def compute_entangling_capability(ansatz, n_samples=200):
    """
    Compute the Meyer-Wallach entanglement measure.

    See explanation_physicist.md, Section 5.1.

    Q = (2/n) * sum_k (1 - Tr(rho_k^2))

    where rho_k is the reduced density matrix of qubit k.

    Q = 0: product state (no entanglement)
    Q = 1: maximally entangled

    Args:
        ansatz: The PQC
        n_samples: Number of random parameter samples

    Returns:
        float: Average Meyer-Wallach entanglement measure
    """
    n = ansatz.num_qubits
    rng = np.random.default_rng(42)

    Q_values = []

    for _ in range(n_samples):
        params = rng.uniform(0, 2 * np.pi, ansatz.num_parameters)
        qc = ansatz.assign_parameters(params)
        sv = Statevector(qc)
        dm = DensityMatrix(sv)

        Q = 0
        for k in range(n):
            # Trace out all qubits except k
            qubits_to_trace = [i for i in range(n) if i != k]
            rho_k = partial_trace(dm, qubits_to_trace)
            purity = np.real(np.trace(rho_k.data @ rho_k.data))
            Q += (1 - purity)

        Q = (2 / n) * Q
        Q_values.append(Q)

    return np.mean(Q_values)


def build_custom_ansatz(num_qubits, reps=1):
    """
    Build a custom ansatz to demonstrate manual PQC construction.

    This creates a "brick-layer" ansatz with:
        - R_Y rotations on all qubits
        - Alternating even-odd and odd-even CNOT pairs
        - This pattern ensures better connectivity coverage

    See explanation_physicist.md, Section 3.

    Args:
        num_qubits: Number of qubits
        reps: Number of repetition layers

    Returns:
        QuantumCircuit: Custom ansatz
    """
    params = ParameterVector('theta', num_qubits * (reps + 1))
    qc = QuantumCircuit(num_qubits)

    param_idx = 0

    # Initial rotation layer
    for i in range(num_qubits):
        qc.ry(params[param_idx], i)
        param_idx += 1

    for rep in range(reps):
        qc.barrier()

        # Even-odd CNOT pairs: (0,1), (2,3), (4,5), ...
        for i in range(0, num_qubits - 1, 2):
            qc.cx(i, i + 1)

        # Odd-even CNOT pairs: (1,2), (3,4), (5,6), ...
        for i in range(1, num_qubits - 1, 2):
            qc.cx(i, i + 1)

        qc.barrier()

        # Rotation layer
        for i in range(num_qubits):
            qc.ry(params[param_idx], i)
            param_idx += 1

    return qc


def demonstrate_feature_maps():
    """
    Demonstrate different feature maps for QML data encoding.

    See explanation_physicist.md, Section 8.
    """
    print("\n" + "=" * 70)
    print("FEATURE MAPS FOR QUANTUM MACHINE LEARNING")
    print("=" * 70)

    num_qubits = 3

    # ZFeatureMap: single-qubit Z rotations
    z_map = ZFeatureMap(feature_dimension=num_qubits, reps=2)
    print(f"\n--- ZFeatureMap ---")
    print(f"Parameters: {z_map.num_parameters}")
    print(f"Depth: {z_map.depth()}")
    print(z_map.draw(output="text", fold=80))

    # ZZFeatureMap: includes ZZ interactions
    zz_map = ZZFeatureMap(feature_dimension=num_qubits, reps=2)
    print(f"\n--- ZZFeatureMap ---")
    print(f"Parameters: {zz_map.num_parameters}")
    print(f"Depth: {zz_map.depth()}")
    print(zz_map.draw(output="text", fold=80))

    # PauliFeatureMap: general Pauli rotations
    pauli_map = PauliFeatureMap(
        feature_dimension=num_qubits,
        paulis=['Z', 'ZZ'],
        reps=1,
    )
    print(f"\n--- PauliFeatureMap ---")
    print(f"Parameters: {pauli_map.num_parameters}")
    print(f"Depth: {pauli_map.depth()}")
    print(pauli_map.draw(output="text", fold=80))


def main():
    print("=" * 70)
    print("Parameterized Quantum Circuits & Ansatz Design (Local Simulator)")
    print("=" * 70)

    num_qubits = 4

    # =========================================================================
    # STEP 1: Survey Qiskit Ansatze
    # =========================================================================

    print("\n--- Step 1: Ansatz Survey ---")

    ansatze = {
        'RealAmplitudes (reps=1)': RealAmplitudes(num_qubits, reps=1),
        'RealAmplitudes (reps=2)': RealAmplitudes(num_qubits, reps=2),
        'EfficientSU2 (reps=1)': EfficientSU2(num_qubits, reps=1),
        'EfficientSU2 (reps=2)': EfficientSU2(num_qubits, reps=2),
        'TwoLocal RY-CZ (reps=2)': TwoLocal(num_qubits, 'ry', 'cz', reps=2),
        'TwoLocal RY+RZ-CX (reps=2)': TwoLocal(num_qubits, ['ry', 'rz'], 'cx',
                                                  entanglement='full', reps=2),
        'Custom Brick (reps=2)': build_custom_ansatz(num_qubits, reps=2),
    }

    stats = []
    for name, ansatz in ansatze.items():
        s = analyze_ansatz(ansatz, name)
        stats.append(s)

    # =========================================================================
    # STEP 2: Expressibility Analysis
    # =========================================================================

    print("\n" + "=" * 70)
    print("Step 2: Expressibility Analysis")
    print("=" * 70)

    # Select a subset for expressibility analysis (expensive computation)
    expr_ansatze = {
        'RealAmplitudes': RealAmplitudes(num_qubits, reps=2),
        'EfficientSU2': EfficientSU2(num_qubits, reps=2),
        'TwoLocal full': TwoLocal(num_qubits, ['ry', 'rz'], 'cx',
                                  entanglement='full', reps=2),
    }

    expr_results = {}
    for name, ansatz in expr_ansatze.items():
        print(f"\n  Computing expressibility for {name}...")
        fids, kl = compute_expressibility(ansatz, n_samples=300)
        expr_results[name] = {'fidelities': fids, 'kl_divergence': kl}
        print(f"    KL divergence from Haar: {kl:.6f}")
        print(f"    (lower = more expressive)")

    # =========================================================================
    # STEP 3: Entangling Capability
    # =========================================================================

    print("\n" + "=" * 70)
    print("Step 3: Entangling Capability")
    print("=" * 70)

    ent_results = {}
    for name, ansatz in expr_ansatze.items():
        print(f"\n  Computing entangling capability for {name}...")
        Q = compute_entangling_capability(ansatz, n_samples=200)
        ent_results[name] = Q
        print(f"    Meyer-Wallach Q = {Q:.4f}")
        print(f"    (0 = no entanglement, 1 = maximal)")

    # =========================================================================
    # STEP 4: Feature Maps for QML
    # =========================================================================

    demonstrate_feature_maps()

    # =========================================================================
    # STEP 5: Visualization
    # =========================================================================

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Parameters vs Depth
    names = [s['name'] for s in stats]
    params = [s['num_params'] for s in stats]
    depths = [s['depth'] for s in stats]

    x_pos = range(len(stats))
    axes[0, 0].bar(x_pos, params, color='steelblue')
    axes[0, 0].set_xticks(x_pos)
    axes[0, 0].set_xticklabels([n.split('(')[0].strip() for n in names],
                                rotation=45, ha='right', fontsize=8)
    axes[0, 0].set_ylabel('Number of Parameters')
    axes[0, 0].set_title('PQC Parameters Comparison', fontsize=13)

    # Plot 2: Circuit depth
    axes[0, 1].bar(x_pos, depths, color='coral')
    axes[0, 1].set_xticks(x_pos)
    axes[0, 1].set_xticklabels([n.split('(')[0].strip() for n in names],
                                rotation=45, ha='right', fontsize=8)
    axes[0, 1].set_ylabel('Circuit Depth')
    axes[0, 1].set_title('PQC Depth Comparison', fontsize=13)

    # Plot 3: Expressibility (fidelity histograms)
    for name, data in expr_results.items():
        axes[1, 0].hist(data['fidelities'], bins=40, alpha=0.5, density=True,
                        label=f"{name} (KL={data['kl_divergence']:.4f})")

    # Haar reference
    N = 2**num_qubits
    f_range = np.linspace(0, 1, 100)
    haar = (N - 1) * (1 - f_range)**(N - 2)
    axes[1, 0].plot(f_range, haar, 'k--', linewidth=2, label='Haar reference')
    axes[1, 0].set_xlabel('Fidelity |<psi1|psi2>|^2')
    axes[1, 0].set_ylabel('Density')
    axes[1, 0].set_title('Expressibility (Fidelity Distribution)', fontsize=13)
    axes[1, 0].legend(fontsize=8)

    # Plot 4: Entangling capability
    ent_names = list(ent_results.keys())
    ent_vals = list(ent_results.values())
    bars = axes[1, 1].bar(ent_names, ent_vals, color=['#3498db', '#2ecc71', '#e74c3c'])
    axes[1, 1].set_ylabel('Meyer-Wallach Q')
    axes[1, 1].set_title('Entangling Capability', fontsize=13)
    axes[1, 1].set_ylim(0, 1)
    for bar, val in zip(bars, ent_vals):
        axes[1, 1].text(bar.get_x() + bar.get_width()/2, val + 0.02,
                        f'{val:.3f}', ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/09_PQC_ansatz_design/pqc_analysis.png",
                dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/09_PQC_ansatz_design/pqc_analysis.png")

    # =========================================================================
    # Summary
    # =========================================================================

    print("\n" + "=" * 70)
    print("ANSATZ SELECTION GUIDE")
    print("=" * 70)
    print("""
    +---------------------+------------------+--------------------+
    | Use Case            | Recommended      | Why                |
    +---------------------+------------------+--------------------+
    | VQE (chemistry)     | EfficientSU2     | Good expressibility|
    |                     | or UCCSD         | Problem-specific   |
    +---------------------+------------------+--------------------+
    | QAOA (optimization) | QAOAAnsatz       | Problem-encoded    |
    +---------------------+------------------+--------------------+
    | QML classification  | Feature map +    | Data-dependent     |
    |                     | RealAmplitudes   | expressibility     |
    +---------------------+------------------+--------------------+
    | General exploration | TwoLocal (full)  | Most expressive    |
    +---------------------+------------------+--------------------+
    | NISQ hardware       | EfficientSU2     | Short depth,       |
    |                     | (reps=1-2)       | hardware-friendly  |
    +---------------------+------------------+--------------------+

    Key trade-offs:
    - More layers = more expressive, but deeper circuits and barren plateaus
    - Full entanglement = more capable, but requires SWAP routing
    - Problem-specific ansatze avoid barren plateaus but limit generality
    """)


if __name__ == "__main__":
    main()
