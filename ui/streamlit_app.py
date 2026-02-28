import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from tools.resume_parser import extract_text_from_pdf
from agents.resume_screening_agent import extract_skills_with_llm
from tools.job_requirement_extractor import extract_jd_skills
from tools.skill_matcher import match_skills
from agents.technical_question_agent import generate_technical_questions
from agents.offline_interview_agent import generate_offline_interview

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Recruiter AI Agent", layout="wide")

st.title("🤖 Recruiter AI Agent")
st.subheader("AI-Powered Resume Screening & Interview System")


# ---------------- SESSION STATE ----------------
if "skills_list" not in st.session_state:
    st.session_state.skills_list = []

if "resume_analyzed" not in st.session_state:
    st.session_state.resume_analyzed = False

if "match_result" not in st.session_state:
    st.session_state.match_result = None

if "jd_skills" not in st.session_state:
    st.session_state.jd_skills = []
# ==================================================
#                 RESUME SECTION
# ==================================================

st.header("📄 Resume Analysis")

uploaded_file = st.file_uploader(
    "Upload Candidate Resume (PDF only)",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    st.success("Resume text extracted")

    if st.button("🔍 Analyze Resume with AI"):
        with st.spinner("Extracting skills using LLM..."):
            skills = extract_skills_with_llm(resume_text)

        st.subheader("✅ Extracted Skills")
        st.write(skills)

        # Collect all technical skills properly
        all_skills = []
        all_skills.extend(skills.get("technical_skills", []))
        all_skills.extend(skills.get("tools_and_technologies", []))

        st.session_state.skills_list = all_skills
        st.session_state.resume_analyzed = True

        st.success("Resume analyzed successfully!")


# ==================================================
#              JOB DESCRIPTION SECTION
# ==================================================

st.header("📋 Job Description Matching")

jd_text = st.text_area("Paste Job Description here")

if st.button("Match Resume with JD") and jd_text:

    if not st.session_state.resume_analyzed:
        st.warning("⚠️ Please analyze resume first.")
    else:
        with st.spinner("Extracting JD requirements..."):
            jd_data = extract_jd_skills(jd_text)
            jd_skills = jd_data.get("required_skills", [])

            st.session_state.jd_skills = jd_skills

        st.subheader("📌 JD Skills Extracted")
        st.write(jd_skills)

        # Store match result safely
        st.session_state.match_result = match_skills(
            st.session_state.skills_list,
            jd_skills
        )


# ==================================================
#              MATCH RESULTS SECTION
# ==================================================

if st.session_state.match_result:

    result = st.session_state.match_result

    st.metric("🎯 Match Percentage", f"{result['match_percentage']}%")

    col1, col2 = st.columns(2)

    with col1:
        st.success("✅ Matched Skills")
        st.write(result["matched_skills"])

    with col2:
        st.error("❌ Missing Skills")
        st.write(result["missing_skills"])


# ==================================================
#           INTERVIEW MODE SELECTION
# ==================================================

if st.session_state.match_result and st.session_state.match_result["matched_skills"]:

    st.header("🎤 Interview Mode Selection")

    interview_mode = st.radio(
        "Select Interview Mode",
        ["Offline Interview", "Online Interview"]
    )

    difficulty = st.selectbox(
        "Select Difficulty Level",
        ["easy", "medium", "hard"]
    )

    # -----------------------------
# 🟢 OFFLINE MODE
# -----------------------------
if interview_mode == "Offline Interview":

    if st.button("Generate Offline Interview Questions"):

        with st.spinner("Generating questions and reference answers..."):
            interview_content = generate_offline_interview(
                st.session_state.jd_skills,
                st.session_state.match_result["matched_skills"],
                difficulty
            )

        # Store generated content
        st.session_state.offline_content = interview_content


    # -----------------------------
    # Display Questions + Scoring
    # -----------------------------
    if "offline_content" in st.session_state:

        st.subheader("📋 Interview Questions")

        content = st.session_state.offline_content

        # Split questions
        blocks = content.split("Q")
        total_score = 0

        for i, block in enumerate(blocks):
            if block.strip() == "":
                continue

            question_block = "Q" + block.strip()

            parts = question_block.split("Answer:")
            question_text = parts[0].strip()
            answer_text = parts[1].strip() if len(parts) > 1 else "No reference answer."

            st.markdown(f"### {question_text}")

            with st.expander("📘 View Reference Answer"):
                st.write(answer_text)

            score = st.slider(
                f"Score for Question {i}",
                0, 10, 5,
                key=f"score_{i}"
            )

            total_score += score

        st.divider()

        st.subheader("📝 Interviewer Notes")
        notes = st.text_area("Write observations about candidate performance")

        st.divider()

        st.subheader("📊 Final Score")
        st.metric("Total Score (Out of 50)", total_score)

        if total_score >= 40:
            st.success("Recommendation: Strong Hire")
        elif total_score >= 30:
            st.info("Recommendation: Consider")
        else:
            st.error("Recommendation: Not Recommended")

    # -----------------------------
    # 🔵 ONLINE MODE (Coming Next)
    # -----------------------------
    if interview_mode == "Online Interview":
        st.info("Online Interview Mode will be implemented next.")