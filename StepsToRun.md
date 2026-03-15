# Large-Scale Data Analysis Using Hadoop MapReduce

**Module:** Cloud Computing (EE7222/EC7204) — University of Ruhuna  
**Semester:** 7 | February 2026  
**Task:** Count total Uber pickups per hour of the day (00:00–23:00)  
**Dataset:** [Uber Pickups in New York City — FiveThirtyEight (Kaggle)](https://www.kaggle.com/datasets/fivethirtyeight/uber-pickups-in-new-york-city?select=uber-raw-data-jul14.csv)

---

## Step 1 — Check Hadoop is Installed and Running in WSL

Open your WSL terminal and run:

```bash
hadoop version
```

Expected output:
```
Hadoop 3.3.6
```

If you get `command not found`, Hadoop is not installed. Install it first:

```bash
# Install Java
sudo apt update && sudo apt install -y openjdk-11-jdk

# Download and install Hadoop
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
mv hadoop-3.3.6 ~/hadoop

# Add to ~/.bashrc
echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))' >> ~/.bashrc
echo 'export HADOOP_HOME=~/hadoop' >> ~/.bashrc
echo 'export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 2 — Start Hadoop Services

```bash
start-dfs.sh && start-yarn.sh
```

Verify all 5 processes are running:

```bash
jps
```

Expected output:
```
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
```

> ⚠️ If `DataNode` is missing, run this fix then start again:
> ```bash
> stop-dfs.sh && stop-yarn.sh
> rm -rf ~/hadoopdata/namenode/* ~/hadoopdata/datanode/*
> rm -f /tmp/hadoop-$USER-*.pid
> hdfs namenode -format
> start-dfs.sh && start-yarn.sh
> ```

---

## Step 3 — Get the Project Files

You have two options — choose one:

---

### Option A — Using the ZIP file

1. Download the ZIP and extract it:

```bash
unzip Large-Scale-Data-Analysis-MapReduce.zip
cd Large-Scale-Data-Analysis-MapReduce
```

2. Verify the files are there:

```bash
ls
# Should show: mapper.py  reducer.py  run_hadoop.sh  data/  results/  README.md
```

---

### Option B — Using Git (Clone the Repository)

```bash
git clone https://github.com/KesharaGunathilaka/Large-Scale-Data-Analysis-MapReduce.git
cd Large-Scale-Data-Analysis-MapReduce
```

> ⚠️ Make sure your project folder path has **no spaces**.
> Good: `~/cloud/Large-Scale-Data-Analysis-MapReduce`
> Bad: `~/My Projects/Large Scale Data Analysis`

---

## Step 4 — Download the Dataset

Download `uber-raw-data-jul14.csv` from [Kaggle](https://www.kaggle.com/datasets/fivethirtyeight/uber-pickups-in-new-york-city) and place it inside the `data/` folder:

```bash
ls data/
# Should show: uber-raw-data-jul14.csv
```

---

## Step 5 — Set the Hadoop Streaming JAR

```bash
export HADOOP_STREAMING_JAR=$(find $HADOOP_HOME -name "hadoop-streaming*.jar" | grep -v sources | grep -v tests | head -1)
```

Verify it is set:

```bash
echo $HADOOP_STREAMING_JAR
# Should print something like: /home/youruser/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar
```

---

## Step 6 — Upload the Dataset to HDFS

```bash
hdfs dfs -mkdir -p /user/uber/input
hdfs dfs -put data/uber-raw-data-jul14.csv /user/uber/input/
```

Verify the upload:

```bash
hdfs dfs -ls /user/uber/input/
# Should show the CSV file listed
```

---

## Step 7 — Run the MapReduce Job

```bash
hadoop jar $HADOOP_STREAMING_JAR -files mapper.py,reducer.py -mapper "python3 mapper.py" -reducer "python3 reducer.py" -input /user/uber/input/uber-raw-data-jul14.csv -output /user/uber/output
```

You will see Hadoop logs while the job runs. Wait for:
```
Job job_local... completed successfully
map 100% reduce 100%
```

> ⚠️ If you see **"Output directory already exists"**, delete it and re-run:
> ```bash
> hdfs dfs -rm -r /user/uber/output
> ```

---

## Step 8 — View the Results

```bash
hdfs dfs -cat /user/uber/output/part-*
```

---

## Step 9 — Save Results Locally

```bash
hdfs dfs -cat /user/uber/output/part-* > results/output.txt
cat results/output.txt
```

---

## Expected Output

```
Hour 00:00      17953
Hour 01:00      11527
Hour 02:00       8562   <- Quietest hour
Hour 03:00       9199
Hour 04:00      10040
Hour 05:00      14932
Hour 06:00      23456
Hour 07:00      32545
Hour 08:00      33387
Hour 09:00      28486
Hour 10:00      28558
Hour 11:00      30120
Hour 12:00      30900
Hour 13:00      35832
Hour 14:00      41357
Hour 15:00      46053
Hour 16:00      52403
Hour 17:00      58260   <- Peak hour
Hour 18:00      57268
Hour 19:00      52332
Hour 20:00      51859
Hour 21:00      49528
Hour 22:00      42218
Hour 23:00      29346
```

| Metric | Value |
|--------|-------|
| Total trips processed | 796,121 |
| Peak hour | 17:00 — 58,260 trips |
| Quietest hour | 02:00 — 8,562 trips |

---

## Project Structure

```
Large-Scale-Data-Analysis-MapReduce/
├── mapper.py            # Mapper: extracts hour from CSV row, emits hour->1
├── reducer.py           # Reducer: sums trip counts per hour
├── run_hadoop.sh        # Automated job runner script
├── data/                # Place dataset here (not tracked by Git)
├── results/
│   └── output.txt       # MapReduce output (24 hourly counts)
└── README.md
```

---

## Useful Web UIs (while Hadoop is running)

| Interface | URL |
|-----------|-----|
| HDFS NameNode | http://localhost:9870 |
| YARN ResourceManager | http://localhost:8088 |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `hadoop: command not found` | Run `source ~/.bashrc` or reinstall Hadoop |
| `DataNode` missing from `jps` | Follow the DataNode fix in Step 2 |
| `Connection refused` on port 9000 | Run `start-dfs.sh` |
| `Output directory already exists` | Run `hdfs dfs -rm -r /user/uber/output` |
| `Illegal character in path` (spaces) | Move project to a path with no spaces |
| `HADOOP_STREAMING_JAR` is empty | Re-run the export command in Step 5 |
