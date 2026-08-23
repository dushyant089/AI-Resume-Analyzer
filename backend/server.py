from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
from docx import Document

from skills import find_skills
from scorer import calculate_resume_score
from job_matcher import calculate_job_match
from recommendations import generate_recommendations
from improvements import generate_improvements

import re


app = Flask(__name__)
CORS(app)


# =========================================
# PDF TEXT EXTRACTION
# =========================================

def extract_pdf_text(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================================
# DOCX TEXT EXTRACTION
# =========================================

def extract_docx_text(file):

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text


# =========================================
# CONTACT INFORMATION
# =========================================

def extract_contact_info(text):

    email_match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    phone_match = re.search(
        r'(?:\+91[\s-]?)?[6-9]\d{9}',
        text
    )

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    name = lines[0] if lines else ""

    return {
        "name": name,
        "email": email_match.group(0)
        if email_match else "",
        "phone": phone_match.group(0)
        if phone_match else ""
    }


# =========================================
# HOME ROUTE
# =========================================

@app.route("/")
def home():

    return "AI Resume Analyzer Backend is Running!"


# =========================================
# RESUME ANALYZER
# =========================================

@app.route("/analyze", methods=["POST"])
def analyze_resume():

    if "resume" not in request.files:

        return jsonify({
            "error": "No resume uploaded"
        }), 400


    file = request.files["resume"]


    if file.filename == "":

        return jsonify({
            "error": "No file selected"
        }), 400


    filename = file.filename.lower()


    try:

        # -----------------------------
        # Extract Resume Text
        # -----------------------------

        if filename.endswith(".pdf"):

            text = extract_pdf_text(file)


        elif filename.endswith(".docx"):

            text = extract_docx_text(file)


        else:

            return jsonify({
                "error":
                "Only PDF and DOCX files are supported"
            }), 400


        # -----------------------------
        # Find Skills
        # -----------------------------

        skills = find_skills(text)


        # -----------------------------
        # Contact Information
        # -----------------------------

        contact = extract_contact_info(text)


        # -----------------------------
        # Resume Score
        # -----------------------------

        score = calculate_resume_score(
            text,
            skills
        )


        # -----------------------------
        # Resume Improvements
        # -----------------------------

        improvements = generate_improvements(
            text,
            score["total"]
        )


        # -----------------------------
        # Response
        # -----------------------------

        return jsonify({

            "message":
                "Resume analyzed successfully",

            "filename":
                file.filename,

            "text":
                text,

            "skills":
                skills,

            "contact":
                contact,

            "score":
                score,

            "improvements":
                improvements

        })


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =========================================
# JOB MATCHER
# =========================================

@app.route("/job-match", methods=["POST"])
def job_match():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "No data provided"
        }), 400


    resume_skills = data.get(
        "resume_skills",
        []
    )


    job_description = data.get(
        "job_description",
        ""
    )


    resume_score = data.get(
        "resume_score",
        0
    )


    if not job_description:

        return jsonify({
            "error":
            "Job description is required"
        }), 400


    try:

        # -----------------------------
        # Calculate Job Match
        # -----------------------------

        result = calculate_job_match(
            resume_skills,
            job_description
        )


        # -----------------------------
        # Generate AI Recommendations
        # -----------------------------

        recommendations = generate_recommendations(
            result["missing_skills"],
            resume_score
        )


        # -----------------------------
        # Response
        # -----------------------------

        return jsonify({

            "match_percentage":
                result["match_percentage"],

            "matched_skills":
                result["matched_skills"],

            "missing_skills":
                result["missing_skills"],

            "recommendations":
                recommendations

        })


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =========================================
# START SERVER
# =========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )