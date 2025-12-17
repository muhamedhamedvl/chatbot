"""
Model Layer: NLP preprocessing and ML model
============================================
This module contains the NLP preprocessing logic and the machine learning
model for intent classification and response generation.
"""

import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder


class NLPPreprocessor:
    """
    Model Layer: Handles text preprocessing for NLP tasks.
    Responsible for cleaning and normalizing input text.
    """
    
    @staticmethod
    def preprocess(text):
        """
        Basic text preprocessing: lowercase + remove extra chars
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned and normalized text
        """
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation
        return text


class ChatbotMLModel:
    """
    Model Layer: Manages ML model training and prediction.
    Encapsulates TF-IDF vectorization, label encoding, and neural network.
    """
    
    def __init__(self, data_repository, preprocessor):
        """
        Initialize the ML model with data and preprocessor
        
        Args:
            data_repository (ChatbotDataRepository): Data source
            preprocessor (NLPPreprocessor): Text preprocessor
        """
        self.data_repository = data_repository
        self.preprocessor = preprocessor
        
        # ML components
        self.vectorizer = TfidfVectorizer()
        self.label_encoder = LabelEncoder()
        self.classifier = None
        self.model_accuracy = 0.0
        self.confidence_threshold = 0.5
        
    def train(self):
        """
        Train the chatbot model using data from repository.
        Sets up vectorizer, encoder, and trains the neural network.
        
        Returns:
            float: Training accuracy percentage
        """
        # Get training data
        X, y = self.data_repository.get_training_data()
        
        # Preprocess training texts
        X_clean = [self.preprocessor.preprocess(text) for text in X]
        
        # TF-IDF vectorization
        X_vectorized = self.vectorizer.fit_transform(X_clean).toarray()
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Initialize and train MLPClassifier (Neural Network)
        self.classifier = MLPClassifier(
            hidden_layer_sizes=(16, 8),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=42
        )
        self.classifier.fit(X_vectorized, y_encoded)
        
        # Calculate training accuracy
        self.model_accuracy = self.classifier.score(X_vectorized, y_encoded) * 100
        
        return self.model_accuracy
    
    def predict(self, text):
        """
        Predict intent and generate response for input text.
        Includes confidence checking and fallback handling.
        
        Args:
            text (str): User input text
            
        Returns:
            str: Bot response message
        """
        # Preprocess input
        processed_text = self.preprocessor.preprocess(text)
        
        # Vectorize input
        X_test = self.vectorizer.transform([processed_text]).toarray()
        
        # Get prediction probabilities
        probabilities = self.classifier.predict_proba(X_test)[0]
        confidence = max(probabilities)
        
        # Check confidence threshold
        if confidence < self.confidence_threshold:
            return self.data_repository.get_fallback_response()
        
        # Predict intent
        prediction = self.classifier.predict(X_test)[0]
        intent = self.label_encoder.inverse_transform([prediction])[0]
        
        # Get response from data repository
        return self.data_repository.get_response_for_intent(intent)
    
    def get_accuracy(self):
        """Return model training accuracy"""
        return self.model_accuracy
