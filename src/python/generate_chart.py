import json
import matplotlib.pyplot as plt
import numpy as np

def create_histogram(data_file='performance_stats.json', output_file='solution_histogram.png'):
    """
    Reads performance data and generates a histogram of solution lengths.
    """
    try:
        with open(data_file, 'r') as f:
            stats = json.load(f)
    except FileNotFoundError:
        print(f"Error: {data_file} not found. Please run the solver to generate stats.")
        # As a fallback, create a sample distribution if no file is found
        print("Generating a sample histogram...")
        move_counts = np.random.normal(loc=19.5, scale=1.5, size=1000)
        move_counts = [int(max(15, min(25, x))) for x in move_counts]
    else:
        move_counts = stats['raw_data']['move_counts']
        if not move_counts:
            print("Error: No move counts found in the data file.")
            return

    # --- Plotting Style ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Determine bins for integer move counts
    min_moves = min(move_counts)
    max_moves = max(move_counts)
    bins = np.arange(min_moves, max_moves + 2) - 0.5

    # Create the histogram
    ax.hist(move_counts, bins=bins, color='#1e3a8a', alpha=0.75, edgecolor='black')

    # --- Labels and Titles ---
    ax.set_title('Distribution of Solution Lengths (N={})'.format(len(move_counts)), fontsize=16, fontweight='bold')
    ax.set_xlabel('Number of Moves to Solve', fontsize=12)
    ax.set_ylabel('Frequency (Number of Solves)', fontsize=12)
    ax.set_xticks(np.arange(min_moves, max_moves + 1))
    ax.grid(axis='y', alpha=0.75)
    
    # Add a vertical line for the average
    avg_moves = np.mean(move_counts)
    ax.axvline(avg_moves, color='#f59e0b', linestyle='dashed', linewidth=2)
    ax.text(avg_moves * 1.01, ax.get_ylim()[1] * 0.9, f'Average: {avg_moves:.2f}', color='#f59e0b', fontweight='bold')

    # --- Save and Show ---
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Histogram saved to {output_file}")
    plt.show()

if __name__ == '__main__':
    create_histogram()

