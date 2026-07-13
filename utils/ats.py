from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate


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
    parser = PydanticOutputParser(pydantic_object=ResumeAnalysis)
    
    prompt = PromptTemplate(
        template="""
        You are an expert ATS (Applicant Tracking System) recruiter.
        Analyze the following resume and return the data in strictly valid JSON format.
        
        {format_instructions}
        
        Resume Content:
        {resume_text}
        """,
        input_variables=["resume_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | chat_model | parser
    return chain.invoke({"resume_text": resume_text})
