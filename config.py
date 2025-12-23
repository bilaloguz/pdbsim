"""
config.py
Central repository for all stabilized parameters of the simulation.
"""

# --- World & Geometry Configuration ---
WORLD_SETTINGS = {
    "geometry": "square",       # Options: "square", "torus", "l-shape"
    "grid_size": (50, 50),      # Width, Height
    "transparency": 0.5,        # [0-1] Visibility of true history
    "fame_decay": 0.5,          # [0-1] Speed of reputation expiration
    "fame_radius": 10,           # Moore neighborhood radius for reputation
    "gossip_reliability": 0.5,   # [0-1] Accuracy of reputation transmission
    "initial_fame": 0.5        # Starting fame for unknown agents
}

# --- Game & Economic Physics ---
GAME_PHYSICS = {
    # PD Matrix: (Reward, Temptation, Sucker, Punishment)
    "payoff_matrix": {
        ("C", "C"): 5,
        ("D", "C"): 10,
        ("C", "D"): -10,
        ("D", "D"): -1
    },
    "base_existence_tax": 0.1,
    "cognitive_tax_rate": 0.01, # Cost per unit of memory capacity
    "brain_complexity_tax": 0.01, # Cost per hidden neuron
    "movement_tax": 0.1,
    "interaction_cost": 0.01,    # Fee to engage in a game
    "migration_tax": 1        # Cost to colonize distant lands (Launch protocol)
}

# --- Population & Evolutionary Rules ---
POPULATION_SETTINGS = {
    "initial_agents": 100,
    "reproduction_threshold": 150,
    "mutation_rate": 0.1,
    "birth_protocol": "launch", # Options: "stay", "displace", "launch"
    "starting_points": 149,
    "max_age": 100             # Maximum lifespan in ticks
}

# --- Default DNA / Character Bounds ---
# These are the ranges used for initial generation and mutation
# --- Neural Network / Brain Configuration ---
BRAIN_SETTINGS = {
    "input_size": 6,      # [MyPts, MyAge, OppFame, OppHistory, Bias, Ideology]
    "min_hidden": 2,      # Minimum neurons in hidden layer
    "max_hidden": 20,     # Maximum neurons in hidden layer
    "output_size": 4,     # [Prob_Coop, Prob_Defect, Prob_Move, Prob_Ignore]
    "mutation_power": 0.1, # Standard deviation of Gaussian noise added to weights
    "mutation_rate": 0.1   # Probability of a weight being mutated
}