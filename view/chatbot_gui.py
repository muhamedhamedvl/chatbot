"""
View Layer: Tkinter GUI components
===================================
This module contains the ChatbotView class which manages all UI components
and visual presentation for the chatbot application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ChatbotView:
    """
    View Layer: Manages all UI components and visual presentation.
    Responsible for rendering the chat interface and handling user interactions.
    """
    
    def __init__(self, root, model_accuracy):
        """
        Initialize the chatbot GUI
        
        Args:
            root (tk.Tk): Root window
            model_accuracy (float): Model training accuracy percentage
        """
        self.root = root
        self.root.title("Deep Learning Chatbot")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a2e")

        # UI Color scheme
        self.bg_color = "#1a1a2e"
        self.secondary_bg = "#16213e"
        self.accent_color = "#0f3460"
        self.user_msg_color = "#533483"
        self.bot_msg_color = "#16213e"
        self.text_color = "#ffffff"
        self.input_bg = "#0f3460"

        # Chat history for export functionality
        self.chat_log = []  # list of tuples: ("User"/"Bot", message)

        self.model_accuracy = model_accuracy
        
        # UI Components (initialized in setup_ui)
        self.canvas = None
        self.scrollable_frame = None
        self.input_field = None
        
        # Event callbacks (to be set by controller)
        self.on_send_message = None
        self.on_clear_input = None
        self.on_clear_chat = None
        self.on_export_chat = None
        self.on_show_about = None
        self.on_example_selected = None

        # Build UI
        self.setup_ui()
        
        # Welcome messages
        self.add_bot_message("Hello! I'm a Deep Learning Chatbot. How can I help you today?")
        self.add_bot_message(f"Model trained successfully with accuracy: {self.model_accuracy:.2f}%")


    def setup_ui(self):
        """Build and configure all UI components"""
        self._create_header_frame()
        self._create_main_chat_area()
        self._create_input_frame()
        self._create_examples_frame()
        self._create_status_bar()
    
    def _create_header_frame(self):
        """Create header with title and action buttons"""
        # ===== Top Header Frame =====
        header_frame = tk.Frame(self.root, bg="#533483", height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        left_header = tk.Frame(header_frame, bg="#533483")
        left_header.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Title
        title_label = tk.Label(
            left_header,
            text="🧠 Deep Learning Chatbot",
            font=("Helvetica", 20, "bold"),
            bg="#533483",
            fg=self.text_color
        )
        title_label.pack(anchor="w", pady=(10, 0))

        # Subtitle
        subtitle_label = tk.Label(
            left_header,
            text="Neural Network • TF-IDF • MLP Classifier",
            font=("Helvetica", 10),
            bg="#533483",
            fg="#e0e0e0"
        )
        subtitle_label.pack(anchor="w")

        # Right header buttons (About + Export + Clear Chat)
        right_header = tk.Frame(header_frame, bg="#533483")
        right_header.pack(side=tk.RIGHT, padx=10)

        about_btn = tk.Button(
            right_header,
            text="ℹ About",
            font=("Helvetica", 9),
            bg="#0f3460",
            fg=self.text_color,
            activebackground="#7b4397",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.on_show_about() if self.on_show_about else None
        )
        about_btn.pack(side=tk.TOP, pady=2, padx=5)

        export_btn = tk.Button(
            right_header,
            text="💾 Export Chat",
            font=("Helvetica", 9),
            bg="#0f3460",
            fg=self.text_color,
            activebackground="#7b4397",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.on_export_chat() if self.on_export_chat else None
        )
        export_btn.pack(side=tk.TOP, pady=2, padx=5)

        clear_chat_btn = tk.Button(
            right_header,
            text="🗑️ Clear Chat",
            font=("Helvetica", 9),
            bg="#d32f2f",
            fg=self.text_color,
            activebackground="#b71c1c",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.on_clear_chat() if self.on_clear_chat else None
        )
        clear_chat_btn.pack(side=tk.TOP, pady=2, padx=5)
    
    def _create_main_chat_area(self):
        """Create scrollable chat display area"""
        # ===== Main Chat Area =====
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Chat display area with custom scrollbar
        chat_frame = tk.Frame(main_frame, bg=self.secondary_bg)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Canvas for custom scrolling
        self.canvas = tk.Canvas(chat_frame, bg=self.secondary_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.secondary_bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Store main_frame for later use in input and examples
        self.main_frame = main_frame
    
    def _create_input_frame(self):
        """Create message input area with send and clear buttons"""
        # ===== Input frame =====
        input_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X)

        # Text input
        self.input_field = tk.Entry(
            input_frame,
            font=("Helvetica", 12),
            bg=self.input_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            relief=tk.FLAT,
            bd=10
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10)
        self.input_field.bind("<Return>", lambda e: self.on_send_message() if self.on_send_message else None)
        self.input_field.focus()

        # Clear input button
        clear_input_button = tk.Button(
            input_frame,
            text="✖ Clear",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg=self.text_color,
            activebackground=self.input_bg,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            cursor="hand2",
            command=lambda: self.on_clear_input() if self.on_clear_input else None
        )
        clear_input_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Send button
        send_button = tk.Button(
            input_frame,
            text="Send ➤",
            font=("Helvetica", 12, "bold"),
            bg="#533483",
            fg=self.text_color,
            activebackground="#7b4397",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            cursor="hand2",
            command=lambda: self.on_send_message() if self.on_send_message else None
        )
        send_button.pack(side=tk.RIGHT, padx=(10, 0))
    
    def _create_examples_frame(self):
        """Create example query buttons"""
        # ===== Example queries frame =====
        examples_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        examples_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Label(
            examples_frame,
            text="Try:",
            font=("Helvetica", 9),
            bg=self.bg_color,
            fg="#888888"
        ).pack(side=tk.LEFT, padx=(0, 5))

        examples = ["When is the lecture?", "Check my grades", "Hello", "Bye"]
        for example in examples:
            btn = tk.Button(
                examples_frame,
                text=example,
                font=("Helvetica", 8),
                bg=self.accent_color,
                fg=self.text_color,
                activebackground=self.input_bg,
                relief=tk.FLAT,
                bd=0,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda e=example: self.on_example_selected(e) if self.on_example_selected else None
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def _create_status_bar(self):
        """Create status bar at bottom"""
        # ===== Status bar =====
        status_bar = tk.Label(
            self.root,
            text="Model: MLPClassifier • Features: TF-IDF • Intents: lecture_time, grades, greet, bye",
            bd=1,
            relief=tk.SUNKEN,
            anchor="w",
            bg=self.secondary_bg,
            fg="#888888",
            font=("Helvetica", 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # ===== Message Display Methods =====
    
    def add_message(self, message, is_user=False):
        """
        Add a message bubble to the chat display
        
        Args:
            message (str): Message text
            is_user (bool): True for user messages, False for bot messages
        """
        msg_frame = tk.Frame(self.scrollable_frame, bg=self.secondary_bg)
        msg_frame.pack(fill=tk.X, padx=10, pady=5)

        if is_user:
            # User message (right aligned)
            container = tk.Frame(msg_frame, bg=self.secondary_bg)
            container.pack(anchor="e")

            msg_label = tk.Label(
                container,
                text=message,
                font=("Helvetica", 11),
                bg=self.user_msg_color,
                fg=self.text_color,
                wraplength=500,
                justify=tk.LEFT,
                padx=15,
                pady=10
            )
            msg_label.pack(side=tk.RIGHT)

            user_icon = tk.Label(
                container,
                text="👤",
                font=("Helvetica", 16),
                bg=self.secondary_bg,
                fg=self.text_color
            )
            user_icon.pack(side=tk.RIGHT, padx=(0, 5))
        else:
            # Bot message (left aligned)
            container = tk.Frame(msg_frame, bg=self.secondary_bg)
            container.pack(anchor="w")

            bot_icon = tk.Label(
                container,
                text="🤖",
                font=("Helvetica", 16),
                bg=self.secondary_bg,
                fg=self.text_color
            )
            bot_icon.pack(side=tk.LEFT, padx=(0, 5))

            msg_label = tk.Label(
                container,
                text=message,
                font=("Helvetica", 11),
                bg=self.bot_msg_color,
                fg=self.text_color,
                wraplength=500,
                justify=tk.LEFT,
                padx=15,
                pady=10
            )
            msg_label.pack(side=tk.LEFT)

        # Scroll to bottom
        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def add_bot_message(self, message):
        """Add bot message and log it"""
        self.chat_log.append(("Bot", message))
        self.add_message(message, is_user=False)

    def add_user_message(self, message):
        """Add user message and log it"""
        self.chat_log.append(("User", message))
        self.add_message(message, is_user=True)
    
    def show_thinking_indicator(self):
        """
        Show 'thinking' indicator while processing
        
        Returns:
            tk.Frame: The thinking indicator frame (to be removed later)
        """
        thinking_frame = tk.Frame(self.scrollable_frame, bg=self.secondary_bg)
        thinking_frame.pack(fill=tk.X, padx=10, pady=5)

        thinking_label = tk.Label(
            thinking_frame,
            text="🤖 Thinking...",
            font=("Helvetica", 10, "italic"),
            bg=self.secondary_bg,
            fg="#888888"
        )
        thinking_label.pack(anchor="w", padx=(30, 0))
        
        return thinking_frame
    
    def remove_thinking_indicator(self, thinking_frame):
        """Remove the thinking indicator"""
        thinking_frame.destroy()
    
    # ===== Input Field Methods =====
    
    def get_input_text(self):
        """Get text from input field"""
        return self.input_field.get().strip()
    
    def clear_input_field(self):
        """Clear the input field"""
        self.input_field.delete(0, tk.END)
        self.input_field.focus()
    
    def set_input_text(self, text):
        """Set text in input field"""
        self.input_field.delete(0, tk.END)
        self.input_field.insert(0, text)
        self.input_field.focus()
    
    # ===== Chat Management Methods =====
    
    def clear_all_messages(self):
        """Clear all chat messages from display"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.chat_log.clear()
    
    def get_chat_log(self):
        """Get the full chat history"""
        return self.chat_log
    
    # ===== Dialog Methods =====
    
    def show_about_dialog(self):
        """Show About information dialog"""
        info = (
            "Deep Learning Chatbot\n"
            "--------------------------\n"
            "• Built with Python & Tkinter\n"
            "• NLP: TF-IDF Vectorizer\n"
            "• Model: MLPClassifier (Neural Network)\n"
            "• Intents: lecture_time, grades, greet, bye\n\n"
            "Developed by: The 5 Warriors\n"
            "NLP Project"
        )
        messagebox.showinfo("About", info)
    
    def show_warning(self, title, message):
        """Show warning message box"""
        messagebox.showwarning(title, message)
    
    def show_info(self, title, message):
        """Show info message box"""
        messagebox.showinfo(title, message)
    
    def show_error(self, title, message):
        """Show error message box"""
        messagebox.showerror(title, message)
    
    def ask_yes_no(self, title, message):
        """Ask yes/no question"""
        return messagebox.askyesno(title, message)
    
    def ask_save_file(self):
        """Open save file dialog"""
        return filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Chat History"
        )
    
    # ===== Utility Methods =====
    
    def schedule_callback(self, delay_ms, callback):
        """Schedule a callback after delay"""
        self.root.after(delay_ms, callback)
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
