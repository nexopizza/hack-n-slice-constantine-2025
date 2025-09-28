# 🍽 Smart Menu AI

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

```bash
pip install -r ../requirements.txt
pip install jupyter matplotlib seaborn plotly
npm install
```

---

## Setup & Launch

1. **Start Django backend** (in project root, separate terminal):

```bash
python manage.py runserver 0.0.0.0:8000
```

2. **Launch Jupyter notebooks**:

```bash
jupyter notebook notebooks/
```

3. **Run frontend**:

```bash
npm start
```

> ⚠️ Without connecting to backend, frontend shows demo data only.

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
Username: test
Password: test
```

---

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

---
