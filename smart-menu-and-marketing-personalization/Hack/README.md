## Smart Menu & Personalized Marketing

A Django + FastAPI project for smart restaurant menu recommendations, personalized marketing, and real-time analytics.  
It uses Django for backend & admin management, PostgreSQL for persistence, and FastAPI for the AI-powered recommendation service.

---

### Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/nexopizza/hack-n-slice-constantine-2025.git
cd hack-n-slice-constantine-2025/smart-menu-and-marketing-personalization/Hack
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
