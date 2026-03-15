# run_hadoop.sh — script to run the Uber Pickups MapReduce job on Hadoop

set -e   

# Configuration
CSV_FILE="${1:-uber-raw-data-jul14.csv}"          # Local dataset path
HDFS_INPUT="/user/uber/input"                     # HDFS input directory
HDFS_OUTPUT="/user/uber/output"                   # HDFS output directory
HADOOP_STREAMING_JAR=$(find $HADOOP_HOME -name "hadoop-streaming*.jar" 2>/dev/null | grep -v sources | grep -v tests | head -1)
MAPPER="mapper.py"
REDUCER="reducer.py"
RESULTS_FILE="results/output.txt"

# Colour helpers
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# Pre-flight checks
info "=== Uber Pickups MapReduce Job ==="

[ -z "$HADOOP_HOME" ]         && error "HADOOP_HOME is not set. Did you source hadoop-env.sh?"
[ -z "$HADOOP_STREAMING_JAR" ] && error "hadoop-streaming jar not found in \$HADOOP_HOME"
[ ! -f "$CSV_FILE" ]           && error "Dataset not found: $CSV_FILE"
[ ! -f "$MAPPER" ]             && error "mapper.py not found in current directory"
[ ! -f "$REDUCER" ]            && error "reducer.py not found in current directory"

info "Hadoop home      : $HADOOP_HOME"
info "Streaming jar    : $HADOOP_STREAMING_JAR"
info "Dataset          : $CSV_FILE  ($(wc -l < "$CSV_FILE") lines)"

# ── Make scripts executable ────────────────────────────────────────────────────
chmod +x mapper.py reducer.py
info "Scripts marked executable."

# ── Start Hadoop services (if not running) ─────────────────────────────────────
info "Checking HDFS status..."
# Check if namenode process is actually running (more reliable than dfsadmin)
if ! jps 2>/dev/null | grep -q "NameNode"; then
    warn "NameNode not found — starting DFS and YARN..."
    start-dfs.sh
    start-yarn.sh
    info "Waiting for services to be ready..."
    sleep 8
    info "Hadoop services started."
else
    info "Hadoop services already running ($(jps 2>/dev/null | grep -E 'NameNode|DataNode|ResourceManager' | awk '{print $2}' | tr '\n' ' '))"
fi

# ── Upload dataset to HDFS ─────────────────────────────────────────────────────
info "Preparing HDFS directories..."
hdfs dfs -mkdir -p "$HDFS_INPUT"

# Remove old output if it exists (Hadoop refuses to overwrite)
if hdfs dfs -test -d "$HDFS_OUTPUT" 2>/dev/null; then
    warn "Removing existing HDFS output: $HDFS_OUTPUT"
    hdfs dfs -rm -r "$HDFS_OUTPUT"
fi

info "Uploading $CSV_FILE to HDFS..."
hdfs dfs -put -f "$CSV_FILE" "$HDFS_INPUT/"
info "Upload complete."

# ── Run MapReduce job ──────────────────────────────────────────────────────────
info "Submitting MapReduce streaming job..."
hadoop jar "$HADOOP_STREAMING_JAR" \
    -files "$MAPPER,$REDUCER" \
    -mapper  "python3 $MAPPER"  \
    -reducer "python3 $REDUCER" \
    -input   "$HDFS_INPUT/$(basename $CSV_FILE)" \
    -output  "$HDFS_OUTPUT"

info "MapReduce job completed successfully!"

# ── Retrieve results ───────────────────────────────────────────────────────────
mkdir -p results
info "Fetching results from HDFS..."
hdfs dfs -cat "$HDFS_OUTPUT/part-*" > "$RESULTS_FILE"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  UBER PICKUPS BY HOUR OF DAY — JULY 2014"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "$RESULTS_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Print peak hour
PEAK=$(sort -t$'\t' -k2 -rn "$RESULTS_FILE" | head -1)
echo ""
info "Peak hour: $PEAK"
info "Results saved to: $RESULTS_FILE"
