from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
from docx import Document

from skills import find_skills
from scorer import calculate_resume_score
from job_matcher import calculate_job_match
from recommendations import generate_recommendations
from improvements import generate_improvements
from ai_analyzer import analyze_with_ai

import re
import json
import traceback


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

CORS(app)


# =========================================================
# PDF TEXT EXTRACTION
# =========================================================

def extract_pdf_text(file):
    reader = PdfReader(file)

    text_parts = []

    for page in reader.pages:
        try:
            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

        except Exception as error:
            print("PDF page extraction error:", error)

    return "\n".join(text_parts).strip()


# =========================================================
# DOCX TEXT EXTRACTION
# =========================================================

def extract_docx_text(file):
    document = Document(file)

    text_parts = []

    for paragraph in document.paragraphs:
        paragraph_text = paragraph.text.strip()

        if paragraph_text:
            text_parts.append(paragraph_text)

    return "\n".join(text_parts).strip()


# =========================================================
# CONTACT INFORMATION
# =========================================================

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


# =========================================================
# AI RESPONSE PARSER
# =========================================================

def parse_ai_response(ai_result):

    print("\n====================================")
    print("PARSING AI RESPONSE")
    print("====================================")

    if not ai_result:
        print("AI RESULT IS EMPTY")
        return {}

    # AI already returned a dictionary
    if isinstance(ai_result, dict):

        print("AI RESULT TYPE: DICTIONARY")

        return ai_result

    # AI returned JSON string
    if isinstance(ai_result, str):

        cleaned = ai_result.strip()

        # Remove markdown JSON wrapper
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]

        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:

            parsed = json.loads(cleaned)

            print("AI JSON PARSED SUCCESSFULLY")

            return parsed

        except json.JSONDecodeError as error:

            print("AI JSON PARSE ERROR:")
            print(error)

            return {
                "summary": cleaned,
                "strengths": [],
                "weaknesses": [],
                "missing_skills": [],
                "ats_analysis": "",
                "improvements": [],
                "recommended_projects": [],
                "interview_questions": [],
                "career_suggestions": []
            }

    print("UNKNOWN AI RESPONSE TYPE:")

    print(type(ai_result))

    return {}


# =========================================================
# DEFAULT AI RESPONSE
# =========================================================

def default_ai_analysis(improvements=None):
    return {
        "summary": "AI analysis is temporarily unavailable.",

        "strengths": [],

        "weaknesses": [],

        "missing_skills": [],

        "ats_analysis":
            "ATS analysis is temporarily unavailable.",

        "improvements":
            improvements or [],

        "recommended_projects": [],

        "interview_questions": [],

        "career_suggestions": []
    }


# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "AI Resume Analyzer Backend is Running!",
        "status": "online",
        "endpoints": [
            "/",
            "/health",
            "/analyze",
            "/job-match"
        ]
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "healthy",
        "service": "AI Resume Analyzer Backend"
    })


# =========================================================
# RESUME ANALYZER
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze_resume():

    print("\n====================================")
    print("NEW RESUME ANALYSIS REQUEST")
    print("====================================")

    if "resume" not in request.files:
        return jsonify({
            "success": False,
            "error": "No resume uploaded."
        }), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({
            "success": False,
            "error": "No file selected."
        }), 400

    filename = file.filename.lower()

    try:

        # -------------------------------------------------
        # EXTRACT TEXT
        # -------------------------------------------------

        print("Extracting resume text...")

        if filename.endswith(".pdf"):
            text = extract_pdf_text(file)

        elif filename.endswith(".docx"):
            text = extract_docx_text(file)

        else:
            return jsonify({
                "success": False,
                "error":
                    "Only PDF and DOCX files are supported."
            }), 400

        if not text.strip():
            return jsonify({
                "success": False,
                "error":
                    "Could not extract text from this resume."
            }), 400

        print(
            "Resume text extracted:",
            len(text),
            "characters"
        )


        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------

        print("Detecting skills...")

        skills = find_skills(text)

        print("Skills found:", skills)


        # -------------------------------------------------
        # CONTACT
        # -------------------------------------------------

        contact = extract_contact_info(text)


        # -------------------------------------------------
        # RESUME SCORE
        # -------------------------------------------------

        score = calculate_resume_score(
            text,
            skills
        )


        # -------------------------------------------------
        # BASIC IMPROVEMENTS
        # -------------------------------------------------

        improvements = generate_improvements(
            text,
            score.get("total", 0)
        )


        # -------------------------------------------------
        # AI ANALYSIS
        # -------------------------------------------------

        print("Calling Gemini for job analysis...")

        ai_analysis = {}

        try:

            ai_result = analyze_with_ai(
                resume_text=text
            )

            print("AI response received.")

            ai_analysis = parse_ai_response(
                ai_result
            ) 
            print("\n====================================")
            print("FINAL AI ANALYSIS:")
            print(ai_analysis)
            print("====================================\n")

            print("AI analysis parsed successfully.")

        except Exception as ai_error:

            print("AI ANALYSIS ERROR:")
            print(str(ai_error))

            traceback.print_exc()

            ai_analysis = default_ai_analysis(
                improvements
            )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "message":
                "Resume analyzed successfully.",

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
                improvements,

            "ai_analysis":
                ai_analysis
        })


    except Exception as error:

        print("RESUME ANALYSIS ERROR:")
        print(str(error))

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# JOB MATCH
# =========================================================

@app.route("/job-match", methods=["POST"])
def job_match():

    print("\n====================================")
    print("NEW JOB MATCH REQUEST")
    print("====================================")

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "No data provided."
        }), 400

    resume_skills = data.get(
        "resume_skills",
        []
    )

    resume_text = data.get(
        "resume_text",
        ""
    )

    job_description = data.get(
        "job_description",
        ""
    )

    resume_score = data.get(
        "resume_score",
        0
    )

    if not isinstance(job_description, str):
        return jsonify({
            "success": False,
            "error": "Invalid job description."
        }), 400

    if not job_description.strip():
        return jsonify({
            "success": False,
            "error": "Job description is required."
        }), 400

    try:

        # -------------------------------------------------
        # NORMAL JOB MATCH
        # -------------------------------------------------

        result = calculate_job_match(
            resume_skills,
            job_description
        )


        # -------------------------------------------------
        # BASIC RECOMMENDATIONS
        # -------------------------------------------------

        recommendations = generate_recommendations(
            result.get(
                "missing_skills",
                []
            ),
            resume_score
        )


        # -------------------------------------------------
        # AI JOB ANALYSIS
        # -------------------------------------------------

        ai_analysis = {}

        if isinstance(resume_text, str) and resume_text.strip():

            print(
                "Calling OpenAI for job analysis..."
            )

            try:

                ai_result = analyze_with_ai(
                    resume_text=resume_text,
                    job_description=job_description
                )

                ai_analysis = parse_ai_response(
                    ai_result
                )

                print(
                    "AI job analysis completed."
                )

            except Exception as ai_error:

                print(
                    "AI JOB ANALYSIS ERROR:"
                )

                print(
                    str(ai_error)
                )

                traceback.print_exc()

                ai_analysis = default_ai_analysis(
                    recommendations
                )


        # -------------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "match_percentage":
                result.get(
                    "match_percentage",
                    0
                ),

            "matched_skills":
                result.get(
                    "matched_skills",
                    []
                ),

            "missing_skills":
                result.get(
                    "missing_skills",
                    []
                ),

            "recommendations":
                recommendations,

            "ai_analysis":
                ai_analysis
        })


    except Exception as error:

        print(
            "JOB MATCH ERROR:"
        )

        print(
            str(error)
        )

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({

        "success": False,

        "error":
            "API endpoint not found."

    }), 404


# =========================================================
# 500 ERROR
# =========================================================

@app.errorhandler(500)
def server_error(error):

    return jsonify({

        "success": False,

        "error":
            "Internal server error."

    }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("\n====================================")
    print("🤖 AI RESUME ANALYZER BACKEND")
    print("====================================")
    print("Server: http://127.0.0.1:5000")
    print("Health: http://127.0.0.1:5000/health")
    print("====================================\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )