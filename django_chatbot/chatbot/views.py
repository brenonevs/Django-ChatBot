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


class ChatbotView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    """ def _get_last_line(self, text):
        #Extract the last non-empty line from the text, and remove 'AI:' prefix if present.
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        last_line = lines[-1] if lines else ""
        return last_line.replace("AI:", "").strip() """

    def _process_message(self, message):
        return self.conversation.run(input=message)

    def get(self, request):
        load_dotenv()

        character_id = request.GET.get("character_id")
        character = get_object_or_404(Character, id=character_id)

        self.chat_model = ChatOpenAI(
            model_name="gpt-3.5-turbo-0613",
            temperature=0,
            max_tokens=1024,
        )

        self.system_message_template = SystemMessagePromptTemplate.from_template(
            "Você é Doutrinator, um político especialista, capaz de identificar a idelogia de qualquer pessoa a partir do que ela diz. Após a primeira frase dela, você deve dizer sua ideologia política."
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

        return render(request, "chatbot.html", {"character": character})

    def post(self, request):
        """Handle POST requests and return the response from OpenAI."""
        message = request.POST.get("message")
        if not message:
            return JsonResponse({"error": "Message is required"}, status=400)

        response = self._process_message(message)
        return JsonResponse({"message": message, "response": response})


class HomeView(View):
    def get(self, request):
        """Render the home page."""
        return render(request, "index.html")
