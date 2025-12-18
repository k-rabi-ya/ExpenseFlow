import unittest
from src.preprocessing.processor import Processor

class TestProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = Processor()

    def test_tokenization(self):
        text = "This is a sample transaction description."
        expected_output = ["This", "is", "a", "sample", "transaction", "description"]
        self.assertEqual(self.processor.tokenize(text), expected_output)

    def test_tfidf_transformation(self):
        documents = [
            "This is the first document.",
            "This document is the second document.",
            "And this is the third one.",
            "Is this the first document?"
        ]
        tfidf_matrix = self.processor.tfidf_transform(documents)
        self.assertEqual(tfidf_matrix.shape[0], len(documents))
        self.assertGreater(tfidf_matrix.shape[1], 0)

if __name__ == '__main__':
    unittest.main()