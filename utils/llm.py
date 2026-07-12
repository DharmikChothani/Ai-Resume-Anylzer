import os
import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()

@st.cache_resource
def get_llm():
    """Initializes and returns the Qwen3-8B model."""
    
    # Initialize the endpoint
    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen3-8B",
        task="text-generation",
        max_new_tokens=1024,
        temperature=0.2, # Low temp for factual, analytical responses
        
    )
    
    # Wrap it in the Chat interface
    chat = ChatHuggingFace(llm=llm)
    
    return chat