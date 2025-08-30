# Nexo Pizza Mini-Game (**Mobile App gamefication)**

A fun, pizza-themed game integrated into the Nexo Pizza app, designed to entertain customers while they wait for their order. Players earn **Nexo Coins** by completing challenges, which can later be redeemed for rewards, discounts, or special offers.

---

## 📖 Overview

Waiting for a delivery can feel boring. The **Nexo Pizza Mini-Game** makes the wait exciting by offering a simple, interactive game inside the Nexo Pizza app.

It’s fun, brand-themed, and adds value to the customer experience by combining entertainment with loyalty rewards.

**Problems it solves:**

- Long waiting times feel shorter — customers stay entertained while waiting.
- Low engagement — now customers earn **Nexo Coins** through play.
- Weak brand connection — pizza-themed games reinforce the Nexo Pizza identity.
- Limited app usage — users spend more time inside the app, not just for ordering.

**Users:**

- Customers waiting for delivery
- Customers browsing the app

---

## Game Ideas

- **Pizza Box Stacker** – Stack boxes without tipping them over.
- **Pizza Builder** – Assemble ingredients in the right order before time runs out

---

## How It Works

1. Customer places an order in the Nexo Pizza app
2. While waiting for delivery, they can open the **Mini-Game section( maybe even be availbale when network not exist)**
3. Playing games earns them **Nexo Coins** based on performance
4. Nexo Coins can be saved and redeemed for discounts, free items, or special offers
5. The game ends when the delivery arrives, or the customer can continue playing anytime

---

## Tech Stack

- **Game Framework:**
    - **Flutter Flame** (if using Flutter) → Lightweight 2D game engine perfect for mini-games inside apps
- **Backend & Data:**
    - 
- **Authentication & Security:**
    - **Firebase Authentication** → Link scores and coins to each user account
- **Offline Support:**
    - Local device storage → Allow users to play even without internet, syncing progress when back online
- **Rewards & Notifications:**
    - **Firebase Cloud Messaging** → Notify users about leaderboard updates, rewards, or special challenges

---

## Future Enhancements

- **Leaderboards** – Let customers compete by showing high scores.  The **top scorer each month** could win a special gift or exclusive reward.
- **Special Rewards** – Unlock limited-time offers or secret menu items.
- **Multiplayer Mode** – Play against friends or other Nexo Pizza customers in real time (the loser will paid the bill or split the bill).
- **Engagement Strategy** – Promote the game inside the app (push notifications, banners, rewards campaigns) to drive usage.

---

## What Needs to Be Done

To successfully build and launch the **Nexo Pizza Mini-Game**, the following tasks should be completed:

- **Game Design & Branding** – Create a fun, simple, pizza-themed game that reflects the Nexo Pizza brand identity.
- **Feature Development** – Implement the mini-games (e.g., Pizza Box Stacker, Pizza Builder) with smooth gameplay and scoring logic.
- **Rewards System** – Integrate **Nexo Coins** .
- **Offline Play Support** – Allow the game to run without internet and sync progress when reconnected.
- **Clean & Maintainable Code** – Write well-structured, documented code for easy updates and scaling.
