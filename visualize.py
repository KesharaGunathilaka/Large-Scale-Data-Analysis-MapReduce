import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def generate_visuals(json_file, output_dir, file_prefix):
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print(f"Loading data from {json_file}...")
    if not json_file.exists():
        print(f"Error: {json_file} not found!")
        return

    with open(json_file) as f:
        data = json.load(f)
    results = data['data']

    # Sort and prepare
    sorted_hours = sorted(results.keys(), key=lambda h: int(h))
    hours = [f"{int(h):02d}:00" for h in sorted_hours]
    counts = [results[h] for h in sorted_hours]
    total = sum(counts)

    # Generate bar chart
    print(f"Generating bar chart for {file_prefix}...")
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(counts)))
    bars = ax.bar(range(len(hours)), counts, color=colors,
                  edgecolor='black', linewidth=0.5)

    ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Trips', fontsize=12, fontweight='bold')
    ax.set_title(
        f'Hourly Distribution - {file_prefix.replace("_", " ").title()}', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(hours)))
    ax.set_xticklabels(hours, rotation=45)
    ax.grid(True, axis='y', alpha=0.3)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    bar_path = output_dir / f'{file_prefix}_bar_chart.png'
    plt.savefig(bar_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Bar chart saved to: {bar_path}")

    # Statistics Report Logic
    avg = np.mean(counts)
    max_count = max(counts)
    max_hour = hours[counts.index(max_count)]

    report = f"""
--- {file_prefix.upper()} STATISTICS ---
Total Trips: {total:,}
Peak Hour: {max_hour} ({max_count:,} trips)
Average: {avg:.2f}
"""
    print(report)
    report_path = output_dir / f'{file_prefix}_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)


if __name__ == '__main__':
    base_dir = Path(__file__).parent

    json_py = base_dir / 'output' / 'hourly_trips.json'
    out_py = base_dir / 'output'
    generate_visuals(json_py, out_py, "hourly")

    json_wsl = base_dir / 'results' / 'output_daily_avg.json'
    out_wsl = base_dir / 'results'
    generate_visuals(json_wsl, out_wsl, "average")
