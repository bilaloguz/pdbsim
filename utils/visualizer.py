"""
utils/visualizer.py
The "Eye" of the simulation. Renders the social grid with wealth and reputation data.
Updated to strictly use the Red-Yellow-Green (RdYlGn) diverging spectrum.
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# Force interactive backend for Linux environments
try:
    matplotlib.use('TkAgg') 
except:
    pass

class Visualizer:
    def __init__(self, world_size):
        self.width, self.height = world_size
        plt.ion()  # Turn on interactive mode
        
        # Setup Figure with GridSpec: Left=Map, Right=Graphs
        self.fig = plt.figure(figsize=(16, 10))
        gs = self.fig.add_gridspec(3, 2, width_ratios=[1.5, 1])
        
        # 1. The Map (Spans all rows on the left)
        self.ax_map = self.fig.add_subplot(gs[:, 0])
        
        # 2. The Graphs (Stacked on the right)
        self.ax_pop = self.fig.add_subplot(gs[0, 1])
        self.ax_social = self.fig.add_subplot(gs[1, 1])
        self.ax_brain = self.fig.add_subplot(gs[2, 1])
        
        self.cbar = None
        
        # Data History
        self.history_ticks = []
        self.history_pop = []
        self.history_fame = []
        self.history_idl = []
        self.history_hidden = []
        self.history_mem = []

    def _add_legend(self):
        """Creates a custom legend for dot sizes (Wealth/Points)."""
        sizes = [20, 100, 200]
        labels = ["Poor", "Middle", "Wealthy"]
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label=labels[i],
                   markerfacecolor='gray', markersize=np.sqrt(sizes[i]), 
                   markeredgecolor='black')
            for i in range(len(sizes))
        ]
        self.ax_map.legend(handles=legend_elements, loc='upper right', title="Wealth Levels")

    def update(self, world, social_ledger, tick, stats=None):
        """Redraws the world state and updates graphs."""
        
        # --- 1. Draw Map ---
        self.ax_map.clear()
        self.ax_map.set_title(f"Tick: {tick} | Social Reputation Map", fontsize=14)
        self.ax_map.set_xlim(-0.5, self.width - 0.5)
        self.ax_map.set_ylim(-0.5, self.height - 0.5)
        self.ax_map.set_aspect('equal')
        self.ax_map.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5, alpha=0.1)

        x_coords, y_coords, fame_values, sizes = [], [], [], []

        for x in range(self.width):
            for y in range(self.height):
                agent = world.grid[x, y]
                if agent is not None:
                    x_coords.append(x)
                    y_coords.append(y)
                    fame = social_ledger.get_fame(agent.id)
                    fame_values.append(fame)
                    size = min(max(agent.points / 2, 10), 400)
                    sizes.append(size)

        if x_coords:
            scatter = self.ax_map.scatter(
                x_coords, y_coords, 
                c=fame_values, s=sizes, 
                edgecolors='black', alpha=0.85, cmap='RdYlGn', vmin=0.0, vmax=1.0
            )
            
            if self.cbar is None:
                self.cbar = self.fig.colorbar(scatter, ax=self.ax_map, orientation='vertical', pad=0.05)
                self.cbar.set_label('Social Fame', rotation=270, labelpad=15)
            else:
                self.cbar.update_normal(scatter)

        self._add_legend()

        # --- 2. Update Graphs ---
        if stats:
            self.history_ticks.append(tick)
            self.history_pop.append(stats['pop'])
            self.history_fame.append(stats['avg_fame'])
            self.history_idl.append(stats.get('avg_idl', 0.5))
            self.history_hidden.append(stats.get('avg_hidden', 6.0))
            self.history_mem.append(stats.get('avg_mem', 10.0))

            # Plot Population
            self.ax_pop.clear()
            self.ax_pop.plot(self.history_ticks, self.history_pop, color='blue', linewidth=1.5)
            self.ax_pop.set_title("Population Size")
            self.ax_pop.grid(True, alpha=0.3)
            
            # Plot Social Capital (Fame + Ideology)
            self.ax_social.clear()
            self.ax_social.plot(self.history_ticks, self.history_fame, color='green', linewidth=1.5, label='Avg Fame')
            self.ax_social.plot(self.history_ticks, self.history_idl, color='purple', linewidth=1.5, linestyle='--', label='Avg Ideology')
            self.ax_social.set_title("Social Capital (Reputation vs Trust)")
            self.ax_social.set_ylim(0, 1)
            self.ax_social.legend(loc='lower right', fontsize='small')
            self.ax_social.grid(True, alpha=0.3)
            
            # Plot Cognitive Evolution (Neurons + Memory)
            self.ax_brain.clear()
            self.ax_brain.plot(self.history_ticks, self.history_hidden, color='red', linewidth=1.5, label='Neurons')
            self.ax_brain.plot(self.history_ticks, self.history_mem, color='orange', linewidth=1.5, linestyle='--', label='Memory')
            self.ax_brain.set_title("Cognitive Evolution (Neurons vs Memory)")
            self.ax_brain.legend(loc='upper right', fontsize='small')
            self.ax_brain.grid(True, alpha=0.3)

        # Render
        plt.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        """Cleanup after simulation ends."""
        plt.ioff()
        plt.show()