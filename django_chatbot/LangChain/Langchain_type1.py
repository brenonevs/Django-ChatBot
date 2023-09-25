# ESSE MODELO REENVIA O PROMPT NOVO COM OS PROMPTS ANTERIORES

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.chains import ConversationChain

llm = OpenAI(model_name='text-davinci-003', temperature=0, max_tokens=256, openai_api_key="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")

memory = ConversationBufferMemory() 

conversation = ConversationChain(llm=llm, verbose=True, memory=memory)

conversation.predict(input='Hi There! I am Sam')
conversation.predict(input='How are you today?')
conversation.predict(input='Can you help with some codes?')
print(conversation.memory.buffer)


