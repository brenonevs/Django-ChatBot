# ESSE MODELO É UMA MISTURA DO MODELO 2 E DO MODELO 3

from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain import OpenAI
from langchain.chains import ConversationChain

llm = OpenAI(model_name='text-davinci-003', temperature=0, max_tokens=256, openai_api_key="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")

# Para k=2, mantém apenas as últimas 2 interações
# Para max_tokens_limit=40 limita o número de tokens, precisa de transformers instalado
memory = ConversationSummaryBufferMemory(llm=OpenAI(openai_api_key="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"))

conversation = ConversationChain(llm=llm, verbose=True, memory=memory)

conversation.predict(input="Hi There! I am Sam")
conversation.predict(input="How are you today?")
conversation.predict(input="Can you help me with some codes?")
conversation.predict(input="Debug this code in python: 'printf('hello')'")
conversation.predict(input="okay")
print(conversation.memory.buffer)

