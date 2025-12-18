"""
Prediction CLI script
"""
import sys
import joblib
from pathlib import Path
import argparse


def predict_category(description: str, model_path: str = "models/classifier.pkl",
                    vectorizer_path: str = "models/tfidf_vectorizer.pkl"):
    """
    Predict category for a transaction description

    Args:
        description: Transaction description
        model_path: Path to trained model
        vectorizer_path: Path to TF-IDF vectorizer
    """
    try:
        # Load model and vectorizer
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)

        # Transform and predict
        X = vectorizer.transform([description])
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        confidence = max(probabilities)

        print(f"\nTransaction: {description}")
        print(f"Predicted Category: {prediction}")
        print(f"Confidence Score: {confidence:.2%}\n")

    except FileNotFoundError as e:
        print(f"Error: Model files not found. Please train the model first.\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict expense category from description")
    parser.add_argument("description", type=str, help="Transaction description")
    parser.add_argument(
        "--model",
        type=str,
        default="models/classifier.pkl",
        help="Path to trained model"
    )
    parser.add_argument(
        "--vectorizer",
        type=str,
        default="models/tfidf_vectorizer.pkl",
        help="Path to TF-IDF vectorizer"
    )

    args = parser.parse_args()
    predict_category(args.description, args.model, args.vectorizer)
