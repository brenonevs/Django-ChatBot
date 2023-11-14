from urllib.parse import urlencode
from django.shortcuts import render
from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate,
)
from decouple import config
from .models import Character, UserMessage, CharacterMessage, Conversation
import logging
from django.urls import reverse
from django.views import generic
from .forms import SignUpForm

logger = logging.getLogger(__name__)


class SignUp(generic.CreateView):
    form_class = SignUpForm
    template_name = "signup.html"

    async def form_valid(self, form):
        # Save the new user first
        user = form.save()
        # Then log the user in
        login(self.request, user)
        return super(SignUp, self).form_valid(form)

    async def get_success_url(self):
        # Construct your base URL with reverse
        url = reverse("chatbot")

        # grab Doutrinator id
        doutrinator_id = await Character.objects.aget(name="Doutrinator").id

        # Prepare your query parameters as a dictionary
        query_params = {"character_id": doutrinator_id}

        # Encode the parameters into a query string
        query_string = urlencode(query_params)

        # Return the complete URL by concatenating the base URL and the encoded query string
        return f"{url}?{query_string}"


class ChatbotView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        character_id = request.GET.get("character_id")

        try:
            self.character = Character.objects.get(id=character_id)
        except Exception:
            self.character = Character.objects.get(name="Doutrinator")

        self.chat_model = ChatOpenAI(
            openai_api_key=str(config("OPENAI_API_KEY")),
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

        self.conversation_chain = ConversationChain(
            llm=self.chat_model,
            prompt=self.prompt,
            verbose=True,
            memory=self.memory,
        )

        self.conversation = Conversation.objects.create(character=self.character)

    def _process_message(self, message):
        logger.info(f"Sending message to chatbot: {message}")
        return self.conversation_chain.run(input=message)

    def get(self, request):
        return render(request, "chatbot.html", {"character": self.character})

    def post(self, request):
        """Handle POST requests and return the response from OpenAI."""
        logger.info(f"POST request to ChatbotView: {request.POST}")
        message = request.POST.get("message")
        if not message:
            logger.warning("POST request was made to ChatbotView without message")
            return JsonResponse({"error": "Message is required"}, status=400)

        UserMessage.objects.create(content=message)

        response = self._process_message(message)

        CharacterMessage.objects.create(sender=self.character, content=response)

        logger.info(f"Chatbot response: {response}")
        return JsonResponse({"message": message, "response": response})


class HomeView(View):
    async def get(self, request):
        # context should be filled with characters, but asynchronously
        characters = [character async for character in Character.objects.all()]
        context = {"characters": characters}
        return render(request, "index.html", context=context)
