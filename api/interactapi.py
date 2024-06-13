import requests
import streamlit as st

# Getting the response from ollama

# def getOpenAIResponse(input_text):
#     response = requests.post("http://localhost:8000/story/invoke", # Url which is responsible for calling 
#                              json={'input':{'topic':input_text}}) # Hit the url along with this input
#     return response.json()['output']['content']# Dictionary

def getOllamaResponse(input_text):
    response = requests.post("http://localhost:8000/story/invoke", # Url which is responsible for calling 
                             json={'input':{'topic':input_text}}) # Hit the url along with this input
    return response.json()['output'] # Dictionary

# Streamlit

st.title("Langchain with LLAMA2 API")
inputText = st.text_input("Write a story")

if input:
    st.write(getOllamaResponse(inputText))
    

