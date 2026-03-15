#!/usr/bin/env python3
"""
Mapper: Extracts hourly data from Uber trip records.
"""

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(message)s')

def parse_hour_from_datetime(datetime_str):
    time_part = datetime_str.split(' ')[1]
    hour = int(time_part.split(':')[0])
    if hour < 0 or hour > 23:
        raise ValueError(f"Invalid hour: {hour}")
    return f"{hour:02d}"

# Main processing loop
for line in sys.stdin:
    line = line.strip()
    
    # Skip header row
    if line.startswith('"Date/Time"') or line.startswith('Date/Time'):
        continue
    
    # Skip empty lines
    if not line:
        continue
    
    try:
        # Parse CSV line and remove quotes
        fields = line.replace('"', '').split(',')
        
        if len(fields) < 1:
            continue
        
        datetime_str = fields[0].strip()
        hour = parse_hour_from_datetime(datetime_str)
        
        print(f"{hour}\t1")
        
    except (IndexError, ValueError) as e:
        # Log errors to stderr but continue processing
        logging.debug(f"Skipped malformed line: {line} - {str(e)}")
