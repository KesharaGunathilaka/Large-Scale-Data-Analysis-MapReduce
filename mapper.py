#Mapper: Extracts hourly trip count data from Uber NYC pickup records.

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                    format='%(levelname)s: %(message)s')

def parse_hour(datetime_str):
    datetime_str = datetime_str.strip().strip('"')
    parts = datetime_str.split(' ')
    if len(parts) < 2:
        raise ValueError(f"Cannot split date/time from: '{datetime_str}'")
    time_part = parts[1]
    hour = int(time_part.split(':')[0])
    if hour < 0 or hour > 23:
        raise ValueError(f"Hour out of range: {hour}")
    return f"{hour:02d}"

# Main processing loop
lines_processed = 0
lines_skipped   = 0

for line in sys.stdin:
    line = line.strip()

    # Skip blank lines
    if not line:
        continue

    # Skip header row 
    if line.startswith('"Date/Time"') or line.startswith('Date/Time'):
        continue

    try:
        # Remove surrounding quotes, then split on comma
        fields = line.replace('"', '').split(',')

        if len(fields) < 1:
            raise ValueError("No fields found")

        datetime_str = fields[0].strip()
        hour = parse_hour(datetime_str)

        # Emit: hour TAB 1
        print(f"{hour}\t1")
        lines_processed += 1

    except (IndexError, ValueError) as e:
        logging.warning(f"Skipped malformed line: {repr(line)} — {e}")
        lines_skipped += 1

# Report stats to stderr
logging.warning(f"Mapper done — processed: {lines_processed}, skipped: {lines_skipped}")
