# Separate imports by source for clarity
from openai import OpenAI
import logging
from decouple import config

# Grouped imports from the same module
from .models import Conversation, Message

logger = logging.getLogger(__name__)

# Constants
API_KEY = str(config("OPENAI_API_KEY"))
print(API_KEY)
CHAT_MODEL = "gpt-3.5-turbo"


class Chatbot:
    """A chatbot class for managing interactions in a chatroom."""

    def __init__(self, conversation: Conversation):
        if conversation.character:
            self.character = conversation.character
            self.prompt = conversation.character.prompt
            self.chat_model_name = conversation.character.chat_model_name
            self.client = OpenAI(api_key=API_KEY)
            self.conversation = conversation
            self.messages = [self._create_system_message()]

    def __deepcopy__(self, memo):
        """Create a deepcopy of the instance, excluding non-pickleable client."""
        return Chatbot(self.conversation)

    def _create_system_message(self):
        """Create a system message for initializing the chat."""
        return {"role": "system", "content": self.prompt}

    def fetch_new_messages(self):
        """Fetch new messages from the chatroom asynchronously."""
        self.messages = [self._create_system_message()]
        new_messages = self._query_new_messages()
        for msg in new_messages:
            formatted_message = self._format_message(msg)
            self.messages.append(formatted_message)

    def _query_new_messages(self):
        """Query new messages from the database."""
        return Message.objects.filter(conversation=self.conversation).order_by(
            "timestamp"
        )

    @staticmethod
    def _format_message(msg):
        """Format a single message for the chatbot."""
        if hasattr(msg, "charactermessage"):
            role = "assistant"
            content = msg.charactermessage.content
        elif hasattr(msg, "usermessage"):
            role = "user"
            content = msg.usermessage.content
        else:
            raise ValueError(f"Message {msg} is not a CharacterMessage or UserMessage")

        return {"role": role, "content": content}

    def get_chatbot_response(self):
        """Generate a response from the chatbot."""
        self.fetch_new_messages()
        logger.debug(f"Sending prompt with messages: {self.messages}")
        response = self.client.chat.completions.create(
            model=self.chat_model_name, messages=self.messages
        )
        return response.choices[0].message.content
