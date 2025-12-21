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
        self.fig, self.ax = plt.subplots(figsize=(12, 9))
        self.cbar = None

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
        self.ax.legend(handles=legend_elements, loc='upper right', title="Wealth Levels")

    def update(self, world, social_ledger, tick):
        """Redraws the world state based on the current tick."""
        self.ax.clear()
        
        # Grid and UI Setup
        self.ax.set_title(f"Tick: {tick} | Social Reputation Map", fontsize=14, pad=20)
        self.ax.set_xlim(-0.5, self.width - 0.5)
        self.ax.set_ylim(-0.5, self.height - 0.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, which='both', color='gray', linestyle='-', linewidth=0.5, alpha=0.1)

        x_coords, y_coords, fame_values, sizes = [], [], [], []

        # Iterate through grid to find agents
        for x in range(self.width):
            for y in range(self.height):
                agent = world.grid[x, y]
                if agent is not None:
                    x_coords.append(x)
                    y_coords.append(y)
                    
                    # Store raw fame value for the colormap
                    fame = social_ledger.get_fame(agent.id)
                    fame_values.append(fame)
                    
                    # Scale point balance to visible dot size
                    size = min(max(agent.points / 2, 10), 400)
                    sizes.append(size)

        if x_coords:
            # IMPORTANT: c=fame_values and cmap='RdYlGn' forces the Red-Yellow-Green scale
            scatter = self.ax.scatter(
                x_coords, y_coords, 
                c=fame_values, 
                s=sizes, 
                edgecolors='black', 
                alpha=0.85, 
                cmap='RdYlGn',
                vmin=0.0,  # Force 0 to be pure Red
                vmax=1.0   # Force 1 to be pure Green
            )
            
            # Initialize or refresh Color Bar
            if self.cbar is None:
                self.cbar = self.fig.colorbar(scatter, ax=self.ax, orientation='vertical', pad=0.05)
                self.cbar.set_label('Social Fame', rotation=270, labelpad=15)
            else:
                self.cbar.update_normal(scatter)

        # Draw the Wealth Legend
        self._add_legend()

        # Update the live figure
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        """Cleanup after simulation ends."""
        plt.ioff()
        plt.show()