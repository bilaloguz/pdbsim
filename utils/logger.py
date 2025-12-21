"""
utils/logger.py
Handles the recording of simulation history to a CSV file for post-analysis.
"""
import csv
import os
from datetime import datetime

class WorldLogger:
    def __init__(self, filename=None):
        if filename is None:
            # Create a unique filename based on the current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.filename = f"world_history_{timestamp}.csv"
        else:
            self.filename = filename
            
        self.filepath = os.path.join("logs", self.filename)
        
        # Ensure the logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Define the headers based on our social metrics
        self.headers = [
            "tick", "population", "avg_points", "avg_fame", 
            "avg_memory", "total_cooperations", "total_defections", "total_deaths"
        ]
        
        # Initialize the CSV file with headers
        with open(self.filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    def log_tick(self, stats):
        """Appends a single tick's statistics to the CSV."""
        with open(self.filepath, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                stats.get("tick"),
                stats.get("pop"),
                round(stats.get("avg_pts", 0), 2),
                round(stats.get("avg_fame", 0), 3),
                round(stats.get("avg_mem", 0), 2),
                stats.get("total_C", 0),
                stats.get("total_D", 0),
                stats.get("total_deaths", 0)
            ])

    def get_log_path(self):
        return self.filepath