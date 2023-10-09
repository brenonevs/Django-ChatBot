from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate,
)
from .models import Character
import logging

logger = logging.getLogger(__name__)


class ChatbotView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        load_dotenv()

        character_id = request.GET.get("character_id")

        try:
            self.character = get_object_or_404(Character, id=character_id)
        except Exception:
            self.character = get_object_or_404(Character, name="Doutrinator")

        self.chat_model = ChatOpenAI(
            model=self.character.chat_model_name,
            temperature=0,
            max_tokens=1024,
        )
        self.system_message_template = SystemMessagePromptTemplate.from_template(
            self.character.prompt
        )
        self.message_placeholder = MessagesPlaceholder(variable_name="chat_history")
        self.human_message_template = HumanMessagePromptTemplate.from_template(
            "{input}"
        )

        self.prompt = ChatPromptTemplate(
            input_variables=["input", "chat_history"],
            messages=[
                self.system_message_template,
                self.message_placeholder,
                self.human_message_template,
            ],
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        self.conversation = ConversationChain(
            llm=self.chat_model,
            prompt=self.prompt,
            verbose=True,
            memory=self.memory,
        )

    def _process_message(self, message):
        logger.info(f"Sending message to chatbot: {message}")
        return self.conversation.run(input=message)

    def get(self, request):
        return render(request, "chatbot.html", {"character": self.character})

    def post(self, request):
        """Handle POST requests and return the response from OpenAI."""
        logger.info(f"POST request to ChatbotView: {request.POST}")
        message = request.POST.get("message")
        if not message:
            logger.warning("POST request was made to ChatbotView without message")
            return JsonResponse({"error": "Message is required"}, status=400)

        response = self._process_message(message)
        logger.info(f"Chatbot response: {response}")
        return JsonResponse({"message": message, "response": response})


class HomeView(View):
    def get(self, request):
        context = {"characters": Character.objects.all()}
        return render(request, "index.html", context=context)
