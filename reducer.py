#Reducer: Aggregates trip counts by hour.

import sys
import logging

# Configure logging 
logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                    format='%(levelname)s: %(message)s')

current_hour  = None
current_count = 0
total_trips   = 0

# Main processing loop 
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

    # Reducer logic
    if current_hour == hour:
        current_count += count         
    else:
        if current_hour is not None:    
            print(f"Hour {current_hour:02d}:00\t{current_count}")
            total_trips += current_count
        current_hour  = hour
        current_count = count

# Flush the last hour
if current_hour is not None:
    print(f"Hour {current_hour:02d}:00\t{current_count}")