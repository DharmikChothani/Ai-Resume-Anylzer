import streamlit as st
from utils.parser import extract_text
from utils.ats import analyze_resume
from utils.llm import get_llm
from utils.jd_matcher import compare_resume
from utils.resume_rewriter import rewrite_resume
from utils.career_advisor import get_career_advice
from utils.interview import get_interview_questions

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# 1. Using Streamlit's built-in color tags
st.title("📄 :blue[AI Resume] :violet[Analyzer]")
st.write("Analyze your resume using :orange[Artificial Intelligence] to get ahead in your career.")

# 2. Using custom HTML/CSS for a colored background box
st.markdown("""
    <style>
    .info-box {
        background-color: #e6f3ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0066cc;
        color: #333333;
    }
    </style>
    <div class="info-box">
        <strong>Tip:</strong> Ensure your resume is in a standard format (PDF or DOCX) for the best AI analysis! ✨
    </div>
    <br>
""", unsafe_allow_html=True)

resume = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if resume:
    st.toast("Resume uploaded! Starting analysis...", icon="✅")
    
    # Extract the text
    resume_text = extract_text(resume)
    
    if not resume_text.strip():
        st.error("No text could be extracted from the uploaded resume.")
        st.stop()
    
    # Initialize the AI model
    chat_model = get_llm()

    with st.spinner("Analyzing Resume... This takes a few seconds..."):
        result = analyze_resume(chat_model, resume_text)

    st.success("Analysis Complete!")

    # --- ATS ANALYSIS DISPLAY ---
    try:
        col1, col2 = st.columns([1, 3])
        with col1:
            score = result.get("ats_score", 0)
            st.metric("ATS Score", f"{score}/100")
            st.progress(score / 100)
        
        with col2:
            st.write(result.get("summary", "No summary provided."))

        st.divider()
        
        with st.expander("💪 Strengths", expanded=True):
            for item in result.get("strengths", []):
                st.success(item)

        with st.expander("⚠️ Weaknesses"):
            for item in result.get("weaknesses", []):
                st.error(item)

        with st.expander("🔍 Missing Skills"):
            for skill in result.get("missing_skills", []):
                st.warning(skill)

        with st.expander("💡 Suggestions"):
            for tip in result.get("suggestions", []):
                st.info(tip)
        
        st.subheader("🎯 Recommended Roles")
        if isinstance(result.get("recommended_roles"), list):
            for role in result.get("recommended_roles"):
                st.write(f"- {role}")
        else:
            st.write(result.get("recommended_roles", "No roles recommended."))

        st.divider()

        # --- REWRITE CODE ---
        st.subheader("📝 Tailor Your Resume to a Job")
        job_description = st.text_area("Paste a job description here to rewrite your resume for the role:", height=150)
        
        rewrite = None
        if job_description.strip():
            with st.spinner("✍️ Rewriting Resume..."):
                rewrite = rewrite_resume(
                    chat_model,
                    resume_text,
                    job_description
                )
            
            if rewrite:
                st.divider()
                st.header("✍️ AI Resume Rewriter")

                with st.expander("Professional Summary", expanded=True):
                    st.write(rewrite.get("professional_summary", "No summary provided."))

                with st.expander("Experience"):
                    for exp in rewrite.get("experience", []):
                        st.success(exp)

                with st.expander("Projects"):
                    for project in rewrite.get("projects", []):
                        st.info(project)

                with st.expander("Skills"):
                    st.write(", ".join(rewrite.get("skills", [])))

                with st.expander("Additional Suggestions"):
                    for tip in rewrite.get("additional_suggestions", []):
                        st.warning(tip)

        st.divider()

        # --- CAREER ADVISOR CODE ---
        st.subheader("🧭 Explore Career Paths")
        
        if st.button("Generate Career Advice"):
            career_result = None
            with st.spinner("Analyzing career trajectories..."):
                # career_result = get_career_advice(chat_model, resume_text)
                
                # Mock data for testing
                career_result = {
                    "career_match_score": 85,
                    "recommended_roles": ["Data Scientist", "Machine Learning Engineer"],
                    "salary_range": "$90,000 - $130,000",
                    "top_skills_to_learn": ["TensorFlow", "Advanced SQL"],
                    "recommended_certifications": ["AWS Certified Machine Learning"],
                    "career_summary": "Your background shows strong analytical skills perfect for transitioning into AI.",
                    "next_steps": ["Update LinkedIn", "Build a portfolio project"]
                }

            if career_result:
                st.divider()
                st.header("🚀 AI Career Advisor")

                score = career_result.get("career_match_score", 0)

                st.metric("Career Match Score", f"{score}/100")
                st.progress(score / 100)

                st.subheader("🎯 Recommended Roles")
                for role in career_result.get("recommended_roles", []):
                    st.success(role)

                st.subheader("💰 Estimated Salary Range")
                st.info(career_result.get("salary_range", "Not available"))

                st.subheader("🛠️ Top Skills to Learn")
                for skill in career_result.get("top_skills_to_learn", []):
                    st.warning(skill)

                st.subheader("🎓 Recommended Certifications")
                for cert in career_result.get("recommended_certifications", []):
                    st.info(cert)

                st.subheader("📝 Career Summary")
                st.write(career_result.get("career_summary", ""))

                st.subheader("📌 Next Steps")
                for step in career_result.get("next_steps", []):
                    st.write(f"✅ {step}")
                    
        st.divider()
        
        # --- NEW INTERVIEW PREP CODE INTEGRATED HERE ---
        st.subheader("🗣️ Interview Preparation")
        
        if st.button("Generate Interview Questions"):
            questions = None
            with st.spinner("Formulating personalized interview questions..."):
                # questions = get_interview_questions(chat_model, resume_text, job_description)
                
                # Mock data for testing
                questions = {
                    "technical": [
                        "Can you explain your approach to handling overfitting in machine learning models like XGBoost?",
                        "How would you optimize a model designed to predict binary outcomes?",
                        "Describe your experience deploying Python-based web applications."
                    ],
                    "hr": [
                        "How do you balance your academic coursework with independent technical projects?",
                        "What motivates you to apply your technical skills to outside interests or sports analytics?"
                    ],
                    "behavioral": [
                        "Tell me about a time you had to troubleshoot a complex hardware or software integration issue.",
                        "Describe a time you collaborated with peers on a shared project or responsibility."
                    ]
                }
                
            if questions:
                st.divider()
                st.header("🎤 AI Interview Questions")

                tech_tab, hr_tab, beh_tab = st.tabs(
                    [
                        "Technical",
                        "HR",
                        "Behavioral"
                    ]
                )

                with tech_tab:
                    for i, q in enumerate(questions.get("technical", [])):
                        st.write(f"**Q{i+1}.** {q}")

                with hr_tab:
                    for i, q in enumerate(questions.get("hr", [])):
                        st.write(f"**Q{i+1}.** {q}")

                with beh_tab:
                    for i, q in enumerate(questions.get("behavioral", [])):
                        st.write(f"**Q{i+1}.** {q}")
        # --- END OF INTERVIEW PREP CODE ---

    except AttributeError:
        st.error("The AI returned an unexpected format. Here is the raw output:")
        st.write(result)
        
    st.balloons()