import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
from fpdf import FPDF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Settings
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="📄",
    layout="wide"
)

# Title
st.title("📄 AI Resume Analyzer Pro")
st.write("Analyze Resume | ATS Score | Job Match")

# Upload Resume
resume_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# Job Description Input
jd = st.text_area(
    "Paste Job Description Here"
)

# Main Logic
if resume_file:

    # Read PDF Resume
    with pdfplumber.open(resume_file) as pdf:

        resume_text = ""

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                resume_text += text

    st.success(
        "✅ Resume Uploaded Successfully"
    )

    # Skills List
    skills = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "machine learning",
        "excel",
        "power bi",
        "django",
        "c++"
    ]

    # Find Skills
    found_skills = []

    for skill in skills:
        if skill in resume_text.lower():
            found_skills.append(skill)

    # Show Skills
    st.subheader("🛠 Skills Found")
    st.write(found_skills)

    # ATS Score
    ats_score = len(found_skills) * 10

    if ats_score > 100:
        ats_score = 100

    st.subheader("📊 ATS Score")
    st.progress(ats_score / 100)
    st.write(f"{ats_score}%")

    # Pie Chart
    fig, ax = plt.subplots()

    labels = [
        "Skills Found",
        "Missing"
    ]

    sizes = [
        len(found_skills),
        10 - len(found_skills)
    ]

    ax.pie(
        sizes,
        labels=labels,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    # Resume Suggestions
    st.subheader("📌 Resume Suggestions")

    if ats_score < 50:
        st.error(
            "Your resume is weak. Add more technical skills and projects."
        )

    elif ats_score < 80:
        st.warning(
            "Resume is good but can be improved."
        )

    else:
        st.success(
            "Excellent Resume for ATS!"
        )

    # Resume Improvement Advisor
    st.subheader(
        "🚀 Resume Improvement Advisor"
    )

    improvements = []

    # Check Projects
    if "project" not in resume_text.lower():
        improvements.append(
            "Add at least 2 strong projects."
        )

    # Check Skills
    if len(found_skills) < 4:
        improvements.append(
            "Add more technical skills like Python, SQL, Excel."
        )

    # Check Internship
    if (
        "internship"
        not in resume_text.lower()
        and
        "experience"
        not in resume_text.lower()
    ):
        improvements.append(
            "Add internship or practical experience."
        )

    # Check Certification
    if (
        "certificate"
        not in resume_text.lower()
        and
        "certification"
        not in resume_text.lower()
    ):
        improvements.append(
            "Add certifications from Coursera, Udemy, NPTEL etc."
        )

    # Check GitHub
    if "github" not in resume_text.lower():
        improvements.append(
            "Add GitHub profile link."
        )

    # Show Improvement Tips
    if improvements:

        st.warning(
            "Ways to Improve Resume:"
        )

        for tip in improvements:
            st.write(f"✅ {tip}")

    else:
        st.success(
            "Excellent Resume! No major improvements needed 😎"
        )

    # Resume vs Job Description
    if jd:

        text = [
            resume_text,
            jd
        ]

        cv = CountVectorizer()

        matrix = cv.fit_transform(
            text
        )

        similarity = cosine_similarity(
            matrix
        )[0][1]

        st.subheader(
            "🎯 Resume Match Score"
        )

        st.write(
            f"{round(similarity * 100, 2)}%"
        )

        # Missing Skills
        missing_skills = []

        for skill in skills:

            if (
                skill in jd.lower()
                and
                skill not in resume_text.lower()
            ):
                missing_skills.append(
                    skill
                )

        st.subheader(
            "❌ Missing Skills"
        )

        st.write(
            missing_skills
        )

    # Interview Questions
    st.subheader(
        "💼 Interview Questions"
    )

    if "python" in found_skills:
        st.write(
            "• What is OOP in Python?"
        )
        st.write(
            "• Difference between List and Tuple?"
        )

    if "sql" in found_skills:
        st.write(
            "• Difference between WHERE and HAVING?"
        )
        st.write(
            "• What is JOIN?"
        )

    if "java" in found_skills:
        st.write(
            "• What is JVM?"
        )
        st.write(
            "• Explain Inheritance."
        )

    # Career Roadmap
    st.subheader(
        "🚀 Career Roadmap"
    )

    role = st.selectbox(
        "Choose Career Role",
        [
            "Python Developer",
            "Data Analyst"
        ]
    )

    if role == "Python Developer":
        st.info(
            "Roadmap: Python → OOP → SQL → Django → Projects"
        )

    elif role == "Data Analyst":
        st.info(
            "Roadmap: Excel → SQL → Python → Power BI"
        )

    # Roast Mode
    st.subheader(
        "🔥 Resume Roast Mode"
    )

    if st.button(
        "Roast My Resume"
    ):

        if (
            "hardworking"
            in resume_text.lower()
        ):
            st.warning(
                "Everyone writes 'Hardworking' 😄 Add proof using projects."
            )

        elif (
            "team player"
            in resume_text.lower()
        ):
            st.warning(
                "Team Player is common 😄 Add achievements instead."
            )

        else:
            st.success(
                "Good Resume! No boring words found 😎"
            )

    # PDF Report
    st.subheader(
        "📄 Download Report"
    )

    if st.button(
        "Generate PDF Report"
    ):

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font(
            "Arial",
            size=12
        )

        pdf.cell(
            200,
            10,
            txt="Resume Analysis Report",
            ln=True
        )

        pdf.cell(
            200,
            10,
            txt=f"ATS Score: {ats_score}%",
            ln=True
        )

        pdf.cell(
            200,
            10,
            txt=f"Skills: {', '.join(found_skills)}",
            ln=True
        )

        pdf.output(
            "resume_report.pdf"
        )

        st.success(
            "✅ PDF Generated Successfully!"
        )