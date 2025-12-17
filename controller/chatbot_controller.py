"""
Controller Layer: Application orchestration
============================================
This module contains the ChatbotController class which orchestrates
interactions between the Model and View layers.
"""


class ChatbotController:
    """
    Controller Layer: Orchestrates interactions between Model and View.
    Handles user events, coordinates model predictions, and updates the view.
    """
    
    def __init__(self, view, model):
        """
        Initialize controller with view and model
        
        Args:
            view (ChatbotView): The UI view
            model (ChatbotMLModel): The ML model
        """
        self.view = view
        self.model = model
        
        # Wire up event handlers
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """Connect view events to controller methods"""
        self.view.on_send_message = self.handle_send_message
        self.view.on_clear_input = self.handle_clear_input
        self.view.on_clear_chat = self.handle_clear_chat
        self.view.on_export_chat = self.handle_export_chat
        self.view.on_show_about = self.handle_show_about
        self.view.on_example_selected = self.handle_example_selected
    
    # ===== Event Handlers =====
    
    def handle_send_message(self):
        """Handle user sending a message"""
        message = self.view.get_input_text()

        if not message:
            return

        # Display user message
        self.view.add_user_message(message)

        # Clear input field
        self.view.clear_input_field()

        # Show thinking indicator
        thinking_frame = self.view.show_thinking_indicator()

        # Schedule response after delay (simulate thinking)
        self.view.schedule_callback(
            800, 
            lambda: self._process_and_respond(message, thinking_frame)
        )
    
    def _process_and_respond(self, message, thinking_frame):
        """Process message and show bot response"""
        # Remove thinking indicator
        self.view.remove_thinking_indicator(thinking_frame)

        # Get response from model
        response = self.model.predict(message)

        # Display bot response
        self.view.add_bot_message(response)
    
    def handle_clear_input(self):
        """Handle clearing the input field"""
        self.view.clear_input_field()
    
    def handle_clear_chat(self):
        """Handle clearing all chat history"""
        result = self.view.ask_yes_no(
            "Clear Chat",
            "Are you sure you want to clear all chat history?"
        )
        if result:
            self.view.clear_all_messages()
            self.view.add_bot_message("Chat cleared! How can I help you?")
    
    def handle_export_chat(self):
        """Handle exporting chat history to file"""
        chat_log = self.view.get_chat_log()
        
        if not chat_log:
            self.view.show_warning("Export Chat", "No chat history to export.")
            return

        file_path = self.view.ask_save_file()
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for sender, msg in chat_log:
                    f.write(f"{sender}: {msg}\n")
            self.view.show_info("Export Chat", "Chat history exported successfully!")
        except Exception as e:
            self.view.show_error("Export Chat", f"Error saving file:\n{e}")
    
    def handle_show_about(self):
        """Handle showing about dialog"""
        self.view.show_about_dialog()
    
    def handle_example_selected(self, example_text):
        """Handle user clicking an example query"""
        self.view.set_input_text(example_text)
    
    def run(self):
        """Start the application"""
        self.view.run()
