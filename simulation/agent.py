"""
simulation/agent.py
Defines the Agent class with DNA-based traits and a four-mode 
utility-driven decision engine (Cooperate, Defect, Move, Ignore).
"""
import uuid
import random
from config import POPULATION_SETTINGS, DNA_BOUNDS, GAME_PHYSICS

class Agent:
    def __init__(self, position, dna=None):
        # 1. Identity & State
        self.id = uuid.uuid4()
        self.points = POPULATION_SETTINGS["starting_points"]
        self.position = position  # (x, y) tuple
        
        # 2. DNA (The Genetic Baseline)
        if dna is None:
            self.dna = self._generate_random_dna()
        else:
            self.dna = dna
            
        # 3. Memory (Private Experience)
        # { opponent_id: ['C', 'D', ...] }
        self.private_memory = {}
        
    def _generate_random_dna(self):
        """Initializes agent traits within the bounds defined in config.py."""
        return {
            "memory_capacity": random.randint(*DNA_BOUNDS["memory_capacity"]),
            "mobility_inclination": random.uniform(*DNA_BOUNDS["mobility_inclination"]),
            "trustworthiness": random.uniform(*DNA_BOUNDS["trustworthiness"]),
            "vengefulness": random.uniform(*DNA_BOUNDS["vengefulness"]),
            "social_sensitivity": random.uniform(*DNA_BOUNDS["social_sensitivity"]),
            "hunger_threshold": random.uniform(*DNA_BOUNDS["hunger_threshold"])
        }

    def update_memory(self, opponent_id, move):
        """Adds a move to private memory, respecting memory capacity (Cognitive Tax)."""
        if opponent_id not in self.private_memory:
            self.private_memory[opponent_id] = []
        
        history = self.private_memory[opponent_id]
        history.append(move)
        
        # Prune oldest memory if capacity exceeded
        if len(history) > self.dna["memory_capacity"]:
            history.pop(0)

    def decide(self, opponent_id, opponent_fame):
        """
        The 'Independent Brain'. Calculates the utility of acting 
        based on DNA, Social Fame, and Survival Pressure.
        """
        # 1. Calculate Survival Pressure (Hunger)
        # 0 = Safe, 1 = Desperate (about to die)
        hunger_level = 0
        if self.points < self.dna["hunger_threshold"]:
            hunger_level = 1 - (self.points / self.dna["hunger_threshold"])

        # 2. Evaluate Trust based on Private Memory and Social Fame
        trust_score = self._evaluate_trust(opponent_id, opponent_fame)

        # 3. Independent Thinking Overrides
        # If starving, the utility of 'Defect' (stealing) is extremely high
        if hunger_level > 0.85:
            return "D" if random.random() < 0.9 else "MOVE"

        # 4. Standard Decision Logic based on Weighted Traits
        # P(C) is influenced by internal trustworthiness and external trust_score
        # Weighted by Social Sensitivity (how much they care about fame/reputation)
        base_trust = self.dna["trustworthiness"]
        sensitivity = self.dna["social_sensitivity"]
        
        # Combined probability of cooperating
        prob_cooperate = (base_trust * (1 - sensitivity)) + (trust_score * sensitivity)

        # Apply a 'Whim' (5% chance of unpredictable social behavior)
        if random.random() < 0.05:
            return random.choice(["C", "D", "MOVE", "IGNORE"])

        # Final Action Selection
        if prob_cooperate > 0.7:
            return "C"
        elif prob_cooperate < 0.2:
            # If I distrust you deeply, do I flee or just ostracize you?
            # Decision depends on current points vs cost of moving
            if self.points > (GAME_PHYSICS["movement_tax"] * 2):
                return "MOVE"
            return "IGNORE"
        elif 0.2 <= prob_cooperate < 0.45:
            return "D" # Low trust leads to pre-emptive defection
        else:
            return "IGNORE" # Default to 'Social Avoidance' for safety

    def _evaluate_trust(self, opponent_id, opponent_fame):
        """Combines social reputation with personal 'grudges' from memory."""
        # Start with the public 'Fame'
        score = opponent_fame 

        # If we have met this specific agent before, use our private record
        if opponent_id in self.private_memory:
            history = self.private_memory[opponent_id]
            private_ratio = history.count("C") / len(history)
            
            # Use 'Vengefulness' trait to weigh private experience over public fame
            v = self.dna["vengefulness"]
            score = (score * (1 - v)) + (private_ratio * v)

        return score

    def is_alive(self):
        return self.points > 0

    def __repr__(self):
        return f"<Agent {self.id.hex[:4]} | Pts: {self.points:.1f} | Pos: {self.position}>"