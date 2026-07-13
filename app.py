import os
import streamlit as st
from utils.parser import extract_text
from utils.ats import analyze_resume
from utils.jd_matcher import compare_resume
from utils.dashboard import ats_gauge, job_gauge, skill_chart
from utils.llm import get_huggingface_llm

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ---
st.markdown("""
    <style>
    [data-testid="collapsedControl"] { display: none; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .info-box {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0066cc;
        color: #333333;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# --- HEADER ---
st.title("📄 :blue[AI Resume] :violet[Analyzer]")
st.write("Analyze your resume using :orange[Artificial Intelligence] to get ahead in your career.")

# --- INPUT SECTION ---
resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])
job_description = st.text_area("Paste a Job Description (Optional) to calculate Match %:", height=100)

if resume:
    resume_text = extract_text(resume)
    
    if not resume_text.strip():
        st.error("No text could be extracted.")
        st.stop()
    
    # Initialize the Model
    chat_model = get_huggingface_llm()

    # --- CORE ANALYSIS ---
    with st.spinner("Analyzing..."):
        result = analyze_resume(chat_model, resume_text)
        
        jd_result = None
        if job_description.strip():
            jd_result = compare_resume(chat_model, resume_text, job_description)

    st.success("Analysis Complete!")
    st.divider()

    # --- SUMMARY METRICS ---
    col1, col2, col3 = st.columns(3) 
    # Convert the Pydantic object to a dictionary
    result_dict = result.model_dump()

# Now .get() will work perfectly
    ats_score = result_dict.get("ats_score", 0)
    match_score = jd_result.get("match_percentage", 0) if jd_result else 0
    
    col1.metric("ATS Score", f"{ats_score}/100")
    col2.metric("Job Match", f"{match_score}%" if jd_result else "N/A")
    res_dict = result.model_dump() 
    col3.metric("Resume Level", res_dict.get("resume_level", "Unknown"))
    col1.metric("Match Score", res_dict.get("match_percentage", 0))
    st.divider()

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Analysis", "📈 Charts"])
    res = result.model_dump()
    with tab1:
        gauge_col1, gauge_col2 = st.columns(2)
        with gauge_col1:
            st.plotly_chart(ats_gauge(ats_score), use_container_width=True)
        with gauge_col2:
            if jd_result:
                st.plotly_chart(job_gauge(match_score), use_container_width=True)
        st.write(res.get("summary", "No summary provided."))
    res = result.model_dump()
    with tab2:
        with st.expander("💪 Strengths", expanded=True):
            for item in res.get("strengths", []): st.success(item)
        with st.expander("⚠️ Weaknesses"):
            for item in res.get("weaknesses", []): st.error(item)
        with st.expander("💡 Suggestions"):
            for tip in res.get("suggestions", []): st.info(tip)
        
        st.subheader("🎯 Recommended Roles")
        roles = res.get("recommended_roles", [])
        st.write(roles if roles else "No specific roles recommended.")

    with tab3:
        res = result.model_dump()
        missing_skills = res.get("missing_skills", [])
        if missing_skills:
            st.plotly_chart(skill_chart(missing_skills), use_container_width=True)
            for skill in missing_skills: st.warning(skill)
        else:
            st.success("No key skills missing.")