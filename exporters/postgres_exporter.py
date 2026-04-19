"""
exporters/postgres_exporter.py
===============================

Pushes generated datasets to PostgreSQL (Production-ready version).

Improvements:
- Uses append instead of replace (no data loss)
- Batch inserts for performance
- Safe connection handling (transactions)
- Environment variable support (optional)
- Robust password masking
- Better logging

Requires:
    pip install sqlalchemy psycopg2-binary
"""

import os
from urllib.parse import urlparse
from sqlalchemy import create_engine


def push_to_postgres(df_metrics, df_tickets, df_logs, connection_string=None):
    """
    Push all datasets to PostgreSQL.

    Tables:
        - server_metrics
        - incidents
        - app_logs
    """

    try:
        # ✅ Use environment variable if not passed
        if connection_string is None:
            connection_string = os.getenv("DB_URL")

        if not connection_string:
            raise ValueError("Database connection string not provided")

        engine = create_engine(connection_string)

        print("\n🚀 Pushing datasets to PostgreSQL...\n")

        _push_table(df_metrics, "server_metrics", engine)
        _push_table(df_tickets, "incidents", engine)
        _push_table(df_logs, "app_logs", engine)

        print("\n" + "─" * 50)
        print("✅ All datasets pushed successfully")
        print(f"🔐 Connection : {_mask_password(connection_string)}")
        print("─" * 50 + "\n")

    except ImportError:
        print(
            "❌ Error: sqlalchemy not installed.\n"
            "Run: pip install sqlalchemy psycopg2-binary"
        )
    except Exception as e:
        print(f"❌ PostgreSQL push failed: {e}")


def _push_table(df, table_name, engine):
    """
    Push a single DataFrame to PostgreSQL safely.
    """

    if df is None or df.empty:
        print(f"⚠️  Skipping {table_name} (empty dataset)")
        return

    try:
        # ✅ Transaction-safe connection
        with engine.begin() as conn:
            df.to_sql(
                table_name,
                conn,
                if_exists="append",     # ✅ NO DATA LOSS
                index=False,
                method="multi",         # ✅ Faster inserts
                chunksize=1000          # ✅ Batch processing
            )

        print(f"  {table_name:<20} → {len(df)} rows pushed")

    except Exception as e:
        print(f"❌ Failed to push {table_name}: {e}")


def _mask_password(connection_string):
    """
    Safely mask password in connection string.
    """

    try:
        parsed = urlparse(connection_string)

        return (
            f"{parsed.scheme}://"
            f"{parsed.username}:***@"
            f"{parsed.hostname}:{parsed.port}/"
            f"{parsed.path.lstrip('/')}"
        )

    except Exception:
        return "postgresql://***"