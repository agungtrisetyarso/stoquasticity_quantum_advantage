import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from matplotlib.patches import Rectangle

# ==================== Pauli Matrices ====================
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I = np.eye(2, dtype=complex)

def kron(*ops):
    result = ops[0]
    for op in ops[1:]:
        result = np.kron(result, op)
    return result

# ==================== Build 3-qubit Triangle Hamiltonians ====================
def build_triangle_hamiltonian(Jzz=1.0, Jxx=0.0, h=0.0):
    """Build H = sum Jzz * Zi*Zj + sum Jxx * Xi*Xj + h * sum Zi for triangle"""
    # ZZ terms (edges 01, 12, 20)
    H_zz = (Jzz * (kron(Z, Z, I) + kron(I, Z, Z) + kron(Z, I, Z)))
    
    # XX terms
    H_xx = (Jxx * (kron(X, X, I) + kron(I, X, X) + kron(X, I, X)))
    
    # Local field
    H_field = h * (kron(Z, I, I) + kron(I, Z, I) + kron(I, I, Z))
    
    return H_zz + H_xx + H_field

# ==================== Compute Average Sign <s> ====================
def average_sign(H, beta):
    """Compute <s> = Tr(exp(-beta H)) / Tr(exp(-beta |H_offdiag|))"""
    # Stoquastic version (replace off-diagonal with absolute value)
    H_stoq = np.copy(H)
    np.fill_diagonal(H_stoq, 0)           # remove diagonal
    H_stoq = -np.abs(H_stoq)              # make off-diagonal negative
    np.fill_diagonal(H_stoq, np.diag(H))  # restore diagonal
    
    Z = np.trace(expm(-beta * H))
    Z_stoq = np.trace(expm(-beta * H_stoq))
    return Z / Z_stoq

# ==================== Panel (a): <s> vs Inverse Temperature ====================
betas = np.linspace(0.1, 5, 50)

# Model definitions (approximating the paper's M1-M4)
models = {
    'M1: Classical (AF ZZ + field)': build_triangle_hamiltonian(Jzz=-1.0, Jxx=0.0, h=0.5),
    'M2: Single off-diagonal (AF XX)': build_triangle_hamiltonian(Jzz=0.0, Jxx=-1.0, h=0.0),
    'M3: ZZ + XX (both AF)': build_triangle_hamiltonian(Jzz=-1.0, Jxx=-1.0, h=0.0),
    'M4: Heisenberg-like': build_triangle_hamiltonian(Jzz=-1.0, Jxx=-0.5, h=0.0),
}

plt.figure(figsize=(12, 5))

# --- Panel (a) ---
ax1 = plt.subplot(1, 2, 1)
colors = ['green', 'orange', 'red', 'purple']
labels = list(models.keys())

for i, (label, H) in enumerate(models.items()):
    signs = [average_sign(H, b) for b in betas]
    ax1.semilogy(betas, signs, label=label.split(':')[0], color=colors[i], linewidth=2.5)

ax1.set_xlabel('Inverse Temperature β', fontsize=12)
ax1.set_ylabel(r'Average Sign $\langle s \rangle$', fontsize=12)
ax1.set_title('(a) Sign Problem vs Temperature\n(Triangle Motif)', fontsize=13, fontweight='bold')
ax1.legend(fontsize=9, loc='lower left')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(1e-3, 2)

# Add annotation
ax1.annotate('Advantage Band\n(Sign Problem Opens)', xy=(3.5, 0.05), 
             fontsize=10, color='red', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='pink', alpha=0.4))

# --- Panel (b): Curability Classification ---
ax2 = plt.subplot(1, 2, 2)

# Create classification grid
ax2.set_xlim(0, 2)
ax2.set_ylim(0, 2)
ax2.set_xticks([0.5, 1.5])
ax2.set_xticklabels(['Cooperative\nFrustrated', 'Competitive\nFrustrated'], fontsize=10)
ax2.set_yticks([0.5, 1.5])
ax2.set_yticklabels(['No', 'Yes'], fontsize=10)
ax2.set_ylabel('Non-commuting Axes?', fontsize=11)
ax2.set_xlabel('Type of Frustration', fontsize=11)
ax2.set_title('(b) Curability Classification\n(Theorem 3 / 7)', fontsize=13, fontweight='bold')

# Colored regions
ax2.add_patch(Rectangle((0, 0), 1, 1, facecolor='lightgreen', alpha=0.7))   # M1
ax2.add_patch(Rectangle((1, 0), 1, 1, facecolor='lightyellow', alpha=0.7)) # M2
ax2.add_patch(Rectangle((0, 1), 1, 1, facecolor='lightyellow', alpha=0.7)) # M2
ax2.add_patch(Rectangle((1, 1), 1, 1, facecolor='lightcoral', alpha=0.8))  # M3/M4 (Uncurable)

# Labels
ax2.text(0.5, 0.5, 'M1\n(Classical)', ha='center', va='center', fontsize=11, fontweight='bold')
ax2.text(1.5, 0.5, 'M2\n(Curable by\nbasis change)', ha='center', va='center', fontsize=10)
ax2.text(0.5, 1.5, 'M2\n(Curable)', ha='center', va='center', fontsize=10)
ax2.text(1.5, 1.5, 'M3 / M4\n(UNCURABLE)\nQuantum Advantage\nPossible', 
         ha='center', va='center', fontsize=10, fontweight='bold', color='darkred')

ax2.text(1.5, 1.85, 'Advantage Region', ha='center', fontsize=10, 
         color='darkred', fontweight='bold', style='italic')

plt.tight_layout()
plt.show()
