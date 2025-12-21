"""
config.py
Central repository for all stabilized parameters of the simulation.
"""

# --- World & Geometry Configuration ---
WORLD_SETTINGS = {
    "geometry": "square",       # Options: "square", "torus", "l-shape"
    "grid_size": (40, 40),      # Width, Height
    "transparency": 0.3,        # [0-1] Visibility of true history
    "fame_decay": 0.4,          # [0-1] Speed of reputation expiration
    "fame_radius": 5,           # Moore neighborhood radius for reputation
    "gossip_reliability": 0.5,   # [0-1] Accuracy of reputation transmission
    "initial_fame": 0.4        # Starting fame for unknown agents
}

# --- Game & Economic Physics ---
GAME_PHYSICS = {
    # PD Matrix: (Reward, Temptation, Sucker, Punishment)
    "payoff_matrix": {
        ("C", "C"): 4,
        ("D", "C"): 10,
        ("C", "D"): -6,
        ("D", "D"): -1
    },
    "base_existence_tax": 1.5,
    "cognitive_tax_rate": 0.05, # Cost per unit of memory capacity
    "movement_tax": 0.2,
    "interaction_cost": 0.2     # Fee to engage in a game
}

# --- Population & Evolutionary Rules ---
POPULATION_SETTINGS = {
    "initial_agents": 250,
    "reproduction_threshold": 300,
    "mutation_rate": 0.1,
    "birth_protocol": "displace", # Options: "stay", "displace", "launch"
    "starting_points": 150
}

# --- Default DNA / Character Bounds ---
# These are the ranges used for initial generation and mutation
DNA_BOUNDS = {
    "memory_capacity": (1, 20),
    "mobility_inclination": (0.0, 1.0),
    "trustworthiness": (0.0, 1.0),
    "vengefulness": (0.0, 1.0),
    "social_sensitivity": (0.0, 1.0),
    "hunger_threshold": (10.0, 30.0)
}