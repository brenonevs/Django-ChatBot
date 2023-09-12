from django.shortcuts import render
from django.http import JsonResponse
import openai

openai_api_key = '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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = f'Faça uma posição sobre a minha ideologia política e dê detalhes a partir das seguintes afirmações: {message}',
        max_tokens = 1000,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    answer = response.choices[0].text.strip('.')
    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html') 
