"""
Zero-Noise Extrapolation (ZNE) - IBM Production-Ready Implementation
=====================================================================

Production workflow for ZNE on IBM hardware.
Uses gate folding for noise amplification and exponential extrapolation.

Qiskit Version: 2.4.1
NOT ACTUALLY DEPLOYED.

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
ZNE runs circuits at noise factors lambda = 1, 3, 5, ... via gate
folding (G -> G G^dag G), then extrapolates E(lambda) to lambda=0.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
from scipy.optimize import curve_fit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2, Session

RESULTS_DIR = "quantum/mitigation/05_ZNE/production_results"


# =============================================================================
# GATE FOLDING
# =============================================================================

def fold_circuit(circuit: QuantumCircuit, noise_factor: int) -> QuantumCircuit:
    """
    Global gate folding for noise amplification.

    Folding (see explanation_physicist.md, Section 4.1):
        C_folded = C . (C^dag . C)^k for noise_factor = 2k+1.

    Args:
        circuit: Circuit without measurements.
        noise_factor: Odd integer >= 1.

    Returns:
        Folded circuit.
    """
    if noise_factor == 1:
        return circuit.copy()

    n_folds = (noise_factor - 1) // 2
    folded = circuit.copy()
    for _ in range(n_folds):
        folded = folded.compose(circuit.inverse())
        folded = folded.compose(circuit.copy())
    return folded


# =============================================================================
# EXTRAPOLATION
# =============================================================================

def extrapolate_to_zero(
    noise_factors: List[float],
    values: List[float],
    method: str = 'exponential'
) -> float:
    """
    Extrapolate to zero noise.

    Methods (see explanation_physicist.md, Section 3):
        - linear: E = a + b*lambda
        - exponential: E = A*exp(-B*lambda) + C
        - richardson: optimal linear combination

    Args:
        noise_factors: Noise amplification factors.
        values: Measured expectation values.
        method: Extrapolation method.

    Returns:
        Zero-noise estimate.
    """
    x = np.array(noise_factors)
    y = np.array(values)

    if method == 'linear':
        coeffs = np.polyfit(x, y, 1)
        return float(np.polyval(coeffs, 0))

    elif method == 'exponential':
        def exp_model(lam, a, b, c):
            return a * np.exp(-b * lam) + c
        try:
            popt, _ = curve_fit(exp_model, x, y, p0=[y[0], 0.1, 0], maxfev=5000)
            return float(exp_model(0, *popt))
        except (RuntimeError, ValueError):
            coeffs = np.polyfit(x, y, 1)
            return float(np.polyval(coeffs, 0))

    elif method == 'richardson':
        M = len(x)
        V = np.vander(x, M, increasing=True).T
        rhs = np.zeros(M)
        rhs[0] = 1.0
        try:
            w = np.linalg.solve(V, rhs)
        except np.linalg.LinAlgError:
            w = np.linalg.lstsq(V, rhs, rcond=None)[0]
        return float(w @ y)

    else:
        raise ValueError(f"Unknown method: {method}")


# =============================================================================
# TARGET CIRCUIT
# =============================================================================

def build_target_circuit(n_qubits: int = 3) -> QuantumCircuit:
    """
    Build target circuit for ZNE demonstration.

    GHZ state: ideal <ZZ...Z> = 1.

    Args:
        n_qubits: Number of qubits.

    Returns:
        Circuit without measurements.
    """
    qc = QuantumCircuit(n_qubits)
    qc.h(0)
    for i in range(1, n_qubits):
        qc.cx(0, i)
    return qc


def compute_zz_expectation(counts: Dict[str, int], n_qubits: int) -> float:
    """Compute <ZZ...Z> from measurement counts."""
    total = sum(counts.values())
    exp_val = 0.0
    for bs, count in counts.items():
        parity = sum(int(b) for b in bs.zfill(n_qubits)) % 2
        exp_val += (-1) ** parity * count / total
    return exp_val


# =============================================================================
# PRODUCTION WORKFLOW
# =============================================================================

def run_production_workflow(use_simulator: bool = True):
    """
    Full ZNE production workflow.

    Steps:
        1. Configure backend
        2. Build target circuit
        3. Create folded circuits at each noise level
        4. Transpile and run
        5. Extrapolate to zero noise
        6. Compare methods and save

    Args:
        use_simulator: If True, use noisy AerSimulator.
    """
    print("=" * 70)
    print("Zero-Noise Extrapolation - Production Workflow")
    print("=" * 70)

    n_qubits = 3
    shots = 8192
    noise_factors = [1, 3, 5]

    # -----------------------------------------------------------------
    # Step 1: Backend
    # -----------------------------------------------------------------
    print("\nStep 1: Backend setup")
    if use_simulator:
        noise_model = NoiseModel()
        noise_model.add_all_qubit_quantum_error(depolarizing_error(0.002, 1),
                                                 ['x', 'h', 'sx', 'rz'])
        noise_model.add_all_qubit_quantum_error(depolarizing_error(0.015, 2), ['cx'])
        backend = AerSimulator(noise_model=noise_model)
        print("  AerSimulator with depolarizing noise")
    else:
        # service = QiskitRuntimeService(channel="ibm_quantum")
        # backend = service.least_busy(min_num_qubits=n_qubits)
        # Note: Runtime has built-in ZNE:
        # options.resilience_level = 2
        # options.resilience.zne.noise_factors = [1, 3, 5]
        print("  IBM hardware (commented out)")
        return

    # -----------------------------------------------------------------
    # Step 2: Target circuit
    # -----------------------------------------------------------------
    print(f"\nStep 2: Building GHZ-{n_qubits} target circuit")
    target = build_target_circuit(n_qubits)
    ideal_value = 1.0  # <ZZZ> for GHZ state
    print(f"  Ideal <{'Z'*n_qubits}> = {ideal_value}")

    # -----------------------------------------------------------------
    # Step 3: Create folded circuits
    # -----------------------------------------------------------------
    print(f"\nStep 3: Creating folded circuits at lambda = {noise_factors}")
    folded_circuits = {}
    for lam in noise_factors:
        folded = fold_circuit(target, lam)
        qc_meas = folded.copy()
        qc_meas.measure_all()
        folded_circuits[lam] = qc_meas
        print(f"  lambda={lam}: depth={qc_meas.depth()}")

    # -----------------------------------------------------------------
    # Step 4: Run
    # -----------------------------------------------------------------
    print(f"\nStep 4: Running {len(noise_factors)} circuits ({shots} shots each)")
    noisy_values = []
    for lam in noise_factors:
        qc = folded_circuits[lam]
        if not use_simulator:
            pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
            qc = pm.run(qc)
        result = backend.run(qc, shots=shots).result()
        counts = result.get_counts()
        val = compute_zz_expectation(counts, n_qubits)
        noisy_values.append(val)
        print(f"  lambda={lam}: <{'Z'*n_qubits}> = {val:.6f}")

    # -----------------------------------------------------------------
    # Step 5: Extrapolate
    # -----------------------------------------------------------------
    print("\nStep 5: Extrapolation")
    methods = ['linear', 'exponential', 'richardson']
    results_dict = {}

    print(f"\n  {'Method':<16} {'E_ZNE':<12} {'|Error|':<12} {'Improv.':<10}")
    print(f"  {'-'*50}")

    raw_error = abs(noisy_values[0] - ideal_value)
    for method in methods:
        zne_val = extrapolate_to_zero(noise_factors, noisy_values, method)
        error = abs(zne_val - ideal_value)
        improv = raw_error / error if error > 1e-8 else float('inf')
        print(f"  {method:<16} {zne_val:<12.6f} {error:<12.6f} {improv:<10.1f}x")
        results_dict[method] = zne_val

    print(f"\n  Raw error (lambda=1): {raw_error:.6f}")

    # -----------------------------------------------------------------
    # Step 6: Save
    # -----------------------------------------------------------------
    os.makedirs(RESULTS_DIR, exist_ok=True)
    save_data = {
        "timestamp": datetime.now().isoformat(),
        "n_qubits": n_qubits,
        "shots": shots,
        "noise_factors": noise_factors,
        "noisy_values": noisy_values,
        "ideal_value": ideal_value,
        "zne_results": results_dict,
    }

    filepath = os.path.join(RESULTS_DIR, "zne_results.json")
    with open(filepath, 'w') as f:
        json.dump(save_data, f, indent=2)
    print(f"\n  Results saved to {filepath}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run ZNE production workflow."""
    run_production_workflow(use_simulator=True)


if __name__ == '__main__':
    main()
