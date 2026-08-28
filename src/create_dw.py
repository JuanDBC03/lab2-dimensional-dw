import sqlite3
import os

# 1. Get the absolute path of the directory where this script lives (src/)
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Build the path to the database folder one level up (..)
db_dir = os.path.join(script_dir, "..", "database")

# 3. Create the database folder if it doesn't exist
os.makedirs(db_dir, exist_ok=True)

# 4. Define the final database file path
db_path = os.path.join(db_dir, "retail_dw.db")

# 5. Connect to the database
conexion = sqlite3.connect(db_path)
cursor = conexion.cursor()

# Drop tables in reverse order (FactSales first due to FK dependencies)
# so every pipeline run starts from a clean slate
cursor.execute("DROP TABLE IF EXISTS FactSales")
cursor.execute("DROP TABLE IF EXISTS DimDate")
cursor.execute("DROP TABLE IF EXISTS DimProduct")
cursor.execute("DROP TABLE IF EXISTS DimStore")
cursor.execute("DROP TABLE IF EXISTS DimChannel")
cursor.execute("DROP TABLE IF EXISTS DimPromotion")

# DimDate
cursor.execute("""
CREATE TABLE IF NOT EXISTS DimDate (
    date_key INTEGER PRIMARY KEY,
    sale_date TEXT NOT NULL,
    day INTEGER,
    month INTEGER,
    year INTEGER
);
""")

# DimProduct
cursor.execute("""
CREATE TABLE IF NOT EXISTS DimProduct (
    product_key INTEGER PRIMARY KEY,
    product_id TEXT NOT NULL,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    list_price REAL,
    unit_cost REAL
);
""")

# DimStore
cursor.execute("""
CREATE TABLE IF NOT EXISTS DimStore (
    store_key INTEGER PRIMARY KEY,
    store_id TEXT NOT NULL,
    store_name TEXT,
    city TEXT,
    region TEXT
);
""")

# DimChannel
cursor.execute("""
CREATE TABLE IF NOT EXISTS DimChannel (
    channel_key INTEGER PRIMARY KEY,
    channel_id TEXT NOT NULL,
    channel_name TEXT
);
""")

# DimPromotion
cursor.execute("""
CREATE TABLE IF NOT EXISTS DimPromotion (
    promotion_key INTEGER PRIMARY KEY,
    promotion_id TEXT NOT NULL,
    promotion_name TEXT,
    discount_pct REAL
);
""")

# FactSales
cursor.execute("""
CREATE TABLE IF NOT EXISTS FactSales (
    fact_sales_key INTEGER PRIMARY KEY,

    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    store_key INTEGER NOT NULL,
    channel_key INTEGER NOT NULL,
    promotion_key INTEGER NOT NULL,

    quantity INTEGER NOT NULL,
    gross_sales REAL,
    net_sales REAL,
    discount_amount REAL,
    cost_amount REAL,
    gross_profit REAL,

    FOREIGN KEY (date_key) REFERENCES DimDate(date_key),
    FOREIGN KEY (product_key) REFERENCES DimProduct(product_key),
    FOREIGN KEY (store_key) REFERENCES DimStore(store_key),
    FOREIGN KEY (channel_key) REFERENCES DimChannel(channel_key),
    FOREIGN KEY (promotion_key) REFERENCES DimPromotion(promotion_key)
);
""")

conexion.commit()
conexion.close()

print("Schema created successfully.")