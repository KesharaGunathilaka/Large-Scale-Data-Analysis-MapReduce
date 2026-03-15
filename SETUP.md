# Setup & Run Guide (WSL + Hadoop environment)
Steps to run this project from your WSL Ubuntu terminal.

## 1. Open WSL and go to the project

```bash
wsl                          # from Windows, opens your WSL shell

# inside WSL, go to your project folder
cd /path/to/Large-Scale-Data-Analysis-MapReduce
```

If you use git, cloned it:
```bash
git clone https://github.com/KesharaGunathilaka/Large-Scale-Data-Analysis-MapReduce.git
cd Large-Scale-Data-Analysis-MapReduce
```

## 2. Make sure Hadoop / WSL environment is ready

- Hadoop already installed and configured in WSL
- Hadoop services running (optional for this local job):

```bash
start-dfs.sh
```

## 3. Install Python dependencies (inside WSL)

```bash
pip3 install matplotlib numpy
```

## 4. Run the MapReduce-style analysis

```bash
python3 main.py
```

## 5. Generate visualizations

```bash
python3 visualize.py
```

## 6. Output locations

- `output/hourly_trips.txt` – Text results
- `output/hourly_trips.json` – JSON results
- `visualizations/bar_chart.png` – Chart visualization
- `visualizations/statistics_report.txt` – Statistics

## More details

For full environment setup and extra explanation, see the
GitHub docs: https://github.com/KesharaGunathilaka/Large-Scale-Data-Analysis-MapReduce