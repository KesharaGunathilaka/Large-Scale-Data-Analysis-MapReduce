set -euo pipefail

# Run Hadoop Streaming
CSV_FILE="${1:-data/uber-raw-data-jul14.csv}"
HDFS_INPUT="/user/uber/input"
HDFS_OUTPUT="/user/uber/output"
HADOOP_STREAMING_JAR="${HADOOP_STREAMING_JAR:-$(find "$HADOOP_HOME" -name "hadoop-streaming*.jar" 2>/dev/null | grep -v sources | grep -v tests | head -1)}"
MAPPER="mapper.py"
REDUCER="reducer.py"
DAYS_IN_MONTH=31

RESULTS_DIR="results"
TOTAL_RESULTS_FILE="$RESULTS_DIR/output.txt"
AVERAGE_JSON_FILE="$RESULTS_DIR/output_daily_avg.json"

log() {
  echo "[INFO] $*"
}

fail() {
  echo "[ERROR] $*"
  exit 1
}

[ -z "${HADOOP_HOME:-}" ] && fail "HADOOP_HOME is not set"
[ -z "$HADOOP_STREAMING_JAR" ] && fail "hadoop-streaming jar not found"
[ ! -f "$CSV_FILE" ] && fail "Dataset not found: $CSV_FILE"
[ ! -f "$MAPPER" ] && fail "mapper.py not found"
[ ! -f "$REDUCER" ] && fail "reducer.py not found"

chmod +x "$MAPPER" "$REDUCER"

if ! jps 2>/dev/null | grep -q "NameNode"; then
  log "Starting Hadoop services..."
  start-dfs.sh
  start-yarn.sh
  sleep 8
fi

hdfs dfs -mkdir -p "$HDFS_INPUT"
hdfs dfs -rm -r -f "$HDFS_OUTPUT" >/dev/null 2>&1 || true
hdfs dfs -put -f "$CSV_FILE" "$HDFS_INPUT/"

log "Running Hadoop Streaming job..."
hadoop jar "$HADOOP_STREAMING_JAR" \
  -files "$MAPPER,$REDUCER" \
  -mapper "python3 $MAPPER" \
  -reducer "python3 $REDUCER" \
  -input "$HDFS_INPUT/$(basename "$CSV_FILE")" \
  -output "$HDFS_OUTPUT"

mkdir -p "$RESULTS_DIR"
hdfs dfs -cat "$HDFS_OUTPUT/part-*" > "$TOTAL_RESULTS_FILE"

python3 - "$TOTAL_RESULTS_FILE" "$AVERAGE_JSON_FILE" "$DAYS_IN_MONTH" <<'PY'
import json
import sys
from datetime import datetime

raw_file = sys.argv[1]
json_file = sys.argv[2]
days = float(sys.argv[3])

data = {}
total = 0

with open(raw_file, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        hour_label = parts[0].replace("Hour ", "").replace(":00", "")
        count = int(parts[1])
        total += count
        data[hour_label] = round(count / days, 2)

out = {
    "timestamp": datetime.now().isoformat(),
    "metric": "daily_average_per_hour",
    "days_divisor": int(days),
    "data": data,
    "summary": {
        "total_monthly_trips": total,
        "average_daily_trips": round(total / days, 2),
        "hours_analyzed": len(data),
    },
}

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)
PY

log "Total count text output: $TOTAL_RESULTS_FILE"
log "Daily average JSON output: $AVERAGE_JSON_FILE"