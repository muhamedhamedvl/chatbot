"""
Data Layer: Training data, intents, and response templates
===========================================================
This module contains the ChatbotDataRepository class which manages
all training data, intent labels, and response templates for the chatbot.
"""

import random


class ChatbotDataRepository:
    """
    Data Layer: Manages training data, intents, and response templates.
    Responsible for providing data to the model layer.
    """
    
    def __init__(self):
        """Initialize training data and response templates"""
        self.training_texts = [
            # lecture_time intents
            "when is the lecture",
            "what time is class",
            "class schedule",
            "when do we study",
            "lecture time",
            "what time is the lecture",

            # grades intents
            "grades",
            "my marks",
            "what is my score",
            "when are results released",
            "my grade",
            "results",
            "check grades",
            "tell me my marks",

            # greet intents
            "hello",
            "hi",
            "hey",
            "good morning",

            # bye intents
            "goodbye",
            "bye",
            "see you later"
        ]

        self.training_labels = [
            # lecture_time labels
            "lecture_time",
            "lecture_time",
            "lecture_time",
            "lecture_time",
            "lecture_time",
            "lecture_time",

            # grades labels
            "grades",
            "grades",
            "grades",
            "grades",
            "grades",
            "grades",
            "grades",
            "grades",

            # greet labels
            "greet",
            "greet",
            "greet",
            "greet",

            # bye labels
            "bye",
            "bye",
            "bye"
        ]

        self.intent_responses = {
            "lecture_time": [
                "Lecture is on Monday at 10 AM.",
                "Classes are scheduled for Monday at 10:00 AM.",
                "The lecture time is Monday 10 AM."
            ],
            "grades": [
                "Your grades will be announced soon.",
                "Results will be released next week.",
                "Grades are currently being processed and will be available shortly."
            ],
            "greet": [
                "Hello! How can I help you today?",
                "Hi there! Ask me about lecture times or grades.",
                "Hey! I'm here to answer your questions about the course."
            ],
            "bye": [
                "Goodbye! 👋",
                "See you later!",
                "Bye! Feel free to come back anytime."
            ]
        }
    
    def get_training_data(self):
        """Return training texts and labels"""
        return self.training_texts, self.training_labels
    
    def get_response_for_intent(self, intent):
        """Get a random response for the given intent"""
        responses = self.intent_responses.get(intent, ["Sorry, I didn't understand."])
        return random.choice(responses)
    
    def get_fallback_response(self):
        """Get fallback response for low confidence predictions"""
        return "Sorry, I didn't understand your question. Try asking about lecture times or grades."
