#!/usr/bin/env python3
"""
Reducer: Aggregates Uber pickup counts by hour of day.
Task: Sum all counts emitted by the Mapper for each hour key.

Input format (sorted key\tvalue from Hadoop shuffle):
  00\t1
  00\t1
  01\t1
  ...

Output format:
  Hour 00:00\t<total_count>
  Hour 01:00\t<total_count>
  ...
  Hour 23:00\t<total_count>
"""

import sys
import logging

# Configure logging to stderr so it does not pollute Hadoop output
logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                    format='%(levelname)s: %(message)s')

current_hour  = None
current_count = 0
total_trips   = 0

# ── Main processing loop ──────────────────────────────────────────────────────
# Hadoop guarantees input is sorted by key, so all records for the same
# hour arrive consecutively.  We just accumulate until the key changes.

for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    try:
        parts = line.split('\t')
        if len(parts) != 2:
            logging.warning(f"Unexpected format (expected 2 fields): {repr(line)}")
            continue

        hour_str, count_str = parts
        hour  = int(hour_str)
        count = int(count_str)

        # Basic validation
        if hour < 0 or hour > 23:
            logging.warning(f"Hour out of range: {hour}")
            continue

    except ValueError as e:
        logging.warning(f"Skipped malformed line: {repr(line)} — {e}")
        continue

    # ── Reducer logic ──
    if current_hour == hour:
        current_count += count          # Same key → accumulate
    else:
        if current_hour is not None:    # Flush previous hour
            print(f"Hour {current_hour:02d}:00\t{current_count}")
            total_trips += current_count
        current_hour  = hour
        current_count = count

# Flush the last hour
if current_hour is not None:
    print(f"Hour {current_hour:02d}:00\t{current_count}")
    total_trips += current_count

logging.warning(f"Reducer done — total trips counted: {total_trips}")
