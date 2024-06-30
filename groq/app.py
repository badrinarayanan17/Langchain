# End to End Advanced RAG - GROQ Inferencing

import streamlit as st
from langchain_groq import ChatGroq # For inferencing
from langchain_community.document_loaders import WebBaseLoader # Scraping the web
from langchain_community.embeddings import OllamaEmbeddings # For vector embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain # For chaining
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
import os # For detecting env


load_dotenv()


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY") # Setting up the groq environment

# Using session state in streamlit - Remembers the history of widgets and variables

# Initially performing vector embeddings

if "vectors" not in st.session_state:

    st.session_state.embeddings = OllamaEmbeddings()
    st.session_state.loader = WebBaseLoader("https://fastapi.tiangolo.com/#license") # Loading the document (Url - Web)
    st.session_state.docs = st.session_state.loader.load() # Essential step
    
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    # Chunk overlap maintains context and continuity between chunks
    # If there are two consecutive chunks, the first 200 characters of the second chunk will be the same as the last 200 characters of the first chunk.
    
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:5])
    # Storing into vector store - Chroma DB
    st.session_state.vectors = Chroma.from_documents(st.session_state.final_documents,st.session_state.embeddings)
    
st.title("Talk with fastapi docs, the leading API framework in python")

# Instancing the model using groq inference

groqllm = ChatGroq(model="Gemma-7b-It",temperature=0) # Using gemma open source model
    
# Defining prompt template

prompt = ChatPromptTemplate.from_template(
    """
    Answer to the question with full accuracy, don't go with unrelated context
    
    <context>
    {context}
    <context/>
    
    Question:{input} 
    
    """
)

# Chain and Retriever

documentChain = create_stuff_documents_chain(groqllm,prompt) # Combining these

# Retrieving from the vector store
retriever = st.session_state.vectors.as_retriever()

# Retrieval chain
# Combining both chain and retriever

retrievalChain = create_retrieval_chain(documentChain,retriever)


prompt = st.text_input("Give your queries on fastapi")

if prompt:
    response = retrievalChain.invoke({"input":prompt})
    st.write(response['answer'])
    
    # Expander to getting the context
    
    with st.expander("Similarity Search"):
        
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_context)
    
    
    
