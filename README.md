# AIOps Dataset Generator

Generates realistic IT operations datasets for AIOps learning, prototyping, and ML pipeline development.

---

## Project Structure

```
aiops-dataset-generator/
│
├── generate_datasets.py       ← entry point — CLI and orchestration only
├── requirements.txt
├── README.md
├── .gitignore
│
├── generators/
│   ├── __init__.py
│   ├── server_metrics.py      ← server performance metric generation
│   ├── incidents.py           ← incident ticket generation
│   └── app_logs.py            ← application log generation
│
└── exporters/
    ├── __init__.py
    ├── csv_exporter.py        ← saves datasets to CSV files
    └── postgres_exporter.py   ← pushes datasets to PostgreSQL
```

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
| priority | int | Priority: 1 (critical) / 2 (high) / 3 (normal) |
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
| error_code | string | Error code (null for INFO/WARNING rows) |

---

## Intentional Data Quality Issues

Each dataset includes realistic data quality problems for cleaning practice:

| Issue | Dataset | Description |
|-------|---------|-------------|
| Missing values | server_metrics | Monitoring agent downtime |
| Missing values | incidents | Unresolved tickets have no resolved_at |
| Missing values | app_logs | INFO/WARNING logs have no error_code |
| Duplicate rows | all three | Pipeline retry ingestion |
| Inconsistent formats | incidents | "cpu high", " Disk Full ", "MEMORY LEAK" |
| Outlier spikes | server_metrics | Incident signatures in response_ms and cpu_pct |

---

## Installation

```bash
git clone https://github.com/Ravindra919/aiops-dataset-generator.git
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

### CSV + PostgreSQL push

```bash
python generate_datasets.py --postgres postgresql://postgres:postgres@localhost:5432/opsdb
```

### Custom scale

```bash
python generate_datasets.py --servers 10 --hours 720 --tickets 500 --logs 1000
```

### All options

```
--output    Output directory for CSV files       (default: ./data)
--seed      Random seed for reproducibility      (default: 42)
--servers   Number of servers to simulate        (default: 5)
--hours     Hours of metric data to generate     (default: 100)
--tickets   Number of incident tickets           (default: 200)
--logs      Number of log entries                (default: 300)
--postgres  PostgreSQL connection string         (optional)
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

  server_metrics.csv     → shape: (525, 7)   | nulls: 89    | dupes: 25
  incidents.csv          → shape: (213, 7)   | nulls: 80    | dupes: 10
  app_logs.csv           → shape: (315, 5)   | nulls: 49    | dupes: 15

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

- [pandas-aiops](https://github.com/Ravindra919/pandas-aiops) — Pandas learning curriculum built on these datasets

---

## Stack

Python 3.x · Pandas · NumPy · SQLAlchemy · psycopg2

---

## Author

AIOps Engineer — Enterprise AI for IT Operations
