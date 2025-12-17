"""
Deep Learning Chatbot Application
==================================
Main entry point for the chatbot application.

Architecture: Clean layered architecture (Data, Model, View, Controller)
- Data Layer: Training data, intents, and responses
- Model Layer: NLP preprocessing, ML model training and prediction
- View Layer: Tkinter GUI components
- Controller Layer: Application orchestration and event handling

To run the application:
    python main.py

Author: The 5 Warriors
Project: NLP Chatbot
"""

import tkinter as tk
from data import ChatbotDataRepository
from models import NLPPreprocessor, ChatbotMLModel
from view import ChatbotView
from controller import ChatbotController


def create_and_run_application():
    """
    Application Factory: Creates and wires up all layers, then runs the app.
    This is the main entry point that orchestrates the entire application.
    """
    # 1. Initialize Data Layer
    print("Initializing Data Layer...")
    data_repository = ChatbotDataRepository()
    
    # 2. Initialize Model Layer
    print("Initializing Model Layer...")
    preprocessor = NLPPreprocessor()
    ml_model = ChatbotMLModel(data_repository, preprocessor)
    
    # 3. Train the model
    print("Training ML Model...")
    model_accuracy = ml_model.train()
    print(f"Model trained successfully! Accuracy: {model_accuracy:.2f}%")
    
    # 4. Initialize View Layer
    print("Initializing GUI...")
    root = tk.Tk()
    view = ChatbotView(root, model_accuracy)
    
    # 5. Initialize Controller Layer (wires everything together)
    print("Initializing Controller...")
    controller = ChatbotController(view, ml_model)
    
    # 6. Run the application
    print("Starting application...")
    print("-" * 50)
    controller.run()


if __name__ == "__main__":
    print("=" * 50)
    print("Deep Learning Chatbot")
    print("=" * 50)
    create_and_run_application()
