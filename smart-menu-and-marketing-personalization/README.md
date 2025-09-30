# Smart Menu AI

Hybrid AI-powered menu recommendation system (backend + frontend demo) for restaurants. Combines **collaborative filtering**, **popularity scoring**, and **contextual intelligence**.

---

## Table of Contents

* [Overview](#overview)  
* [Prerequisites](#prerequisites)  
* [Setup & Launch](#setup--launch)  
* [Notebooks](#notebooks)  
* [Frontend Demo](#frontend-demo)  
* [Technical Architecture](#technical-architecture)  
* [Performance Metrics](#performance-metrics)  
* [Future Improvements](#future-improvements)  

---

## Overview

**Smart Menu AI** provides personalized menu recommendations using:

* **Collaborative Filtering (CF)** – "People like you also liked…"  
* **Popularity-based Scoring** – Trending items  
* **Contextual Intelligence** – Time, budget, dietary preferences  

**Hybrid Scoring Formula:**

```
Hybrid Score = (CF)^0.7 × (Popularity)^0.3
```

---

## Prerequisites

- Python 3.9+  
- PostgreSQL  
- Node.js + npm  

---

## Setup & Launch

### 1. Clone the Repository
```bash
git clone https://github.com/nexopizza/hack-n-slice-constantine-2025.git
cd hack-n-slice-constantine-2025/smart-menu-and-marketing-personalization/frontend
```

### 2. Create a Virtual Environment (for the backend)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements_ai.txt
```

Install frontend dependencies:
```bash
cd ..
npm install
```

### 4. Database Setup (PostgreSQL)
- Ensure PostgreSQL is installed and running.  
- Create a database named `slice`:
```sql
CREATE DATABASE slice;
```
- Update `backend/settings.py` with your PostgreSQL username and password.

### 5. Apply Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed the Database
```bash
python seed_db.py
```

### 7. Start the Backend (Django)
```bash
python manage.py runserver 0.0.0.0:8000
```

### 8. Start the AI Recommendation Service (FastAPI)
```bash
uvicorn src.api:app --reload
```

### 9. Launch Jupyter Notebooks (Optional, for experiments)
```bash
jupyter notebook notebooks/
```

### 10. Run the Frontend
```bash
cd ..
npm start
```

> Without connecting to the backend, the frontend runs with demo data only.

---

## Notebooks

* `hackathon_presentation.ipynb` – Full hybrid AI workflow, visualizations, and demos  
* `cf.ipynb` – Collaborative filtering: user-item matrix, similarity, cold start handling  
* `contextual.ipynb` – Context-aware recommendations: time, budget, dietary, seasonal factors  
* `popularity.ipynb` – Popularity scoring: trends, recency decay, scoring optimization  

---

## Frontend Demo

**Features Implemented:**

* Mocked AI recommendations in "For You" section  
* Questionnaire popup (content filled via backend)  
* Static menu demo (defaults to Veggie Pizza)  
* Translations (`i18n.js`)  
* Demo visuals: cart, coins/rewards system  

**Tech Stack:**

* React.js + TypeScript  
* CSS & TailwindCSS  
* Axios for API calls  
* i18n.js for translations  

**Testing Account:**

```
Username: karim_dz
Password: password123
```

---

## Backend Demo
#### Send a POST request to the following endpoint
```bash
/recommendations?user_id={id}
ex : /recommendations?user_id=11
```

#### Response :

```bash
"recommendations": [
        {
            "item_id": 631,
            "name": "Mushroom Vegetarian",
            "category": "pizza",
            "subcategory": "pizza",
            "price": 650.0,
            "dietary_tags": [
                "vegetarian"
            ],
            "time_preference": "dinner",
            "budget_category": "low",
            "score": 0.47692799999999985,
            "cf_score": 0.0,
            "hybrid_score": 0.009438817989113002,
            "smart_score": 0.5150822399999998
        },
        {
            "item_id": 592,
            "name": "3 Cheeses",
            "category": "pizza",
            "subcategory": "pizza",
            "price": 500.0,
            "dietary_tags": [
                "vegetarian"
            ],
            "time_preference": "dinner",
            "budget_category": "low",
            "score": 0.38154239999999995,
            "cf_score": 0.0,
            "hybrid_score": 0.008073851584127623,
            "smart_score": 0.41206579199999993
        },
        {
            "item_id": 630,
            "name": "Vegetarian",
            "category": "pizza",
            "subcategory": "pizza",
            "price": 450.0,
            "dietary_tags": [
                "vegetarian"
            ],
            "time_preference": "dinner",
            "budget_category": "low",
            "score": 0.38154239999999995,
            "cf_score": 0.0,
            "hybrid_score": 0.008073851584127623,
            "smart_score": 0.41206579199999993
        },
        {
            "item_id": 594,
            "name": "Anchovies",
            "category": "pizza",
            "subcategory": "pizza",
            "price": 700.0,
            "dietary_tags": [],
            "time_preference": "dinner",
            "budget_category": "low",
            "score": 0.36686769235472655,
            "cf_score": 0.0,
            "hybrid_score": 0.007855203783901374,
            "smart_score": 0.39621710774310465
        }
    ],
    "metadata": {
        "user_id": 20,
        "time_of_day": "dinner",
        "budget_level": null,
        "total_recommendations": 10,
        "from_cache": false,
        "processing_time_seconds": 0.768348,
        "timestamp": "2025-09-28T20:00:16.976829",
        "system_version": "2.0.0"
    }
}
```


## Technical Architecture

**System Flow:**

```
User Input → Context Processing → Hybrid Engine → Personalization → Response
```

**Components:**

* Collaborative Filtering – item-item similarity (cosine)  
* Popularity Scoring – recency-decayed popularity  
* Contextual Intelligence – time, budget, dietary, seasonality  
* Hybrid Engine – weighted geometric mean  
* Personalization – user preference integration  
* Diversity Enhancement – category limiting  

---

## Performance Metrics

* Response Time (<100ms)  
* Accuracy & User Satisfaction  
* Coverage (% of items recommended)  
* Diversity (variety of categories)  
* Cold Start handling  
* Memory Usage  

**Visualization Tools:** heatmaps, time series, scatter plots, bar charts, network graphs  

---

## Future Improvements

* Full AI integration with backend  
* Dynamic questionnaire with allergy/preferences data  
* Coins/reward system fully implemented  
* Polished user account area & separate pages  
* Enhanced UX & frontend pages  
