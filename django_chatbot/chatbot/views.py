from django.shortcuts import render
from django.http import JsonResponse
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.chains import ConversationChain
import openai

llm = OpenAI(model_name='gpt-3.5-turbo-0613', temperature=0, max_tokens=256, openai_api_key="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")

memory = ConversationBufferMemory() 

conversation = ConversationChain(llm=llm, verbose=True, memory=memory)

def get_last_line(text):

    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    last_line = str(lines[-1]) if lines else None
    last_line = last_line.replace("AI:", "").strip()
    return last_line

def ask_openai(message):
    conversation.predict(input=message)

    answer = get_last_line(conversation.memory.buffer)

    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html') 

def home(request):
    return render(request, 'index.html') 