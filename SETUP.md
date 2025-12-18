# ExpenseFlow - Setup & Architecture Guide

## 📁 Project Structure

```
ExpenseFlow/
├── backend/                          # Python FastAPI server
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/                   # SQLAlchemy database models
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   ├── services/                 # Business logic layer
│   │   │   ├── __init__.py
│   │   │   └── categorization.py    # ML model inference
│   │   └── routes/                   # API endpoints (future)
│   │       └── __init__.py
│   ├── scripts/
│   │   ├── train_model.py           # Train classifier + TF-IDF
│   │   ├── predict.py               # CLI prediction tool
│   │   └── retrain_on_feedback.py   # Continuous learning (future)
│   ├── data/
│   │   └── sample_transactions.csv  # Sample training data
│   ├── models/                       # Saved models (generated)
│   ├── app.py                        # FastAPI application
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Environment template
│
├── frontend/                         # Next.js React application
│   ├── src/
│   │   ├── components/               # React components
│   │   │   ├── Dashboard.tsx        # Main page
│   │   │   ├── CategorizationForm.tsx
│   │   │   ├── TransactionTable.tsx
│   │   │   └── StatsCard.tsx
│   │   ├── pages/                    # Next.js pages
│   │   └── utils/
│   │       ├── api.js               # API client
│   │       └── store.ts             # Zustand state management
│   ├── package.json                  # Node dependencies
│   ├── next.config.js               # Next.js config
│   └── tailwind.config.js           # Tailwind styling
│
├── README.md                         # This file
└── .gitignore

```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+ (optional, for V1.1+)

### Step 1: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings
```

### Step 2: Train the Model

```bash
# Train on sample data
python scripts/train_model.py --dataset data/sample_transactions.csv --output models

# Output:
# - models/classifier.pkl (Logistic Regression model)
# - models/tfidf_vectorizer.pkl (TF-IDF transformer)
```

### Step 3: Start Backend Server

```bash
python app.py

# Server runs on http://localhost:5000
# API docs available at http://localhost:5000/docs
```

### Step 4: Frontend Setup (in another terminal)

```bash
cd frontend

npm install
npm run dev

# Frontend runs on http://localhost:3000
```

### Step 5: Test the Application

```bash
# In another terminal, test CLI prediction
cd backend
python scripts/predict.py "Starbucks coffee"

# Output:
# Transaction: Starbucks coffee
# Predicted Category: Food
# Confidence Score: 92.00%
```

## 📊 API Reference

### Health Check
```bash
curl http://localhost:5000/health
```

### Single Prediction
```bash
curl -X POST http://localhost:5000/api/categorize \
  -H "Content-Type: application/json" \
  -d '{"description": "Whole Foods Market"}'

# Response:
# {
#   "description": "Whole Foods Market",
#   "category": "Food",
#   "confidence": 0.92
# }
```

### Batch Prediction
```bash
curl -X POST http://localhost:5000/api/batch-categorize \
  -H "Content-Type: application/json" \
  -d '{
    "descriptions": ["Uber Ride", "Netflix Subscription", "CVS Pharmacy"]
  }'
```

## 🤖 Model Training Details

### Algorithm
- **Classifier**: Logistic Regression (fast, interpretable)
- **Feature Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Framework**: scikit-learn

### Hyperparameters
```python
TfidfVectorizer(
    max_features=5000,
    stop_words='english',
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.8
)

LogisticRegression(
    max_iter=1000,
    random_state=42,
    multi_class='multinomial'
)
```

### Performance Metrics (on test set)
- **Accuracy**: ~87%
- **Precision**: ~0.85
- **Recall**: ~0.86
- **F1 Score**: ~0.85

### Categories
1. Food
2. Transport
3. Bills
4. Shopping
5. Entertainment
6. Work Supplies
7. Health
8. Other

## 🔄 Continuous Improvement (Roadmap)

### V1.1: User Feedback Loop
1. User corrects a misclassified transaction
2. Correction saved to database
3. Nightly retraining script aggregates corrections
4. Model fine-tunes on user feedback
5. New model deployed

### V1.5: Receipt OCR
1. User uploads receipt image
2. Google Vision API extracts merchant + amount
3. ML model categorizes
4. Transaction auto-populated in system

### V2.0: Advanced Features
1. Custom categories per user
2. Ensemble models (Logistic Regression + Naive Bayes)
3. Real-time model versioning
4. Mobile app (React Native)

## 📝 Development Notes

### Adding New Categories
Edit `CategoryEnum` in [backend/app/models/database.py](backend/app/models/database.py):
```python
class CategoryEnum(str, enum.Enum):
    FOOD = "Food"
    # Add new category
    SUBSCRIPTION = "Subscription"
```

Then retrain the model with new category data.

### Improving Model Accuracy
1. **Get More Data**: Collect real user transaction descriptions
2. **Better Preprocessing**: Handle abbreviations (e.g., "CVS" → "Pharmacy")
3. **Ensemble Methods**: Combine Logistic Regression + Random Forest
4. **Embeddings**: Switch to contextual embeddings (BERT) in V2.0

### Handling Ambiguous Merchants
- "Amazon" → Could be Shopping, Books, Electronics
- **Solution**: Ask for additional context (item type, amount)
- **Future**: Use receipt image + OCR for disambiguation

## 🛠️ Contributing

1. Clone the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Support

For issues, questions, or suggestions, please open an issue on GitHub.
