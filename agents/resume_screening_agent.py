from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
import json

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

def extract_skills_with_llm(resume_text: str):
    """
    Extract structured resume information:
    - Technical Skills
    - Tools & Technologies
    - Certifications
    - Hackathons
    - Workshops
    """

    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template="""
You are an AI recruitment assistant.

From the resume text below, extract information into the following STRICT categories.
If a category is not present, return an empty list.

Return ONLY valid JSON in this exact format:

{{
  "technical_skills": [],
  "tools_and_technologies": [],
  "certifications": [],
  "hackathons_and_competitions": [],
  "workshops_and_training": []
}}

Rules:
- Do NOT add explanations
- Do NOT repeat items
- Do NOT mix categories
- Keep items concise

Resume Text:
{resume_text}
"""
    )

    response = llm.invoke(prompt.format(resume_text=resume_text))

    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {
            "technical_skills": [],
            "tools_and_technologies": [],
            "certifications": [],
            "hackathons_and_competitions": [],
            "workshops_and_training": []
        }