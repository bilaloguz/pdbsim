from simulation.engine import SimulationEngine
from config import WORLD_SETTINGS, POPULATION_SETTINGS
import time
import sys

def run_verification():
    print("--- BRAIN EVOLUTION VERIFICATION START ---")
    print(f"Goal: Observe if 'AvgHidden' changes over time.")
    
    # Speed up for verification
    POPULATION_SETTINGS["initial_agents"] = 100
    
    engine = SimulationEngine()
    
    # Header
    print(f"{'Tick':<6} | {'Pop':<5} | {'AvgFame':<8} | {'AvgMem':<8} | {'AvgHidden':<9} | {'AvgIdl':<8} |")
    print("-" * 70)

    for t in range(500):
        engine.run_tick()
        
        if t % 50 == 0:
            pop = len(engine.agents)
            if pop > 0:
                avg_fame = sum(engine.social_ledger.get_fame(a.id) for a in engine.agents) / pop
                avg_mem = sum(a.memory_capacity for a in engine.agents) / pop
                # NEW: Track Avg Hidden Neurons
                avg_hidden = sum(a.dna["hidden_size"] for a in engine.agents) / pop
                avg_idl = sum(a.ideology for a in engine.agents) / pop
                
                print(f"{t:<6} | {pop:<5} | {avg_fame:<8.2f} | {avg_mem:<8.1f} | {avg_hidden:<9.1f} | {avg_idl:<8.2f} |")
            else:
                print(f"{t:<6} | 0     | EXTINCT")
                break

if __name__ == "__main__":
    run_verification()
