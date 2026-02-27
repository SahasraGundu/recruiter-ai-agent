import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from tools.resume_parser import extract_text_from_pdf
from agents.resume_screening_agent import extract_skills_with_llm
st.set_page_config(page_title="Recruiter AI Agent", layout="wide")

st.title("🤖 Recruiter AI Agent")
st.subheader("Resume Screening & Skill Extraction")

uploaded_file = st.file_uploader(
    "Upload Candidate Resume (PDF only)",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("📄 Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.success("Resume text extracted")

    if st.button("🔍 Analyze Resume with AI"):
        with st.spinner("🧠 LLM analyzing resume..."):
            skills = extract_skills_with_llm(resume_text)

        st.subheader("✅ Extracted Skills")
        st.write(skills)