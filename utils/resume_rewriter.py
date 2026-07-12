from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are an expert Resume Writer and ATS Specialist.

Task:
Rewrite the resume to improve clarity, professionalism,
and ATS compatibility.

Rules:
- Never invent experience or achievements.
- Improve wording only.
- Use strong action verbs.
- Add measurable impact ONLY if it is already implied.
- Optimize for the given Job Description.

Resume:
{resume}

Job Description:
{jd}

Return ONLY valid JSON.

{{
"professional_summary":"",
"experience":[
"",
""
],
"projects":[
"",
""
],
"skills":[
"",
""
],
"additional_suggestions":[]
}}
""")

def rewrite_resume(llm, resume, jd):
    chain = prompt | llm | parser

    return chain.invoke({
        "resume": resume,
        "jd": jd
    })