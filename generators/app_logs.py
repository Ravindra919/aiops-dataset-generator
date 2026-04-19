"""
generators/app_logs.py
=======================
Generates application log entries.

Simulates real application log exports with:
- Timestamped log entries per server
- Log levels : INFO / WARNING / ERROR / CRITICAL
- Free-text messages from common IT operations scenarios
- Error codes for ERROR and CRITICAL entries
- Missing error codes : expected for INFO/WARNING, issue for ERROR/CRITICAL
- Duplicate rows      : pipeline retry ingestion
"""

import numpy as np
import pandas as pd


MESSAGES = [
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

LOG_LEVELS       = ["INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_LEVEL_PROBS  = [0.50, 0.25, 0.15, 0.10]
ERROR_CODES      = ["E001", "E002", "E003", "E004", None]
ERROR_CODE_PROBS = [0.20, 0.20, 0.20, 0.20, 0.20]


def generate_app_logs(servers, n_entries, seed):
    """
    Generate application log entries.

    Args:
        servers   : list of server IDs
        n_entries : number of log entries to generate
        seed      : random seed for reproducibility

    Returns:
        pd.DataFrame : application logs dataset
    """
    np.random.seed(seed)

    logs = []
    for i in range(n_entries):
        ts = pd.Timestamp("2026-01-01") + pd.Timedelta(
                 minutes=int(np.random.randint(0, 14400))
             )
        logs.append({
            "timestamp":  ts,
            "server_id":  np.random.choice(servers),
            "log_level":  np.random.choice(LOG_LEVELS, p=LOG_LEVEL_PROBS),
            "message":    np.random.choice(MESSAGES),
            "error_code": np.random.choice(ERROR_CODES, p=ERROR_CODE_PROBS)
        })

    df = pd.DataFrame(logs)
    df = _inject_duplicates(df, n=15)

    return df


def _inject_duplicates(df, n):
    """
    Inject duplicate rows.
    Simulates pipeline retry ingestion of same data batch.
    """
    duplicate_rows = df.iloc[:n].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    return df
