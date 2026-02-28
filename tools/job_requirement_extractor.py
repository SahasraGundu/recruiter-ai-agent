from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
import os


class JDOutput(BaseModel):
    required_skills: list[str]
    good_to_have: list[str]
    experience_level: str
    location: str
    role: str


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

structured_llm = llm.with_structured_output(JDOutput)


def extract_jd_skills(jd_text: str):
    prompt = ChatPromptTemplate.from_template("""
You are an ATS system.

Extract the information from this Job Description.

Job Description:
{jd_text}
""")

    response = structured_llm.invoke(
        prompt.format_messages(jd_text=jd_text)
    )

    return response.dict()