"""
simulation/engine.py
The Orchestrator. Manages the simulation loop, taxes, and life cycles.
"""
import random
from config import WORLD_SETTINGS, GAME_PHYSICS, POPULATION_SETTINGS
from simulation.world import World
from simulation.social import SocialLedger
from simulation.agent import Agent

class SimulationEngine:
    def __init__(self):
        self.world = World()
        self.social_ledger = SocialLedger()
        self.agents = []
        self.tick = 0
        
        # Statistics Trackers (Reset every tick)
        self.deaths_this_tick = 0
        self.coops_this_tick = 0
        self.defects_this_tick = 0
        
        self._seed_population()

    def _seed_population(self):
        count = 0
        while count < POPULATION_SETTINGS["initial_agents"]:
            x = random.randint(0, self.world.width - 1)
            y = random.randint(0, self.world.height - 1)
            if self.world.grid[x, y] is None:
                new_agent = Agent(position=(x, y))
                self.world.place_agent(new_agent, x, y)
                self.agents.append(new_agent)
                count += 1

    def run_tick(self):
        # Reset counters for the new tick
        self.deaths_this_tick = 0
        self.coops_this_tick = 0
        self.defects_this_tick = 0
        
        # 1. Process Actions
        self._process_turn()
        
        # 2. Apply Economic Pressure
        self._apply_taxes()

        # 3. Lifecycle Management
        self._manage_lifecycle()
        
        # 4. Social Maintenance
        self.social_ledger.apply_fame_decay()
        self.tick += 1

    def _process_turn(self):
        active_agents = list(self.agents)
        random.shuffle(active_agents)
        played_this_turn = set()

        for agent in active_agents:
            if agent.id in played_this_turn or not agent.is_alive():
                continue
                
            neighbors = self.world.get_neighbors(*agent.position)
            if not neighbors:
                # If lonely, check for independent movement decision
                if random.random() < agent.dna["mobility_inclination"]:
                    self._handle_movement(agent)
                continue

            neighbor = random.choice(neighbors)
            if neighbor.id in played_this_turn:
                continue

            # --- INDEPENDENT DECISION PHASE ---
            fame_a = self.social_ledger.get_fame(agent.id)
            fame_b = self.social_ledger.get_fame(neighbor.id)

            move_a = agent.decide(neighbor.id, fame_b)
            move_b = neighbor.decide(agent.id, fame_a)

            # --- RESOLUTION PHASE ---
            # Handle Avoidance (Ignore or Move)
            if "IGNORE" in [move_a, move_b] or "MOVE" in [move_a, move_b]:
                if move_a == "MOVE": self._handle_movement(agent)
                if move_b == "MOVE": self._handle_movement(neighbor)
                continue

            # Resolve PD Interaction
            agent.points -= GAME_PHYSICS["interaction_cost"]
            neighbor.points -= GAME_PHYSICS["interaction_cost"]

            payoff_a = GAME_PHYSICS["payoff_matrix"][(move_a, move_b)]
            payoff_b = GAME_PHYSICS["payoff_matrix"][(move_b, move_a)]
            
            agent.points += payoff_a
            neighbor.points += payoff_b

            # Update Counters for Logger
            if move_a == "C": self.coops_this_tick += 1
            else: self.defects_this_tick += 1
            if move_b == "C": self.coops_this_tick += 1
            else: self.defects_this_tick += 1

            # Memory & Ledger Update
            agent.update_memory(neighbor.id, move_b)
            neighbor.update_memory(agent.id, move_a)
            self.social_ledger.record_action(agent.id, move_a)
            self.social_ledger.record_action(neighbor.id, move_b)

            played_this_turn.update([agent.id, neighbor.id])

    def _handle_movement(self, agent):
        new_pos = self.world.find_empty_adjacent(*agent.position)
        if new_pos:
            if self.world.move_agent(agent, new_pos):
                agent.points -= GAME_PHYSICS["movement_tax"]

    def _apply_taxes(self):
        for agent in self.agents:
            # Metabolism
            agent.points -= GAME_PHYSICS["base_existence_tax"]
            # Cognitive Tax
            agent.points -= (agent.dna["memory_capacity"] * GAME_PHYSICS["cognitive_tax_rate"])

    def _manage_lifecycle(self):
        for agent in self.agents[:]:
            # Death Check
            if not agent.is_alive():
                self.world.grid[agent.position[0], agent.position[1]] = None
                self.agents.remove(agent)
                self.deaths_this_tick += 1
                continue
            
            # Reproduction Check
            if agent.points >= POPULATION_SETTINGS["reproduction_threshold"]:
                self._reproduce(agent)

    def _reproduce(self, parent):
        target_pos = self.world.find_empty_adjacent(*parent.position)
        if target_pos:
            child_points = parent.points / 2
            parent.points /= 2
            
            # Inheritance with mutation (logic can be expanded in agent.py)
            child = Agent(position=target_pos, dna=parent.dna.copy())
            child.points = child_points
            
            self.world.place_agent(child, *target_pos)
            self.agents.append(child)