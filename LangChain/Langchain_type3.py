# ESSE MODELO REENVIA O PROMPT NOVO COM OS PROMPTS ANTERIORES, NO ENTANTO, VOCÊ PODE LIMITAR A QUANTIDADE DE PROMPTS ANTERIOR QUE VOCÊ DESEJA REENVIAR

from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain import OpenAI
from langchain.chains import ConversationChain

llm = llm = OpenAI(model_name='text-davinci-003', temperature=0, max_tokens=256, openai_api_key="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")

# Apenas as últimas 2 interações serão mantidas na memória
window_memory = ConversationBufferWindowMemory(k=2)

conversation = ConversationChain(llm=llm, verbose=True, memory=window_memory)

conversation.predict(input="Hi, Im Sam!")
print(conversation.memory.buffer)
conversation.predict(input="I want you to make an assumption about my political ideology based on 3 statements of mine.")
print(conversation.memory.buffer)
conversation.predict(input="I am against abortion, i love Lula so much, i hate Bolsonaro")
print(conversation.memory.buffer)
conversation.predict(input="Can you help me with some codes?")
print(conversation.memory.buffer) 