from pathlib import Path
import pandas as pd

from db import get_connection

DATA_DIR = Path(__file__).resolve().parents[2] / "data"

TABLES = [
    "categories",
    "products",
    "customers",
    "orders",
    "order_items",
    "promotions",
]

def seed_database():
    with get_connection() as conn:
        for table in TABLES:
            file_path = DATA_DIR / f"{table}.csv"

            df = pd.read_csv(file_path)

            df.to_sql(
                name=table,
                con=conn,
                if_exists="replace",
                index=False    
            )

            print(f"{table}: {len(df)} registros importados")

if __name__ == "__main__":
    seed_database()