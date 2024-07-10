# Creating a basic chainlit user interface

import chainlit as cl # Getting chainlit
from langchain_core.prompts import ChatPromptTemplate # For prompts
from langchain_groq import ChatGroq # Inferencing
from langchain_core.output_parsers import StrOutputParser # Parsers
from  dotenv import load_dotenv # For detecting env
import os   

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") # Getting the API key


prompt = """
    (system: ,You are a law assistant, answer the user queries related to specific topic),
    (user:, Question: {question})  """
    
promptinstance = ChatPromptTemplate.from_template(prompt)
    
    
# Chainlit has a lot of decorators for each and every purpose
# @cl.langchain_factory(use_async=True)

@cl.on_message # Decorator
async def assistant(message:cl.Message):
    input_text = message.content # Holds the content
    groqllm = ChatGroq(model="llama3-8b-8192",temperature=0) # llama3 model 
    output = StrOutputParser() 
    chain = promptinstance|groqllm|output # Chain
    res = chain.invoke({'question': input_text}) # Invoking the chain
    await cl.Message(content=res).send() # Sending the response back to the customer

if __name__ == "main":
    cl.run(assistant) 
        