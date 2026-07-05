import numpy as np
import matplotlib.pyplot as plt

# ==================== Data from Figure 3 ====================
solvers = ['MILP\n(exact)', 'GA', 'Tabu', 'SA', 'SQA', 'QAOA\n(p=2)']

# Optimality Gap (%) - Red bars (left axis)
optimality_gap = [2.30, 1.60, 0.48, 0.36, 0.22, 1.53]

# Wall-clock Time (seconds) - Blue bars (right axis)
wall_time = [85, 20, 15, 8, 7, 22]

x = np.arange(len(solvers))  # label locations
width = 0.35  # width of the bars

fig, ax1 = plt.subplots(figsize=(11, 6))

# ==================== Left Axis: Optimality Gap ====================
color_gap = 'tab:red'
bars1 = ax1.bar(x - width/2, optimality_gap, width, label='Optimality Gap (%)', 
                color=color_gap, edgecolor='black', linewidth=1.2)

ax1.set_xlabel('Solver', fontsize=12)
ax1.set_ylabel('Optimality Gap (%)', color=color_gap, fontsize=12)
ax1.tick_params(axis='y', labelcolor=color_gap)
ax1.set_ylim(0, 2.6)

# Add value labels on red bars
for bar in bars1:
    height = bar.get_height()
    ax1.annotate(f'{height:.2f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# ==================== Right Axis: Wall-clock Time ====================
ax2 = ax1.twinx()  # second y-axis sharing the same x-axis
color_time = 'tab:blue'
bars2 = ax2.bar(x + width/2, wall_time, width, label='Wall-clock Time (s)', 
                color=color_time, edgecolor='black', linewidth=1.2, alpha=0.85)

ax2.set_ylabel('Wall-clock Time (s)', color=color_time, fontsize=12)
ax2.tick_params(axis='y', labelcolor=color_time)
ax2.set_ylim(0, 100)

# Add value labels on blue bars
for bar in bars2:
    height = bar.get_height()
    ax2.annotate(f'{int(height)}s',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='darkblue')

# ==================== Title and Formatting ====================
plt.title('Figure 3: Performance of quantum-inspired and classical solvers\n'
          'on tractable sub-instances (N\' = 64 stations, 256 binary variables)', 
          fontsize=13, fontweight='bold', pad=15)

ax1.set_xticks(x)
ax1.set_xticklabels(solvers, fontsize=10)

# Add grid
ax1.grid(True, axis='y', alpha=0.3, linestyle='--')

# Add legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

# Add annotation for best heuristic
ax1.annotate('Best heuristic\n(0.22%)', xy=(3.5, 0.22), xytext=(4.2, 1.2),
            fontsize=10, fontweight='bold', color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.show()
