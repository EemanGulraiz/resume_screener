import streamlit as st
import tempfile
import os
from parser import parse_resume
from scorer import get_match_score
from skill_extractor import get_skill_gap

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="centered"
)

# ── HEADER ──
st.title("📄 AI Resume Screener")
st.markdown("Upload a resume and paste a job description to see how well they match.")
st.divider()

# ── INPUT SECTION ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

with col2:
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the job description here", height=200)

st.divider()

# ── SCREEN BUTTON ──
if st.button("🔍 Screen Resume", use_container_width=True):

    # Validate inputs
    if not uploaded_file:
        st.warning("⚠️ Please upload a resume PDF first.")
    elif not jd_text.strip():
        st.warning("⚠️ Please paste a job description.")
    else:
        with st.spinner("Analyzing resume... please wait"):

            # Save uploaded PDF to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            # Run all three modules
            resume_text = parse_resume(tmp_path)
            score = get_match_score(resume_text, jd_text)
            skills = get_skill_gap(resume_text, jd_text)

            # Clean up temp file
            os.unlink(tmp_path)

        st.divider()

        # ── RESULTS SECTION ──
        st.subheader("📊 Results")

        # Score display
        st.markdown("### Match Score")
        score_color = (
            "🟢" if score >= 70
            else "🟡" if score >= 45
            else "🔴"
        )
        st.metric(label="Overall Match", value=f"{score}%", delta=None)
        st.progress(score / 100)
        if score >= 70:
            st.success("Strong match! This candidate fits the role well.")
        elif score >= 45:
            st.warning("Moderate match. Some key skills may be missing.")
        else:
            st.error("Low match. The resume doesn't align well with this job.")

        st.divider()

        # Skills breakdown
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### ✅ Matched Skills")
            if skills["matched"]:
                for skill in skills["matched"]:
                    st.success(skill)
            else:
                st.info("No matching skills found.")

        with col4:
            st.markdown("### ❌ Missing Skills")
            if skills["missing"]:
                for skill in skills["missing"]:
                    st.error(skill)
            else:
                st.info("No missing skills — great fit!")

        st.divider()

        # Raw resume text (expandable)
        with st.expander("📃 View Extracted Resume Text"):
            st.text(resume_text[:2000])