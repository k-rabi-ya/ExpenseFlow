class Classifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None

    def train(self, X_train, y_train):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.pipeline import make_pipeline

        self.vectorizer = TfidfVectorizer()
        self.model = make_pipeline(self.vectorizer, MultinomialNB())
        self.model.fit(X_train, y_train)

    def save_model(self, model_path, vectorizer_path):
        import joblib
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)

    def predict(self, transaction_descriptions):
        return self.model.predict(transaction_descriptions), self.model.predict_proba(transaction_descriptions)