# 🍕 Gamified Feedback Collection 

## 🎯 Challenge Overview

In hospitality environments, collecting customer feedback is essential—but often feels tedious or intrusive. Your challenge is to **design and prototype an engaging, gamified feedback system** that encourages users to share their experience in a fun, frictionless way. Think of it as turning feedback into a moment of delight.

The goal: **increase feedback volume and quality** while making the process feel like a playful interaction rather than a chore.

## 🧩 Objectives

Participants should:

- Design interactive feedback components such as:
  - Mini-quizzes (e.g. “What kind of pizza spirit are you?”)
  - Emoji sliders (e.g. drag a pizza slice from “normal” to “foooorrrt!!”)
  - Tap-based reactions, animated buttons, or micro-games
- Ensure the system captures useful operational data (e.g. satisfaction, wait time, cleanliness, staff friendliness)
- Make it multilingual and culturally adaptable (especially French, Arabic, and English)
- Integrate visual storytelling or poetic branding (e.g. themed feedback tied to historical or seasonal events)
- Include backend logic or mock API to simulate data collection and analysis
- Consider user fatigue and accessibility — keep it lightweight, intuitive, and inclusive

## 🎮 Bonus Features (Optional but Encouraged)

- Reward systems (e.g. badges, coupons, leaderboard)
- AI-generated personalized feedback prompts
- Real-time dashboard for staff to view feedback trends
- Offline mode or QR-triggered feedback

---

## 🧠 Suggested Approach

### 1. User Journey Mapping
- Identify key touchpoints for feedback (e.g. post-order, checkout, after dining)
- Define user personas (e.g. solo diner, family, tourist) and tailor feedback formats accordingly

### 2. Gamification Strategy
- Use behavioral psychology principles (e.g. instant gratification, curiosity loops)
- Keep interactions short, visual, and rewarding
- Use humor, storytelling, or themed visuals to make feedback memorable

### 3. Data Design
- Define useful metrics (e.g. Net Promoter Score, sentiment, service ratings)
- Structure feedback data in JSON format for easy integration

---

## ✨ Sample Modules

### 🍕 Module 1: Mini-Quiz — “What Kind of Pizza Spirit Are You?”

**Theme:** Inspired by ancient Mediterranean markets and poetic archetypes (merchant, traveler, poet, artisan)

**Flow:**
1. Intro: “Welcome, traveler of taste! Let us divine your pizza spirit…”
2. Questions:
   - “Your ideal evening feels like…” (souks, gardens, taverns, chantier)
   - “How did our service feel today?” (speed, warm, complex, rhythmic)
   - “What flavor would you chase next?” (fromage, citrus mint, harissa & honey, tomato basil)
3. Result: “You are the Artisan Spirit — bold, curious, and full of fire!”  
   - Avatar + badge + optional social share  
   - Feedback stored behind the scenes

**Refinement:**
#### 🍕 Product-Specific Quiz Examples
- **Pizza**: Questions about dough, crust, sauce, baking, cheese, toppings
- **Sandwich**: Bread type, filling freshness, sauce, portion size, packagi
- **Pasta**: Pasta texture, sauce flavor, cheese, portion size
- **Chicken**: Crispiness, seasoning, tenderness, portion size
- **Dessert**: Sweetness, texture, presentation, freshness
- **Drinks**: Temperature, flavor, carbonation, packaging

### 😋 Module 2: Emoji Slider — “Rate Your Flavor Journey”

**Slider Positions:**

| Slider Position | Emoji | Label             |
|----------------|-------|-------------------|
| 0%             | 😐🍕  | “Not my taste”     |
| 25%            | 🙂🍕  | “T3adi”         |
| 50%            | 😋🍕  | “Bnina!”           |
| 75%            | 🤤🍕  | “Forrt!”       |
| 100%           | 🥰🍕  | “Mahboula!”          |

- Background changes subtly with each level
- Optional follow-up: “Would you recommend us?” 👍👎

**Sample JSON Output:**
```json
{
  "user_id": "abc123",
  "quiz_result": "Artisan Spirit",
  "service_rating": "Warm as a hearth",
  "flavor_rating": 75,
  "recommend": true
}
```

**Sample JSON of the feedback as stored in DB:**
This is the document that will be analyzed by NLP in the next subject **customer-sentiment-and-feedback-analysis**
```json
{
  "source": "Mobile App",
  "timestamp": "2025-08-29T18:15:00",
  "user_id": "abc123",
  "product_type": "pizza",
  "quiz_result": "Artisan Spirit",
  "service_rating": "Warm as a hearth",
  "flavor_choice": "Tomate basilic",
  "text_feedback": "Le service était chaleureux et fluide, et la saveur tomate basilic m’a transporté dans un jardin méditerranéen. La pâte était légère, la croûte croustillante, et la sauce parfaitement équilibrée.",
  "recommend": true,
  "language": "fr",
  "location": "El Khroub, Algeria",
  "item_details": {
    "crust": {
      "rating": 5,
      "description": "Croustillante à l’extérieur, tendre à l’intérieur"
    },
    "dough": {
      "rating": 4,
      "description": "Légère et bien levée, avec une belle élasticité"
    },
    "sauce": {
      "rating": 5,
      "description": "Tomate basilic équilibrée, fraîche et parfumée"
    },
    "cheese": {
      "rating": 4,
      "description": "Fondante, bien dosée, avec une touche de caractère"
    },
    "toppings": {
      "rating": 4,
      "description": "Fraîches, bien réparties, et harmonieuses"
    }
  }
}
```