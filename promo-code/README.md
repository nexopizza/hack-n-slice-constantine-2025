

#  🎟️ Rule-Based Promotion System with Promo Codes

## 🎯 Project Overview
Design and implement a rule-based promotion engine that evaluates customer orders and determines applicable promotional offers. The system uses **facts** (order details) and **rules** (promo conditions) to decide whether a discount should be applied.

Additionally, the system should provide a **simple user interface (UI)** that allows users to create promotions. These promotions are converted into structured **facts**, which are then evaluated against predefined rules.

---

## 🧩 Key Concepts
- **Facts**: Real-time data about an order (e.g., date, time, items, order type).
- **Rules**: Conditions that define when a promo code is valid.
- **Evaluation Engine**: Logic that checks if the facts satisfy the rules.
- **Discount Application**: Logic to compute the final price if a promo is applied.
- **UI for Promotion Creation**: Interface for users to define promotions, which are converted into facts.

---

## 🧪 Example Use Case
> **Promo**: "50% off the second pizza"  
> **Conditions**:
> - Only on weekends (Friday or Saturday)
> - Applicable only from 11am to 2pm
> - Only for pizzas 30 cm or larger
> - Only for takeaway or delivery orders
> - Minimum of 2 pizzas in the order

---

## 📥 Input Format (Facts)
```json
{
  "datetime": "2025-08-30T19:45:00",
  "order_type": "delivery",
  "items": [
    {"name": "Margherita", "category": "pizza", "size_cm": 30, "price": 12.0},
    {"name": "Pepperoni", "category": "pizza", "size_cm": 32, "price": 14.0}
  ]
}
```

---

## 📜 Promo Rule Format
```json
{
  "promo_code": "WEEKEND50",
  "description": "50% off second pizza on weekends",
  "conditions": {
    "day_of_week": ["Saturday", "Sunday"],
    "min_pizza_size_cm": 30,
    "order_type": ["delivery", "takeaway"],
    "min_pizza_count": 2
  },
  "discount": {
    "type": "percentage",
    "value": 50,
    "target": "second_pizza"
  }
}
```

---

## 📤 Output Format (Evaluation Result)
```json
{
  "promo_applied": true,
  "promo_code": "WEEKEND50",
  "discount_amount": 7.0,
  "final_price": 19.0
}
```

---

## 🛠 Hint
Use an existing **rule engine**

---

## 💡 Learning Objectives
- Understand how to model business rules in code
- Practice working with structured data (JSON)
- Learn how to evaluate conditions dynamically
- Build a modular and testable backend system
- Create a user-friendly interface for defining promotions

---

## 💡 Optional Challenges
- Support multiple promo codes and choose the best one
- Add expiration dates or usage limits to promo codes
- Create a web interface to test promo codes
- Log evaluation steps for debugging

