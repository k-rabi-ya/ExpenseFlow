"""
Categorization service using ML model
"""
import joblib
import os
from pathlib import Path
from typing import Tuple
import numpy as np


class CategorizationService:
    """Service for transaction categorization"""

    def __init__(self, model_path: str = None, vectorizer_path: str = None):
        """Initialize the categorization service with pre-trained model"""
        if model_path is None:
            model_path = os.getenv(
                "MODEL_PATH",
                Path(__file__).parent.parent.parent / "models" / "classifier.pkl"
            )
        if vectorizer_path is None:
            vectorizer_path = os.getenv(
                "VECTORIZER_PATH",
                Path(__file__).parent.parent.parent / "models" / "tfidf_vectorizer.pkl"
            )

        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.model_loaded = True
        except FileNotFoundError:
            self.model = None
            self.vectorizer = None
            self.model_loaded = False

    def predict(self, description: str) -> Tuple[str, float]:
        """
        Predict category for a transaction description

        Args:
            description: Transaction description text

        Returns:
            Tuple of (category, confidence_score)
        """
        if not self.model_loaded:
            return "Other", 0.0

        try:
            # Transform text to TF-IDF features
            X = self.vectorizer.transform([description])

            # Get prediction and probability
            prediction = self.model.predict(X)[0]
            probabilities = self.model.predict_proba(X)[0]
            confidence = float(np.max(probabilities))

            return prediction, confidence
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return "Other", 0.0

    def batch_predict(self, descriptions: list) -> list:
        """
        Predict categories for multiple descriptions

        Args:
            descriptions: List of transaction descriptions

        Returns:
            List of (category, confidence) tuples
        """
        return [self.predict(desc) for desc in descriptions]
