import unittest
from src.models.classifier import Classifier

class TestClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = Classifier()
        self.training_data = [
            {"description": "Grocery store purchase", "category": "Groceries"},
            {"description": "Monthly rent payment", "category": "Housing"},
            {"description": "Electricity bill payment", "category": "Utilities"},
        ]
        self.classifier.train(self.training_data)

    def test_prediction(self):
        test_description = "Bought some fruits and vegetables"
        predicted_category, confidence = self.classifier.predict(test_description)
        self.assertIn(predicted_category, ["Groceries", "Housing", "Utilities"])
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)

    def test_training(self):
        self.assertTrue(self.classifier.is_trained)

    def test_invalid_description(self):
        predicted_category, confidence = self.classifier.predict("")
        self.assertEqual(predicted_category, "Unknown")
        self.assertEqual(confidence, 0.0)

if __name__ == '__main__':
    unittest.main()