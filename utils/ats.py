from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

# 1. Define the exact structure you want
class ResumeAnalysis(BaseModel):
    ats_score: int = Field(description="Score out of 100")
    resume_level: str = Field(description="Level of the resume, e.g., Entry-level, Mid-level")
    summary: str = Field(description="Brief summary of the resume")
    strengths: List[str] = Field(description="List of strengths")
    weaknesses: List[str] = Field(description="List of weaknesses")
    suggestions: List[str] = Field(description="List of suggestions for improvement")
    recommended_roles: List[str] = Field(description="List of recommended job roles")
    missing_skills: List[str] = Field(description="List of missing key skills")

def analyze_resume(chat_model, resume_text):
    # 2. Bind the structured output to the model
    structured_llm = chat_model.with_structured_output(ResumeAnalysis)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert ATS resume analyzer. Extract the data into the requested JSON schema."),
        ("user", "Analyze the following resume:\n\n{resume}")
    ])
    
    # 3. Create the chain
    chain = prompt | structured_llm
    
    # 4. Invoke
    # Result will now be a Pydantic object, we convert to dict to match your app.py
    result = chain.invoke({"resume": resume_text})
    return result.model_dump()