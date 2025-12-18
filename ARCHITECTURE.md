# ExpenseFlow - Architecture & Components Overview

## 🎯 Vision
**ExpenseFlow** transforms chaotic transaction data into organized, categorized insights through zero-effort, AI-powered expense classification.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
│                      (Next.js/React)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ • Dashboard (Stats & Overview)                           │   │
│  │ • Transaction Table (Grid View)                          │   │
│  │ • Categorization Form (Single)                           │   │
│  │ • CSV Importer (Batch)                                   │   │
│  │ • Receipt Upload (OCR)                                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API SERVER                            │
│                   (FastAPI/Python)                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ FastAPI Routes:                                          │   │
│  │ • POST /api/categorize (single transaction)             │   │
│  │ • POST /api/batch-categorize (multiple)                 │   │
│  │ • POST /api/import (CSV file)                           │   │
│  │ • POST /api/ocr-categorize (receipt image)              │   │
│  │ • POST /api/correct (user feedback)                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────┬────────────────────────┬────────────────────┬──────────┘
         │                        │                    │
         ▼                        ▼                    ▼
    ┌─────────────┐      ┌──────────────┐      ┌───────────┐
    │   ML MODEL  │      │  DATABASE    │      │   OCR API │
    │ (Inference) │      │ (PostgreSQL) │      │ (Google)  │
    ├─────────────┤      ├──────────────┤      └───────────┘
    │ • Logistic  │      │ • Users      │
    │   Regression│      │ • Transactions
    │ • TF-IDF    │      │ • Corrections│
    │ • joblib    │      │ • Categories │
    └─────────────┘      └──────────────┘
```

---

## 📦 Core Components

### 1. **Backend Services**

#### `CategorizationService` (`app/services/categorization.py`)
- **Purpose**: Inference engine for transaction categorization
- **Input**: Transaction description (text)
- **Output**: (Category, Confidence Score)
- **Model**: Pre-trained Logistic Regression + TF-IDF
- **Speed**: < 10ms per prediction

```python
service = CategorizationService()
category, confidence = service.predict("Starbucks coffee")
# Output: ("Food", 0.92)
```

#### `DatabaseModels` (`app/models/database.py`)
- **User**: Authentication & preferences
- **Transaction**: Raw transaction data + predictions
- **Correction**: User feedback for retraining
- **Categories**: Customizable expense categories

### 2. **Frontend Components**

#### `Dashboard` (Main Page)
- **Top Section**: Key stats (Total, Categorized %, Uncategorized)
- **Import Zone**: Drag-drop CSV or receipt images
- **Transaction Table**: Full list with status indicators

#### `CategorizationForm` (Interactive)
- **Input**: Free-form transaction description
- **Output**: Real-time prediction with confidence
- **Feedback**: Record if prediction was correct/incorrect

#### `TransactionTable` (Grid View)
- **Columns**: Description, Amount, Category, Confidence, Status, Actions
- **Status Colors**:
  - 🟢 Green: High confidence (>70%)
  - 🟡 Yellow: Medium confidence (50-70%)
  - 🔴 Red: Low/Uncategorized (<50%)
  - 🔵 Blue: User-corrected

---

## 🤖 ML Pipeline

### Training Phase (One-Time Setup)

```
Raw Data (CSV)
    ↓
[description, category]
    ↓
Text Preprocessing (lowercase, remove special chars)
    ↓
TF-IDF Vectorization
    ├─ Max features: 5000
    ├─ Stopwords: English
    ├─ N-grams: 1-2
    ↓
Logistic Regression Training
    ├─ Max iterations: 1000
    ├─ Random state: 42
    ↓
Model Evaluation
    ├─ Accuracy: ~87%
    ├─ Precision: ~0.85
    ├─ Recall: ~0.86
    ├─ F1 Score: ~0.85
    ↓
Save Models
    ├─ classifier.pkl
    └─ tfidf_vectorizer.pkl
```

### Inference Phase (Production)

```
New Transaction Description
    ↓
TF-IDF Vectorization (using saved vectorizer)
    ↓
Logistic Regression Prediction
    ├─ Predicted class: category
    ├─ Probabilities: confidence per category
    ↓
Post-Processing
    ├─ Extract top prediction
    ├─ Calculate max probability (confidence)
    ↓
Return (Category, Confidence)
```

---

## 🔄 Continuous Learning Workflow

### V1.1+ Feature: User Feedback Loop

```
Prediction displayed to user
    ↓
User sees: Category + Confidence
    ↓
If Correct → ✅ User acknowledges
If Wrong → 🔴 User clicks "Correct"
    ↓
[Correction recorded to database]
    ↓
Nightly Batch Job (scheduled)
    ├─ Aggregate all corrections
    ├─ Extract: (description, corrected_category)
    ├─ Merge with original training data
    ├─ Retrain model
    ├─ Evaluate performance
    ├─ If improved → Deploy new model
    └─ If degraded → Keep old model
```

---

## 📊 API Endpoints

| Method | Endpoint | Input | Output | Purpose |
|--------|----------|-------|--------|---------|
| POST | `/api/categorize` | `{description}` | `{category, confidence}` | Single prediction |
| POST | `/api/batch-categorize` | `{descriptions[]}` | `{results[], processed, categorized}` | Batch prediction |
| POST | `/api/import` | CSV file | `{processed, categorized, uncategorized}` | Import & categorize |
| POST | `/api/ocr-categorize` | Image file | `{merchant, amount, category, confidence}` | Receipt OCR + categorize |
| POST | `/api/correct` | `{transaction_id, correct_category}` | `{status, retraining_scheduled}` | Record user feedback |
| GET | `/health` | — | `{status, model_loaded}` | Health check |

---

## 📈 Performance Targets

### Latency
- **Single Prediction**: < 10ms
- **Batch (100 items)**: < 500ms
- **CSV Import (1000 rows)**: < 5s

### Accuracy
- **Current**: 87% on balanced test set
- **Target V1.5**: 90%+ (with user feedback)
- **Target V2.0**: 93%+ (with ensemble methods)

### Scalability
- **Users**: 10,000+ concurrent (via API gateway)
- **Transactions/Day**: 1M+ (async batch processing)
- **Model Size**: ~5MB (fast distribution)

---

## 🚀 Deployment Strategy

### V1.0 (MVP) - Current
```
Vercel         Digital Ocean App Platform
Frontend  ←→   Backend + Model
(Next.js)       (FastAPI) + SQLite
```

### V1.5+ (Scaling)
```
Vercel / Netlify    AWS ECS / K8s
   ↓                    ↓
Static assets      Container: FastAPI
                   Load balancer
                   Auto-scale (2-10 instances)
                   PostgreSQL (RDS)
                   Redis cache (for model versions)
```

---

## 🎓 Learning Mechanisms

### 1. **Rule-Based Preprocessing**
- Standardize merchant names ("CVS Pharmacy" → "CVS")
- Detect category keywords ("coffee" → Food)
- Handle aliases ("Starbucks" = "Coffee Shop")

### 2. **Feature Engineering** (TF-IDF)
- Automatically finds discriminative words
- Example: "Starbucks" strongly correlates → Food
- Example: "Uber" strongly correlates → Transport

### 3. **Confidence Calibration**
- High confidence (>85%): Show category, let user verify
- Medium confidence (60-85%): Ask for confirmation
- Low confidence (<60%): Manual categorization required

---

## 🔐 Security Considerations

1. **User Data**: Encrypted in transit (HTTPS) and at rest
2. **Model Predictions**: No sensitive data in feature extraction
3. **Feedback Loop**: User corrections never expose personal info
4. **API**: Rate limiting + JWT authentication (for future)

---

## 📚 Future Enhancements

### Short Term (V1.5)
- [ ] Receipt OCR integration
- [ ] Custom categories per user
- [ ] Export to Google Sheets
- [ ] Mobile-responsive design

### Medium Term (V2.0)
- [ ] React Native mobile app
- [ ] Ensemble models (improve accuracy to 93%+)
- [ ] Real-time model versioning
- [ ] Advanced analytics dashboard

### Long Term (V3.0)
- [ ] Predictive spending insights
- [ ] Budget recommendations
- [ ] Multi-currency support
- [ ] Bank account sync (Plaid API)

---

## 🛠️ Tech Stack Rationale

| Technology | Why? |
|-----------|------|
| **FastAPI** | 🚀 Fast (async), modern, auto-docs (Swagger) |
| **Next.js** | ⚡ Server-side rendering, static gen, great DX |
| **Logistic Regression** | 🎯 Fast, interpretable, perfect for text classification |
| **TF-IDF** | 📝 Battle-tested for NLP, no need for embeddings yet |
| **PostgreSQL** | 🛡️ ACID compliance, relational data |
| **Tailwind CSS** | 🎨 Utility-first, responsive, rapid prototyping |
| **Zustand** | 🏪 Lightweight state management (simpler than Redux) |

---

## 📞 Support & Questions

For architecture questions or suggestions, refer to:
- [README.md](README.md) - High-level overview
- [SETUP.md](SETUP.md) - Installation & usage
- [Code comments](backend/app/) - Implementation details
