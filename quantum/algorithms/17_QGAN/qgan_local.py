"""
Quantum Generative Adversarial Network (QGAN) - Local Simulator
================================================================

Implements a QGAN with quantum generator and classical discriminator
to learn a target probability distribution.

Qiskit Version: 2.4.1

Architecture (see explanation_physicist.md):
    - Generator: parameterized quantum circuit G(theta)|0>
      Produces Born distribution P_G(x) = |<x|G(theta)|0>|^2
    - Discriminator: classical neural network (numpy)
      D(x; phi) -> probability that x is real

Training: alternating optimization of D and G.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import expit as sigmoid

from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector


# =============================================================================
# TARGET DISTRIBUTION
# =============================================================================

def create_target_distribution(n_qubits=3):
    """
    Create a target distribution (log-normal-like on discrete values).

    The generator will learn to produce samples matching this distribution.
    """
    n_states = 2 ** n_qubits
    # Approximate log-normal shape
    x = np.arange(n_states)
    mu, sigma = 1.0, 0.8
    target = np.exp(-(np.log(x + 1) - mu) ** 2 / (2 * sigma ** 2)) / (x + 1)
    target /= target.sum()
    return target


def sample_from_distribution(dist, n_samples):
    """Draw samples from a discrete distribution."""
    return np.random.choice(len(dist), size=n_samples, p=dist)


# =============================================================================
# QUANTUM GENERATOR
# =============================================================================

def build_generator(n_qubits, n_layers=3):
    """
    Build parameterized quantum generator circuit.

    Architecture (see explanation_physicist.md, Section 3.1):
        Layer: R_Y on each qubit + CNOT chain + R_Z on each qubit

    The output state |psi(theta)> defines the Born distribution:
        P_G(x) = |<x|psi(theta)>|^2

    This is a natural probability distribution -- always normalized,
    always non-negative -- unlike classical generators that need
    explicit normalization.
    """
    n_params = n_qubits * 2 * n_layers
    params = ParameterVector('g', n_params)
    qc = QuantumCircuit(n_qubits)

    idx = 0
    for layer in range(n_layers):
        for q in range(n_qubits):
            qc.ry(params[idx], q)
            idx += 1
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
        for q in range(n_qubits):
            qc.rz(params[idx], q)
            idx += 1

    return qc, n_params


def generator_distribution(circuit, param_values):
    """Get the Born distribution from the generator circuit."""
    bound = circuit.assign_parameters(dict(zip(circuit.parameters, param_values)))
    sv = Statevector(bound)
    return sv.probabilities()


# =============================================================================
# CLASSICAL DISCRIMINATOR (numpy NN)
# =============================================================================

class Discriminator:
    """
    Simple feedforward neural network discriminator.

    Architecture: Input(n_states) -> Hidden(16) -> ReLU -> Output(1) -> Sigmoid

    The discriminator D(x) outputs the probability that input x is real.
    Training maximizes: E[log D(real)] + E[log(1 - D(fake))]
    """

    def __init__(self, input_dim, hidden_dim=16, lr=0.01):
        rng = np.random.default_rng(42)
        scale = np.sqrt(2.0 / input_dim)
        self.W1 = rng.normal(0, scale, (input_dim, hidden_dim))
        self.b1 = np.zeros(hidden_dim)
        self.W2 = rng.normal(0, np.sqrt(2.0 / hidden_dim), (hidden_dim, 1))
        self.b2 = np.zeros(1)
        self.lr = lr

    def forward(self, x):
        """Forward pass. x is one-hot encoded."""
        self.z1 = x @ self.W1 + self.b1
        self.a1 = np.maximum(self.z1, 0)  # ReLU
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = sigmoid(self.z2)
        return self.a2

    def train_step(self, x_real_batch, x_fake_batch):
        """
        One training step for the discriminator.

        Loss: -[mean(log D(real)) + mean(log(1 - D(fake)))]
        """
        eps = 1e-8
        # Forward real
        d_real = self.forward(x_real_batch)
        loss_real = -np.mean(np.log(d_real + eps))

        # Backprop real
        dL_da2 = -1.0 / (d_real + eps) / len(x_real_batch)
        da2_dz2 = d_real * (1 - d_real)
        dz2 = dL_da2 * da2_dz2
        dW2_r = self.a1.T @ dz2
        db2_r = np.sum(dz2, axis=0)
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)
        dW1_r = x_real_batch.T @ dz1
        db1_r = np.sum(dz1, axis=0)

        # Forward fake
        d_fake = self.forward(x_fake_batch)
        loss_fake = -np.mean(np.log(1 - d_fake + eps))

        # Backprop fake
        dL_da2 = 1.0 / (1 - d_fake + eps) / len(x_fake_batch)
        da2_dz2 = d_fake * (1 - d_fake)
        dz2 = dL_da2 * da2_dz2
        dW2_f = self.a1.T @ dz2
        db2_f = np.sum(dz2, axis=0)
        da1 = dz2 @ self.W2.T
        dz1 = da1 * (self.z1 > 0)
        dW1_f = x_fake_batch.T @ dz1
        db1_f = np.sum(dz1, axis=0)

        # Update
        self.W1 -= self.lr * (dW1_r + dW1_f)
        self.b1 -= self.lr * (db1_r + db1_f)
        self.W2 -= self.lr * (dW2_r + dW2_f)
        self.b2 -= self.lr * (db2_r + db2_f)

        return loss_real + loss_fake


# =============================================================================
# QGAN TRAINING
# =============================================================================

def one_hot(indices, n_classes):
    """Convert indices to one-hot encoding."""
    result = np.zeros((len(indices), n_classes))
    result[np.arange(len(indices)), indices] = 1.0
    return result


def train_qgan(n_qubits=3, n_layers=3, n_epochs=100, batch_size=32):
    """
    Train the QGAN.

    Alternating training (see explanation_physicist.md, Section 4):
        1. Update discriminator (k_d steps) to better distinguish real vs fake
        2. Update generator (parameter shift) to better fool discriminator

    Generator gradient uses parameter shift rule:
        dL_G/d(theta_j) = (1/2)[L_G(theta_j + pi/2) - L_G(theta_j - pi/2)]
    """
    print(f"\n{'='*70}")
    print(f"QGAN Training ({n_qubits} qubits, {n_layers} layers)")
    print(f"{'='*70}")

    n_states = 2 ** n_qubits
    target = create_target_distribution(n_qubits)

    # Generator
    gen_circuit, n_gen_params = build_generator(n_qubits, n_layers)
    rng = np.random.default_rng(42)
    gen_params = rng.uniform(-np.pi, np.pi, n_gen_params)

    # Discriminator
    disc = Discriminator(n_states, hidden_dim=16, lr=0.01)

    print(f"  Generator params: {n_gen_params}")
    print(f"  Target distribution: {n_states} states")

    # Training loop
    gen_lr = 0.1
    k_d = 3  # Discriminator steps per generator step
    g_loss_history = []
    d_loss_history = []
    kl_history = []

    for epoch in range(n_epochs):
        # --- Discriminator training ---
        d_loss_epoch = 0
        for _ in range(k_d):
            real_samples = sample_from_distribution(target, batch_size)
            real_onehot = one_hot(real_samples, n_states)

            gen_dist = generator_distribution(gen_circuit, gen_params)
            fake_samples = sample_from_distribution(gen_dist, batch_size)
            fake_onehot = one_hot(fake_samples, n_states)

            d_loss = disc.train_step(real_onehot, fake_onehot)
            d_loss_epoch += d_loss

        d_loss_history.append(d_loss_epoch / k_d)

        # --- Generator training (parameter shift) ---
        gen_dist = generator_distribution(gen_circuit, gen_params)
        gen_samples = sample_from_distribution(gen_dist, batch_size)
        gen_onehot = one_hot(gen_samples, n_states)

        eps = 1e-8
        d_fake = disc.forward(gen_onehot)
        g_loss = -np.mean(np.log(d_fake + eps))
        g_loss_history.append(g_loss)

        # Parameter shift gradient for generator
        grad = np.zeros(n_gen_params)
        for j in range(n_gen_params):
            # Shift +pi/2
            params_plus = gen_params.copy()
            params_plus[j] += np.pi / 2
            dist_plus = generator_distribution(gen_circuit, params_plus)
            samples_plus = sample_from_distribution(dist_plus, batch_size)
            oh_plus = one_hot(samples_plus, n_states)
            loss_plus = -np.mean(np.log(disc.forward(oh_plus) + eps))

            # Shift -pi/2
            params_minus = gen_params.copy()
            params_minus[j] -= np.pi / 2
            dist_minus = generator_distribution(gen_circuit, params_minus)
            samples_minus = sample_from_distribution(dist_minus, batch_size)
            oh_minus = one_hot(samples_minus, n_states)
            loss_minus = -np.mean(np.log(disc.forward(oh_minus) + eps))

            grad[j] = (loss_plus - loss_minus) / 2

        gen_params -= gen_lr * grad

        # KL divergence tracking
        gen_dist_current = generator_distribution(gen_circuit, gen_params)
        kl = np.sum(target * np.log((target + eps) / (gen_dist_current + eps)))
        kl_history.append(kl)

        if (epoch + 1) % 20 == 0:
            print(f"  Epoch {epoch+1:3d}: G_loss={g_loss:.4f}, D_loss={d_loss_history[-1]:.4f}, KL={kl:.4f}")

    # Final distribution
    final_dist = generator_distribution(gen_circuit, gen_params)
    final_kl = np.sum(target * np.log((target + eps) / (final_dist + eps)))

    print(f"\nFinal KL divergence: {final_kl:.6f}")
    print(f"\nTarget vs Generated:")
    for i in range(n_states):
        bs = format(i, f'0{n_qubits}b')
        if target[i] > 0.01 or final_dist[i] > 0.01:
            print(f"  |{bs}>: target={target[i]:.4f}, gen={final_dist[i]:.4f}")

    return (target, final_dist, g_loss_history, d_loss_history, kl_history, n_qubits)


# =============================================================================
# VISUALIZATION
# =============================================================================

def plot_results(target, generated, g_losses, d_losses, kl_hist, n_qubits):
    """Visualize QGAN training results."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 11))

    n_states = len(target)
    labels = [format(i, f'0{n_qubits}b') for i in range(n_states)]

    # Distribution comparison
    ax = axes[0, 0]
    x = np.arange(n_states)
    ax.bar(x - 0.2, target, 0.35, label='Target', color='#3498db')
    ax.bar(x + 0.2, generated, 0.35, label='QGAN', color='#e74c3c')
    ax.set_xticks(x)
    ax.set_xticklabels([f'|{l}>' for l in labels], fontsize=8)
    ax.set_ylabel('Probability')
    ax.set_title('Target vs QGAN Distribution', fontsize=13)
    ax.legend()

    # Generator & discriminator loss
    ax = axes[0, 1]
    ax.plot(g_losses, 'b-', alpha=0.7, label='Generator')
    ax.plot(d_losses, 'r-', alpha=0.7, label='Discriminator')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('GAN Training Losses', fontsize=13)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # KL divergence
    ax = axes[1, 0]
    ax.plot(kl_hist, 'g-', linewidth=2)
    ax.set_xlabel('Epoch')
    ax.set_ylabel('KL Divergence')
    ax.set_title('Distribution Convergence', fontsize=13)
    ax.grid(True, alpha=0.3)

    # Per-state error
    ax = axes[1, 1]
    errors = generated - target
    colors = ['#2ecc71' if e >= 0 else '#e74c3c' for e in errors]
    ax.bar(x, errors, color=colors)
    ax.set_xticks(x)
    ax.set_xticklabels([f'|{l}>' for l in labels], fontsize=8)
    ax.set_ylabel('P_gen - P_target')
    ax.set_title('Per-State Probability Error', fontsize=13)
    ax.axhline(y=0, color='k', linewidth=0.5)

    plt.tight_layout()
    plt.savefig("quantum/algorithms/17_QGAN/qgan_results.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nPlot saved to quantum/algorithms/17_QGAN/qgan_results.png")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("Quantum GAN (QGAN) - Local Simulator")
    print("=" * 70)

    results = train_qgan(n_qubits=3, n_layers=3, n_epochs=100, batch_size=32)
    target, generated, g_losses, d_losses, kl_hist, n_q = results

    plot_results(target, generated, g_losses, d_losses, kl_hist, n_q)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    QGAN demonstrated:

    Architecture:
        - Quantum Generator: parameterized circuit producing Born distribution
          P_G(x) = |<x|G(theta)|0>|^2
        - Classical Discriminator: feedforward NN distinguishing real vs fake

    Training:
        - Alternating: update D (k steps) then update G (parameter shift)
        - Generator gradient via parameter shift rule (exact)
        - KL divergence tracks distribution convergence

    Key insights:
        - Born distribution is naturally normalized (quantum advantage)
        - Adversarial training avoids direct KL optimization
        - Mode collapse and training instability remain challenges
    """)


if __name__ == "__main__":
    main()