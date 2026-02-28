from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.3
)


def generate_offline_interview(jd_skills, matched_skills, difficulty="medium"):

    jd_text = ", ".join(jd_skills)
    matched_text = ", ".join(matched_skills)

    prompt = ChatPromptTemplate.from_template("""
You are a senior technical interviewer.

Generate 5 {difficulty} level technical interview questions.

Rules:
- 3 questions must be based on JD required skills.
- 2 questions must be based on candidate's matched skills.
- Provide short ideal answers (3–5 lines max).
- Keep answers concise and technical.

JD Required Skills:
{jd_skills}

Candidate Matched Skills:
{matched_skills}

Format strictly like:

Q1: Question text
Answer: Short reference answer
""")

    response = llm.invoke(
        prompt.format_messages(
            jd_skills=jd_text,
            matched_skills=matched_text,
            difficulty=difficulty
        )
    )

    return response.content