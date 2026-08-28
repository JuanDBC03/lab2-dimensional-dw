import sqlite3
import pandas as pd
import os

def load_facts():
    # Configure paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "database", "retail_dw.db")
    sales_data_path = os.path.join(script_dir, "..", "data", "sales_transactions.csv")

    connection = sqlite3.connect(db_path)

    # 1. Read source transactions from CSV
    df_sales = pd.read_csv(sales_data_path)

    # 2. Read dimension surrogate keys from SQLite
    dim_date = pd.read_sql("SELECT date_key, sale_date FROM DimDate", connection)
    dim_product = pd.read_sql("SELECT product_key, product_id, list_price, unit_cost FROM DimProduct", connection)
    dim_store = pd.read_sql("SELECT store_key, store_id FROM DimStore", connection)
    dim_channel = pd.read_sql("SELECT channel_key, channel_id FROM DimChannel", connection)
    dim_promotion = pd.read_sql("SELECT promotion_key, promotion_id FROM DimPromotion", connection)

    # 3. Map source identifiers to surrogate keys
    df_fact = df_sales.merge(dim_date, on="sale_date", how="left")
    df_fact = df_fact.merge(dim_product, on="product_id", how="left")
    df_fact = df_fact.merge(dim_store, on="store_id", how="left")
    df_fact = df_fact.merge(dim_channel, on="channel_id", how="left")
    df_fact = df_fact.merge(dim_promotion, on="promotion_id", how="left")

    # 4. Calculate analytical measures
    df_fact["gross_sales"] = df_fact["quantity"] * df_fact["list_price"]
    df_fact["net_sales"] = df_fact["quantity"] * df_fact["unit_price_sale"]
    df_fact["discount_amount"] = df_fact["gross_sales"] - df_fact["net_sales"]
    df_fact["cost_amount"] = df_fact["quantity"] * df_fact["unit_cost"]
    df_fact["gross_profit"] = df_fact["net_sales"] - df_fact["cost_amount"]

    # 5. Select final columns and load into SQLite
    cols = [
        "date_key", "product_key", "store_key", "channel_key", "promotion_key",
        "quantity", "gross_sales", "net_sales", "discount_amount", "cost_amount", "gross_profit"
    ]
    df_fact[cols].to_sql("FactSales", connection, if_exists="append", index=False)

    connection.close()
    print("Fact table loaded successfully.")

if __name__ == "__main__":
    load_facts()