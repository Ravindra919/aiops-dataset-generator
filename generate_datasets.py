"""
generate_datasets.py
=====================
AIOps Dataset Generator — entry point.

Orchestrates dataset generation and export.
All data logic lives in generators/ and exporters/ modules.

Usage:
    python generate_datasets.py
    python generate_datasets.py --output ./data
    python generate_datasets.py --postgres postgresql://user:pass@host:port/db
    python generate_datasets.py --servers 10 --hours 720 --tickets 500 --logs 1000

Author  : AIOps Learning Project
Stack   : Python 3.x · Pandas · NumPy · SQLAlchemy
"""

import argparse

from generators import generate_server_metrics, generate_incidents, generate_app_logs
from exporters  import save_to_csv, push_to_postgres


# ── Defaults ───────────────────────────────────────────────────────────────────

DEFAULT_SEED        = 42
DEFAULT_OUTPUT_DIR  = "./data"
DEFAULT_N_SERVERS   = 5
DEFAULT_HOURS       = 100
DEFAULT_TICKETS     = 200
DEFAULT_LOG_ENTRIES = 300


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args():
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
        "--servers", type=int, default=DEFAULT_N_SERVERS,
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
    parser.add_argument(
        "--postgres",
        help=(
            "Push datasets to PostgreSQL after generating CSV files.\n"
            "Format: postgresql://user:password@host:port/dbname\n"
            "Example: postgresql://postgres:postgres@localhost:5432/opsdb"
        )
    )
    return parser.parse_args()


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    args    = parse_args()
    servers = [f"srv-{str(i + 1).zfill(2)}" for i in range(args.servers)]

    _print_config(args, servers)

    # Generate
    print("Generating datasets...\n")
    df_metrics = generate_server_metrics(servers, args.hours,   args.seed)
    df_tickets = generate_incidents(     servers, args.tickets, args.seed)
    df_logs    = generate_app_logs(      servers, args.logs,    args.seed)
    print()

    # Export to CSV
    save_to_csv(df_metrics, df_tickets, df_logs, args.output)

    # Export to PostgreSQL if flag provided
    if args.postgres:
        push_to_postgres(df_metrics, df_tickets, df_logs, args.postgres)


def _print_config(args, servers):
    print(f"\nAIOps Dataset Generator")
    print(f"{'─' * 50}")
    print(f"  Output dir  : {args.output}")
    print(f"  Seed        : {args.seed}")
    print(f"  Servers     : {servers}")
    print(f"  Hours       : {args.hours}")
    print(f"  Tickets     : {args.tickets}")
    print(f"  Log entries : {args.logs}")
    if args.postgres:
        print(f"  PostgreSQL  : enabled")
    print(f"{'─' * 50}")


if __name__ == "__main__":
    main()
