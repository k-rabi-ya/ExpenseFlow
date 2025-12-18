"""
Training script for the ML model
"""
import pandas as pd
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import argparse
import os


def train_model(dataset_path: str, output_dir: str = "models"):
    """
    Train the expense categorization model

    Args:
        dataset_path: Path to CSV file with columns: description, category
        output_dir: Directory to save trained model and vectorizer
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Load dataset
    print(f"Loading dataset from {dataset_path}...")
    df = pd.read_csv(dataset_path)

    if 'description' not in df.columns or 'category' not in df.columns:
        raise ValueError("Dataset must have 'description' and 'category' columns")

    # Split data
    X = df['description'].values
    y = df['category'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    print(f"Categories: {set(y)}\n")

    # Feature extraction
    print("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.8
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Train model
    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, random_state=42, multi_class='multinomial')
    model.fit(X_train_tfidf, y_train)

    # Evaluate
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)

    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}\n")

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model and vectorizer
    model_path = os.path.join(output_dir, "classifier.pkl")
    vectorizer_path = os.path.join(output_dir, "tfidf_vectorizer.pkl")

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    print(f"\nModel saved to {model_path}")
    print(f"Vectorizer saved to {vectorizer_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train expense categorization model")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to training dataset CSV file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models",
        help="Output directory for model and vectorizer"
    )

    args = parser.parse_args()
    train_model(args.dataset, args.output)
