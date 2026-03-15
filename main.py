#!/usr/bin/env python3
"""
MapReduce Pipeline: Analyze Uber trip data by hour
python main.py

Pipeline:
1. mapper.py → Extracts hours from trip data
2. Sorting → Groups records by hour
3. reducer.py → Aggregates counts per hour
4. Display & Save results
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

def run_pipeline():
    
    # Setup paths
    base_dir = Path(__file__).parent
    data_file = base_dir / 'data' / 'uber-raw-data-jul14.csv'
    mapper_script = base_dir / 'mapper.py'
    reducer_script = base_dir / 'reducer.py'
    output_dir = base_dir / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # Phase 1: Run mapper
    print("Running mapper...")
    with open(data_file) as f:
        mapper_result = subprocess.run(['python', str(mapper_script)], 
                                      stdin=f, capture_output=True, text=True)
    mapper_output = [line for line in mapper_result.stdout.split('\n') if line]
    print(f"Mapper produced {len(mapper_output)} records")
    
    # Phase 2: Sort by hour
    print("Sorting records by hour...")
    sorted_output = sorted(mapper_output, key=lambda x: int(x.split('\t')[0]))
    print(f"Sorted {len(sorted_output)} records")
    
    # Phase 3: Run reducer
    print("Running reducer...")
    reducer_input = '\n'.join(sorted_output)
    reducer_result = subprocess.run(['python', str(reducer_script)],
                                   input=reducer_input, capture_output=True, text=True)
    reducer_output = [line for line in reducer_result.stdout.split('\n') if line]
    
    # Parse results
    results = {}
    for line in reducer_output:
        parts = line.split('\t')
        if len(parts) == 2:
            hour = parts[0].replace('Hour ', '').replace(':00', '')
            count = int(parts[1])
            results[hour] = count
    print(f"Reducer produced {len(results)} hourly aggregates")
    
    # Save results as JSON
    output_file = output_dir / 'hourly_trips.json'
    total = sum(results.values())
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': results,
            'summary': {'total': total, 'hours': len(results), 'average': total / len(results) if results else 0}
        }, f, indent=2)
    print(f"\nResults saved to: {output_file}")
    
    # Display hourly data
    print("\n" + "="*70)
    print("COMPLETE HOURLY TRIP DATA".center(70))
    print("="*70)
    print(f"{'Hour':<15} {'Trip Count':<20} ")
    print("-"*70)
    
    for hour_str in sorted(results.keys(), key=lambda h: int(h)):
        hour_int = int(hour_str)
        count = results[hour_str]
        print(f"{hour_int:02d}:00{'':<10} {count:>8,} trips")
    
    print("-"*70)
    print(f"{'TOTAL':<15} {total:>8,} trips")
    print("="*70)
    
    # Top 5 peak hours
    print("\nTOP 5 BUSIEST HOURS".center(70))
    print("-"*70)
    sorted_hours = sorted(results.items(), key=lambda x: x[1], reverse=True)[:5]
    for rank, (hour, count) in enumerate(sorted_hours, 1):
        hour_int = int(hour)
        pct = (count / total * 100) if total > 0 else 0
        print(f"  {rank}. Hour {hour_int:02d}:00 - {count:>8,} trips ({pct:.2f}%)")
    print("="*70)
    
if __name__ == '__main__':
    run_pipeline()