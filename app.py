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
    layout="wide"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #f8f9fa;
    }

    /* Hide default streamlit menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    .hero h1 {
        color: #ffffff;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .hero p {
        color: #a0aec0;
        font-size: 1.1rem;
        margin: 0;
    }
    .hero span {
        color: #63b3ed;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    /* Score box */
    .score-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 24px rgba(102,126,234,0.4);
    }
    .score-number {
        font-size: 4rem;
        font-weight: 900;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .score-label {
        font-size: 1rem;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Skill badges */
    .skill-matched {
        display: inline-block;
        background: #c6f6d5;
        color: #22543d;
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    .skill-missing {
        display: inline-block;
        background: #fed7d7;
        color: #742a2a;
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }

    /* Section title */
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.5);
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed #cbd5e0;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        font-size: 0.95rem;
    }
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.15);
    }
</style>
""", unsafe_allow_html=True)

# ── HERO SECTION ──
st.markdown("""
<div class="hero">
    <h1>📄 AI Resume <span>Screener</span></h1>
    <p>Upload a resume and paste a job description — get an instant match score and skill gap analysis</p>
</div>
""", unsafe_allow_html=True)

# ── INPUT SECTION ──
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-title">📁 Upload Resume (PDF)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} uploaded successfully!")

with col2:
    st.markdown('<div class="section-title">📋 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area("", placeholder="Paste the job description here...", height=180, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# ── SCREEN BUTTON ──
col_btn = st.columns([1, 2, 1])[1]
with col_btn:
    screen_clicked = st.button("🔍 Screen Resume")

if screen_clicked:
    if not uploaded_file:
        st.warning("⚠️ Please upload a resume PDF first.")
    elif not jd_text.strip():
        st.warning("⚠️ Please paste a job description.")
    else:
        with st.spinner("🤖 Analyzing resume... this may take a moment"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            resume_text = parse_resume(tmp_path)
            score = get_match_score(resume_text, jd_text)
            skills = get_skill_gap(resume_text, jd_text)
            os.unlink(tmp_path)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)

        # ── RESULTS ──
        # Score + feedback side by side
        col_score, col_feedback = st.columns([1, 2], gap="large")

        with col_score:
            score_color = "#48bb78" if score >= 70 else "#ed8936" if score >= 45 else "#fc8181"
            st.markdown(f"""
            <div class="score-box">
                <div class="score-number">{score}%</div>
                <div class="score-label">Match Score</div>
            </div>
            """, unsafe_allow_html=True)

        with col_feedback:
            st.markdown('<div class="section-title">📊 Analysis Summary</div>', unsafe_allow_html=True)
            if score >= 70:
                st.success("🟢 **Strong Match!** This resume aligns well with the job requirements.")
            elif score >= 45:
                st.warning("🟡 **Moderate Match.** Some important skills or experience may be missing.")
            else:
                st.error("🔴 **Low Match.** This resume doesn't align well with the job description.")

            st.markdown("<br>", unsafe_allow_html=True)
            total_jd_skills = len(skills["jd_skills"])
            total_matched = len(skills["matched"])
            if total_jd_skills > 0:
                skill_pct = round((total_matched / total_jd_skills) * 100)
                st.markdown(f"**Skill Coverage:** {total_matched} of {total_jd_skills} required skills found ({skill_pct}%)")
                st.progress(skill_pct / 100)

        st.markdown("<br>", unsafe_allow_html=True)

        # Skills breakdown
        col3, col4 = st.columns(2, gap="large")

        with col3:
            st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
            if skills["matched"]:
                badges = "".join([f'<span class="skill-matched">✓ {s}</span>' for s in skills["matched"]])
                st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)
            else:
                st.info("No matching skills found from our skills list.")

        with col4:
            st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
            if skills["missing"]:
                badges = "".join([f'<span class="skill-missing">✗ {s}</span>' for s in skills["missing"]])
                st.markdown(f'<div>{badges}</div>', unsafe_allow_html=True)
            else:
                st.success("🎉 No missing skills — excellent match!")

        st.markdown("<br>", unsafe_allow_html=True)

        # Extracted text
        with st.expander("📃 View Extracted Resume Text"):
            st.text(resume_text[:2000])