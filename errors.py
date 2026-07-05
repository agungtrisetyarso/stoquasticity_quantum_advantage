import numpy as np
import matplotlib.pyplot as plt

# ==================== Data from Figure 4 ====================
solvers = ['GA', 'Tabu', 'SA', 'SQA']

# Mean best QUBO objective value (lower is better)
# Approximated from the figure
mean_objective = [-0.05, -0.35, -0.85, -1.15]   # Approximate values

# Standard deviation (error bars)
std_dev = [0.08, 0.12, 0.06, 0.05]               # Approximate std

x = np.arange(len(solvers))

fig, ax = plt.subplots(figsize=(10, 6))

# ==================== Bar Plot with Error Bars ====================
colors = ['#6a5acd', '#8b4513', '#ff8c00', '#32cd32']  # Purple, Brown, Orange, Green

bars = ax.bar(x, mean_objective, yerr=std_dev, capsize=8, 
              color=colors, edgecolor='black', linewidth=1.5,
              error_kw={'linewidth': 2, 'capthick': 2})

# ==================== Formatting ====================
ax.set_ylabel('Best QUBO Objective Value\n(lower is better)', fontsize=12)
ax.set_xlabel('Solver', fontsize=12)
ax.set_title('Figure 4: Full-scale solution quality on instances with\n'
             'N = 13,603 stations (54,412 binary variables)\n'
             'Mean ± Std Dev over 5 independent random seeds', 
             fontsize=13, fontweight='bold', pad=15)

ax.set_xticks(x)
ax.set_xticklabels(solvers, fontsize=11)

# Add value labels on top of bars
for bar, mean, std in zip(bars, mean_objective, std_dev):
    height = bar.get_height()
    ax.annotate(f'{mean:.2f}\n±{std:.2f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 12),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# Add grid
ax.grid(True, axis='y', alpha=0.3, linestyle='--')

# ==================== Highlight SQA and add annotation ====================
# Make SQA bar stand out more
bars[3].set_edgecolor('darkgreen')
bars[3].set_linewidth(3)

# Annotation showing SQA improvement
ax.annotate('SQA: -0.3% better\nthan GA (on average)', 
            xy=(3, mean_objective[3]), 
            xytext=(2.2, mean_objective[3] - 0.6),
            fontsize=11, fontweight='bold', color='darkgreen',
            arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2),
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.9))

ax.set_ylim(min(mean_objective) - 0.8, max(mean_objective) + 0.3)

plt.tight_layout()
plt.show()
