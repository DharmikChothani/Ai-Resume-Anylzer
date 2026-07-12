from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are an AI Interview Evaluator.

Question:

{question}

Candidate Answer:

{answer}

Evaluate.

Return JSON.

{{
"score":0,
"strengths":[],
"weaknesses":[],
"improved_answer":""
}}
""")

def evaluate(llm,question,answer):

    chain = prompt | llm | parser

    return chain.invoke({

        "question":question,
        "answer":answer

    })