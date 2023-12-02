from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from .models import Character, UserMessage, CharacterMessage, Conversation
import logging
from django.urls import reverse
from django.views import generic
from .forms import SignUpForm
from chatbot.chatbot import Chatbot
from django.contrib.auth.mixins import LoginRequiredMixin

logger = logging.getLogger(__name__)


class SignUp(generic.CreateView):
    form_class = SignUpForm
    template_name = "signup.html"

    def form_valid(self, form):
        # Save the new user first
        user = form.save()
        # Then log the user in
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        # Construct your base URL with reverse
        url = reverse("chatbot")

        # grab Doutrinator id
        doutrinator_id = Character.objects.get(name="Doutrinator").id

        # Prepare your query parameters as a dictionary
        query_params = {"character_id": doutrinator_id}

        # Encode the parameters into a query string
        query_string = urlencode(query_params)

        # Return the complete URL by concatenating the base URL and the encoded query string
        return f"{url}?{query_string}"


class ChatbotView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        character_id = request.GET.get("character_id")

        try:
            self.character = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            self.character = Character.objects.get(name="Doutrinator")

        # Check if there's an existing conversation ID in the session
        conversation_id = request.session.get("conversation_id")
        if conversation_id:
            try:
                self.conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                self.conversation = self._create_new_conversation()
        else:
            self.conversation = self._create_new_conversation()

        self.chatbot = Chatbot(self.conversation)

    def _create_new_conversation(self):
        conversation = Conversation.objects.create(character=self.character)
        # Store the conversation ID in the session
        self.request.session["conversation_id"] = conversation.id
        return conversation

    def _process_message(self):
        logger.info(f"Getting chatbot response.")
        return self.chatbot.get_chatbot_response()

    def get(self, request):
        return render(request, "chatbot.html", {"character": self.character})

    def post(self, request):
        logger.info(f"POST request to ChatbotView: {request.POST}")
        message = request.POST.get("message")
        if not message:
            logger.warning("POST request was made to ChatbotView without message")
            return JsonResponse({"error": "Message is required"}, status=400)

        # Create a UserMessage regardless of whether the user is authenticated
        sender = request.user if request.user.is_authenticated else None
        UserMessage.objects.create(
            content=message, sender=sender, conversation=self.conversation
        )

        response = self._process_message()

        CharacterMessage.objects.create(
            sender=self.character, content=response, conversation=self.conversation
        )

        logger.info(f"Chatbot response: {response}")
        return JsonResponse({"message": message, "response": response})


class HomeView(View):
    async def get(self, request):
        # context should be filled with characters, but asynchronously
        characters = [character async for character in Character.objects.all()]
        context = {"characters": characters}
        return render(request, "home.html", context=context)


class AboutView(View):
    def get(self, request):
        return render(request, "about.html")
    

class PersonasView(View):
    def get(self, request):
        return render(request, "personas.html")

