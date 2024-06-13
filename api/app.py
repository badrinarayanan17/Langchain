# Defining API routes for calling each model, whether it is paid llm's or open source llms

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate # Prompt template
from langchain_community.llms import Ollama # Open souce llms
from langchain.chat_models import ChatOpenAI # If I'm using Open AI models
from langserve import add_routes # For adding all the add_routes
# Specific routes to interact with specific models (openai,llama,claude)
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# os.environ["OPENAI_API_KEY"]=os.getenv["OPENAI_API_KEY"] # For getting OpenAI API key from env

# Fastapi Instance

app = FastAPI(
    title="Langchain Server"
)

# Adding the routes
 
# add_routes(
#     app,
#     ChatOpenAI(),
#     path="./openai"
# )

# Integrating with prompt template 

# model = ChatOpenAI()
llm = Ollama(model="llama2")

# Defining the prompts for each models
promptOne = ChatPromptTemplate.from_template("Write an essay about a {topic} with 200 words") # This is for OpenAI routes
promptTwo = ChatPromptTemplate.from_template("You are a consultation friend {topic}, give proper insights for the user queries") # This is for Ollama routes, calling llm models

# add_routes(
#     app,
#     promptOne|model,
#     path="/essay" # Api url
# )

add_routes(
    app,
    promptTwo|llm, # chain
    path="/story" # Api url(Endpoint)
)

# Invoking the api server
if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)


