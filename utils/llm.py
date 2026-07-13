import streamlit as st
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

@st.cache_resource
def get_huggingface_llm():
    # Retrieve the token from Streamlit secrets
    hf_token = st.secrets.get("HUGGINGFACEHUB_API_TOKEN")
    
    if not hf_token:
        st.error("Hugging Face API Token not found in secrets.toml.")
        st.stop()

    # Initialize the Endpoint (using a popular open-source model)
    # You can change 'repo_id' to any supported text-generation model
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct", 
        huggingfacehub_api_token=hf_token,
        temperature=0.3,
        max_new_tokens=512
    )
    
    # Wrap it in ChatHuggingFace for Chat-style interaction
    return ChatHuggingFace(llm=llm)

# Usage remains similar to your previous code
llm = get_huggingface_llm()
# response = llm.invoke("Your prompt here")