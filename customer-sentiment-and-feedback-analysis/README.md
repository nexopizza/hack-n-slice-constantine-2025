
# 🤖 Customer Sentiment & Feedback Analysis

## 🎯 Project Objective
Apply Natural Language Processing (NLP) techniques to analyze customer reviews and feedback collected from the Nexo Pizza mobile app as in Feedback [Collection Gamification subject.](https://github.com/nexopizza/hack-n-slice-constantine-2025/tree/main/feedback-collection-gamification)
The goal is to detect satisfaction trends, flag potential issues early, and suggest actionable improvements or new offerings based on sentiment clusters.

---

## 🧩 Functional Requirements

### 1. 📥 Feedback Collection
- Collect customer feedback from:
  - **Mobile app feedback form**:
    - Text feedback
    - Emoji sliders or rating scales
    - Optional photo upload (e.g., order image or receipt)

### 2. 🧠 Sentiment Analysis
- Use NLP to:
  - Classify feedback as positive, neutral, or negative
  - Identify keywords and phrases associated with sentiment
  - Detect emotional tone and intensity

### 3. 📊 Trend Detection
- Track sentiment over time
- Visualize satisfaction trends
- Flag recurring issues or complaints

### 4. 💡 Suggest Improvements
- Cluster feedback by topic and sentiment
- Recommend product or service enhancements
- Identify opportunities for new offerings

---

## 🧪 Sample Data Format

### Feedback Entry
**Sample JSON of the feedback as stored in DB:**
This is the document stored by feedback form in the mobile app  as in [The Feedback Collection Gamification subject](https://github.com/nexopizza/hack-n-slice-constantine-2025/tree/main/feedback-collection-gamification)
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

### Sentiment Output
```json
{
  "sentiment": "positive",
  "confidence": 0.93,
  "keywords": [
    "chaleureux", "fluide", "tomate basilic", "croustillante", "équilibrée", "fondante"
  ],
  "emotion": "joyful",
  "persona_cluster": "Artisan Spirit",
  "suggested_action": "Promote tomato basilic as a signature flavor; highlight crust texture and poetic branding in seasonal campaign"
}
```

## 🧠 Suggested Approach

### Step-by-Step Guide
1. **Data Collection**: Generate data using the feedback input sample above
3. **Preprocessing**: Clean and tokenize text, remove stopwords, normalize data.
4. **Sentiment Analysis**: Apply NLP models to classify sentiment and extract keywords.
5. **Trend Analysis**: Aggregate sentiment over time and visualize trends.
6. **Clustering**: Group feedback by topic and sentiment to identify common themes.
7. **Recommendation Engine**: Suggest improvements based on clustered feedback.

---

## 🎓 Learning Objectives
- Understand and apply NLP techniques to real-world data
- Build a sentiment analysis pipeline
- Visualize customer satisfaction trends

---

## 💡 Optional Enhancements
- Multilingual sentiment analysis
- Real-time feedback monitoring dashboard
- Integration with CRM or support systems
