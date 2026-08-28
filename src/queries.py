import sqlite3
import pandas as pd
import os

# Format large numbers with thousands separator and 2 decimal places
pd.options.display.float_format = '{:,.2f}'.format

def clear_screen():
    # Clear the console depending on the OS
    os.system('cls' if os.name == 'nt' else 'clear')

def run_query(query, title, connection):
    clear_screen()
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

    try:
        # Execute SQL and load into a DataFrame
        df = pd.read_sql(query, connection)
        if df.empty:
            print("No data to display. Have you loaded the data yet?")
        else:
            # Print without the pandas numeric index
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Error executing query: {e}")

    input("\n  Press ENTER to return to the main menu...")

def interactive_menu():
    # Connect to the database
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "database", "retail_dw.db")

    if not os.path.exists(db_path):
        print(f"Error! Database not found at: {db_path}")
        return

    connection = sqlite3.connect(db_path)

    # Dictionary with the 5 SQL queries
    queries = {
        "1": {
            "title": "R1: Monthly Net Sales Trend",
            "sql": """
                SELECT d.year AS Year, d.month AS Month, SUM(f.net_sales) AS Net_Sales
                FROM FactSales f
                JOIN DimDate d ON f.date_key = d.date_key
                GROUP BY d.year, d.month
                ORDER BY d.year, d.month;
            """
        },
        "2": {
            "title": "R2: Sales by Store and Channel",
            "sql": """
                SELECT s.store_name AS Store, c.channel_name AS Channel, SUM(f.net_sales) AS Net_Sales
                FROM FactSales f
                JOIN DimStore s ON f.store_key = s.store_key
                JOIN DimChannel c ON f.channel_key = c.channel_key
                GROUP BY s.store_name, c.channel_name
                ORDER BY s.store_name, Net_Sales DESC;
            """
        },
        "3": {
            "title": "R3: Top-Performing Categories and Brands",
            "sql": """
                SELECT p.category AS Category, p.brand AS Brand,
                        SUM(f.net_sales) AS Revenue, SUM(f.quantity) AS Units_Sold
                FROM FactSales f
                JOIN DimProduct p ON f.product_key = p.product_key
                GROUP BY p.category, p.brand
                ORDER BY Revenue DESC;
            """
        },
        "4": {
            "title": "R4: Promotion Performance",
            "sql": """
                SELECT pr.promotion_name AS Promotion, SUM(f.net_sales) AS Sales,
                    SUM(f.quantity) AS Units, SUM(f.discount_amount) AS Discount_Amount
                FROM FactSales f
                JOIN DimPromotion pr ON f.promotion_key = pr.promotion_key
                GROUP BY pr.promotion_name
                ORDER BY Sales DESC;
            """
        },
        "5": {
            "title": "R5: Gross Profit and Gross Margin by Category, Store and Month",
            "sql": """
                SELECT p.category AS Category, s.store_name AS Store, d.month AS Month,
                        SUM(f.gross_profit) AS Gross_Profit,
                        ROUND((SUM(f.gross_profit) / SUM(f.net_sales)) * 100, 2) AS Gross_Margin_Pct
                FROM FactSales f
                JOIN DimProduct p ON f.product_key = p.product_key
                JOIN DimStore s ON f.store_key = s.store_key
                JOIN DimDate d ON f.date_key = d.date_key
                GROUP BY p.category, s.store_name, d.month
                ORDER BY d.month, s.store_name, p.category;
            """
        }
    }

    # Menu loop
    while True:
        clear_screen()
        print("=" * 42)
        print("  ANALYTICAL CONSOLE — RETAIL DW")
        print("=" * 42)
        print("[1] R1: Monthly Net Sales Trend")
        print("[2] R2: Sales by Store and Channel")
        print("[3] R3: Top Categories and Brands")
        print("[4] R4: Promotion Impact")
        print("[5] R5: Gross Profit and Margin")
        print("[0] Exit")
        print("=" * 42)

        option = input("Choose an option (0-5): ")

        if option == "0":
            print("\nClosing the analytical console. Goodbye!\n")
            break
        elif option in queries:
            run_query(queries[option]["sql"], queries[option]["title"], connection)
        else:
            input("\n  Invalid option. Press ENTER to try again...")

    connection.close()

if __name__ == "__main__":
    interactive_menu()
