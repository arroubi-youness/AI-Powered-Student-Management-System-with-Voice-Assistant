import customtkinter as ctk

# Create the main application window
class ChatbotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Chatbot Interface")
        self.geometry("600x500")

        # Chat display area
        self.chat_display = ctk.CTkTextbox(self, width=550, height=350, state="disabled", wrap="word")
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

        # User input entry
        self.user_input = ctk.CTkEntry(self, placeholder_text="Type your message here...")
        self.user_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Send button
        self.send_button = ctk.CTkButton(self, text="Send", command=self.handle_send)
        self.send_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # Configure grid weights for responsiveness
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def handle_send(self):
        """Handle sending a message."""
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message("You", user_message)
            bot_response = self.get_bot_response(user_message)
            self.display_message("Bot", bot_response)
        self.user_input.delete(0, ctk.END)

    def display_message(self, sender, message):
        """Display a message in the chat display."""
        self.chat_display.configure(state="normal")
        self.chat_display.insert(ctk.END, f"{sender}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see(ctk.END)

    def get_bot_response(self, user_message):
        """Generate a response from the chatbot."""
        # Basic example; replace with actual logic or ML model integration
        return "I'm here to help! You said: " + user_message

# Run the application
if __name__ == "__main__":
    app = ChatbotApp()
    app.mainloop()
