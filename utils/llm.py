import streamlit as st
from langchain_groq import ChatGroq
@st.cache_resource
def get_huggingface_llm():

    # Retrieve the token from Streamlit secrets
    groq_token = st.secrets.get("GROQ_API_KEY")
    
    if not groq_token:
        st.error("Groq API Token not found in secrets.toml.")
        st.stop()
    
    llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=groq_token
    )
    return llm

llm = get_huggingface_llm()
