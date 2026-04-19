"""
exporters/postgres_exporter.py
===============================
Pushes generated datasets to PostgreSQL.

Requires:
    pip install sqlalchemy psycopg2-binary

Connection string format:
    postgresql://username:password@host:port/database

Example:
    postgresql://postgres:postgres@localhost:5432/opsdb
"""


def push_to_postgres(df_metrics, df_tickets, df_logs, connection_string):
    """
    Push all three datasets to PostgreSQL.

    Creates or replaces tables:
        - server_metrics
        - incidents
        - app_logs

    Args:
        df_metrics        : server metrics DataFrame
        df_tickets        : incident tickets DataFrame
        df_logs           : application logs DataFrame
        connection_string : PostgreSQL connection string

    Returns:
        None
    """
    try:
        from sqlalchemy import create_engine

        engine = create_engine(connection_string)

        print("Pushing to PostgreSQL...")
        print()

        _push_table(df_metrics, "server_metrics", engine)
        _push_table(df_tickets, "incidents",       engine)
        _push_table(df_logs,    "app_logs",         engine)

        print()
        print(f"{'─' * 50}")
        print(f"All datasets pushed to PostgreSQL")
        print(f"Connection : {_mask_password(connection_string)}")
        print(f"{'─' * 50}\n")

    except ImportError:
        print(
            "Error: sqlalchemy not installed.\n"
            "Run: pip install sqlalchemy psycopg2-binary"
        )
    except Exception as e:
        print(f"PostgreSQL push failed: {e}")


def _push_table(df, table_name, engine):
    """
    Push a single DataFrame to a PostgreSQL table.

    Args:
        df         : DataFrame to push
        table_name : target PostgreSQL table name
        engine     : SQLAlchemy engine
    """
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )
    print(f"  {table_name:<20} → {len(df)} rows pushed")


def _mask_password(connection_string):
    """
    Mask password in connection string for safe printing.

    Example:
        postgresql://postgres:postgres@localhost:5432/opsdb
        → postgresql://postgres:***@localhost:5432/opsdb
    """
    try:
        parts    = connection_string.split(":")
        masked   = parts[0] + ":" + parts[1] + ":***@" + parts[2].split("@")[-1]
        return masked
    except Exception:
        return "postgresql://***"
