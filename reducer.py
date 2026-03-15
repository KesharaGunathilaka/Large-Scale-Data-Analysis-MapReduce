import sys
import logging

logging.basicConfig(
    level=logging.WARNING,
    stream=sys.stderr,
    format="%(levelname)s: %(message)s"
)


def parse_line(line):
    """
    Parses a single tab-separated input line into (hour, count).
    Args:
        line (str): A stripped line in the format '<HH>\\t<count>'.
    Returns:
        tuple[int, int]: A (hour, count) pair.
    """
  
    parts = line.split('\t')

    if len(parts) != 2:
        raise ValueError(f"Expected 2 fields, got {len(parts)}: {repr(line)}")

    hour_str, count_str = parts
    hour  = int(hour_str)
    count = int(count_str)

    if hour < 0 or hour > 23:
        raise ValueError(f"Hour out of range: {hour}")

    return hour, count


def reducer():
    """
    Main reducer function — reads sorted (hour, count) pairs from stdin,
    groups by hour, and emits the total pickup count for each hour to stdout.

    Skips blank lines and malformed records, logging a warning for each.
    Prints a total trip count summary to stderr when finished
    (visible in Hadoop task logs).
    """
    current_hour  = None
    current_count = 0
    total_trips   = 0

    for line in sys.stdin:
        line = line.strip()

        # Skip blank lines
        if not line:
            continue

        try:
            hour, count = parse_line(line)

        except ValueError as e:
            logging.warning(f"Skipped malformed line: {repr(line)} — {e}")
            continue

        if current_hour == hour:
            # Still within the same hour — accumulate the count
            current_count += count
        else:
            # Hour has changed — emit the result for the previous hour
            if current_hour is not None:
                print(f"Hour {current_hour:02d}:00\t{current_count}")
                total_trips += current_count

            # Reset tracking for the new hour
            current_hour  = hour
            current_count = count

    # Flush the final hour after the loop ends
    if current_hour is not None:
        print(f"Hour {current_hour:02d}:00\t{current_count}")
        total_trips += current_count

    # Final summary written to stderr — visible in Hadoop task logs
    logging.warning(f"Reducer done — total trips recorded: {total_trips}")


if __name__ == "__main__":
    reducer()
