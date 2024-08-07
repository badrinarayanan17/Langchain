# Developing multi agent system for writing an news article

from crewai import Agent # For creating agents
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI # For accessing gemini 
from langchain_groq import ChatGroq
from tools import tool
import os

load_dotenv()

# Calling the gemini models

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",verbose=True, temperature=0)
# groqllm = ChatGroq(model='llama3-8b-8192',temperature=0,verbose=True)

# Developing a research agent that is responsible to communicate with all the agents to write a blog or article

researcher = Agent(
    role="Experienced Researcher",
    goal= 'Uncover ground breaking technologies in {topic}',
    memory=True,
    llm=llm,
    backstory=(
        "Driven by curiosity, you're at the forefront of innovation, eager to explore and share knowledge that could change the world."
    ),
    tools = [tool], # Google Serper Tool
    allow_delegation=True # This parameter allows the agent to collaborate with other agents
)

# Developing writer agent

writer = Agent(
    role="Article Writer", # Defining role
    goal='Narrate compelling tech stories about {topic}', # Defining goal
    backstory=(
        "With a flair for simplifying complex topics, you craft engaging narratives that captivate and educate, bringing new    discoveries to light in an accessible manner."),  # Backstory
    tools=[tool], # Calling the serper tool
    verbose=True,
    llm=llm,
    memory=True,
    allow_delegation=False # Not Required 
)