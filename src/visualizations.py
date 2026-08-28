import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

# Format large numbers to millions (e.g. 2500000 -> $2.5M)
def format_millions(x, pos):
    return f'${x*1e-6:,.1f}M'

def generate_charts():
    # Configure paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "database", "retail_dw.db")
    docs_dir = os.path.join(script_dir, "..", "docs")

    os.makedirs(docs_dir, exist_ok=True)
    connection = sqlite3.connect(db_path)

    # Apply default aesthetic style
    plt.style.use('ggplot')
    formatter = FuncFormatter(format_millions)

    # ==========================================
    # Visualization 1: Time-series chart (R1)
    # ==========================================
    print("Generating time-series chart (R1)...")
    df_r1 = pd.read_sql("""
        SELECT d.year, d.month, SUM(f.net_sales) AS net_sales
        FROM FactSales f
        JOIN DimDate d ON f.date_key = d.date_key
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month
    """, connection)

    # Build readable x-axis labels: "Jan 2026", "Feb 2026", etc.
    month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                   7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    df_r1['label'] = df_r1['month'].map(month_names) + ' ' + df_r1['year'].astype(str)

    fig, ax = plt.subplots(figsize=(11, 6))

    # Draw line with improved thickness and color
    ax.plot(range(len(df_r1)), df_r1['net_sales'], marker='o', markersize=8,
            color='#2E86C1', linewidth=3)
    ax.set_title('Monthly Net Sales Trend (R1)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Net Sales (COP)', fontsize=12)

    # Format Y axis and set tick labels
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xticks(range(len(df_r1)))
    ax.set_xticklabels(df_r1['label'], rotation=30, ha='right', fontsize=10)

    # Add data labels above each point
    for i, val in enumerate(df_r1['net_sales']):
        ax.text(i, val + (val * 0.015), f'${val*1e-6:.1f}M',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#333333')

    plt.tight_layout()
    plt.savefig(os.path.join(docs_dir, "tendencia_ventas.png"), dpi=300)
    plt.close()

    # ==========================================
    # Visualization 2: Comparative bar chart (R3)
    # ==========================================
    print("Generating comparative bar chart (R3)...")
    df_r3 = pd.read_sql("""
        SELECT p.category, SUM(f.net_sales) AS net_sales
        FROM FactSales f
        JOIN DimProduct p ON f.product_key = p.product_key
        GROUP BY p.category
        ORDER BY net_sales DESC
    """, connection)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Draw bars with a modern color palette
    colors = ['#1ABC9C', '#2ECC71', '#3498DB', '#9B59B6']
    bars = ax.bar(df_r3['category'], df_r3['net_sales'], color=colors[:len(df_r3)])
    ax.set_title('Total Revenue by Product Category (R3)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Category', fontsize=12)
    ax.set_ylabel('Net Sales (COP)', fontsize=12)

    # Format Y axis
    ax.yaxis.set_major_formatter(formatter)

    # Add data labels above each bar
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + (yval * 0.015),
                f'${yval*1e-6:.1f}M',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333333')

    plt.tight_layout()
    plt.savefig(os.path.join(docs_dir, "comparativo_categorias.png"), dpi=300)
    plt.close()

    print("Charts successfully generated and saved to 'docs/' folder.")
    connection.close()

if __name__ == "__main__":
    generate_charts()