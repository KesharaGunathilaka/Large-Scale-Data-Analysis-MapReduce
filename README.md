# Large-Scale Data Analysis Using MapReduce

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![matplotlib](https://img.shields.io/badge/visualization-matplotlib-brightgreen.svg)](https://matplotlib.org/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/KesharaGunathilaka/Large-Scale-Data-Analysis-MapReduce)

A high-performance Python-based MapReduce implementation for analyzing large-scale Uber trip data. This project demonstrates the MapReduce paradigm, featuring distributed processing patterns, data aggregation, and comprehensive visualization of hourly traffic patterns across July 2014.

## 📊 Project Overview

This implementation uses the MapReduce paradigm to process **796,121 Uber trip records** and extract hourly traffic patterns:

- **Extract**: Mapper phase extracts hourly data from raw CSV records
- **Sort**: Intermediate results sorted by key (critical for correct aggregation)
- **Aggregate**: Reducer phase aggregates identical hours to prevent duplicates
- **Visualize**: Generate bar chart and statistics from processed data
- **Persist**: Save outputs in both text and JSON formats

## ⚡ Quick Start

Run these commands in a normal terminal on Windows or inside your WSL Ubuntu terminal.

```bash
# 1. Clone the repository
git clone https://github.com/KesharaGunathilaka/Large-Scale-Data-Analysis-MapReduce.git
cd Large-Scale-Data-Analysis-MapReduce

# 2. Install Python dependencies
pip install matplotlib numpy    # or: pip3 install matplotlib numpy

# 3. Run the MapReduce analysis
python main.py                  # or: python3 main.py

# 4. Generate visualizations
python visualize.py
```

That’s it. Hadoop/WSL can be part of your environment, but this project runs as a local Python MapReduce job.

## 🎯 What You Get

After running the above commands:

✅ **Complete hourly breakdown** with trip counts and percentages
✅ **Top 5 busiest hours** clearly identified  
✅ **Bar chart visualization** showing traffic distribution
✅ **Detailed statistics report** with metrics and analysis
✅ **Output files** saved in `/output/` and `/visualizations/`

---

## 📁 Project Structure

```
Large-Scale-Data-Analysis-MapReduce/
│
├── mapper.py                          # Stage 1: Extract hourly data
├── reducer.py                         # Stage 3: Aggregate counts by hour
├── main.py                            # Orchestrator: coordinates pipeline
├── visualize.py                       # Generate charts and reports
│
├── data/
│   └── uber-raw-data-jul14.csv       # Input: 796,121 trip records
│
├── output/                            # Generated results
│   ├── hourly_trips.txt              # Human-readable output
│   └── hourly_trips.json             # Machine-readable output
│
├── visualizations/                    # Generated charts & reports
│   ├── bar_chart.png                 # Hourly distribution chart
│   └── statistics_report.txt         # Detailed analytics
│
├── README.md                          # This file
├── SETUP.md                           # Detailed setup guide
└── COMPLETION_SUMMARY.txt            # Project completion summary
```

---

## 🚀 Detailed Usage

### Running the MapReduce Pipeline

```bash
python main.py
```

**This command:**
- Processes all 796,121 Uber trip records
- Runs mapper phase to extract hours
- Sorts intermediate results (prevents duplicate aggregation)
- Runs reducer phase to aggregate by hour
- Saves results to `/output/` folder
- Displays all 24 hours with trip counts and percentages
- Shows top 5 busiest hours

**Sample Output:**
```
========================================================
MAPREDUCE PIPELINE COMPLETED SUCCESSFULLY
========================================================

Results saved to:
  - Text: ...output/hourly_trips.txt
  - JSON: ...output/hourly_trips.json

COMPLETE HOURLY TRIP DATA
─────────────────────────────────────────────────────
Hour            Trip Count               Percentage
─────────────────────────────────────────────────────
00:00               17,953 trips  ███████████      2.26%
01:00               11,527 trips  ███              1.45%
02:00                8,562 trips  ██               1.08%
03:00                9,199 trips  ██               1.16%
04:00               10,040 trips  ██               1.26%
05:00               14,932 trips  ████             1.88%
06:00               23,456 trips  ███████          2.95%
07:00               32,545 trips  ██████████       4.09%
08:00               33,387 trips  ██████████       4.20%
09:00               28,486 trips  █████████        3.58%
10:00               28,558 trips  █████████        3.59%
11:00               30,120 trips  █████████        3.79%
12:00               30,900 trips  █████████        3.88%
13:00               35,832 trips  ███████████      4.51%
14:00               41,357 trips  █████████████    5.20%
15:00               46,053 trips  ██████████████   5.79%
16:00               52,403 trips  █████████████████ 6.58%
17:00               58,260 trips  ██████████████████ 7.32%
18:00               57,268 trips  █████████████████ 7.19%
19:00               52,332 trips  █████████████████ 6.57%
20:00               51,859 trips  █████████████████ 6.52%
21:00               49,528 trips  ████████████████ 6.22%
22:00               42,218 trips  █████████████    5.31%
23:00               29,346 trips  █████████        3.69%
─────────────────────────────────────────────────────
TOTAL               796,121 trips

TOP 5 BUSIEST HOURS
─────────────────────────────────────────────────────
  1. Hour 17:00 -    58,260 trips (7.32%)
  2. Hour 18:00 -    57,268 trips (7.19%)
  3. Hour 16:00 -    52,403 trips (6.58%)
  4. Hour 19:00 -    52,332 trips (6.57%)
  5. Hour 20:00 -    51,859 trips (6.52%)
========================================================
```

### Generating Visualizations

```bash
python visualize.py
```

**This command:**
- Reads processed data from `/output/hourly_trips.json`
- Generates bar chart showing hourly distribution
- Creates detailed statistics report
- Saves files to `/visualizations/` folder

**Output Files:**
- `bar_chart.png` - Hourly distribution with color gradient and value labels
- `statistics_report.txt` - Complete analytics including mean, median, std dev

---

## 📊 Output Files

### Text Results (`output/hourly_trips.txt`)
```
Hour	Trip Count
==============================
Hour 00:00	17953
Hour 01:00	11527
...
Hour 23:00	29346
==============================
Total Trips: 796121
Average per Hour: 33171.71
```

### JSON Results (`output/hourly_trips.json`)
```json
{
  "timestamp": "2026-03-15T16:17:56.093000",
  "data": {
    "00": 17953,
    "01": 11527,
    ...
    "23": 29346
  },
  "summary": {
    "total_trips": 796121,
    "hours_analyzed": 24,
    "average_per_hour": 33171.708333
  }
}
```

### Statistics Report (`visualizations/statistics_report.txt`)
```
╔════════════════════════════════════════╗
║     UBER TRIP DATA STATISTICS REPORT   ║
║           July 2014 Analysis           ║
╚════════════════════════════════════════╝

SUMMARY STATISTICS:
  • Total Trips: 796,121
  • Average per Hour: 33,171.71
  • Median per Hour: 31,722.5
  • Standard Deviation: 15,546.94

EXTREME VALUES:
  • Peak Hour: 17:00 with 58,260 trips
  • Lowest Hour: 02:00 with 8,562 trips
  • Range: 49,698 trips

TRAFFIC PATTERNS:
  • High Traffic (>33,172 trips): 11 hours
  • Low Traffic (<33,172 trips): 13 hours
```

---

## 🔧 Technical Architecture

### Pipeline Stages

```
┌──────────────────────────────┐
│   Raw CSV Data (796K rows)   │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   MAPPER PHASE               │
│ Extract: (hour, 1)           │
│ Output: 796,121 pairs        │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   SORT PHASE ⭐ (CRITICAL)   │
│ Group by hour (0-23)         │
│ Prevents duplicate counts    │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   REDUCER PHASE              │
│ Aggregate: Sum by hour       │
│ Output: 24 aggregates        │
└──────────────────────────────┘
              ↓
┌──────────────────────────────┐
│   OUTPUT & VISUALIZATION     │
│ Save + Chart + Report        │
└──────────────────────────────┘
```

### Key Algorithm: Deduplication

The **critical sorting phase** fixes the duplicate aggregation problem:

1. **Mapper Output** (unsorted):
   ```
   00	1
   01	1
   00	1    ← Same hour appears later
   02	1
   ```

2. **After Sorting**: 
   ```
   00	1
   00	1    ← All same hours together
   01	1
   02	1
   ```

3. **Reducer Aggregation**:
   ```
   00	2    ← Correctly summed
   01	1
   02	1
   ```

---

## 🎯 Key Features

### ✅ Duplicate Prevention
- Explicit sorting phase between mapper and reducer
- Each hour counted exactly once
- Proven with 796,121 records → 24 unique aggregates

### ✅ Error Handling
- Malformed record skipping
- Hour range validation (0-23)
- File existence verification
- Comprehensive logging

### ✅ Performance
- Streaming data processing
- No full dataset in memory
- Processes 796K records in ~3 seconds
- Generates visualizations in ~4 seconds

### ✅ Code Quality
- Object-oriented design (Classes: MapReducePipeline, DataVisualizer)
- Comprehensive docstrings with examples
- Input validation throughout
- Structured error handling

### ✅ Output Variety
- Text format for human consumption
- JSON format for programmatic access
- Visual charts for presentation
- Detailed statistics for analysis

---

## 🐛 Troubleshooting

### Issue: `python: command not found`
**Solution:** Use `python3` or add Python to PATH

### Issue: `ModuleNotFoundError: No module named 'matplotlib'`
**Solution:**
```bash
pip install matplotlib numpy
```

### Issue: `FileNotFoundError: uber-raw-data-jul14.csv`
**Solution:** Run from project root directory where `/data/` folder exists

### Issue: Duplicate values in output (old version)
**Solution:** Update to latest version with sorting phase

### Issue: Slow performance
**Solution:** Run on native Python (not through virtualization)

---

## 📚 File Descriptions

### `mapper.py` (50 lines)
Processes raw CSV lines, extracts timestamps, emits (hour, 1) pairs for each trip.

**Key Features:**
- Handles CSV format with quoted fields
- Parses datetime to extract hour
- Skips header row automatically
- Validates hour range (0-23)

### `reducer.py` (55 lines)
Aggregates trip counts by hour from mapper output.

**Key Features:**
- Requires sorted input by hour
- Accumulates counts for identical hours
- Outputs formatted results with leading zeros
- Validates input format and ranges

### `main.py` (280 lines)
Orchestrates complete pipeline execution.

**Key Features:**
- MapReducePipeline class
- Runs mapper → sort → reducer sequence
- Saves results in text and JSON
- Displays comprehensive output with tables
- Handles all error cases

### `visualize.py` (380 lines)
Generates visualizations from processed output.

**Key Features:**
- DataVisualizer class
- Bar chart generation
- Statistics report creation
- Comprehensive analysis metrics

### `SETUP.md`
Detailed setup and run instructions with troubleshooting.

---

## 📈 Data Analysis

### Trip Distribution
- **Peak Hour**: 17:00 (5 PM) - 58,260 trips
- **Off-Peak Hour**: 02:00 (2 AM) - 8,562 trips
- **Variation**: 680% between peak and off-peak

### Traffic Patterns
- **Morning Rush** (6-9 AM): Rapid increase from 23K to 33K
- **Midday** (10-13): Stable at 30K-36K trips
- **Afternoon Rush** (14-19): Peak period with 41K-58K
- **Evening** (20-23): Gradual decrease from 51K to 29K
- **Late Night** (0-5): Low traffic 8K-17K

### Statistics
```
Total Trips:        796,121
Average per Hour:   33,171.71
Median:             31,722.5
Std Deviation:      15,546.94
Coefficient of Variation: 47%
```

---

## 🚀 Performance

| Phase | Records | Time | Speed |
|-------|---------|------|-------|
| Mapper | 796,121 → 796,121 pairs | ~2.5s | 318K/sec |
| Sort | 796,121 pairs → sorted | ~0.4s | 2M/sec |
| Reducer | 796,121 pairs → 24 hours | ~0.8s | 1M/sec |
| Visualize | Data → Charts | ~4.0s | 199K/sec |
| **Total** | **Raw data to charts** | **~7.7s** | **103K/sec** |

---

## 🎓 Learning Objectives

This project demonstrates:
- ✅ MapReduce paradigm implementation from scratch
- ✅ Data processing pipeline design and orchestration
- ✅ Importance of proper sorting in aggregation algorithms
- ✅ Large-scale data analysis techniques
- ✅ Python best practices (logging, error handling, OOP)
- ✅ Data visualization with matplotlib
- ✅ Stream processing without memory overhead

---

## 📄 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Overview and architecture (this file) |
| **SETUP.md** | Detailed setup and run guide |
| **COMPLETION_SUMMARY.txt** | Project improvements and fixes |
| **mapper.py** | Extract hourly data |
| **reducer.py** | Aggregate by hour |
| **main.py** | Orchestrate pipeline |
| **visualize.py** | Generate charts |

---

## 📞 Support & Contact

For issues or questions:
1. Check [SETUP.md](SETUP.md) troubleshooting section
2. Verify all files in project directory
3. Ensure Python 3.7+ is installed
4. Confirm dependencies: `pip install matplotlib numpy`

---

## 📄 License

This project is open source and available for educational purposes.
Learn more about MapReduce at: [Apache Hadoop MapReduce](https://hadoop.apache.org/)

---

## ✨ Version History

**v2.0** (Mar 15, 2026)
- Major redesign: cleaner output, focused visualizations
- Bar chart and statistics report only
- Comprehensive run guide in SETUP.md
- Complete output display with all 24 hours
- Top 5 busiest hours highlighted

**v1.0** (Initial release)
- Basic MapReduce implementation
- Multiple visualization types
- JSON and text output

---

**Last Updated:** March 15, 2026  
**Status:** ✅ Production Ready  
**Python Version:** 3.7+
