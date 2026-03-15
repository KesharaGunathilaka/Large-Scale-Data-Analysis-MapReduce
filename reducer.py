#Reducer: Aggregates trip counts by hour.

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

current_hour = None
current_count = 0

# Main processing loop - input assumed to be sorted by hour from mapper output
for line in sys.stdin:
    line = line.strip()
    
    # Skip empty lines
    if not line:
        continue
    
    try:
        # Parse mapper output format: hour\tcount
        parts = line.split('\t')
        if len(parts) != 2:
            logging.debug(f"Skipped invalid format: {line}")
            continue
            
        hour_str, count_str = parts
        hour = int(hour_str)
        count = int(count_str)
        
        # Validate hour range (0-23)
        if hour < 0 or hour > 23:
            logging.debug(f"Invalid hour range: {hour}")
            continue
            
    except ValueError as e:
        logging.debug(f"Skipped malformed line: {line} - {str(e)}")
        continue
    
    # Accumulate counts for current hour
    if current_hour == hour:
        current_count += count
    else:
        if current_hour is not None:
            print(f"Hour {current_hour:02d}:00\t{current_count}")
        
        current_hour = hour
        current_count = count

# Output the final hour's total
if current_hour is not None:
    print(f"Hour {current_hour:02d}:00\t{current_count}")
