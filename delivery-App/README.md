# 🚴 Delivery Man App – for **Nexo Pizza**

A smart delivery mobile app that speeds up Nexo Pizza’s delivery process by instantly receiving order details and presenting them in an interactive, easy-to-use interface for delivery riders.

---

## 📖 Overview

The **Delivery Man App** is designed for **Nexo Pizza** to streamline the entire delivery process.

It empowers riders with instant notifications, real-time maps, and detailed order information, ensuring pizzas reach customers on time while keeping managers and customers updated.

**Key problems it solves:**

- **Slow rider assignment** – Orders are sent directly to riders, removing manual assignment delays.
- **Lack of order visibility** – Customers and managers no longer wait in the dark; delivery status updates in real time.
- **No delivery insights** – Managers can now see who delivered what, when, and how long it took.

**Primary users:**

- Delivery riders

---

## Features

- **Best route suggestions** for faster delivery
- **View order location** on the map
- **Notifications for riders** when a new order is assigned
- **Notifications for customers** when their order is delivered
- **Secure login** for riders to access their account
- **View order details** (customer info, address, items, etc.)

---

## Tech Stack

- **Mobile App:** Flutter (or another modern cross-platform mobile framework)
- **Backend:** Provided via JSON APIs (no need to build backend logic)
- **Maps & Routes:** Google Maps API for location, directions, and optimized routing
- **Login & Security:** Firebase Authentication

---

## How It Works

1. Customer orders pizza in the Nexo Pizza app
2. The restaurant accepts and prepares the order using KDS
3. Once ready, if it’s a delivery, the status changes to **“Delivering”**
4. The system automatically assigns the order to the **best available rider** (based on availability, location, or another business rule such as closest distance or least busy rider)
5. The assigned rider receives the order instantly in the **Delivery Man App**
6. Rider navigates to the customer, completes the delivery, and marks the order as **“Delivered”**

---

## ✅ What Needs to Be Done

To make the **Delivery Man App** production-ready, the following tasks should be completed:

- **UI/UX Design** – Create a clean, modern design that fits the **Nexo Pizza brand** (colors, fonts, style consistency)
- **Feature Implementation** – Ensure all listed features (routing, notifications, order details, login, etc.) work smoothly
- **Code Understanding** – Review and understand the existing codebase.
- **Clean Code Practices** – Write maintainable, well-structured, and well-documented code.
- **Security & Privacy** – Protect rider and customer data with proper authentication and data handling

---

## Bonus Ideas

- **Proof of delivery** – Signature or photo confirmation
- **Live tracking for customers** – Watch the rider’s journey in real time

---

## Assets
