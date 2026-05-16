"""
CVaR-VQE / CVaR-QAOA - IBM Production-Ready Implementation
=============================================================

This script demonstrates CVaR optimization in a production setting,
using Qiskit's SamplingVQE with CVaR aggregation for IBM hardware.

Qiskit Version: 2.4.1

Production Notes:
    - CVaR is especially valuable on noisy hardware because it
      naturally filters out high-energy (noisy) measurement outcomes
    - The alpha parameter should be tuned based on the noise level
    - On IBM hardware, alpha=0.25-0.5 typically works well
"""

import json
import os
from datetime import datetime

import numpy as np
from qiskit.circuit.library import QAOAAnsatz, EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms.minimum_eigensolvers import SamplingVQE, QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_aer.primitives import SamplerV2 as AerSampler, EstimatorV2 as AerEstimator

# IBM Runtime (uncomment for real hardware)
# from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Session


def build_portfolio_hamiltonian():
    """
    Build a portfolio optimization Hamiltonian.

    Portfolio optimization is a natural application of CVaR because:
        1. CVaR originates from financial risk management
        2. Portfolio selection is a QUBO problem
        3. The "tail focus" of CVaR aligns with risk-averse investing

    Problem: Select assets to maximize return while minimizing risk
    Minimize: mu * (risk) - (1-mu) * (return) + penalty * (constraint violations)

    For 4 assets with simplified parameters:
        H = sum_i r_i Z_i + sum_{i<j} sigma_{ij} Z_i Z_j

    Returns:
        SparsePauliOp: The portfolio Hamiltonian
        dict: Problem metadata
    """
    # Simplified 4-asset portfolio
    returns = [-0.3, 0.2, -0.4, 0.1]    # Negative = good (minimization)
    correlations = {
        (0, 1): 0.15,   # Assets 0,1 positively correlated
        (0, 2): -0.1,   # Assets 0,2 negatively correlated (diversification)
        (1, 3): 0.2,
        (2, 3): -0.05,
    }

    # Risk-return trade-off parameter
    mu = 0.5  # Balance between risk and return

    pauli_list = []
    n = 4

    # Return terms (linear)
    for i, r in enumerate(returns):
        z_str = ["I"] * n
        z_str[n - 1 - i] = "Z"
        pauli_list.append(("".join(z_str), -(1 - mu) * r))

    # Risk terms (quadratic correlations)
    for (i, j), sigma in correlations.items():
        zz_str = ["I"] * n
        zz_str[n - 1 - i] = "Z"
        zz_str[n - 1 - j] = "Z"
        pauli_list.append(("".join(zz_str), mu * sigma))

    hamiltonian = SparsePauliOp.from_list(pauli_list).simplify()

    metadata = {
        "num_assets": n,
        "returns": returns,
        "correlations": {f"({i},{j})": s for (i, j), s in correlations.items()},
        "risk_weight": mu,
    }

    return hamiltonian, metadata


def cvar_aggregation(alpha):
    """
    Create a CVaR aggregation function for SamplingVQE.

    This function is passed to SamplingVQE as the `aggregation` parameter.
    It processes the measurement results to compute CVaR instead of
    the standard expectation value.

    See explanation_physicist.md, Section 2.5.

    Args:
        alpha: CVaR confidence level in (0, 1]

    Returns:
        callable: Aggregation function for SamplingVQE
    """
    def aggregate(measurements):
        """
        Aggregate measurement results using CVaR.

        Args:
            measurements: List of (eigenvalue, probability) tuples

        Returns:
            float: CVaR value
        """
        # Sort by eigenvalue (ascending for minimization)
        sorted_m = sorted(measurements, key=lambda x: x[0])

        # Accumulate probability until we reach alpha
        cumulative_prob = 0.0
        cvar_sum = 0.0

        for eigenvalue, probability in sorted_m:
            if cumulative_prob + probability <= alpha:
                cvar_sum += eigenvalue * probability
                cumulative_prob += probability
            else:
                # Partial contribution for the last sample
                remaining = alpha - cumulative_prob
                cvar_sum += eigenvalue * remaining
                cumulative_prob = alpha
                break

        return cvar_sum / alpha if alpha > 0 else sorted_m[0][0]

    return aggregate


def run_production():
    print("=" * 70)
    print("CVaR Optimization - Production Implementation")
    print("=" * 70)

    # =========================================================================
    # STEP 1: Problem Setup
    # =========================================================================

    print("\n--- Step 1: Portfolio Optimization Problem ---")

    hamiltonian, metadata = build_portfolio_hamiltonian()
    print(f"Assets: {metadata['num_assets']}")
    print(f"Risk weight: {metadata['risk_weight']}")
    print(f"Hamiltonian terms: {len(hamiltonian)}")

    # Exact solution
    n = metadata['num_assets']
    exact_energies = {}
    for x in range(2**n):
        bs = format(x, f'0{n}b')
        from qiskit.quantum_info import Statevector
        state = Statevector.from_label(bs)
        energy = state.expectation_value(hamiltonian).real
        exact_energies[bs] = energy

    exact_min = min(exact_energies.values())
    exact_best = [bs for bs, e in exact_energies.items() if np.isclose(e, exact_min)]

    print(f"\nAll portfolios:")
    for bs in sorted(exact_energies.keys()):
        marker = " <-- OPTIMAL" if bs in exact_best else ""
        assets = [f"A{i}" for i, b in enumerate(bs) if b == '1']
        print(f"  |{bs}> ({', '.join(assets) or 'empty':>12s}): "
              f"E = {exact_energies[bs]:+.4f}{marker}")

    # =========================================================================
    # STEP 2: Compare CVaR levels
    # =========================================================================

    print("\n--- Step 2: CVaR at Multiple Alpha Levels ---")

    sampler = AerSampler()
    estimator = AerEstimator()

    alpha_results = {}

    for alpha in [1.0, 0.5, 0.25, 0.1]:
        print(f"\n  Running SamplingVQE with CVaR alpha={alpha}...")

        ansatz = EfficientSU2(num_qubits=n, reps=2, entanglement="linear")

        # SamplingVQE with CVaR aggregation
        vqe = SamplingVQE(
            sampler=sampler,
            ansatz=ansatz,
            optimizer=COBYLA(maxiter=300),
            aggregation=cvar_aggregation(alpha),
        )

        result = vqe.compute_minimum_eigenvalue(hamiltonian)

        energy = result.eigenvalue.real if hasattr(result.eigenvalue, 'real') else result.eigenvalue
        alpha_results[alpha] = {
            'energy': float(energy),
            'best_measurement': result.best_measurement if hasattr(result, 'best_measurement') else None,
        }

        print(f"    Energy: {energy:.6f}")
        print(f"    Exact min: {exact_min:.6f}")
        print(f"    Error: {abs(energy - exact_min):.6f}")

    # =========================================================================
    # STEP 3: Save Results
    # =========================================================================

    print("\n--- Step 3: Saving Results ---")

    output_dir = "quantum/algorithms/05_cvar_optimization/results"
    os.makedirs(output_dir, exist_ok=True)

    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "algorithm": "CVaR-VQE",
        "qiskit_version": "2.4.1",
        "problem": metadata,
        "exact_solution": {
            "min_energy": float(exact_min),
            "optimal_portfolios": exact_best,
        },
        "cvar_results": {
            str(alpha): {
                "energy": r["energy"],
                "error": abs(r["energy"] - exact_min),
            }
            for alpha, r in alpha_results.items()
        },
    }

    filepath = os.path.join(output_dir, "cvar_results.json")
    with open(filepath, "w") as f:
        json.dump(results_dict, f, indent=2)
    print(f"Results saved to {filepath}")

    # =========================================================================
    # Production Notes
    # =========================================================================

    print("\n" + "=" * 70)
    print("PRODUCTION NOTES")
    print("=" * 70)
    print("""
    CVaR on IBM Hardware:

    1. Alpha Selection Guide:
       - alpha=1.0: standard VQE (baseline)
       - alpha=0.5: good default for most problems
       - alpha=0.25: aggressive, works well for clean signals
       - alpha<0.1: requires many shots for stable estimates

    2. Shot Budget:
       - CVaR needs enough samples in the alpha-tail
       - Minimum shots: N >= 100/alpha (rule of thumb)
       - alpha=0.1 -> need at least 1000 shots
       - alpha=0.01 -> need at least 10000 shots

    3. Noise Interaction:
       - CVaR naturally rejects high-energy noisy samples
       - Acts as implicit error mitigation
       - Synergizes well with TREX (readout error mitigation)

    4. For Real Hardware:
       - Use SamplingVQE with CVaR aggregation
       - Combine with resilience_level=1 (TREX)
       - Use SPSA optimizer (robust to noise)
       - Start with alpha=0.5, adjust based on convergence

    5. Financial Applications:
       - Portfolio optimization (natural CVaR setting)
       - Risk assessment (CVaR quantifies tail risk)
       - Option pricing (focus on extreme scenarios)
    """)


if __name__ == "__main__":
    run_production()
