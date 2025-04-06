import streamlit as st
import openai
import docx2txt
import PyPDF2
import io
import os

# Set your OpenAI API key here or load from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
        text = docx2txt.process(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")
    return text

def evaluate_with_openai(resume_text: str, jd_text: str):
    prompt = f"""
    Job Description:
    {jd_text}

    Candidate Resume:
    {resume_text}

    Based on the job description and the candidate's resume, provide:
    1. A Fit Score out of 100.
    2. A 3-4 sentence summary highlighting key relevant experience and potential gaps.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

st.set_page_config(page_title="RecruitAI Copilot", layout="wide")
st.title("RecruitAI Copilot – Resume Matcher")

st.markdown("""
Upload a candidate resume and input a job description to evaluate the fit using AI.
""")

with st.form("resume_form"):
    jd_input = st.text_area("Job Description", height=200)
    uploaded_resume = st.file_uploader("Upload Candidate Resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    submitted = st.form_submit_button("Evaluate")

if submitted:
    if jd_input and uploaded_resume:
        resume_text = extract_text_from_file(uploaded_resume)
        with st.spinner("Analyzing with OpenAI..."):
            ai_output = evaluate_with_openai(resume_text, jd_input)

        st.subheader("AI Evaluation Result")
        st.success(ai_output)
    else:
        st.error("Please upload a resume file and enter a job description.")
