# The main goal

As a pizzeria manager, I want to be able to predict the busiest hours of operation for my restaurant
in order to optimize staffing and inventory management.

You should be able to create a predictive model that can accurately predict some or all of the following:

- Daily order volume - how many orders/pizzas I will likely sell each day/hour
- Peak hours - the busiest hours of operation during the day
- Seasonal trends - how order volume changes with seasons, holidays, and special events
- Seasonal demand - fluctuations during weekdays, holidays, footbal events, Ramadan, summer, etc.
- Weather impact - how weather conditions (e.g., temperature, rain) affect order volume
- Special events - how local events (e.g., sports games) impact order volume
- Delivery vs pickup ratio - how the ratio of delivery to pickup orders changes over time
- Ingredient usage - how much cheese, pepperoni, and other ingredients are needed based on predicted order volume
- Stock shortages - predicting potential shortages before they happen
- Optimal restocking schedule - when and how much to order from suppliers
- Staffing needs - how many staff members are needed during different times of the day/week
- Delivery times - predicting delivery delays and recommending adjustments
- Kitchen bottlenecks – anticipating which items will cause preparation slowdowns

# Stage 1 — Demand Forecasting

Your task

- Predict future daily demand for products (pizzas, drinks, etc.).
- Use the historical orders data as your ground truth.
- Enrich with news events (football matches, holidays, etc.) and weather conditions (temperature, rain, alerts).

Data you will use

- [MongoDB NDJSON][mongoimport] collections:
    - `items.ndjson` (products catalog [link][items.ndjson])
    - `options.ndjson` (sizes, toppings, sauces, edges [link][options.ndjson])
    - `orders.ndjson` (order headers [link][orders.ndjson])
    - `order_items.ndjson` (order line items [link][order_items.ndjson])
- External signals:
    - News & events: [from playground website][playground-website]
    - Weather forecast/observations: from the same site

# Stage 2 — Out-of-Stock Effects

Your task

- Extend your model to consider ingredient restocks and stock consumption.
- Model how outages or waste influence observed demand.

Data you will use

- Additional [NDJSON][mongoimport] collections:
    - `restocks.ndjson` (batches of ingredients delivered to the store [link][restocks.ndjson])
    - `stock_moves.ndjson` (ingredient consumption, waste, corrections [link][stock_moves.ndjson])

# Importing the NDJSON

```bash
mongoimport --db hack-n-slice-2025 --collection items        --file items.ndjson
mongoimport --db hack-n-slice-2025 --collection options      --file options.ndjson
mongoimport --db hack-n-slice-2025 --collection orders       --file orders.ndjson
mongoimport --db hack-n-slice-2025 --collection order_items  --file order_items.ndjson

# Stage 2 only:
mongoimport --db hack-n-slice-2025 --collection restocks     --file restocks.ndjson
mongoimport --db hack-n-slice-2025 --collection stock_moves  --file stock_moves.ndjson
```

# If you get stuck…

We want the challenge to test your forecasting skills, not your ability to fight data formats. If you
encounter difficulties, we can provide additional support:

- If scraping the site is too hard → we can provide the raw CSVs that contain news/events and weather data.
- If you want to directly test using the true causal signals → we can provide the internal news events csv that
  includes `expected_effect` and `bias` columns (delivery/dine-in biases).

Just ask if you need more.

# Deliverables

- For Stage 1, submit forecasts of demand (daily or per-item) and a short description of how
  you incorporated news & weather.
- For Stage 2, extend your solution to account for out-of-stock effects.

# Suggested Evaluation Setup

Data split

- Training set: first 4 years of the dataset (e.g. 2020-01-01 → 2023-12-31)
- Hidden test set: last 1 year (2024-01-01 → 2024-12-31)

# Data Dictionary

## Items
### Product catalog.

_id: ObjectId (product id)
name: product name (Pizza Pepperoni)
category: category (Pizzas, Drinks, etc.)
workflow: preparation workflow (PIZZA, BAR, etc.)
basePrice: base price in cents (e.g. 600 = 600 DZD)
hasSize, hasToppings: booleans for product customization

## Options
### Modifiers (sizes, sauces, toppings, edges).

_id: ObjectId (option id)
kind: SIZE | SAUCE | EDGE | TOPPING
name: option label (30', Tomate, Traditionnelle)
priceDelta: price adjustment (int, cents)
itemScope: list of item ids this option applies to

## Orders
### Order headers.

`_id`: ObjectId (order id)
`storeId`: ObjectId (always the same store in this dataset)
`source`: pos | delivery | online
`status`: DELIVERED, CANCELLED, REJECTED, IN_PROGRESS
`createdAt`: ISO date-time

## Order Items
### Order line items.

`_id`: ObjectId (line id)
`orderId`: reference to orders
`lineNo`: line number in the order (1, 2, …)
`itemId`: reference to items
`qty`: quantity
`unitPrice`: base price (before options)
`appliedOptions`: array of option ids

## Restocks (Stage 2)
### Ingredient restock batches.

`_id`: ObjectId (restock id)
`stockItemId`: ingredient id
`storeId`: ObjectId
`initialQty`: starting quantity (unit below)
`unit`: unit (pcs, gr, ml, …)
`ttlSec`: shelf life in seconds
`createdAt`: timestamp

## Stock moves (Stage 2)
### Ingredient consumption/adjustments.

`restockId`: reference to restock
`uuid`: unique string
`type`: issue | adjust | etc.
`cause`: order-accepted, waste, …
`value`: negative = consumed, positive = added
`orderId`: optional link to the order that caused it
`timestamp`: ISO date-time

Good luck, and may the best forecaster win!

---

[https://www.mongodb.com/docs/database-tools/mongoimport/#mongodb-binary-bin.mongoimport]: mongoimport
[https://news-and-weather.2025.hns.playground.nekso.pizza]: playground-website
[https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/items.ndjson-CbtgqfG0lUliYbnwmJCmC8pzpGkzfX.gz]: items.ndjson
[https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/options.ndjson-5TPjU4AO0PnOj5dlgzeR0NbTahpRAY.gz]: options.ndjson
[https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/order_items.ndjson-QQYwJqJIfdr1uh3YE0dxnyOJdgYqvL.gz]: order_items.ndjson
[https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/orders.ndjson-L3P2bizh2D8yeznW29Og8vzWgx4p4R.gz]: orders.ndjson
[https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/restocks.ndjson-K9YIYdyZf4OXz2AoZyScZSfA7GV7MA.gz]: restocks.ndjson
[https://zot5wjpfseoymwgv.public.blob.vercel-storage.com/datasets/dynamic-demand-forecasting/stock_moves.ndjson-F1IGODrCZAk5PcaL8iB52QKOw9l5ua.gz]: stock_moves.ndjson
