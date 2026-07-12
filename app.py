import streamlit as st
import pandas as pd
from utils.parser import extract_text
from utils.ats import analyze_resume
from utils.llm import get_llm
from utils.jd_matcher import compare_resume
from utils.resume_rewriter import rewrite_resume
from utils.dashboard import ats_gauge, job_gauge, skill_chart


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed" # Forces sidebar to stay closed
)

# --- CSS TO HIDE DEFAULT STREAMLIT UI ELEMENTS & FIX OVERLAP ---
st.markdown("""
    <style>
    /* Hide the sidebar toggle button */
    [data-testid="collapsedControl"] {
        display: none;
    }
    /* Hide the top right hamburger menu */
    #MainMenu {visibility: hidden;}
    /* Hide the default Streamlit footer */
    footer {visibility: hidden;}
    /* Hide the header line */
    header {visibility: hidden;}

    /* Custom Info Box Style */
    .info-box {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0066cc;
        color: #333333;
        margin-top: 10px; /* Pushes the box down so it doesn't overlap the title */
        margin-bottom: 20px; /* Gives space before the uploader */
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("📄 :blue[AI Resume] :violet[Analyzer]")
st.write("Analyze your resume using :orange[Artificial Intelligence] to get ahead in your career.")

st.markdown("""
    <div class="info-box">
        <strong>Tip:</strong> Ensure your resume is in a standard format (PDF or DOCX) for the best AI analysis! ✨
    </div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])
job_description = st.text_area("Paste a Job Description (Optional) to calculate Match % and enable rewriting:", height=100)

if resume:
    st.toast("Resume uploaded! Starting analysis...", icon="✅")
    
    resume_text = extract_text(resume)
    
    if not resume_text.strip():
        st.error("No text could be extracted from the uploaded resume.")
        st.stop()
    
    chat_model = get_llm()

    # --- CORE ANALYSIS ---
    with st.spinner("Analyzing Resume & Job Match... This takes a few seconds..."):
        result = analyze_resume(chat_model, resume_text)
        
        jd_result = None
        if job_description.strip():
            # jd_result = compare_resume(chat_model, resume_text, job_description)
            jd_result = {"match_percentage": 78} # Mock data for UI testing

    st.success("Analysis Complete!")
    st.divider()

    # --- TOP LEVEL SUMMARY ---
    col1, col2, col3, col4 = st.columns(4)
    
    ats_score = result.get("ats_score", 0)
    match_score = jd_result.get("match_percentage", 0) if jd_result else 0
    
    col1.metric("ATS Score", f"{ats_score}/100")
    col2.metric("Job Match", f"{match_score}%")
    col3.metric("Interview Prep", "Ready")
    col4.metric("Resume Level", "Advanced")
    
    st.divider()

    # --- TABBED INTERFACE ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",
        "🔍 Analysis",
        "📈 Charts",
        "📑 Report & Tools"
    ])

    # ------------------ TAB 1: DASHBOARD ------------------
    with tab1:
        st.header("Overall Performance")
        gauge_col1, gauge_col2 = st.columns(2)

        with gauge_col1:
            st.plotly_chart(ats_gauge(ats_score), use_container_width=True)

        with gauge_col2:
            if jd_result:
                st.plotly_chart(job_gauge(match_score), use_container_width=True)
            else:
                st.info("Paste a Job Description on the main page to see your Job Match gauge!")
                
        st.write(result.get("summary", "No summary provided."))

    # ------------------ TAB 2: ANALYSIS ------------------
    with tab2:
        st.header("Detailed Breakdown")
        
        with st.expander("💪 Strengths", expanded=True):
            for item in result.get("strengths", []):
                st.success(item)

        with st.expander("⚠️ Weaknesses"):
            for item in result.get("weaknesses", []):
                st.error(item)

        with st.expander("💡 Suggestions"):
            for tip in result.get("suggestions", []):
                st.info(tip)
        
        st.subheader("🎯 Recommended Roles")
        if isinstance(result.get("recommended_roles"), list):
            for role in result.get("recommended_roles"):
                st.write(f"- {role}")
        else:
            st.write(result.get("recommended_roles", "No roles recommended."))

    # ------------------ TAB 3: CHARTS ------------------
    with tab3:
        st.header("Skills Visualization")
        
        missing_skills = result.get("missing_skills", [])
        if missing_skills:
            st.subheader("Missing Skills (Target Areas)")
            st.plotly_chart(skill_chart(missing_skills), use_container_width=True)
            
            st.write("**Skills to add to your resume:**")
            for skill in missing_skills:
                st.warning(skill)
        else:
            st.success("Great job! No key skills are missing based on this analysis.")

    # ------------------ TAB 4: REPORT & TOOLS ------------------
    with tab4:
        st.header("Actionable AI Tools")
        
        # 1. Resume Rewriter
        if job_description.strip():
            with st.expander("📝 Tailor Resume to Job", expanded=True):
                if st.button("Rewrite Resume for this Role"):
                    with st.spinner("✍️ Rewriting Resume..."):
                        # rewrite = rewrite_resume(chat_model, resume_text, job_description)
                        st.session_state.rewrite = {
                            "professional_summary": "Optimized summary based on JD.",
                            "experience": ["Enhanced bullet point 1", "Enhanced bullet point 2"],
                            "projects": ["Aligned project 1"],
                            "skills": ["Skill A", "Skill B"],
                            "additional_suggestions": ["Format adjustment needed"]
                        }
                    
                # Display if it exists in session state
                if "rewrite" in st.session_state:
                    rewrite_data = st.session_state.rewrite
                    st.subheader("✍️ AI Resume Rewriter")
                    st.write("**Professional Summary:**")
                    st.write(rewrite_data.get("professional_summary", ""))
                    
                    st.write("**Experience:**")
                    for exp in rewrite_data.get("experience", []):
                        st.success(exp)
                        
                    st.write("**Skills:** " + ", ".join(rewrite_data.get("skills", [])))
        else:
            st.info("Paste a Job Description in the input above to unlock the Resume Rewriter.")

        st.divider()

        # 2. Career Advisor
        with st.expander("🧭 Explore Career Paths"):
            if st.button("Generate Career Advice"):
                with st.spinner("Analyzing career trajectories..."):
                    # career_result = get_career_advice(...)
                    st.session_state.career_result = {
                        "salary_range": "$90,000 - $130,000",
                        "top_skills_to_learn": ["TensorFlow", "Advanced SQL"],
                        "recommended_certifications": ["AWS Certified Machine Learning"],
                        "next_steps": ["Update LinkedIn", "Build a portfolio project"]
                    }
                
            if "career_result" in st.session_state:
                career_data = st.session_state.career_result
                st.subheader("💰 Estimated Salary Range")
                st.info(career_data.get("salary_range", "Not available"))

                st.subheader("🎓 Recommended Certifications")
                for cert in career_data.get("recommended_certifications", []):
                    st.info(cert)

                st.subheader("📌 Next Steps")
                for step in career_data.get("next_steps", []):
                    st.write(f"✅ {step}")

        st.divider()
        
        # 3. Interview Prep
        with st.expander("🗣️ Interview Preparation"):
            if st.button("Generate Interview Questions"):
                with st.spinner("Formulating questions..."):
                    # questions = get_interview_questions(...)
                    st.session_state.questions = {
                        "technical": ["Explain your approach to model optimization.", "How do you handle overfitting?"],
                        "hr": ["How do you handle tight deadlines?"],
                        "behavioral": ["Tell me about a time you failed."]
                    }
                    
            if "questions" in st.session_state:
                questions = st.session_state.questions
                tech_tab, hr_tab, beh_tab = st.tabs(["Technical", "HR", "Behavioral"])

                with tech_tab:
                    answers = []
                    for i, q in enumerate(questions.get("technical", [])):
                        st.write(f"**Q{i+1}.** {q}")
                        answers.append(st.text_area("Your Answer:", key=f"ans_{i}", height=100))
                    
                    if st.button("Evaluate Answers"):
                        for q, a in zip(questions.get("technical", []), answers):
                            if not a.strip():
                                st.warning(f"Please provide an answer for Q: *{q}*")
                                continue
                            
                            # result_eval = evaluate(chat_model, q, a)
                            result_eval = {
                                "score": 85,
                                "strengths": "Clear structure.",
                                "weaknesses": "Lacks specific metric examples.",
                                "improved_answer": "Include a specific percentage improvement you achieved."
                            }
                            
                            st.divider()
                            st.markdown(f"**Question:** {q}")
                            st.metric("Score", f"{result_eval.get('score', 0)}/100")
                            st.success(f"**Strengths:** {result_eval.get('strengths', '')}")
                            st.error(f"**Weaknesses:** {result_eval.get('weaknesses', '')}")
                            st.info(f"**Improved Answer:** {result_eval.get('improved_answer', '')}")
                            
                with hr_tab:
                    for i, q in enumerate(questions.get("hr", [])):
                        st.write(f"**Q{i+1}.** {q}")

                with beh_tab:
                    for i, q in enumerate(questions.get("behavioral", [])):
                        st.write(f"**Q{i+1}.** {q}")

    st.balloons()