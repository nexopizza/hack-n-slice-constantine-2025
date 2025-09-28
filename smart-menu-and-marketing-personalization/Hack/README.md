## Smart Menu & Personalized Marketing

A Django + FastAPI project for smart restaurant menu recommendations, personalized marketing, and real-time analytics.  
It uses Django for backend & admin management, PostgreSQL for persistence, and FastAPI for the AI-powered recommendation service.

---

### Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/laufeyland/Hack.git
cd Hack
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements_ai.txt
```

### 4. Database Setup (PostgreSQL)
- Ensure PostgreSQL is installed and running.  
- Create a database named **slice**:
```sql
CREATE DATABASE slice;
```
- Update your `settings.py` with your PostgreSQL username and password.

### 5. Run Django Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed the Database
```bash
python seed_db.py
```

### 7. Start the Django Server
```bash
python manage.py runserver
```

---

##  Start the AI Recommendation Service (FastAPI)
The AI service lives in `src/api`.

```bash
uvicorn src.api:app --reload --port 8001
```

---

##  Example of a recommendation
```bash
/recommendations?user_id=11
```

Response :

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
        "timestamp": "2025-09-28T20:49:16.976829",
        "system_version": "2.0.0"
    }
}
```
