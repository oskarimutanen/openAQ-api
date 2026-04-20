import requests
import pandas as pd
import sqlite3
import io

DB = "database.db"


def create_tables():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS measurement (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER,
        parameter TEXT,
        datetime TEXT,
        value REAL
    )
    """)

    conn.commit()
    conn.close()


def download_day(location_id, year, month, day):
    date_str = f"{year}{month:02d}{day:02d}"

    url = (
        "https://openaq-data-archive.s3.amazonaws.com/records/csv.gz/"
        f"locationid={location_id}/year={year}/month={month:02d}/"
        f"location-{location_id}-{date_str}.csv.gz"
    )

    r = requests.get(url)

    if r.status_code != 200:
        print("Ei dataa:", date_str)
        return

    try:
        df = pd.read_csv(io.BytesIO(r.content), compression="gzip")
    except Exception as e:
        print("CSV virhe:", e)
        return

    required_cols = ["location_id", "parameter", "datetime", "value"]

    if not all(col in df.columns for col in required_cols):
        print("Puuttuvia sarakkeita:", date_str)
        return

    conn = sqlite3.connect(DB)

    df[required_cols].to_sql(
        "measurement",
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    print("Tallennettu:", date_str)


if __name__ == "__main__":
    create_tables()

    LOCATION_ID = 10122

    for day in range(1, 32):
        download_day(LOCATION_ID, 2024, 1, day)