"""
AIOps Dataset Generator
=======================
Generates realistic IT operations datasets for AIOps learning,
prototyping, and ML pipeline development.

Datasets generated:
    - server_metrics.csv   : Time-series server performance metrics
    - incidents.csv        : IT incident ticket data (ServiceNow-style)
    - app_logs.csv         : Application log entries

Each dataset includes intentional data quality issues:
    - Missing values       : Simulates monitoring agent downtime
    - Duplicate rows       : Simulates pipeline retry ingestion
    - Inconsistent formats : Simulates multi-source data exports
    - Outliers             : Simulates real incident spikes

Usage:
    python generate_datasets.py
    python generate_datasets.py --output ./data --seed 42 --servers 10

Author  : AIOps Learning Project
Stack   : Python 3.x · Pandas · NumPy
"""

import argparse
import os
import pandas as pd
import numpy as np


# ── Configuration Defaults ─────────────────────────────────────────────────────

DEFAULT_SEED        = 42
DEFAULT_OUTPUT_DIR  = "./data"
DEFAULT_SERVERS     = ["srv-01", "srv-02", "srv-03", "srv-04", "srv-05"]
DEFAULT_HOURS       = 100
DEFAULT_TICKETS     = 200
DEFAULT_LOG_ENTRIES = 300


# ── Dataset 1: Server Metrics ──────────────────────────────────────────────────

def generate_server_metrics(servers, hours, seed, output_dir):
    """
    Generate time-series server performance metrics.

    Simulates real monitoring tool exports with:
    - CPU, memory, disk utilization percentages
    - HTTP response times in milliseconds
    - Server status classifications
    - Missing values (monitoring agent downtime)
    - Duplicate rows (pipeline retry ingestion)
    - Outlier spikes (real incident signatures)

    Args:
        servers    : list of server IDs
        hours      : number of hourly intervals to generate
        seed       : random seed for reproducibility
        output_dir : directory to save CSV file

    Returns:
        pd.DataFrame : generated server metrics dataset
    """
    np.random.seed(seed)
    timestamps = pd.date_range("2026-01-01", periods=hours, freq="1h")

    records = []
    for ts in timestamps:
        for srv in servers:
            records.append({
                "timestamp":   ts,
                "server_id":   srv,
                "cpu_pct":     round(np.random.uniform(20, 99), 1),
                "memory_pct":  round(np.random.uniform(30, 98), 1),
                "response_ms": round(np.random.uniform(50, 1200), 1),
                "disk_pct":    round(np.random.uniform(30, 95), 1),
                "status":      np.random.choice(
                                   ["ok", "warning", "critical"],
                                   p=[0.75, 0.20, 0.05]
                               )
            })

    df = pd.DataFrame(records)

    # Inject outlier spikes — simulates real incidents
    spike_indices = np.random.choice(len(df), size=10, replace=False)
    df.loc[spike_indices, "response_ms"] = round(np.random.uniform(2000, 5000), 1)
    df.loc[spike_indices, "cpu_pct"]     = round(np.random.uniform(92, 99), 1)

    # Inject missing values — simulates monitoring agent downtime
    null_cpu_idx  = df.index[::10]   # every 10th row
    null_resp_idx = df.index[::15]   # every 15th row
    df.loc[null_cpu_idx,  "cpu_pct"]     = np.nan
    df.loc[null_resp_idx, "response_ms"] = np.nan

    # Inject duplicate rows — simulates pipeline retry ingestion
    duplicate_rows = df.iloc[:25].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Save
    filepath = os.path.join(output_dir, "server_metrics.csv")
    df.to_csv(filepath, index=False)

    print(f"  server_metrics.csv → shape: {df.shape} | "
          f"nulls: {df.isnull().sum().sum()} | "
          f"dupes: {df.duplicated().sum()}")

    return df


# ── Dataset 2: Incident Tickets ────────────────────────────────────────────────

def generate_incidents(servers, n_tickets, seed, output_dir):
    """
    Generate IT incident ticket data in ServiceNow style.

    Simulates real incident management exports with:
    - Ticket IDs, server assignments, categories, priorities
    - Created and resolved timestamps
    - Resolution status flags
    - Guaranteed P1 unresolved tickets on high-risk server
    - Inconsistent category formatting (real export behavior)
    - Duplicate rows (pipeline retry ingestion)

    Args:
        servers    : list of server IDs
        n_tickets  : number of tickets to generate
        seed       : random seed for reproducibility
        output_dir : directory to save CSV file

    Returns:
        pd.DataFrame : generated incidents dataset
    """
    np.random.seed(seed)

    categories = ["CPU High", "Disk Full", "Network Lag", "Memory Leak", "Service Down"]

    tickets = []
    for i in range(n_tickets):
        created     = pd.Timestamp("2026-01-01") + pd.Timedelta(
                          hours=int(np.random.randint(0, 2400))
                      )
        resolved    = created + pd.Timedelta(hours=int(np.random.randint(1, 72)))
        is_resolved = np.random.choice([True, False], p=[0.65, 0.35])

        tickets.append({
            "ticket_id":   f"INC{str(i + 1).zfill(4)}",
            "server_id":   np.random.choice(servers),
            "category":    np.random.choice(categories),
            "priority":    int(np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])),
            "created_at":  created,
            "resolved_at": resolved if is_resolved else pd.NaT,
            "resolved":    is_resolved
        })

    df = pd.DataFrame(tickets)

    # Inject guaranteed P1 unresolved tickets on srv-04
    # Ensures lab tasks always return non-empty results
    guaranteed = [
        {
            "ticket_id":   "INC0201",
            "server_id":   "srv-04",
            "category":    "CPU High",
            "priority":    1,
            "created_at":  pd.Timestamp("2026-01-03 10:00:00"),
            "resolved_at": pd.NaT,
            "resolved":    False
        },
        {
            "ticket_id":   "INC0202",
            "server_id":   "srv-04",
            "category":    "Memory Leak",
            "priority":    1,
            "created_at":  pd.Timestamp("2026-01-03 14:00:00"),
            "resolved_at": pd.NaT,
            "resolved":    False
        },
        {
            "ticket_id":   "INC0203",
            "server_id":   "srv-04",
            "category":    "Service Down",
            "priority":    1,
            "created_at":  pd.Timestamp("2026-01-04 08:00:00"),
            "resolved_at": pd.NaT,
            "resolved":    False
        },
    ]
    df = pd.concat([df, pd.DataFrame(guaranteed)], ignore_index=True)

    # Inject inconsistent category formatting — simulates real export behavior
    df.loc[df.index[::5],  "category"] = "cpu high"
    df.loc[df.index[::7],  "category"] = " Disk Full "
    df.loc[df.index[::11], "category"] = "MEMORY LEAK"

    # Inject duplicate rows — simulates pipeline retry ingestion
    duplicate_rows = df.iloc[:10].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Save
    filepath = os.path.join(output_dir, "incidents.csv")
    df.to_csv(filepath, index=False)

    print(f"  incidents.csv      → shape: {df.shape} | "
          f"nulls: {df.isnull().sum().sum()} | "
          f"dupes: {df.duplicated().sum()}")

    return df


# ── Dataset 3: Application Logs ────────────────────────────────────────────────

def generate_app_logs(servers, n_entries, seed, output_dir):
    """
    Generate application log entries.

    Simulates real application log exports with:
    - Timestamped log entries per server
    - Log levels: INFO, WARNING, ERROR, CRITICAL
    - Free-text messages from common IT operations scenarios
    - Error codes for ERROR and CRITICAL entries
    - Missing error codes (expected for INFO/WARNING, issue for ERROR)
    - Duplicate rows (pipeline retry ingestion)

    Args:
        servers    : list of server IDs
        n_entries  : number of log entries to generate
        seed       : random seed for reproducibility
        output_dir : directory to save CSV file

    Returns:
        pd.DataFrame : generated application logs dataset
    """
    np.random.seed(seed)

    messages = [
        "CPU threshold exceeded",
        "Disk usage at 90%",
        "Connection timeout error",
        "Memory allocation failed",
        "Service restarted successfully",
        "Network packet loss detected",
        "Database query slow",
        "Authentication failed",
        "Health check passed",
        "Backup completed successfully",
        "SSL certificate expiring soon",
        "Load balancer health check failed",
    ]

    logs = []
    for i in range(n_entries):
        ts = pd.Timestamp("2026-01-01") + pd.Timedelta(
                 minutes=int(np.random.randint(0, 14400))
             )
        logs.append({
            "timestamp":  ts,
            "server_id":  np.random.choice(servers),
            "log_level":  np.random.choice(
                              ["INFO", "WARNING", "ERROR", "CRITICAL"],
                              p=[0.50, 0.25, 0.15, 0.10]
                          ),
            "message":    np.random.choice(messages),
            "error_code": np.random.choice(
                              ["E001", "E002", "E003", "E004", None],
                              p=[0.20, 0.20, 0.20, 0.20, 0.20]
                          )
        })

    df = pd.DataFrame(logs)

    # Inject duplicate rows — simulates pipeline retry ingestion
    duplicate_rows = df.iloc[:15].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # Save
    filepath = os.path.join(output_dir, "app_logs.csv")
    df.to_csv(filepath, index=False)

    print(f"  app_logs.csv       → shape: {df.shape} | "
          f"nulls: {df.isnull().sum().sum()} | "
          f"dupes: {df.duplicated().sum()}")

    return df


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate AIOps datasets for learning and prototyping"
    )
    parser.add_argument(
        "--output", default=DEFAULT_OUTPUT_DIR,
        help="Output directory for CSV files (default: ./data)"
    )
    parser.add_argument(
        "--seed", type=int, default=DEFAULT_SEED,
        help="Random seed for reproducibility (default: 42)"
    )
    parser.add_argument(
        "--servers", type=int, default=len(DEFAULT_SERVERS),
        help="Number of servers to simulate (default: 5)"
    )
    parser.add_argument(
        "--hours", type=int, default=DEFAULT_HOURS,
        help="Hours of metric data to generate (default: 100)"
    )
    parser.add_argument(
        "--tickets", type=int, default=DEFAULT_TICKETS,
        help="Number of incident tickets to generate (default: 200)"
    )
    parser.add_argument(
        "--logs", type=int, default=DEFAULT_LOG_ENTRIES,
        help="Number of log entries to generate (default: 300)"
    )

    args    = parser.parse_args()
    servers = [f"srv-{str(i+1).zfill(2)}" for i in range(args.servers)]

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    print(f"\nAIOps Dataset Generator")
    print(f"{'─' * 50}")
    print(f"  Output dir  : {args.output}")
    print(f"  Seed        : {args.seed}")
    print(f"  Servers     : {servers}")
    print(f"  Hours       : {args.hours}")
    print(f"  Tickets     : {args.tickets}")
    print(f"  Log entries : {args.logs}")
    print(f"{'─' * 50}")
    print(f"Generating datasets...")
    print()

    generate_server_metrics(servers, args.hours,   args.seed, args.output)
    generate_incidents(     servers, args.tickets, args.seed, args.output)
    generate_app_logs(      servers, args.logs,    args.seed, args.output)

    print()
    print(f"{'─' * 50}")
    print(f"All datasets saved to: {args.output}/")
    print(f"{'─' * 50}\n")


if __name__ == "__main__":
    main()
