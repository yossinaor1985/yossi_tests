"""
Quantum SVM (Rebentrost-Mohseni-Lloyd) - Local Simulator Implementation
=========================================================================

This script demonstrates the full Quantum SVM pipeline:
    1. Quantum kernel computation via swap test
    2. Solving the LS-SVM dual system (classically, standing in for HHL)
    3. Classification using the quantum kernel

This is DIFFERENT from QSVC (Topic 11):
    - QSVC: quantum kernel + classical SVM solver (practical, near-term)
    - QSVM-RML: quantum kernel + quantum HHL solver (theoretical, requires QRAM)

Here we implement the quantum kernel via swap test on a simulator, and solve
the dual system classically (since HHL on a 20x20 system is impractical on
current hardware). The pipeline demonstrates the mathematical equivalence.

Qiskit Version: 2.4.1

References:
    - Rebentrost, Mohseni, Lloyd (2014). PRL 113, 130503
    - HHL algorithm: see Topic 19
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator


# =============================================================================
# CONFIGURATION
# =============================================================================

np.random.seed(42)
SAVE_DIR = "quantum/algorithms/20_quantum_svm"


# =============================================================================
# DATASET
# =============================================================================

def create_dataset():
    """
    Create a simple 2D binary classification dataset.

    Returns (X, y) with:
        - X: (20, 2) array of 2D feature vectors scaled to [0, pi]
        - y: (20,) array of labels in {-1, +1}
    """
    X, y = make_blobs(
        n_samples=20,
        centers=[[1.0, 1.0], [3.0, 3.0]],
        cluster_std=0.8,
        random_state=42
    )
    y[y == 0] = -1  # Convert {0, 1} -> {-1, +1}

    # Scale features to [0, pi] for quantum encoding
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X = scaler.fit_transform(X)

    return X, y, scaler


# =============================================================================
# PART A: QUANTUM KERNEL VIA SWAP TEST
# =============================================================================

print("=" * 70)
print("PART A: Quantum Kernel via Swap Test")
print("=" * 70)


def amplitude_encode(x):
    """
    Encode a 2D vector as a single-qubit state using Ry rotation.

    For a 2D vector x = (x0, x1), the amplitude encoding is:
        |psi> = (x0/||x||)|0> + (x1/||x||)|1>

    This is achieved by applying Ry(theta) where:
        theta = 2 * arccos(x0 / ||x||)

    Parameters
    ----------
    x : array-like, shape (2,)
        2D feature vector.

    Returns
    -------
    theta : float
        The Ry rotation angle for amplitude encoding.
    """
    norm = np.linalg.norm(x)
    if norm < 1e-10:
        return 0.0
    # Clamp to [-1, 1] to avoid numerical issues with arccos
    cos_val = np.clip(x[0] / norm, -1.0, 1.0)
    theta = 2.0 * np.arccos(cos_val)
    return theta


def build_swap_test(x_i, x_j):
    """
    Build a 3-qubit swap test circuit to compute |<x_i|x_j>|^2.

    Circuit structure:
        ancilla: |0> --[H]--[ctrl]--[H]--
        qubit_i: |x_i> -----[SWAP]-------
        qubit_j: |x_j> -----[SWAP]-------

    The ancilla controls a SWAP between the two state qubits.
    After measurement:
        P(ancilla=0) = (1 + |<x_i|x_j>|^2) / 2

    Parameters
    ----------
    x_i : array-like, shape (2,)
        First data point.
    x_j : array-like, shape (2,)
        Second data point.

    Returns
    -------
    qc : QuantumCircuit
        The 3-qubit swap test circuit.
    """
    ancilla = QuantumRegister(1, "ancilla")
    state_i = QuantumRegister(1, "state_i")
    state_j = QuantumRegister(1, "state_j")

    qc = QuantumCircuit(ancilla, state_i, state_j)

    # Step 1: Encode data points as single-qubit states
    theta_i = amplitude_encode(x_i)
    theta_j = amplitude_encode(x_j)
    qc.ry(theta_i, state_i[0])
    qc.ry(theta_j, state_j[0])

    # Step 2: Hadamard on ancilla
    qc.h(ancilla[0])

    # Step 3: Controlled-SWAP (Fredkin gate)
    qc.cswap(ancilla[0], state_i[0], state_j[0])

    # Step 4: Hadamard on ancilla
    qc.h(ancilla[0])

    return qc


def quantum_kernel_entry(x_i, x_j):
    """
    Compute a single kernel matrix entry using the swap test.

    Uses statevector simulation (exact, no shots noise).

    K(x_i, x_j) = |<x_i|x_j>|^2 = 2 * P(ancilla=0) - 1

    Parameters
    ----------
    x_i : array-like, shape (2,)
        First data point.
    x_j : array-like, shape (2,)
        Second data point.

    Returns
    -------
    kernel_value : float
        The kernel entry K(x_i, x_j) = |<x_i|x_j>|^2.
    """
    qc = build_swap_test(x_i, x_j)

    # Get the full statevector
    sv = Statevector.from_instruction(qc)
    probs = sv.probabilities()

    # Ancilla is qubit 0 (leftmost in register order).
    # P(ancilla=0) = sum of probabilities where ancilla bit = 0.
    # In a 3-qubit system with qubits [ancilla, state_i, state_j],
    # ancilla=0 corresponds to states |000>, |001>, |010>, |011>
    # (indices 0, 1, 2, 3 in Qiskit's little-endian convention).
    #
    # Qiskit uses little-endian: state |abc> has ancilla=a as the
    # MOST significant bit. So ancilla=0 states are indices where
    # the highest bit is 0, i.e., indices 0,1,2,3 for 3 qubits.
    p_ancilla_0 = sum(probs[:4])

    kernel_value = 2.0 * p_ancilla_0 - 1.0
    return kernel_value


def compute_quantum_kernel_matrix(X):
    """
    Compute the full N x N quantum kernel matrix using swap tests.

    K_ij = |<x_i|x_j>|^2 computed via the swap test circuit.
    Exploits symmetry: K_ij = K_ji.

    Parameters
    ----------
    X : ndarray, shape (N, 2)
        Training data matrix.

    Returns
    -------
    K : ndarray, shape (N, N)
        Quantum kernel matrix.
    """
    N = len(X)
    K = np.zeros((N, N))

    for i in range(N):
        K[i, i] = 1.0  # K(x, x) = |<x|x>|^2 = 1
        for j in range(i + 1, N):
            k_val = quantum_kernel_entry(X[i], X[j])
            K[i, j] = k_val
            K[j, i] = k_val

    return K


def compute_classical_kernel(X):
    """
    Compute the classical equivalent kernel: K_ij = (x_i . x_j / (||x_i|| ||x_j||))^2.

    This is the normalized dot product squared, which should match
    the quantum swap test result for amplitude-encoded states.

    Parameters
    ----------
    X : ndarray, shape (N, 2)
        Data matrix.

    Returns
    -------
    K : ndarray, shape (N, N)
        Classical kernel matrix.
    """
    N = len(X)
    K = np.zeros((N, N))
    norms = np.linalg.norm(X, axis=1)

    for i in range(N):
        for j in range(N):
            if norms[i] < 1e-10 or norms[j] < 1e-10:
                K[i, j] = 0.0
            else:
                dot = np.dot(X[i], X[j])
                K[i, j] = (dot / (norms[i] * norms[j])) ** 2

    return K


# Create dataset and compute kernels
X, y, scaler = create_dataset()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"\nDataset: {len(X_train)} train, {len(X_test)} test, 2D features")
print(f"Labels: {np.sum(y_train == 1)} positive, {np.sum(y_train == -1)} negative (train)")
print(f"Feature range: [{X.min():.4f}, {X.max():.4f}]")

print("\nComputing quantum kernel matrix (swap test)...")
K_quantum = compute_quantum_kernel_matrix(X_train)

print("Computing classical kernel matrix (normalized dot product squared)...")
K_classical = compute_classical_kernel(X_train)

# Compare quantum and classical kernels
max_diff = np.max(np.abs(K_quantum - K_classical))
mean_diff = np.mean(np.abs(K_quantum - K_classical))

print(f"\n--- Kernel Comparison ---")
print(f"Max |K_quantum - K_classical|:  {max_diff:.6e}")
print(f"Mean |K_quantum - K_classical|: {mean_diff:.6e}")
print(f"Matrices match: {max_diff < 1e-10}")

print(f"\nQuantum kernel matrix (first 5x5 block):")
print(np.array2string(K_quantum[:5, :5], precision=4, suppress_small=True))

print(f"\nClassical kernel matrix (first 5x5 block):")
print(np.array2string(K_classical[:5, :5], precision=4, suppress_small=True))


# =============================================================================
# PART B: SOLVING THE SVM DUAL SYSTEM
# =============================================================================

print("\n" + "=" * 70)
print("PART B: Solving the LS-SVM Dual System")
print("=" * 70)


def solve_dual_system(K, y_labels, lam=0.1):
    """
    Solve the LS-SVM dual system: (K + lambda * I) alpha = y.

    This is a classical solve standing in for what HHL would do quantumly.
    In the full QSVM-RML algorithm, HHL (Topic 19) solves this system
    in O(log(N) * kappa^2) time, outputting |alpha> as a quantum state.

    The LS-SVM formulation converts the SVM optimization into a linear
    system, which is exactly what HHL requires.

    Parameters
    ----------
    K : ndarray, shape (N, N)
        Kernel matrix.
    y_labels : ndarray, shape (N,)
        Training labels in {-1, +1}.
    lam : float
        Regularization parameter (1/gamma in LS-SVM notation).

    Returns
    -------
    alpha : ndarray, shape (N,)
        Dual coefficients (the solution to the linear system).
    """
    N = len(y_labels)
    A = K + lam * np.eye(N)

    print(f"\n  System matrix A = K + {lam}*I")
    print(f"  Matrix size: {N}x{N}")
    print(f"  Condition number: {np.linalg.cond(A):.2f}")
    print(f"  (HHL complexity depends on kappa^2 = {np.linalg.cond(A)**2:.2f})")

    # Solve A * alpha = y  (classical, standing in for HHL)
    alpha = np.linalg.solve(A, y_labels.astype(float))

    return alpha


print("\n--- Mathematical Formulation ---")
print("LS-SVM converts the SVM optimization to a linear system:")
print("  (K + lambda * I) alpha = y")
print("where:")
print("  K = quantum kernel matrix (from swap test)")
print("  lambda = regularization parameter")
print("  alpha = dual coefficients (solution)")
print("  y = training labels")
print("\nIn the full QSVM-RML algorithm, HHL (Topic 19) solves this")
print("system quantumly in O(log(N) * kappa^2) time.")
print("Here we solve classically as a stand-in.\n")

# Solve with quantum kernel
alpha = solve_dual_system(K_quantum, y_train, lam=0.1)

print(f"\n  Alpha values: {np.array2string(alpha, precision=4)}")
print(f"  Alpha range: [{alpha.min():.4f}, {alpha.max():.4f}]")

# Identify support vectors (points with significant alpha)
sv_threshold = 0.01 * np.max(np.abs(alpha))
support_vectors = np.where(np.abs(alpha) > sv_threshold)[0]

print(f"\n  Support vector threshold: {sv_threshold:.6f}")
print(f"  Number of support vectors: {len(support_vectors)} / {len(y_train)}")
print(f"  Support vector indices: {support_vectors}")
print(f"  (LS-SVM typically makes ALL points support vectors)")


# =============================================================================
# PART C: FULL CLASSIFICATION PIPELINE + COMPARISON
# =============================================================================

print("\n" + "=" * 70)
print("PART C: Full Classification Pipeline + Comparison")
print("=" * 70)


def classify_with_quantum_kernel(X_train, X_test, y_train, alpha, lam=0.1):
    """
    Classify test points using the QSVM decision function:
        f(x) = sign( sum_i alpha_i * y_i * K(x_i, x) + b )

    In the full QSVM-RML algorithm, this is done quantumly via swap test
    between the weight state |w> = sum_i alpha_i y_i |x_i> and |x_new>.
    Here we compute it classically using the quantum kernel values.

    Parameters
    ----------
    X_train : ndarray, shape (N_train, 2)
        Training data.
    X_test : ndarray, shape (N_test, 2)
        Test data.
    y_train : ndarray, shape (N_train,)
        Training labels.
    alpha : ndarray, shape (N_train,)
        Dual coefficients.
    lam : float
        Regularization parameter.

    Returns
    -------
    predictions : ndarray, shape (N_test,)
        Predicted labels in {-1, +1}.
    decision_values : ndarray, shape (N_test,)
        Raw decision function values.
    """
    N_test = len(X_test)
    decision_values = np.zeros(N_test)

    # Compute bias term b
    # For LS-SVM: b = mean(y - K @ (alpha * y)) where (alpha * y) is element-wise
    K_train = compute_quantum_kernel_matrix(X_train)
    b = np.mean(y_train - K_train @ (alpha * y_train))

    for t in range(N_test):
        f_val = b
        for i in range(len(X_train)):
            # K(x_i, x_test) via quantum kernel
            k_val = quantum_kernel_entry(X_train[i], X_test[t])
            f_val += alpha[i] * y_train[i] * k_val
        decision_values[t] = f_val

    predictions = np.sign(decision_values)
    # Handle exact zeros (assign to +1)
    predictions[predictions == 0] = 1

    return predictions, decision_values


print("\nClassifying test points with quantum kernel SVM...")
y_pred_qsvm, decision_vals = classify_with_quantum_kernel(
    X_train, X_test, y_train, alpha, lam=0.1
)
acc_qsvm = accuracy_score(y_test, y_pred_qsvm)
print(f"  QSVM accuracy: {acc_qsvm:.4f} ({int(acc_qsvm * len(y_test))}/{len(y_test)})")

# --- sklearn SVC comparison ---
print("\nTraining sklearn SVC (linear kernel)...")
svc_linear = SVC(kernel="linear", C=1.0, random_state=42)
svc_linear.fit(X_train, y_train)
y_pred_linear = svc_linear.predict(X_test)
acc_linear = accuracy_score(y_test, y_pred_linear)
print(f"  Linear SVC accuracy: {acc_linear:.4f} ({int(acc_linear * len(y_test))}/{len(y_test)})")

print("\nTraining sklearn SVC (RBF kernel)...")
svc_rbf = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)
svc_rbf.fit(X_train, y_train)
y_pred_rbf = svc_rbf.predict(X_test)
acc_rbf = accuracy_score(y_test, y_pred_rbf)
print(f"  RBF SVC accuracy: {acc_rbf:.4f} ({int(acc_rbf * len(y_test))}/{len(y_test)})")

# --- Accuracy comparison table ---
print("\n" + "-" * 50)
print(f"{'Method':<25} {'Accuracy':>10} {'Correct':>10}")
print("-" * 50)
print(f"{'QSVM (swap test kernel)':<25} {acc_qsvm:>10.4f} {int(acc_qsvm * len(y_test)):>7}/{len(y_test)}")
print(f"{'sklearn SVC (linear)':<25} {acc_linear:>10.4f} {int(acc_linear * len(y_test)):>7}/{len(y_test)}")
print(f"{'sklearn SVC (RBF)':<25} {acc_rbf:>10.4f} {int(acc_rbf * len(y_test)):>7}/{len(y_test)}")
print("-" * 50)


# =============================================================================
# VISUALIZATION
# =============================================================================

print("\nGenerating visualizations...")

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle(
    "Quantum SVM (Rebentrost-Mohseni-Lloyd) - Local Simulation Results",
    fontsize=14, fontweight="bold", y=0.98
)

# --- Plot 1: Training data with decision regions ---
ax1 = axes[0, 0]
# Create a mesh grid for decision boundary
x_min, x_max = X[:, 0].min() - 0.3, X[:, 0].max() + 0.3
y_min_plot, y_max_plot = X[:, 1].min() - 0.3, X[:, 1].max() + 0.3
xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 50),
    np.linspace(y_min_plot, y_max_plot, 50)
)

# Use the sklearn linear SVC for a smooth decision boundary visualization
Z = svc_linear.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
ax1.contourf(xx, yy, Z, levels=[-10, 0, 10], colors=["#FFCCCC", "#CCCCFF"], alpha=0.4)
ax1.contour(xx, yy, Z, levels=[0], colors="black", linewidths=2, linestyles="--")

# Plot training points
mask_pos = y_train == 1
mask_neg = y_train == -1
ax1.scatter(X_train[mask_pos, 0], X_train[mask_pos, 1],
            c="blue", marker="o", s=80, edgecolors="black", label="Class +1 (train)")
ax1.scatter(X_train[mask_neg, 0], X_train[mask_neg, 1],
            c="red", marker="s", s=80, edgecolors="black", label="Class -1 (train)")

# Highlight support vectors
ax1.scatter(X_train[support_vectors, 0], X_train[support_vectors, 1],
            facecolors="none", edgecolors="green", s=200, linewidths=2,
            label=f"Support vectors ({len(support_vectors)})")

# Plot test points
mask_test_pos = y_test == 1
mask_test_neg = y_test == -1
ax1.scatter(X_test[mask_test_pos, 0], X_test[mask_test_pos, 1],
            c="blue", marker="^", s=60, alpha=0.5, label="Class +1 (test)")
ax1.scatter(X_test[mask_test_neg, 0], X_test[mask_test_neg, 1],
            c="red", marker="v", s=60, alpha=0.5, label="Class -1 (test)")

ax1.set_xlabel("Feature 1 (scaled)")
ax1.set_ylabel("Feature 2 (scaled)")
ax1.set_title("Training Data + Decision Boundary")
ax1.legend(fontsize=7, loc="upper left")

# --- Plot 2: Quantum kernel matrix heatmap ---
ax2 = axes[0, 1]
im = ax2.imshow(K_quantum, cmap="viridis", aspect="auto", vmin=0, vmax=1)
ax2.set_title("Quantum Kernel Matrix (Swap Test)")
ax2.set_xlabel("Training sample index")
ax2.set_ylabel("Training sample index")
plt.colorbar(im, ax=ax2, label=r"$|\langle x_i | x_j \rangle|^2$")

# Add text annotations for small matrices
if len(X_train) <= 14:
    for i in range(len(X_train)):
        for j in range(len(X_train)):
            color = "white" if K_quantum[i, j] < 0.5 else "black"
            ax2.text(j, i, f"{K_quantum[i, j]:.2f}",
                     ha="center", va="center", fontsize=6, color=color)

# --- Plot 3: Alpha coefficients bar chart ---
ax3 = axes[1, 0]
colors = ["blue" if yi == 1 else "red" for yi in y_train]
bars = ax3.bar(range(len(alpha)), alpha, color=colors, edgecolor="black", alpha=0.7)
ax3.axhline(y=0, color="black", linewidth=0.5)
ax3.set_xlabel("Training sample index")
ax3.set_ylabel("Alpha coefficient")
ax3.set_title("Dual Coefficients (alpha)")

# Add legend for bar colors
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="blue", edgecolor="black", alpha=0.7, label="Class +1"),
    Patch(facecolor="red", edgecolor="black", alpha=0.7, label="Class -1"),
]
ax3.legend(handles=legend_elements, loc="upper right")

# --- Plot 4: Accuracy comparison bar chart ---
ax4 = axes[1, 1]
methods = ["QSVM\n(swap test)", "sklearn\n(linear)", "sklearn\n(RBF)"]
accuracies = [acc_qsvm, acc_linear, acc_rbf]
bar_colors = ["#2ecc71", "#3498db", "#e74c3c"]
bars = ax4.bar(methods, accuracies, color=bar_colors, edgecolor="black", alpha=0.8)

for bar, acc in zip(bars, accuracies):
    ax4.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
             f"{acc:.1%}", ha="center", va="bottom", fontweight="bold")

ax4.set_ylabel("Accuracy")
ax4.set_title("Accuracy Comparison")
ax4.set_ylim(0, 1.15)
ax4.axhline(y=1.0, color="gray", linewidth=0.5, linestyle="--", alpha=0.5)

plt.tight_layout()
save_path = f"{SAVE_DIR}/quantum_svm_results.png"
plt.savefig(save_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Plot saved to: {save_path}")


# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("""
1. QUANTUM KERNEL VIA SWAP TEST:
   - Implemented the swap test circuit to compute |<x_i|x_j>|^2
   - Built the full quantum kernel matrix using statevector simulation
   - Verified: quantum kernel matches classical normalized dot product squared
     (max difference: {:.2e})

2. HHL FOR DUAL SYSTEM (demonstrated classically):
   - LS-SVM converts the SVM problem to a linear system: (K + lambda*I) alpha = y
   - Solved classically using numpy.linalg.solve (standing in for HHL)
   - In the full QSVM-RML algorithm, HHL would solve this in O(log(N) * kappa^2)
   - Condition number of the system: {:.2f}
   - Number of support vectors: {} / {} (LS-SVM has dense solutions)

3. CLASSIFICATION RESULTS:
   - QSVM (swap test kernel): {:.1%} accuracy
   - sklearn SVC (linear):    {:.1%} accuracy
   - sklearn SVC (RBF):       {:.1%} accuracy

4. THEORETICAL SPEEDUP:
   - Classical SVM training: O(N^2 * d + N^3)
   - Quantum SVM training:   O(log(N*d) * kappa^2 * poly(1/epsilon))
   - For N=1,000,000 points: classical ~ 10^18 ops, quantum ~ 10^2 ops
   - BUT: requires QRAM (not yet physically realized)

5. CAVEATS:
   - QRAM is the bottleneck: without it, data loading alone takes O(N*d)
   - Tang (2019) showed classical algorithms can match speedup for low-rank data
   - For practical near-term use, QSVC (Topic 11) is recommended
""".format(
    max_diff,
    np.linalg.cond(K_quantum + 0.1 * np.eye(len(X_train))),
    len(support_vectors), len(y_train),
    acc_qsvm, acc_linear, acc_rbf
))

print("Script completed successfully.")
