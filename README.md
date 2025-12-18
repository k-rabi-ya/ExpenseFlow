**ExpenseFlow** is a minimalist web/mobile application designed for freelancers, small business owners, or anyone managing high transaction volumes. Its core value proposition is **zero-effort expense categorization** via automated text analysis and optional receipt scanning.

Problem Statement & Solution

**The Challenge**: Users manually categorize expenses, a tedious and error-prone process that leads to incomplete spending insights.

**The Solution**: ExpenseFlow automates expense categorization through:
- **Instant Text Categorization**: Import CSV/OFX bank statements and automatically categorize all transactions
- **Receipt OCR & Categorization**: Upload receipt photos; the system extracts details and auto-categorizes
- **Learning from Feedback**: Correct misclassified transactions, and the system learns and improves over time
- **Custom Categories**: Define personal or business-specific categories

## Setup & Installation

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend development)
- PostgreSQL 12+
- Git

### Quick Start (Development)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ExpenseFlow
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Train Model** (one-time):
   ```bash
   python scripts/train_model.py --dataset data/sample_transactions.csv
   ```

4. **Frontend Setup**:
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

5. **Start the application**:
   - Backend: `python app.py` (runs on http://localhost:5000)
   - Frontend: `npm run dev` (runs on http://localhost:3000)

## 📊 Training & Evaluation

### Train the ML Model

```bash
cd backend
python scripts/train_model.py --dataset data/transactions.csv --output models/classifier.pkl
```

This will:
- Load labeled transaction data
- Train Logistic Regression + TF-IDF
- Save the model and vectorizer using joblib
- Display performance metrics (accuracy, precision, recall, F1, confusion matrix)

### Evaluate Model Performance

```bash
python scripts/evaluate_model.py --model models/classifier.pkl --test-data data/test_set.csv
```

### Run Predictions via CLI

```bash
python scripts/predict.py "Amazon charge"
# Output: Category: Shopping | Confidence: 0.87
```

## 🔄 Model Retraining (Continuous Learning)

When users correct misclassified transactions, the system:
1. Stores corrections in the database
2. Runs a nightly retraining script: `python scripts/retrain_on_feedback.py`
3. Updates the model with user feedback

## 📈 API Endpoints (Backend)

### Text Categorization
```
POST /api/categorize
Content-Type: application/json
{
  "description": "Whole Foods Market"
}
Response: { "category": "Food", "confidence": 0.92 }
```

### Batch Import (CSV)
```
POST /api/import
multipart/form-data
- file: transactions.csv
Response: { "processed": 150, "categorized": 145, "uncategorized": 5 }
```

### Receipt OCR & Categorization
```
POST /api/ocr-categorize
multipart/form-data
- image: receipt.jpg
Response: { "merchant": "Cafe", "amount": 5.50, "category": "Food", "confidence": 0.89 }
```

### Record Correction (Feedback Loop)
```
POST /api/correct
{
  "transaction_id": 123,
  "predicted_category": "Shopping",
  "correct_category": "Work Supplies"
}
Response: { "status": "recorded", "retraining_scheduled": "tonight" }
```

## 🧠 Model Details

**Algorithm**: Logistic Regression  
**Feature Extraction**: TF-IDF (Term Frequency-Inverse Document Frequency)  
**Categories**: Food, Transport, Bills, Shopping, Entertainment, Work Supplies, Health, Other  
**Training Data**: Labeled transaction descriptions (expand with user corrections over time)  
**Performance Metrics**:
- Accuracy: ~87% (on test set)
- Precision: ~0.85
- Recall: ~0.86
- F1 Score: ~0.85

**Limitations & Future Improvements**:
- Ambiguous merchants (e.g., "Amazon") benefit from additional context (item name, amount)
- OCR errors on low-quality receipt photos may reduce accuracy
- Model learns best from diverse, well-labeled user feedback
- Future: Ensemble methods, contextual embeddings (BERT), real-time model versioning

## Contributing

Contributions to ExpenseFlow are welcome! If you have suggestions for improvements or new features, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
