from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are an ATS expert.

Compare the Resume with the Job Description.

Resume:

{resume}

Job Description:

{jd}

Return ONLY valid JSON.

{{
    "match_percentage": integer,
    "matching_skills": [],
    "missing_skills": [],
    "matched_keywords": [],
    "missing_keywords": [],
    "experience_match": "",
    "education_match": "",
    "summary": ""
}}
""")

def compare_resume(llm, resume, jd):

    chain = prompt | llm | parser

    return chain.invoke({
        "resume": resume,
        "jd": jd
    })