"""
exporters/csv_exporter.py
==========================
Saves generated datasets to CSV files.
"""

import os


def save_to_csv(df_metrics, df_tickets, df_logs, output_dir):
    """
    Save all three datasets to CSV files.

    Args:
        df_metrics : server metrics DataFrame
        df_tickets : incident tickets DataFrame
        df_logs    : application logs DataFrame
        output_dir : directory to save CSV files

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    _save(df_metrics, "server_metrics.csv", output_dir)
    _save(df_tickets, "incidents.csv",      output_dir)
    _save(df_logs,    "app_logs.csv",        output_dir)

    print(f"{'─' * 50}")
    print(f"All datasets saved to: {output_dir}/")
    print(f"{'─' * 50}\n")


def _save(df, filename, output_dir):
    """
    Save a single DataFrame to CSV and print summary.

    Args:
        df         : DataFrame to save
        filename   : output filename
        output_dir : output directory path
    """
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)

    print(f"  {filename:<22} → shape: {str(df.shape):<12} | "
          f"nulls: {df.isnull().sum().sum():<5} | "
          f"dupes: {df.duplicated().sum()}")
