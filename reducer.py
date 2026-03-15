#!/usr/bin/env python3
"""
Reducer
"""

import sys

current_hour = None
current_count = 0

for line in sys.stdin:
    line = line.strip()

    try:
        hour_str, count_str = line.split('\t')
        hour = int(hour_str)
        count = int(count_str)
    except ValueError:
        continue  

    if current_hour == hour:
        current_count += count
    else:
        if current_hour is not None:
            print(f"Hour {current_hour:02d}:00\t{current_count}")
        current_hour = hour
        current_count = count


if current_hour is not None:
    print(f"Hour {current_hour:02d}:00\t{current_count}")