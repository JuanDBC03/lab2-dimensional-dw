# Lab 2 Data Dictionary

## Source 1: sales_transactions.csv

| Field | Description |
|---|---|
| sale_line_id | Unique identifier of the sales line |
| transaction_id | Transaction identifier |
| sale_date | Date of the sale (YYYY-MM-DD) |
| store_id | Store identifier |
| product_id | Product identifier |
| channel_id | Sales channel identifier |
| promotion_id | Promotion applied to the sale |
| quantity | Units sold |
| unit_price_sale | Unit price actually paid by the customer (COP) |

## Source 2: reference_data.json

The JSON file contains four reference collections: `products`, `stores`, `channels`, and `promotions`.

### products
- product_id
- product_name
- category
- brand
- list_price
- unit_cost

### stores
- store_id
- store_name
- city
- region
- channel_id

### channels
- channel_id
- channel_name

### promotions
- promotion_id
- promotion_name
- discount_pct

## Important
The sources are intentionally clean enough to keep the focus on dimensional modeling. Only minimal transformation is required to calculate analytical measures and populate the star schema.
