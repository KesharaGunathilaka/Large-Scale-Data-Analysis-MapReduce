#!/usr/bin/env python3
"""
Mapper
Input format: "Date/Time","Lat","Lon","Base"
              "7/1/2014 0:03:00",40.7586,-73.9706,"B02512"
"""

import sys

for line in sys.stdin:
    line = line.strip()

    if line.startswith('"Date/Time"') or line.startswith('Date/Time'):
        continue

    fields = line.replace('"', '').split(',')

    if len(fields) < 1:
        continue

    try:
        datetime_str = fields[0].strip()        
        time_part = datetime_str.split(' ')[1]  
        hour = time_part.split(':')[0]          
        # convert to int for proper sorting
        hour = int(hour)

        print(f"{hour}\t1")

    except (IndexError, ValueError):
        continue
