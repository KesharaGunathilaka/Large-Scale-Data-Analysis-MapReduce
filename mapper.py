"""
Mapper: Extracts hourly trip count data from Uber NYC pickup records.
Dataset: Uber Pickups in New York City (FiveThirtyEight)
Task: Count the number of Uber pickups per hour of the day (0-23)

Input format (CSV):
  Date/Time,Lat,Lon,Base
  "4/1/2014 0:11:00","40.7690","-73.9549","B02512"

Output format (key\tvalue):
  hour\t1
"""

import sys
import logging

# Configure logging - errors go to stderr (not stdout, which Hadoop reads)
logging.basicConfig(level=logging.WARNING, stream=sys.stderr,
                    format='%(levelname)s: %(message)s')

def parse_hour(datetime_str):
    """
    Parse hour from datetime string like '4/1/2014 0:11:00'
    Returns zero-padded hour string e.g. '00', '13', '23'
    """
    datetime_str = datetime_str.strip().strip('"')
    parts = datetime_str.split(' ')
    if len(parts) < 2:
        raise ValueError(f"Cannot split date/time from: '{datetime_str}'")
    time_part = parts[1]
    hour = int(time_part.split(':')[0])
    if hour < 0 or hour > 23:
        raise ValueError(f"Hour out of range: {hour}")
    return f"{hour:02d}"

# ── Main processing loop ──────────────────────────────────────────────────────
lines_processed = 0
lines_skipped   = 0

for line in sys.stdin:
    line = line.strip()

    # Skip blank lines
    if not line:
        continue

    # Skip header row (handles both quoted and unquoted headers)
    if line.startswith('"Date/Time"') or line.startswith('Date/Time'):
        continue

    try:
        # Remove surrounding quotes, then split on comma
        # Example line: "4/1/2014 0:11:00","40.7690","-73.9549","B02512"
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

# Report stats to stderr (visible in Hadoop task logs, not in output)
logging.warning(f"Mapper done — processed: {lines_processed}, skipped: {lines_skipped}")
