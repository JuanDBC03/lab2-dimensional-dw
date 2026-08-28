import sqlite3
import json
import pandas as pd
import os

def load_dimensions():
    # Configure paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "database", "retail_dw.db")
    ref_data_path = os.path.join(script_dir, "..", "data", "reference_data.json")
    sales_data_path = os.path.join(script_dir, "..", "data", "sales_transactions.csv")

    connection = sqlite3.connect(db_path)

    # 1. Load reference JSON data
    with open(ref_data_path, "r") as f:
        ref_data = json.load(f)

    # Static dimensions
    pd.DataFrame(ref_data["products"]).to_sql("DimProduct", connection, if_exists="append", index=False)

    df_stores = pd.DataFrame(ref_data["stores"])[['store_id', 'store_name', 'city', 'region']]
    df_stores.to_sql("DimStore", connection, if_exists="append", index=False)

    pd.DataFrame(ref_data["channels"]).to_sql("DimChannel", connection, if_exists="append", index=False)
    pd.DataFrame(ref_data["promotions"]).to_sql("DimPromotion", connection, if_exists="append", index=False)

    # 2. Build DimDate from unique dates found in the CSV
    df_sales = pd.read_csv(sales_data_path)
    df_dates = pd.DataFrame({"sale_date": df_sales["sale_date"].unique()})

    df_dates["sale_date"] = pd.to_datetime(df_dates["sale_date"])
    df_dates["day"] = df_dates["sale_date"].dt.day
    df_dates["month"] = df_dates["sale_date"].dt.month
    df_dates["year"] = df_dates["sale_date"].dt.year
    df_dates["sale_date"] = df_dates["sale_date"].dt.strftime("%Y-%m-%d")

    df_dates.to_sql("DimDate", connection, if_exists="append", index=False)

    connection.close()
    print("Dimensions loaded successfully.")

if __name__ == "__main__":
    load_dimensions()