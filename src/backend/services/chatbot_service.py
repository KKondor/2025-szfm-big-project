"""Chatbot service for handling AI interactions via Gemini API."""
import os
import google.generativeai as genai
from typing import Optional


class ChatbotService:
    """Service for managing chatbot interactions with Google Gemini."""

    def __init__(self):
        """Initialize the chatbot service with Gemini API key."""
        api_key = os.getenv("AI_API_KEY")
        if not api_key:
            raise RuntimeError("AI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        system_instruction = (
            "You are a helpful chatbot assistant for a restaurant. "
            "Help customers with their orders, menu questions, and general inquiries."
        )
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash-lite",
            system_instruction=system_instruction
        )
        self.conversation_history = {}  # Store conversation history per user

    def send_message(self, user_id: int, message: str) -> str:
        """
        Send a message to the chatbot and get a response.
        
        Parameters:
            user_id (int): ID of the user sending the message.
            message (str): The user's message.
        
        Returns:
            str: The chatbot's response.
        
        Raises:
            ValueError: If message is empty or invalid.
            RuntimeError: If API call fails.
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")
        
        if len(message) > 5000:
            raise ValueError("Message exceeds maximum length of 5000 characters")
        
        try:
            # Initialize conversation history for new users
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = self.model.start_chat(history=[])
            
            chat = self.conversation_history[user_id]
            response = chat.send_message(message)
            
            return response.text
        except Exception as e:
            raise RuntimeError(f"Chatbot error: {str(e)}")

    def clear_history(self, user_id: int) -> None:
        """
        Clear conversation history for a user.
        
        Parameters:
            user_id (int): ID of the user whose history should be cleared.
        """
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]


# Shared instance
chatbot_service = ChatbotService()
