"""
simulation/world.py
Manages the spatial grid, agent placement, and neighborhood logic.
"""
import numpy as np
from config import WORLD_SETTINGS

class World:
    def __init__(self):
        self.width, self.height = WORLD_SETTINGS["grid_size"]
        self.geometry = WORLD_SETTINGS["geometry"]
        
        # The grid stores Agent objects. None represents an empty cell.
        self.grid = np.empty((self.width, self.height), dtype=object)
        
    def get_neighbors(self, x, y):
        """
        Returns a list of agents in the Moore neighborhood (8 surrounding cells).
        Handles geometry logic (Torus vs. Square).
        """
        neighbors = []
        # Moore neighborhood offsets: -1 to +1 in both axes
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                nx, ny = x + dx, y + dy
                
                # Apply Geometry Logic
                if self.geometry == "torus":
                    # Wrap around
                    nx %= self.width
                    ny %= self.height
                else:  # "square" or "l-shape" (bounds checking)
                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue
                
                agent = self.grid[nx, ny]
                if agent is not None:
                    neighbors.append(agent)
                    
        return neighbors

    def find_empty_adjacent(self, x, y):
        """Finds a random empty cell neighboring (x, y). Returns None if full."""
        import random
        candidates = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                
                nx, ny = x + dx, y + dy
                
                # Wrap or Bound check
                if self.geometry == "torus":
                    nx %= self.width; ny %= self.height
                elif not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                
                if self.grid[nx, ny] is None:
                    candidates.append((nx, ny))
        
        return random.choice(candidates) if candidates else None

    def move_agent(self, agent, new_pos):
        """Updates the grid state when an agent moves."""
        old_x, old_y = agent.position
        new_x, new_y = new_pos
        
        if self.grid[new_x, new_y] is None:
            self.grid[old_x, old_y] = None
            self.grid[new_x, new_y] = agent
            agent.position = (new_x, new_y)
            return True
        return False

    def place_agent(self, agent, x, y):
        """Initial placement of an agent."""
        if self.grid[x, y] is None:
            self.grid[x, y] = agent
            return True
        return False