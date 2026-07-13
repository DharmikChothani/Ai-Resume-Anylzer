AI Resume Analyzer


The AI Resume Analyzer is an intelligent career tool designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). By leveraging the power of Google's Gemini AI, the application provides instant feedback, highlights missing skills, and compares your profile against specific job descriptions to maximize your hiring potential.

🚀 Features
ATS Scoring: Get an instant rating of your resume's compatibility with modern ATS software.

Skill Gap Analysis: Identify missing keywords and skills required for your target roles.

Job Description Matching: Paste a job description to get a tailored "Match Percentage" and personalized improvement suggestions.

Visual Dashboard: View your profile strengths, weaknesses, and skill gaps through interactive charts and gauges.

Privacy-First: Designed to work locally with your API keys to ensure your personal data remains under your control.

🛠 Tech Stack
Framework: Streamlit

AI Engine: Google Gemini API via LangChain

Visualization: Plotly

Processing: Pydantic (for structured JSON parsing)

📋 Prerequisites
Before running the project, ensure you have:

Python 3.10+ installed.

A Google AI Studio API Key. Get one here.

⚙️ Installation
Clone the repository:

Bash
git clone <your-repo-url>
cd "Ai Resume Anylzer"
Create a virtual environment and install dependencies:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure Secrets:
Create a folder named .streamlit and a file named secrets.toml inside it:

Plaintext
# .streamlit/secrets.toml
GOOGLE_API_KEY = "your_actual_api_key_here"
Run the application:

Bash
streamlit run app.py
📂 Project Structure
app.py: The main entry point and UI layout.

utils/ats.py: Core logic for interacting with the Gemini AI model.

utils/parser.py: Functions to extract text from PDF/DOCX files.

utils/jd_matcher.py: Logic to compare resumes against job descriptions.

utils/dashboard.py: Plotly visualization functions for the UI.

💡 How to Use
Upload: Click on the file uploader to upload your resume (PDF or DOCX).

Target: (Optional) Paste a job description in the text area to see how well you match the role.

Analyze: The AI will process your resume and display your ATS score, strengths, and areas for improvement in the Dashboard, Analysis, and Charts tabs.
