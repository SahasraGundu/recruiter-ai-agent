from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.3
)


def generate_technical_questions(skills, difficulty="medium"):
    """
    Generate technical interview questions based on skills list.
    """

    skills_text = ", ".join(skills)

    prompt = ChatPromptTemplate.from_template("""
You are a senior technical interviewer.

Generate 5 {difficulty} level technical interview questions 
based ONLY on the following skills:

Skills:
{skills}

Rules:
- Questions must be technical.
- Mix conceptual and practical questions.
- No explanations.
- Return only a numbered list.
""")

    response = llm.invoke(
        prompt.format_messages(
            skills=skills_text,
            difficulty=difficulty
        )
    )

    return response.content