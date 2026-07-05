import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ==================== Create the Graph ====================
G = nx.Graph()

# Add nodes with labels
G.add_node('G', label='Government')
G.add_node('P', label='Pertamina')
G.add_node('L', label='PLN')

# Add signed edges
# Positive (cooperative) edges
G.add_edge('G', 'P', sign='+', weight=1)
G.add_edge('G', 'L', sign='+', weight=1)

# Negative (competitive) edge
G.add_edge('P', 'L', sign='−', weight=-1)

# ==================== Visualization ====================
plt.figure(figsize=(8, 7))

# Position nodes in a triangle layout
pos = {
    'G': (0, 1.2),      # Top
    'P': (-1, 0),       # Bottom left
    'L': (1, 0)         # Bottom right
}

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2800, 
                       edgecolors='black', linewidths=2)

# Draw node labels
nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold')

# Draw positive edges (solid, green)
positive_edges = [('G', 'P'), ('G', 'L')]
nx.draw_networkx_edges(G, pos, edgelist=positive_edges, 
                       width=3.5, edge_color='green', style='solid')

# Draw negative edge (dashed, red)
negative_edges = [('P', 'L')]
nx.draw_networkx_edges(G, pos, edgelist=negative_edges, 
                       width=3.5, edge_color='red', style='dashed')

# Add edge labels (+ and −)
edge_labels = {('G', 'P'): '+', ('G', 'L'): '+', ('P', 'L'): '−'}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                             font_size=16, font_color='black', 
                             font_weight='bold', label_pos=0.5)

# ==================== Title and Caption ====================
plt.title('Figure 2: A real frustrated but stoquastic coopetition triad', 
          fontsize=14, fontweight='bold', pad=20)

# Add explanatory text box
textstr = '\n'.join([
    'Documented signed relationships among Pertamina (P), PLN (L), and Government (G):',
    '• Government-mandated synergy (positive edges)',
    '• Corporate rivalry (negative edge)',
    '',
    'Sign product around the cycle = negative → Structurally frustrated (F = 1)',
    'However, the induced Hamiltonian is stoquastic (⟨s⟩ ≡ 1)',
    '→ No quantum-exploitable sign problem'
])

props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.85)
plt.text(0.5, -0.35, textstr, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=props, ha='center')

plt.axis('off')
plt.tight_layout()
plt.show()
