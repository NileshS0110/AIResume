import streamlit as st
import os
import openai
from openai import OpenAI
import docx2txt
import PyPDF2

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("AI Resume Evaluator")

# Upload resume file
uploaded_file = st.file_uploader("Upload Resume (PDF or Word)", type=["pdf", "docx"])

# Job description input
job_description = st.text_area("Paste the Job Description here")

# Extract resume text
def extract_text(file):
    if file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in pdf_reader.pages])
    elif file.name.endswith('.docx'):
        return docx2txt.process(file)
    else:
        return ""

# Analyze resume using GPT
def analyze_resume(resume_text, job_description):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert recruiter evaluating resumes."},
            {"role": "user", "content": f"Here is a resume:\n{resume_text}\n\nHere is the job description:\n{job_description}\n\nEvaluate the candidate's fit and give a summary."}
        ]
    )
    return response.choices[0].message.content

if uploaded_file and job_description:
    with st.spinner("Analyzing..."):
        resume_text = extract_text(uploaded_file)
        result = analyze_resume(resume_text, job_description)
        st.subheader("AI Evaluation Result")
        st.write(result)
