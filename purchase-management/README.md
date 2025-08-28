
# 📦 Stock and Purchase Management System

## 📘 Project Overview
This project involves designing a **mobile-friendly application for inventory and purchase management** for store managers. The system helps track stock levels, identify missing products, and generate a printable or shareable purchase list with quantities and suppliers information for each product.

Managers can use their mobile devices to:
- Check inventory levels
- Identify products below the minimum allowed quantity
- Add new products with relevant details
- Automatically generate a purchase list with supplier contact information

---

## 📱 Key Features
- **Mobile-Friendly UI**: Optimized for smartphones and tablets
- **Inventory Tracking**: Manually update product quantities
- **Product Management**: Add/edit products with fields:
  - Name
  - Price
  - Unit (e.g., kg, liter, piece)
  - Supplier name and contact
  - Minimum allowed quantity
  - etc
- **Purchase List Generation**: Automatically compile a list of products below the threshold
- **Export Options**: Share or print the purchase list for procurement

---

## 🧾 Sample Product Entry
```json
{
  "name": "Tomatoes",
  "price": 2.5,
  "unit": "kg",
  "supplier": {
    "name": "Fresh Farms",
    "contact-name": "Abbass",
    "contact-phone": "0567778987"
  },
  "min_quantity": 10,
  "reference_quantity": 30,
  "current_quantity": 6,
}
```

---

## 📤 Output Format (Purchase List)
```json
[
  {
    "name": "Tomatoes",
    "quantity_needed": 24,
    "supplier": {
      "name": "Fresh Farms",
      "contact": "freshfarms@example.com"
    }
  },
  {
    "name": "Olive Oil",
    "quantity_needed": 2,
    "supplier": {
      "name": "Olive Co",
      "contact": "contact@oliveco.com"
    }
  }
]
```


## 🎯 Learning Objectives
- Build a responsive web interface for inventory management
- Model product data and supplier relationships
- Implement logic to detect low-stock items
- Generate and export purchase lists

---

## 💡 Optional Enhancements
- Add barcode scanning for inventory updates
- Include product categories, search and filtering
- Enable notifications for low-stock alerts
- Support multi-user access with authentication
