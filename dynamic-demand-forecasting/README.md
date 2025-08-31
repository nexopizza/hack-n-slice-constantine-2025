# 📈 Dynamic Demand Forecasting


Help the pizzeria manager anticipate busy hours and product demand to optimize staffing, prep, and inventory. Build forecasts that incorporate seasonality, weather, and local events, and extend them to account for stock-outs and waste.

---

## 🎯 Project Objective
Design a machine learning–powered system that analyzes historical restaurant data—including order volumes, staffing configurations, and operational cycles—to forecast:
- Orders volume (hourly/daily/weekly)
- Ingredient usage
- Staffing needs and wage optimization
while dynamically adjusting predictions based on weather conditions, local events, national holidays, and calendar cycles (e.g. day of week, day of month, pay periods).

---

## 🧠 Core Concept
The system learns from the restaurant’s past to anticipate its future. It combines internal operational data with external contextual signals to generate actionable forecasts that optimize prep, staffing, and inventory.

---

## 📊 System Outputs
• 	📈 Demand Forecasts: Predict customer flow by hour/day/week
• 	🧂 Ingredient Planner: It could be simply the rate of increase / decrease in ingredient preparation comparing to the previous day
• 	👥 Staffing Optimizer: Suggested team size and role mix per shift

---

## 🗂️ Data Sources

- [MongoDB NDJSON] collections:
  - `items.ndjson` (catalog — see [items.ndjson])
  - `options.ndjson` (sizes/toppings — see [options.ndjson])
  - `orders.ndjson` (order headers — see [orders.ndjson])
  - `order_items.ndjson` (order lines — see [order_items.ndjson])
- Stage 2 additional collections:
  - `restocks.ndjson` (ingredient batches — see [restocks.ndjson])
  - `stock_moves.ndjson` (consumption/waste — see [stock_moves.ndjson])
- External signals:
  - News/events and weather from the [playground website]

---

## 🧪 Samples From Temp Data

### NDJSON — Items
```json
{
  "_id": "68b35fc2868d406af5688772",
  "name": "Pizza Margherita",
  "category": "Pizzas",
  "workflow": "PIZZA",
  "basePrice": 350,
  "hasSize": false,
  "hasToppings": true
}
```

### NDJSON — Options
```json
{
  "_id": "68b35fc2868d406af5688773",
  "kind": "SAUCE",
  "name": "Sauce Tomate",
  "priceDelta": 0,
  "itemScope": [
    "68b35fc2868d406af5688772"
  ]
}
```

### NDJSON — Orders
```json
{
  "_id": "68b35fc2868d406af5688c70",
  "storeId": "68b35fc2868d406af5688771",
  "source": "pos",
  "status": "DELIVERED",
  "createdAt": "2020-08-28T12:13:40.544Z"
}
```

### NDJSON — Order Items
```json
{
  "_id": "68b35fc2868d406af5688c71",
  "orderId": "68b35fc2868d406af5688c70",
  "lineNo": 1,
  "itemId": "68b35fc2868d406af5688902",
  "qty": 2,
  "unitPrice": 600,
  "appliedOptions": [
    "68b35fc2868d406af5688903",
    "68b35fc2868d406af5688907"
  ]
}
```

### NDJSON — Restocks (Stage 2)
```json
{
  "_id": "68b35fc2868d406af5688a94",
  "stockItemId": "68b35fc2868d406af5688a26",
  "storeId": "68b35fc2868d406af5688771",
  "initialQty": 11310,
  "unit": "ml",
  "ttlSec": 691200,
  "createdAt": "2025-08-08T02:26:50.191Z"
}
```

### NDJSON — Stock Moves (Stage 2)
```json
{
  "_id": "68b35fc2868d406af5688c72",
  "restockId": "68b35fc2868d406af5688a98",
  "type": "issue",
  "cause": "order-accepted",
  "value": -46,
  "orderId": "68b35fc2868d406af5688c70",
  "timestamp": "2020-08-28T12:13:40.544Z"
}
```

### CSV — Weather (daily)
```csv
date,city,country,temp_min_c,temp_max_c,humidity_pct,wind_kph,precip_mm,precip_prob,weather_desc,alerts
2020-08-28,Constantine,DZ,7.5,13.6,93,6,0,0,cloudy,
```

### CSV — News/Events (public)
```csv
date,start_time_local,city,country,event_type,title,description,channel_focus,tags
2020-08-01,00:42,Constantine,DZ,local_news,Public Art Unveiled,Art initiative.,all,community|city
```

### CSV — Daily Orders Forecast (example)
```csv
date,split,y_true,y_pred
2020-08-28,train,160,179.64795793282846
```

---

## 🧠 Suggested Approach

1. Assemble base time series from orders/order_items; aggregate by day/hour and by item/category
2. Engineer calendar, weather, and event features; encode holidays and match schedules
3. Train forecasting models (per-SKU or hierarchical): baseline (naive/ETS), ML (XGBoost), or probabilistic (Prophet/statsmodels)
4. Validate with rolling-origin evaluation; tune by horizon and business metrics
6. Generate actionable outputs: staffing recommendations, ingredient usage, restock plan, and peak-hour windows

---

## 🧪 Importing the NDJSON

```bash
mongoimport --db hack-n-slice-2025 --collection items        --file items.ndjson
mongoimport --db hack-n-slice-2025 --collection options      --file options.ndjson
mongoimport --db hack-n-slice-2025 --collection orders       --file orders.ndjson
mongoimport --db hack-n-slice-2025 --collection order_items  --file order_items.ndjson

mongoimport --db hack-n-slice-2025 --collection restocks     --file restocks.ndjson
mongoimport --db hack-n-slice-2025 --collection stock_moves  --file stock_moves.ndjson
```

---

## 🧪 Evaluation Setup

- Training: first 4 years (e.g., 2020-01-01 → 2023-12-31)
- Hidden test: last 1 year (2024-01-01 → 2024-12-31)
- Report MAE/MAPE/RMSE by horizon and by key SKUs; include peak-hour accuracy

---

## 📚 Data Dictionary

### Items — product catalog
- `_id`: ObjectId (product id)
- `name`: product name (Pizza Pepperoni)
- `category`: category (Pizzas, Drinks, etc.)
- `workflow`: preparation workflow (PIZZA, BAR, etc.)
- `basePrice`: base price in cents (e.g., 600 = 600 DZD)
- `hasSize`, `hasToppings`: customization flags

### Options — modifiers (sizes, sauces, toppings, edges)
- `_id`: ObjectId (option id)
- `kind`: SIZE | SAUCE | EDGE | TOPPING
- `name`: option label (30', Tomate, Traditionnelle)
- `priceDelta`: price adjustment (int, cents)
- `itemScope`: list of item ids this option applies to

### Orders — order headers
- `_id`: ObjectId (order id)
- `storeId`: ObjectId (single store in this dataset)
- `source`: pos | delivery | online
- `status`: DELIVERED | CANCELLED | REJECTED | IN_PROGRESS
- `createdAt`: ISO date-time

### Order Items — line items
- `_id`: ObjectId (line id)
- `orderId`: reference to orders
- `lineNo`: line number (1, 2, …)
- `itemId`: reference to items
- `qty`: quantity
- `unitPrice`: base price (before options)
- `appliedOptions`: array of option ids

### Restocks (Stage 2) — ingredient batches
- `_id`: ObjectId (restock id)
- `stockItemId`: ingredient id
- `storeId`: ObjectId
- `initialQty`: starting quantity (unit below)
- `unit`: unit (pcs, gr, ml, …)
- `ttlSec`: shelf life in seconds
- `createdAt`: timestamp

### Stock Moves (Stage 2) — consumption/adjustments
- `restockId`: reference to restock
- `uuid`: unique string
- `type`: issue | adjust | etc.
- `cause`: order-accepted | waste | …
- `value`: negative = consumed, positive = added
- `orderId`: optional link to causing order
- `timestamp`: ISO date-time

---

## 🛠️ Suggested Tech Stack

- Modeling/ETL: Python, [Pandas], [NumPy], [scikit-learn], [statsmodels], [Prophet], [XGBoost]
- Notebooks/Reports: [JupyterLab], [Matplotlib]/[Seaborn], [Plotly]
- Data store: [MongoDB] (NDJSON import) or Parquet files
- Optional API/Dashboard: [NestJS v11] with a small React dashboard

---

## 💡 Optional Enhancements
- Hierarchical forecasting (store → category → item) with reconciliation
- Peak-hour nowcasting with short-horizon updates using recent orders
- Feature importance/SHAP analysis for event/weather effects
- Recipe mapping to ingredient-level forecasts; what-if simulators for promos
- Anomaly detection for data gaps and outliers; backfill strategies

Good luck, and may the best forecaster win!

---

[MongoDB NDJSON]: https://www.mongodb.com/docs/database-tools/mongoimport/#mongodb-binary-bin.mongoimport
[playground website]: https://nexopizza.github.io/hack-n-slice-constantine-2025/
[items.ndjson]: https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/items.ndjson-mUdL0RXYm2TMrbPkKC6QMylwl3ELcU.gz
[options.ndjson]: https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/options.ndjson-tL9odTf38OogRJ1WnMQXPUMAOBzleW.gz
[order_items.ndjson]: https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/order_items.ndjson-FFstMTL5hTHbSH3PmSOBxJJ0448xDS.gz
[orders.ndjson]: https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/orders.ndjson-imk5Hv1UzVVmC7dBuVKlcQITb1TEPC.gz
[restocks.ndjson]: https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/restocks.ndjson-NwdwaL61TWoJlK17k1GqQPFQqKVxss.gz
[stock_moves.ndjson]: https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/stock_moves.ndjson-34wCXuWoW3diAOs0ovypJWzXVJhiNN.gz

[Pandas]: https://pandas.pydata.org/
[NumPy]: https://numpy.org/
[scikit-learn]: https://scikit-learn.org/
[statsmodels]: https://www.statsmodels.org/
[Prophet]: https://facebook.github.io/prophet/
[XGBoost]: https://xgboost.readthedocs.io/
[JupyterLab]: https://jupyter.org/
[Matplotlib]: https://matplotlib.org/
[Seaborn]: https://seaborn.pydata.org/
[Plotly]: https://plotly.com/python/
[MongoDB]: https://www.mongodb.com/
[NestJS v11]: https://nestjs.com/
