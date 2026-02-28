import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from tools.resume_parser import extract_text_from_pdf
from agents.resume_screening_agent import extract_skills_with_llm 
from tools.job_requirement_extractor import extract_jd_skills
from tools.skill_matcher import match_skills


# ---------- Page Config ----------
st.set_page_config(page_title="Recruiter AI Agent", layout="wide")
st.title("🤖 Recruiter AI Agent")
st.subheader("Resume Screening & Skill Extraction")


# ---------- Session State ----------
if "skills_list" not in st.session_state:
    st.session_state.skills_list = []

if "resume_analyzed" not in st.session_state:
    st.session_state.resume_analyzed = False


# ---------- Resume Upload ----------
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

        # 🔥 FIXED PART: Extract ALL skill categories properly
        all_skills = []

        all_skills.extend(skills.get("technical_skills", []))
        all_skills.extend(skills.get("tools_and_technologies", []))

        st.session_state.skills_list = all_skills
        st.session_state.resume_analyzed = True

        st.success("Resume analyzed successfully!")


# ---------- JD Matching ----------
st.subheader("📄 Job Description Matching")

jd_text = st.text_area("Paste Job Description here")

if st.button("Match Resume with JD") and jd_text:

    if not st.session_state.resume_analyzed:
        st.warning("⚠️ Please analyze resume first.")
    else:
        jd_data = extract_jd_skills(jd_text)
        jd_skills = jd_data.get("required_skills", [])

        st.write("Resume Skills:", st.session_state.skills_list)
        st.write("JD Skills Extracted:", jd_skills)

        match_result = match_skills(
            st.session_state.skills_list,
            jd_skills
        )

        st.metric("🎯 Match Percentage", f"{match_result['match_percentage']}%")

        col1, col2 = st.columns(2)

        with col1:
            st.success("✅ Matched Skills")
            st.write(match_result["matched_skills"])

        with col2:
            st.error("❌ Missing Skills")
            st.write(match_result["missing_skills"])