from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are an expert ATS (Applicant Tracking System) and Senior Technical Recruiter.

Analyze the following resume.

Return ONLY valid JSON.

Resume:
{resume}

Return in this format:

{{
    "ats_score": integer,
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "suggestions": [],
    "recommended_roles": []
}}
""")

def analyze_resume(llm, resume_text):
    chain = prompt | llm | parser
    return chain.invoke({
        "resume": resume_text
    })