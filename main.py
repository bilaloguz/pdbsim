"""
main.py
The orchestration script. Runs the simulation, visualizes it, and logs history.
"""
import time
import sys
from simulation.engine import SimulationEngine
from utils.visualizer import Visualizer
from utils.logger import WorldLogger
from config import WORLD_SETTINGS

def get_social_stats(engine):
    pop = len(engine.agents)
    if pop == 0:
        return None

    avg_points = sum(a.points for a in engine.agents) / pop
    avg_fame = sum(engine.social_ledger.get_fame(a.id) for a in engine.agents) / pop
    avg_mem = sum(a.memory_capacity for a in engine.agents) / pop
    avg_idl = sum(a.ideology for a in engine.agents) / pop
    avg_hidden = sum(a.dna["hidden_size"] for a in engine.agents) / pop
    
    return {
        "tick": engine.tick,
        "pop": pop,
        "avg_pts": avg_points,
        "avg_fame": avg_fame,
        "avg_mem": avg_mem,
        "avg_idl": avg_idl,
        "avg_hidden": avg_hidden,
        "total_C": engine.coops_this_tick,
        "total_D": engine.defects_this_tick,
        "total_deaths": engine.deaths_this_tick
    }

def main():
    print("--- SOCIAL SIMULATION STARTING ---")
    engine = SimulationEngine()
    viz = Visualizer(WORLD_SETTINGS["grid_size"])
    logger = WorldLogger()
    
    print(f"Logging to: {logger.get_log_path()}")

    MAX_TICKS = 5000
    try:
        for t in range(MAX_TICKS):
            # 1. Run Engine
            engine.run_tick()
            
            # 2. Handle Statistics
            stats = get_social_stats(engine)
            
            # 3. Update Visualization
            if t % 1 == 0: # Smooth 60fps
                viz.update(engine.world, engine.social_ledger, t, stats)
            
            # 3. Handle Statistics & Logging
            stats = get_social_stats(engine)
            if stats:
                logger.log_tick(stats)
                if t % 5 == 0:
                    status = (f"Tick: {t:04d} | Pop: {stats['pop']:03d} | "
                             f"Avg Fame: {stats['avg_fame']:.2f} | Pts: {stats['avg_pts']:.1f}")
                    sys.stdout.write("\r" + status)
                    sys.stdout.flush()
            else:
                print("\nSocietal Extinction Reached.")
                break
                
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nSimulation interrupted.")
    finally:
        print("\nFinalizing logs...")
        viz.close()

if __name__ == "__main__":
    main()