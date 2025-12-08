"""Chatbot service for handling AI interactions via OpenRouter API with menu context."""
import os
import requests
from typing import Optional
from services.foods_service import food_service


class ChatbotService:
    """Service for managing chatbot interactions with OpenRouter."""

    def __init__(self):
        """Initialize the chatbot service with OpenRouter API key."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY not found in environment variables")

        self.api_key = api_key
        # Pick any supported model from OpenRouter (swap if needed)
        self.model = "tngtech/deepseek-r1t2-chimera:free"

        self.base_instruction = (
            "You are a helpful chatbot assistant for a restaurant. "
            "Help customers with their orders, menu questions, and general inquiries."
        )
        self.conversation_history = {}  # Store conversation history per user

    def _get_foods_context(self) -> str:
        """Build a text context from all foods in DB."""
        try:
            foods = food_service.get_all_food()  # <-- correct call
            menu_lines = []
            for food in foods:
                menu_lines.append(
                    f"{food.name} ({food.category}) - {food.description} - {food.price}Ft"
                )
            return "\n".join(menu_lines)
        except Exception as e:
            return f"Menu data unavailable: {e}"

    def send_message(self, user_id: int, message: str) -> str:
        """
        Send a message to the chatbot and get a response.

        Parameters:
            user_id (int): ID of the user sending the message.
            message (str): The user's message.

        Returns:
            str: The chatbot's response.
        """
        if not message or not message.strip():
            raise ValueError("Message cannot be empty")

        if len(message) > 5000:
            raise ValueError("Message exceeds maximum length of 5000 characters")

        # Initialize conversation history for new users
        if user_id not in self.conversation_history:
            foods_context = self._get_foods_context()
            system_message = {
                "role": "system",
                "content": (
                    f"{self.base_instruction}\n\n"
                    f"Here is the current menu:\n{foods_context}"
                ),
            }
            self.conversation_history[user_id] = [system_message]

        # Add user message
        self.conversation_history[user_id].append({"role": "user", "content": message})

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": self.conversation_history[user_id],
                },
                timeout=30,
            )

            data = response.json()
            reply = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "Sorry, I couldn't generate a reply.")
            )

            # Add bot reply to history
            self.conversation_history[user_id].append(
                {"role": "assistant", "content": reply}
            )

            return reply
        except Exception as e:
            raise RuntimeError(f"Chatbot error: {str(e)}")

    def clear_history(self, user_id: int) -> None:
        """Clear conversation history for a user."""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]


# Shared instance
chatbot_service = ChatbotService()
