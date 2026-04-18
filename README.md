# AIOps Dataset Generator

Generates realistic IT operations datasets for AIOps learning, prototyping, and ML pipeline development.

---

## Datasets

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `server_metrics.csv` | 525 | 7 | Time-series server performance metrics |
| `incidents.csv` | 213 | 7 | IT incident tickets (ServiceNow-style) |
| `app_logs.csv` | 315 | 5 | Application log entries |

---

## Schema

### server_metrics.csv
| Column | Type | Description |
|--------|------|-------------|
| timestamp | datetime | Hourly metric reading timestamp |
| server_id | string | Server identifier (srv-01 to srv-05) |
| cpu_pct | float | CPU utilization percentage |
| memory_pct | float | Memory utilization percentage |
| response_ms | float | HTTP response time in milliseconds |
| disk_pct | float | Disk utilization percentage |
| status | string | Server status: ok / warning / critical |

### incidents.csv
| Column | Type | Description |
|--------|------|-------------|
| ticket_id | string | Unique ticket identifier (INC0001...) |
| server_id | string | Affected server |
| category | string | Incident category |
| priority | int | Priority level: 1 (critical) / 2 (high) / 3 (normal) |
| created_at | datetime | Ticket creation timestamp |
| resolved_at | datetime | Resolution timestamp (NaT if unresolved) |
| resolved | bool | Resolution status flag |

### app_logs.csv
| Column | Type | Description |
|--------|------|-------------|
| timestamp | datetime | Log entry timestamp |
| server_id | string | Source server |
| log_level | string | INFO / WARNING / ERROR / CRITICAL |
| message | string | Log message text |
| error_code | string | Error code (null for INFO/WARNING) |

---

## Intentional Data Quality Issues

Each dataset includes realistic data quality problems for cleaning practice:

| Issue | Dataset | Simulation |
|-------|---------|------------|
| Missing values | server_metrics | Monitoring agent downtime |
| Missing values | incidents | Unresolved tickets have no resolved_at |
| Missing values | app_logs | INFO/WARNING logs have no error_code |
| Duplicate rows | all three | Pipeline retry ingestion |
| Inconsistent formats | incidents | Category values: "cpu high", " Disk Full ", "MEMORY LEAK" |
| Outlier spikes | server_metrics | Real incident signatures in response_ms and cpu_pct |

---

## Installation

```bash
git clone https://github.com/yourusername/aiops-dataset-generator.git
cd aiops-dataset-generator
pip install -r requirements.txt
```

---

## Usage

### Default — generates all datasets into ./data/

```bash
python generate_datasets.py
```

### Custom output directory

```bash
python generate_datasets.py --output ./datasets
```

### Custom scale

```bash
# 10 servers, 30 days of hourly data, 500 tickets, 1000 log entries
python generate_datasets.py --servers 10 --hours 720 --tickets 500 --logs 1000
```

### Custom seed for reproducibility

```bash
python generate_datasets.py --seed 123
```

### All options

```bash
python generate_datasets.py --help
```

```
usage: generate_datasets.py [-h] [--output OUTPUT] [--seed SEED]
                             [--servers SERVERS] [--hours HOURS]
                             [--tickets TICKETS] [--logs LOGS]

Generate AIOps datasets for learning and prototyping

options:
  --output   Output directory for CSV files (default: ./data)
  --seed     Random seed for reproducibility (default: 42)
  --servers  Number of servers to simulate (default: 5)
  --hours    Hours of metric data to generate (default: 100)
  --tickets  Number of incident tickets to generate (default: 200)
  --logs     Number of log entries to generate (default: 300)
```

---

## Expected Output

```
AIOps Dataset Generator
──────────────────────────────────────────────────
  Output dir  : ./data
  Seed        : 42
  Servers     : ['srv-01', 'srv-02', 'srv-03', 'srv-04', 'srv-05']
  Hours       : 100
  Tickets     : 200
  Log entries : 300
──────────────────────────────────────────────────
Generating datasets...

  server_metrics.csv → shape: (525, 7)  | nulls: 87  | dupes: 25
  incidents.csv      → shape: (213, 7)  | nulls: 72  | dupes: 10
  app_logs.csv       → shape: (315, 5)  | nulls: 63  | dupes: 15

──────────────────────────────────────────────────
All datasets saved to: ./data/
──────────────────────────────────────────────────
```

---

## Use Cases

- **Pandas learning** — cleaning, filtering, groupby, time series, feature engineering
- **ML prototyping** — anomaly detection, ticket classification, log parsing
- **AIOps pipelines** — end-to-end data engineering practice
- **PostgreSQL integration** — load with `pd.read_sql`, write with `df.to_sql`

---

## Related Projects

- [pandas-aiops](https://github.com/yourusername/pandas-aiops) — 23-topic Pandas learning curriculum built on these datasets

---

## Stack

Python 3.x · Pandas · NumPy

---

## Author

AIOps Engineer — AI for IT Operations  

