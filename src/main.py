# main.py

import sys
from models.classifier import Classifier
from data.loader import load_data
from preprocessing.processor import Processor

def main():
    # Load the trained model and processor
    classifier = Classifier()
    classifier.load_model('model.pkl')
    processor = Processor()

    # Prompt user for transaction description
    transaction_description = input("Enter the transaction description: ")

    # Preprocess the input
    processed_description = processor.preprocess(transaction_description)

    # Predict the category and confidence score
    category, confidence = classifier.predict(processed_description)

    # Output the results
    print(f"Predicted Category: {category}")
    print(f"Confidence Score: {confidence:.2f}")

if __name__ == "__main__":
    main()