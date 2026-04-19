"""
generators/server_metrics.py
=============================
Generates time-series server performance metrics.

Simulates real monitoring tool exports with:
- CPU, memory, disk utilization percentages
- HTTP response times in milliseconds
- Server status classifications
- Missing values  : monitoring agent downtime
- Duplicate rows  : pipeline retry ingestion
- Outlier spikes  : real incident signatures
"""

import numpy as np
import pandas as pd


def generate_server_metrics(servers, hours, seed):
    """
    Generate time-series server performance metrics.

    Args:
        servers : list of server IDs
        hours   : number of hourly intervals to generate
        seed    : random seed for reproducibility

    Returns:
        pd.DataFrame : server metrics dataset
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

    df = _inject_outlier_spikes(df)
    df = _inject_missing_values(df)
    df = _inject_duplicates(df, n=25)

    return df


def _inject_outlier_spikes(df):
    """
    Inject outlier spikes into response_ms and cpu_pct.
    Simulates real incident signatures in metric data.
    """
    spike_indices = np.random.choice(len(df), size=10, replace=False)
    df.loc[spike_indices, "response_ms"] = round(np.random.uniform(2000, 5000), 1)
    df.loc[spike_indices, "cpu_pct"]     = round(np.random.uniform(92, 99), 1)
    return df


def _inject_missing_values(df):
    """
    Inject missing values into cpu_pct and response_ms.
    Simulates monitoring agent downtime.
    """
    df.loc[df.index[::10], "cpu_pct"]     = np.nan  # every 10th row
    df.loc[df.index[::15], "response_ms"] = np.nan  # every 15th row
    return df


def _inject_duplicates(df, n):
    """
    Inject duplicate rows.
    Simulates pipeline retry ingestion of same data batch.
    """
    duplicate_rows = df.iloc[:n].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    return df
