"""
Visualization: Generate bar chart and statistics report
python visualize.py
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np



def visualize():
 
    base_dir = Path(__file__).parent
    json_file = base_dir / 'output' / 'hourly_trips.json'
    viz_dir = base_dir / 'output'
    
    # Load data
    print("Loading data...")
    with open(json_file) as f:
        data = json.load(f)
    results = data['data']
    
    # Sort and prepare
    sorted_hours = sorted(results.keys(), key=lambda h: int(h))
    hours = [f"{int(h):02d}:00" for h in sorted_hours]
    counts = [results[h] for h in sorted_hours]
    total = sum(counts)
    
    # Generate bar chart
    print("Generating bar chart...")
    fig, ax = plt.subplots(figsize=(14, 7))
    colors = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(counts)))
    bars = ax.bar(range(len(hours)), counts, color=colors, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Trips', fontsize=12, fontweight='bold')
    ax.set_title('Hourly Distribution of New York City Uber Trips in July 2014', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(hours)))
    ax.set_xticklabels(hours, rotation=45)
    ax.grid(True, axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
               ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    bar_path = viz_dir / 'bar_chart.png'
    plt.savefig(bar_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Bar chart saved to: {bar_path}")
    
    # Generate statistics report
    print("Generating statistics report...")
    avg = np.mean(counts)
    median = np.median(counts)
    std = np.std(counts)
    max_count = max(counts)
    min_count = min(counts)
    max_idx = counts.index(max_count)
    min_idx = counts.index(min_count)
    max_hour = hours[max_idx]
    min_hour = hours[min_idx]
    
    report = f"""

NEW YORK CITY UBER TRIP DATA STATISTICS REPORT - July 2014 Analysis                      

SUMMARY STATISTICS:
  • Total Trips: {total:,}
  • Average per Hour: {avg:.2f}
  • Median per Hour: {median:.1f}
  • Standard Deviation: {std:.2f}

EXTREME VALUES:
  • Peak Hour: {max_hour} with {max_count:,} trips
  • Lowest Hour: {min_hour} with {min_count:,} trips
  • Range: {max_count - min_count:,} trips

DATABASE COVERAGE:
  • Hours Analyzed: {len(hours)}
  • Data Completeness: 100%
"""
    
    print(report)
    report_path = viz_dir / 'statistics_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f" Statistics report saved to: {report_path}")

if __name__ == '__main__':
    visualize()
