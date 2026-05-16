"""
Dynamical Decoupling (DD) - Local Simulator Implementation
=============================================================

Demonstrates dynamical decoupling pulse sequences for suppressing
decoherence during idle periods. Compares circuits with and without
DD using noisy simulation with T1/T2 relaxation.

Qiskit Version: 2.4.1

Theoretical Background (see explanation_physicist.md):
------------------------------------------------------
DD inserts identity-equivalent pulse sequences (e.g., XX, XYXY) during
idle periods to refocus quasi-static noise. Average Hamiltonian theory:
the toggling-frame interaction averages to zero under proper DD sequences.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error


# =============================================================================
# NOISE MODEL WITH T1/T2 RELAXATION
# =============================================================================

def create_relaxation_noise_model(
    t1: float = 50e3,      # T1 in nanoseconds (50 us)
    t2: float = 30e3,      # T2 in nanoseconds (30 us)
    gate_time_1q: float = 50.0,   # Single-qubit gate time in ns
    gate_time_2q: float = 300.0,  # Two-qubit gate time in ns
    n_qubits: int = 3
) -> NoiseModel:
    """
    Create a noise model with T1/T2 thermal relaxation.

    Relaxation model (see explanation_physicist.md, Section 2.1):
        T1: energy relaxation (|1> -> |0>), amplitude damping
        T2: phase relaxation (dephasing), T2 <= 2*T1

    The decoherence during idle periods is what DD aims to suppress.

    Args:
        t1: T1 relaxation time in nanoseconds.
        t2: T2 relaxation time in nanoseconds (T2 <= 2*T1).
        gate_time_1q: Single-qubit gate duration in ns.
        gate_time_2q: Two-qubit gate duration in ns.
        n_qubits: Number of qubits.

    Returns:
        NoiseModel with thermal relaxation errors on all gates.
    """
    noise_model = NoiseModel()

    # Single-qubit gate errors from relaxation
    error_1q = thermal_relaxation_error(t1, t2, gate_time_1q)
    for gate in ['x', 'y', 'z', 'h', 'sx', 'rz', 'ry', 'rx', 'id']:
        noise_model.add_all_qubit_quantum_error(error_1q, gate)

    # Two-qubit gate errors from relaxation
    error_2q = thermal_relaxation_error(t1, t2, gate_time_2q).expand(
        thermal_relaxation_error(t1, t2, gate_time_2q)
    )
    noise_model.add_all_qubit_quantum_error(error_2q, 'cx')

    return noise_model


# =============================================================================
# DD PULSE SEQUENCES
# =============================================================================

def insert_hahn_echo(qc: QuantumCircuit, qubit: int, n_idle_slots: int):
    """
    Insert Hahn echo (single X pulse) during idle period.

    Hahn echo (see explanation_physicist.md, Section 3.1):
        |---tau/2---X---tau/2---|
        Refocuses quasi-static Z dephasing.

    Args:
        qc: Circuit to modify in-place.
        qubit: Qubit index for DD.
        n_idle_slots: Number of identity gate slots to fill.
    """
    half = n_idle_slots // 2

    # First half: identity gates (idle time)
    for _ in range(half):
        qc.id(qubit)

    # Echo pulse
    qc.x(qubit)

    # Second half: identity gates
    for _ in range(n_idle_slots - half - 1):
        qc.id(qubit)


def insert_cpmg(qc: QuantumCircuit, qubit: int, n_idle_slots: int, n_pulses: int = 2):
    """
    Insert CPMG sequence (multiple X pulses) during idle period.

    CPMG (see explanation_physicist.md, Section 3.2):
        |---tau/(2n)---[X---tau/n---]^(n-1)---X---tau/(2n)---|
        Multiple echo pulses for broadband noise suppression.

    Args:
        qc: Circuit to modify.
        qubit: Qubit index.
        n_idle_slots: Number of identity gate slots.
        n_pulses: Number of pi pulses.
    """
    if n_idle_slots < n_pulses:
        # Not enough room; fall back to identity
        for _ in range(n_idle_slots):
            qc.id(qubit)
        return

    spacing = n_idle_slots // n_pulses
    remainder = n_idle_slots - n_pulses * spacing

    for p in range(n_pulses):
        # Identity gates before pulse
        n_id = spacing // 2 if p == 0 else spacing - 1
        for _ in range(n_id):
            qc.id(qubit)
        # Pi pulse
        qc.x(qubit)

    # Fill remaining with identity
    remaining = n_idle_slots - n_pulses
    filled = sum(1 for _ in range(n_pulses)) * (spacing // 2 if True else spacing - 1)
    leftover = n_idle_slots - n_pulses - filled
    for _ in range(max(0, leftover)):
        qc.id(qubit)


def insert_xy4(qc: QuantumCircuit, qubit: int, n_idle_slots: int):
    """
    Insert XY-4 sequence during idle period.

    XY-4 (see explanation_physicist.md, Section 3.3):
        X - Y - X - Y
        Self-compensating sequence that suppresses both Z dephasing
        and systematic pulse errors.

    Args:
        qc: Circuit to modify.
        qubit: Qubit index.
        n_idle_slots: Number of identity gate slots.
    """
    if n_idle_slots < 4:
        for _ in range(n_idle_slots):
            qc.id(qubit)
        return

    # XY-4 pattern: space evenly with X-Y-X-Y
    spacing = (n_idle_slots - 4) // 4

    gates = ['x', 'y', 'x', 'y']
    for i, gate_name in enumerate(gates):
        # Identity gates (spacing)
        for _ in range(spacing):
            qc.id(qubit)
        # DD pulse
        if gate_name == 'x':
            qc.x(qubit)
        else:
            qc.y(qubit)

    # Fill remaining
    filled = 4 * spacing + 4
    for _ in range(n_idle_slots - filled):
        qc.id(qubit)


# =============================================================================
# CIRCUIT BUILDERS
# =============================================================================

def build_t2_experiment_no_dd(n_idle_gates: int) -> QuantumCircuit:
    """
    Build a T2-like experiment: prepare |+>, idle, measure in X basis.

    Without DD, the qubit dephases during the idle period.

    Ideal output: <X> = 1 (if no decoherence).
    With dephasing: <X> = exp(-t/T2).

    Args:
        n_idle_gates: Number of identity gates (idle time units).

    Returns:
        Circuit that measures coherence after idle time.
    """
    qr = QuantumRegister(1, 'q')
    cr = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(qr, cr, name=f'no_DD_{n_idle_gates}')

    # Prepare |+>
    qc.h(qr[0])

    # Idle period (identity gates)
    for _ in range(n_idle_gates):
        qc.id(qr[0])

    # Measure in X basis: H then measure
    qc.h(qr[0])
    qc.measure(qr[0], cr[0])

    return qc


def build_t2_experiment_dd(
    n_idle_gates: int,
    dd_type: str = 'xy4'
) -> QuantumCircuit:
    """
    Build T2 experiment with DD sequence during idle time.

    With DD, dephasing is suppressed (see explanation_physicist.md, Section 6.1):
        T2_DD >> T2_free for low-frequency noise.

    Args:
        n_idle_gates: Number of identity gate slots.
        dd_type: DD sequence type ('hahn', 'cpmg', 'xy4').

    Returns:
        Circuit with DD during idle period.
    """
    qr = QuantumRegister(1, 'q')
    cr = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(qr, cr, name=f'{dd_type}_{n_idle_gates}')

    # Prepare |+>
    qc.h(qr[0])

    # Insert DD during idle period
    if dd_type == 'hahn':
        insert_hahn_echo(qc, 0, n_idle_gates)
    elif dd_type == 'cpmg':
        insert_cpmg(qc, 0, n_idle_gates, n_pulses=max(2, n_idle_gates // 10))
    elif dd_type == 'xy4':
        insert_xy4(qc, 0, n_idle_gates)
    else:
        raise ValueError(f"Unknown DD type: {dd_type}")

    # Measure in X basis
    qc.h(qr[0])
    qc.measure(qr[0], cr[0])

    return qc


def build_multi_qubit_circuit_no_dd(n_qubits: int = 3) -> QuantumCircuit:
    """
    Build a multi-qubit circuit with idle qubits (no DD).

    Circuit applies sequential CNOTs, leaving some qubits idle.
    """
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='multi_no_dd')

    # Prepare GHZ state
    qc.h(qr[0])
    for i in range(n_qubits - 1):
        qc.cx(qr[i], qr[i + 1])
        # Qubits 0..i are idle during subsequent CNOTs

    # Add idle time
    for _ in range(20):
        for q in range(n_qubits):
            qc.id(qr[q])

    qc.measure(qr, cr)
    return qc


def build_multi_qubit_circuit_dd(n_qubits: int = 3) -> QuantumCircuit:
    """
    Build multi-qubit circuit with DD on idle qubits.

    Inserts XY-4 sequences on qubits that are idle during CNOTs
    and during the final idle period.
    """
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    qc = QuantumCircuit(qr, cr, name='multi_dd')

    qc.h(qr[0])
    for i in range(n_qubits - 1):
        qc.cx(qr[i], qr[i + 1])

    # DD during idle period
    n_idle = 20
    for q in range(n_qubits):
        insert_xy4(qc, q, n_idle)

    qc.measure(qr, cr)
    return qc


# =============================================================================
# ANALYSIS UTILITIES
# =============================================================================

def counts_to_x_expectation(counts: Dict[str, int]) -> float:
    """
    Extract <X> expectation value from counts in X-basis measurement.

    Since we apply H before measurement, measuring |0> means |+> (X=+1)
    and measuring |1> means |-> (X=-1).

    Args:
        counts: Measurement counts from single-qubit circuit.

    Returns:
        <X> expectation value.
    """
    total = sum(counts.values())
    p0 = counts.get('0', 0) / total
    p1 = counts.get('1', 0) / total
    return p0 - p1  # <X> = P(+) - P(-)


def compute_fidelity_from_counts(
    counts: Dict[str, int],
    ideal_dist: Dict[str, float]
) -> float:
    """
    Compute classical fidelity between measured and ideal distributions.

    F = (sum_x sqrt(p(x) * q(x)))^2

    Args:
        counts: Measured counts.
        ideal_dist: Ideal probability distribution.

    Returns:
        Classical fidelity.
    """
    total = sum(counts.values())
    measured = {k: v / total for k, v in counts.items()}

    all_keys = set(list(measured.keys()) + list(ideal_dist.keys()))
    f = sum(np.sqrt(measured.get(k, 0) * ideal_dist.get(k, 0)) for k in all_keys)
    return f ** 2


# =============================================================================
# DEMONSTRATIONS
# =============================================================================

def demo_t2_extension():
    """
    Demonstrate T2 extension via DD sequences.

    Sweep idle time and compare coherence decay with and without DD.
    Shows that DD suppresses dephasing during idle periods.
    """
    print("=" * 70)
    print("DEMO 1: T2 Extension via Dynamical Decoupling")
    print("=" * 70)

    # Noise model with realistic T1/T2
    t1 = 50000   # 50 us in ns
    t2 = 30000   # 30 us in ns
    gate_time = 50  # ns per gate

    print(f"\n  T1 = {t1/1000:.0f} us, T2 = {t2/1000:.0f} us")
    print(f"  Gate time = {gate_time} ns")

    noise_model = create_relaxation_noise_model(
        t1=t1, t2=t2, gate_time_1q=gate_time, n_qubits=1
    )
    sim = AerSimulator(noise_model=noise_model)

    shots = 10000
    idle_gates_list = [0, 10, 20, 40, 80, 120, 160, 200, 300, 400]

    results = {
        'no_dd': [],
        'hahn': [],
        'xy4': [],
    }

    print(f"\n  Sweeping idle time ({len(idle_gates_list)} points)...")

    for n_idle in idle_gates_list:
        # No DD
        qc_raw = build_t2_experiment_no_dd(n_idle)
        res = sim.run(qc_raw, shots=shots).result()
        x_raw = counts_to_x_expectation(res.get_counts())
        results['no_dd'].append(x_raw)

        # Hahn echo
        qc_hahn = build_t2_experiment_dd(n_idle, 'hahn')
        res = sim.run(qc_hahn, shots=shots).result()
        x_hahn = counts_to_x_expectation(res.get_counts())
        results['hahn'].append(x_hahn)

        # XY-4
        qc_xy4 = build_t2_experiment_dd(n_idle, 'xy4')
        res = sim.run(qc_xy4, shots=shots).result()
        x_xy4 = counts_to_x_expectation(res.get_counts())
        results['xy4'].append(x_xy4)

    # Print table
    idle_times_us = [n * gate_time / 1000 for n in idle_gates_list]
    print(f"\n  {'Idle (us)':<12} {'No DD <X>':<12} {'Hahn <X>':<12} {'XY-4 <X>':<12}")
    print(f"  {'-'*48}")
    for i, t in enumerate(idle_times_us):
        print(f"  {t:<12.1f} {results['no_dd'][i]:<12.4f} {results['hahn'][i]:<12.4f} "
              f"{results['xy4'][i]:<12.4f}")

    return idle_times_us, results


def demo_multi_qubit_dd():
    """
    Demonstrate DD benefit on multi-qubit GHZ circuit.

    Compares GHZ state fidelity with and without DD during idle periods.
    """
    print("\n" + "=" * 70)
    print("DEMO 2: Multi-Qubit DD on GHZ State")
    print("=" * 70)

    n_qubits = 3
    shots = 20000

    noise_model = create_relaxation_noise_model(
        t1=50000, t2=30000, gate_time_1q=50, gate_time_2q=300, n_qubits=n_qubits
    )
    sim = AerSimulator(noise_model=noise_model)

    ideal_dist = {
        '0' * n_qubits: 0.5,
        '1' * n_qubits: 0.5,
    }

    # Without DD
    print(f"\n  Running GHZ-{n_qubits} without DD...")
    qc_no_dd = build_multi_qubit_circuit_no_dd(n_qubits)
    res = sim.run(qc_no_dd, shots=shots).result()
    counts_no_dd = res.get_counts()
    fid_no_dd = compute_fidelity_from_counts(counts_no_dd, ideal_dist)

    total = sum(counts_no_dd.values())
    print(f"  Top outcomes (no DD):")
    for k, v in sorted(counts_no_dd.items(), key=lambda x: -x[1])[:6]:
        print(f"    {k}: {v/total:.4f}")
    print(f"  Fidelity: {fid_no_dd:.4f}")

    # With DD
    print(f"\n  Running GHZ-{n_qubits} with XY-4 DD...")
    qc_dd = build_multi_qubit_circuit_dd(n_qubits)
    res = sim.run(qc_dd, shots=shots).result()
    counts_dd = res.get_counts()
    fid_dd = compute_fidelity_from_counts(counts_dd, ideal_dist)

    total = sum(counts_dd.values())
    print(f"  Top outcomes (with DD):")
    for k, v in sorted(counts_dd.items(), key=lambda x: -x[1])[:6]:
        print(f"    {k}: {v/total:.4f}")
    print(f"  Fidelity: {fid_dd:.4f}")

    print(f"\n  Fidelity improvement: {fid_dd - fid_no_dd:.4f} ({fid_dd/fid_no_dd:.3f}x)")


def demo_dd_sequence_comparison():
    """
    Compare different DD sequences at a fixed idle time.
    """
    print("\n" + "=" * 70)
    print("DEMO 3: DD Sequence Comparison at Fixed Idle Time")
    print("=" * 70)

    n_idle = 100
    gate_time = 50  # ns
    idle_time_us = n_idle * gate_time / 1000

    print(f"\n  Idle time: {idle_time_us:.1f} us ({n_idle} gate slots)")

    noise_model = create_relaxation_noise_model(
        t1=50000, t2=30000, gate_time_1q=gate_time, n_qubits=1
    )
    sim = AerSimulator(noise_model=noise_model)
    shots = 20000

    # Test all DD types plus no DD
    sequences = {
        'No DD': build_t2_experiment_no_dd(n_idle),
        'Hahn Echo': build_t2_experiment_dd(n_idle, 'hahn'),
        'XY-4': build_t2_experiment_dd(n_idle, 'xy4'),
    }

    print(f"\n  {'Sequence':<16} {'<X>':<10} {'|1-<X>| (error)':<16}")
    print(f"  {'-'*42}")
    for name, qc in sequences.items():
        result = sim.run(qc, shots=shots).result()
        x_val = counts_to_x_expectation(result.get_counts())
        error = abs(1 - x_val)
        print(f"  {name:<16} {x_val:<10.4f} {error:<16.4f}")


def demo_filter_function():
    """
    Visualize the filter functions of different DD sequences.

    Filter function (see explanation_physicist.md, Section 4):
        F(omega) determines which noise frequencies are suppressed.
        Small F(omega) = good suppression at frequency omega.
    """
    print("\n" + "=" * 70)
    print("DEMO 4: DD Filter Functions (Visualization)")
    print("=" * 70)

    tau = 1.0  # Total idle time (normalized)
    omega = np.linspace(0.1, 50, 500)

    # Hahn echo filter function (see explanation_physicist.md, Section 3.1)
    F_hahn = 4 * np.sin(omega * tau / 4) ** 2

    # CPMG-4 filter function
    n_cpmg = 4
    F_cpmg = 8 * np.sin(omega * tau / (4 * n_cpmg)) ** 4 / (
        np.cos(omega * tau / (2 * n_cpmg)) ** 2 + 1e-10
    )
    F_cpmg = np.clip(F_cpmg, 0, 100)

    # Free induction decay (no DD)
    F_free = (omega * tau / 2) ** 2  # Approximately

    print(f"  Computing filter functions for omega in [0.1, 50]...")
    print(f"  Hahn echo: F(omega) ~ sin^2(omega*tau/4)")
    print(f"  CPMG-4: F(omega) peaks shifted to higher frequencies")
    print(f"  Free: F(omega) ~ (omega*tau)^2 (no suppression)")

    return omega, F_free, F_hahn, F_cpmg


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_t2_extension(idle_times, results, save_path=None):
    """Plot T2 coherence decay with and without DD."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    ax.plot(idle_times, results['no_dd'], 'ro-', label='No DD', markersize=6)
    ax.plot(idle_times, results['hahn'], 'bs-', label='Hahn Echo', markersize=6)
    ax.plot(idle_times, results['xy4'], 'g^-', label='XY-4', markersize=6)

    ax.set_xlabel('Idle Time (us)')
    ax.set_ylabel(r'$\langle X \rangle$ (coherence)')
    ax.set_title('Dynamical Decoupling: T2 Extension')
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_ylim(-0.1, 1.1)
    ax.axhline(y=0, color='k', linestyle='--', alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"  Figure saved to {save_path}")
    plt.show()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """
    Run all dynamical decoupling demonstrations.

    Covers:
    - T2 extension with Hahn echo and XY-4
    - Multi-qubit GHZ fidelity improvement
    - DD sequence comparison
    - Filter function visualization
    """
    print("Dynamical Decoupling (DD) - Local Demonstrations")
    print("=" * 70)
    print("See explanation_physicist.md for theoretical background.")
    print("See explanation_simple.md for intuitive explanation.")
    print()

    # Demo 1: T2 extension
    idle_times, results = demo_t2_extension()

    # Demo 2: Multi-qubit
    demo_multi_qubit_dd()

    # Demo 3: Sequence comparison
    demo_dd_sequence_comparison()

    # Demo 4: Filter functions
    demo_filter_function()

    # Plot
    print("\n" + "=" * 70)
    print("Generating T2 extension plot...")
    plot_t2_extension(idle_times, results)

    print("\nAll demonstrations complete.")


if __name__ == '__main__':
    main()
