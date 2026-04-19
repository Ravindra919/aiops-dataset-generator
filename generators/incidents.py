"""
generators/incidents.py
========================
Generates IT incident ticket data in ServiceNow style.

Simulates real incident management exports with:
- Ticket IDs, server assignments, categories, priorities
- Created and resolved timestamps
- Resolution status flags
- Guaranteed P1 unresolved tickets on high-risk server (srv-04)
- Inconsistent category formatting  : real multi-source export behavior
- Duplicate rows                    : pipeline retry ingestion
"""

import numpy as np
import pandas as pd


CATEGORIES = ["CPU High", "Disk Full", "Network Lag", "Memory Leak", "Service Down"]


def generate_incidents(servers, n_tickets, seed):
    """
    Generate IT incident ticket data.

    Args:
        servers   : list of server IDs
        n_tickets : number of tickets to generate
        seed      : random seed for reproducibility

    Returns:
        pd.DataFrame : incidents dataset
    """
    np.random.seed(seed)

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
            "category":    np.random.choice(CATEGORIES),
            "priority":    int(np.random.choice([1, 2, 3], p=[0.3, 0.5, 0.2])),
            "created_at":  created,
            "resolved_at": resolved if is_resolved else pd.NaT,
            "resolved":    is_resolved
        })

    df = pd.DataFrame(tickets)

    df = _inject_guaranteed_p1_tickets(df)
    df = _inject_inconsistent_categories(df)
    df = _inject_duplicates(df, n=10)

    return df


def _inject_guaranteed_p1_tickets(df):
    """
    Inject guaranteed P1 unresolved tickets on srv-04.
    Ensures lab filtering tasks always return non-empty results.
    """
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
    return df


def _inject_inconsistent_categories(df):
    """
    Inject inconsistent category formatting.
    Simulates real behavior when data comes from multiple source systems.
    """
    df.loc[df.index[::5],  "category"] = "cpu high"
    df.loc[df.index[::7],  "category"] = " Disk Full "
    df.loc[df.index[::11], "category"] = "MEMORY LEAK"
    return df


def _inject_duplicates(df, n):
    """
    Inject duplicate rows.
    Simulates pipeline retry ingestion of same data batch.
    """
    duplicate_rows = df.iloc[:n].copy()
    df = pd.concat([df, duplicate_rows], ignore_index=True)
    return df
