"""
analyze_history.py
Reads the simulation logs and generates a visual history of the society.
"""
import pandas as pd
import glob
import os
import matplotlib
matplotlib.use('TkAgg')  # Or 'Qt5Agg' if you prefer Qt
import matplotlib.pyplot as plt
def analyze_latest():
    # 1. Find the most recent log file
    list_of_files = glob.glob('logs/*.csv')
    if not list_of_files:
        print("No log files found in /logs")
        return
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"Analyzing: {latest_file}")

    # 2. Load Data
    df = pd.read_csv(latest_file)

    # 3. Create Plots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    plt.subplots_adjust(hspace=0.3)

    # Pane 1: Population and Wealth
    ax1.plot(df['tick'], df['population'], color='blue', label='Population')
    ax1_twin = ax1.twinx()
    ax1_twin.plot(df['tick'], df['avg_points'], color='green', linestyle='--', label='Avg Points')
    ax1.set_ylabel('Population')
    ax1_twin.set_ylabel('Avg Points')
    ax1.set_title('Societal Growth & Wealth')
    ax1.legend(loc='upper left')

    # Pane 2: Social Fame and Intelligence
    ax2.plot(df['tick'], df['avg_fame'], color='gold', linewidth=2, label='Avg Fame')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(df['tick'], df['avg_memory'], color='purple', alpha=0.5, label='Avg Memory')
    ax2.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5) # The Neutral Line
    ax2.set_ylabel('Reputation (0-1)')
    ax2_twin.set_ylabel('Memory Cap')
    ax2.set_title('Behavioral Evolution')
    ax2.legend(loc='upper left')

    # Pane 3: Conflict Density (Interactions)
    ax3.stackplot(df['tick'], df['total_cooperations'], df['total_defections'], 
                  labels=['Coops', 'Defects'], colors=['#99ff99','#ff9999'], alpha=0.8)
    ax3.set_ylabel('Action Counts')
    ax3.set_xlabel('Tick')
    ax3.set_title('Social Dynamics (Action Mix)')
    ax3.legend(loc='upper left')

    plt.show()

if __name__ == "__main__":
    analyze_latest()