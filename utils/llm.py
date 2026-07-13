import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

@st.cache_resource
def get_gemini_llm():
    # Retrieve the API key from Streamlit secrets
    api_key = st.secrets.get("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("Google API Key not found in secrets.toml.")
        st.stop()

    # Initialize Gemini
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash", 
        google_api_key=api_key,
        temperature=0.3
    )