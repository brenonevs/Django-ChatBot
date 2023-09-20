# ESSE MODELO REENVIA O PROMPT COM UM RESUMO DOS PROMPTS ANTERIORES, GASTANDO MENOS TOKENS QUE O ANTERIOR

from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain import OpenAI
from langchain.chains import ConversationChain

llm = OpenAI(model_name='text-davinci-003', temperature=0, max_tokens=256, openai_api_key="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")

sumary_memory = ConversationSummaryMemory(llm=OpenAI(openai_api_key="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"))

conversation = ConversationChain(llm=llm, verbose=True, memory=sumary_memory)

conversation.predict(input="Hi There! I am Sam")
conversation.predict(input="How are you today?")
conversation.predict(input="Can you help me with some codes?")
conversation.predict(input="Debug this code in python: 'printf('hello')'")
conversation.predict(input="okay")
print(conversation.memory.buffer)

