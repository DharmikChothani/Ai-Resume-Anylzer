from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are an experienced AI Career Advisor.

Analyze the candidate's resume and the provided job description.

Resume:
{resume}

Job Description:
{jd}

Return ONLY valid JSON in the following format:

{{
  "career_match_score": 0,
  "recommended_roles": [],
  "salary_range": "",
  "top_skills_to_learn": [],
  "recommended_certifications": [],
  "career_summary": "",
  "next_steps": []
}}
""")

def career_advisor(llm, resume, jd):
    chain = prompt | llm | parser
    return chain.invoke({
        "resume": resume,
        "jd": jd
    })