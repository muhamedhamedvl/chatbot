# Deep Learning Chatbot - Multi-File Project

## 📋 Project Overview
A modular NLP chatbot application built with clean architecture principles, featuring:
- TF-IDF vectorization for text feature extraction
- MLPClassifier neural network for intent classification
- Modern Tkinter GUI interface
- Clean separation of concerns across multiple files

## 🏗️ Project Structure

```
nlp_chatbot_project/
│
├── data/
│   ├── __init__.py
│   └── intents_data.py          # Data Layer: Training data & responses
│
├── models/
│   ├── __init__.py
│   └── chatbot_model.py         # Model Layer: NLP & ML components
│
├── view/
│   ├── __init__.py
│   └── chatbot_gui.py           # View Layer: Tkinter GUI
│
├── controller/
│   ├── __init__.py
│   └── chatbot_controller.py    # Controller Layer: Event handling
│
├── main.py                      # Application entry point
├── chatbots.py                  # Original single-file version (backup)
└── README.md                    # This file
```

## 📦 File Descriptions

### Data Layer (`data/`)
- **`intents_data.py`**: Contains `ChatbotDataRepository` class
  - Manages training texts and labels
  - Stores intent response templates
  - Provides data access methods for the model layer

### Model Layer (`models/`)
- **`chatbot_model.py`**: Contains NLP and ML components
  - `NLPPreprocessor`: Text preprocessing and normalization
  - `ChatbotMLModel`: TF-IDF vectorization, MLPClassifier training, prediction logic

### View Layer (`view/`)
- **`chatbot_gui.py`**: Contains `ChatbotView` class
  - Complete Tkinter GUI implementation
  - Chat display with message bubbles
  - Input field and action buttons
  - Dialog boxes for interactions

### Controller Layer (`controller/`)
- **`chatbot_controller.py`**: Contains `ChatbotController` class
  - Connects View and Model layers
  - Handles user events (send, clear, export, etc.)
  - Coordinates message processing and responses

### Main Entry Point
- **`main.py`**: Application factory function
  - Initializes all layers in correct order
  - Wires dependencies together
  - Starts the application

## 🚀 How to Run

### Prerequisites
```bash
pip install scikit-learn numpy tkinter
```

### Running the Application
```bash
python main.py
```

The application will:
1. Initialize the data repository
2. Create and train the ML model
3. Display training accuracy
4. Launch the GUI interface

## 🎯 Features

### Supported Intents
- **lecture_time**: Ask about class schedules
- **grades**: Inquire about grades and results
- **greet**: Greet the chatbot
- **bye**: Say goodbye

### GUI Features
- 💬 Chat interface with user/bot message bubbles
- 🤖 Thinking indicator during processing
- 💾 Export chat history to text file
- 🗑️ Clear chat history
- ✖️ Clear input field
- ℹ️ About dialog with project info
- 📝 Example queries for quick testing

### Model Details
- **Feature Extraction**: TF-IDF Vectorizer
- **Classifier**: MLPClassifier (Neural Network)
  - Hidden layers: (16, 8)
  - Activation: ReLU
  - Solver: Adam
  - Max iterations: 500
- **Confidence Threshold**: 0.5

## 🏛️ Architecture Principles

### Clean Architecture
- **Separation of Concerns**: Each layer has a single responsibility
- **Dependency Rule**: Dependencies point inward (View → Controller → Model → Data)
- **Testability**: Each component can be tested independently
- **Maintainability**: Easy to modify one layer without affecting others

### Layer Responsibilities
1. **Data Layer**: Manages data storage and retrieval
2. **Model Layer**: Handles business logic (NLP/ML)
3. **View Layer**: Manages UI presentation
4. **Controller Layer**: Orchestrates interactions between layers

## 🔄 Application Flow

```
User Input → View → Controller → Model → Data
                ↓                   ↓
              Display ← Controller ← Response
```

1. User types message in GUI (View)
2. View notifies Controller via callback
3. Controller gets message from View
4. Controller passes message to Model for prediction
5. Model preprocesses text and predicts intent
6. Model retrieves response from Data layer
7. Controller updates View with bot response
8. View displays response to user

## 👥 Development Team
**The 5 Warriors** - NLP Project

## 📝 License
Educational Project

## 🔧 Maintenance Notes
- All original functionality preserved from single-file version
- Same ML model parameters and behavior
- Identical UI appearance and interactions
- Zero breaking changes to user experience
