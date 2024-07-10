# Globalize text - A application for those who lacks in communication, they can use this app and they can reframe their mail etc.
# Langchain, Open source llm's, Streamlit

import streamlit as st 
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# import os

# load_dotenv()

# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") 

st.set_page_config(page_title="Globalize Email",page_icon="💬") # Setting up some initial things
st.header("Globalize Text",divider='rainbow')

col1, col2 = st.columns(2) # Creating 2 cols

with col1: # Col1 can perform the below
    st.markdown("Struggling to find the right words for your emails? Whether you need to sound professional or keep it casual, our app is here to help! Using advanced language models, we transform your text into polished, well-phrased emails. Simply input your message, choose the tone—formal or informal—and let our app do the rest. Perfect for anyone looking to improve their communication skills effortlessly.")
with col2: # Col2 can perform the below
    st.image(image="communication.png",width=450,caption="Good Communication Takes You Places 🚀")

st.markdown("## Enter Your Email To Convert") 

col3, col4 = st.columns(2)

# Tone and Dialect
with col3: 
    tone = st.selectbox('Which tone would you like to have in email', ('Formal','Informal'))
with col4:
    dialect = st.selectbox('Which english dialect you like',('British','American'))

def getdata(): # For getting the user input
    inp = st.text_area(label="Field",placeholder="Type Your Email")
    return inp

email = getdata()
st.write(email) # Reflecting the response

st.markdown("## Your Converted Email") 

if tone == "Formal" or dialect == "British" or dialect == "American": # Specifying the conditions
    prompts = ChatPromptTemplate.from_messages([
        ("system","You are an email expert, turn the poor communication into formal tone, use british or american dialect"),
        ("user","Question:{question}")
    ])
    
elif tone == "Informal" or dialect == "American" or dialect == "British" : 
    prompts = ChatPromptTemplate.from_messages([
        ("system","You are an email expert, turn the poor communication into informal tone, use american or british dialect"),
        ("user","Question:{question}")
    ])

groqllm = ChatGroq(model='llama3-8b-8192',temperature=0) # Instancing groq
output = StrOutputParser() # Parsing
chain = prompts|groqllm|output # Chain

if email:
    st.write(chain.invoke({'question': email})) # Invoking the chain