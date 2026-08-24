import os
import json
from openai import OpenAI


# =========================================================
# OPENAI CLIENT
# =========================================================

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY environment variable is missing."
    )

client = OpenAI(api_key=api_key)


# =========================================================
# AI RESUME ANALYZER
# =========================================================

def analyze_with_ai(resume_text, job_description=""):

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is empty.")

    job_text = (
        job_description.strip()
        if job_description
        else "No specific job description provided."
    )

    prompt = f"""
You are an expert AI Resume Analyzer and career advisor.

Analyze the resume carefully.

RULES:
1. Use ONLY information present in the resume.
2. Do not invent experience, education, skills or achievements.
3. Give specific and personalized feedback.
4. If a job description is provided, compare the resume with it.
5. Return ONLY valid JSON.
6. Every field must be present.
7. Arrays must contain useful items and must not be null.

RESUME:
==================================================
{resume_text}
==================================================

JOB DESCRIPTION:
==================================================
{job_text}
==================================================

Return exactly this JSON structure:

{{
  "summary": "Write a detailed personalized summary of the candidate.",

  "strengths": [
    "Specific strength based on the resume.",
    "Specific strength based on projects or experience.",
    "Specific technical strength."
  ],

  "weaknesses": [
    "Specific weakness or missing resume detail.",
    "Another realistic improvement area."
  ],

  "missing_skills": [
    "Skill that would improve the candidate's profile.",
    "Another relevant skill."
  ],

  "ats_analysis": "Explain how ATS-friendly the resume is and mention formatting, keywords and content issues.",

  "improvements": [
    "Specific resume improvement.",
    "Specific project or experience improvement.",
    "Specific ATS improvement."
  ],

  "recommended_projects": [
    "A project suitable for this candidate.",
    "Another project suitable for this candidate."
  ],

  "interview_questions": [
    "Technical interview question based on the resume.",
    "Project-related interview question.",
    "Java or backend interview question.",
    "Database-related interview question.",
    "Full-stack interview question."
  ],

  "career_suggestions": [
    "Suitable career role.",
    "Another suitable career role."
  ]
}}
"""

    try:

        print("\n====================================")
        print("CALLING OPENAI...")
        print("====================================")

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    "You are a professional resume analyzer. "
                    "Return accurate personalized JSON only."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            response_format={
                "type": "json_object"
            },

            temperature=0.4,

            max_tokens=2500
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "OpenAI returned an empty response."
            )

        print("\n====================================")
        print("OPENAI RESPONSE RECEIVED")
        print("====================================")

        # -------------------------------------------------
        # Validate JSON
        # -------------------------------------------------

        try:

            parsed = json.loads(content)

        except json.JSONDecodeError as json_error:

            print("JSON PARSE ERROR:", json_error)

            raise RuntimeError(
                "OpenAI returned invalid JSON."
            )

        # -------------------------------------------------
        # Make sure all fields exist
        # -------------------------------------------------

        default_response = {

            "summary": "",

            "strengths": [],

            "weaknesses": [],

            "missing_skills": [],

            "ats_analysis": "",

            "improvements": [],

            "recommended_projects": [],

            "interview_questions": [],

            "career_suggestions": []

        }

        for key, default_value in default_response.items():

            if key not in parsed:

                parsed[key] = default_value

        # -------------------------------------------------
        # Make sure arrays are actually arrays
        # -------------------------------------------------

        array_fields = [

            "strengths",
            "weaknesses",
            "missing_skills",
            "improvements",
            "recommended_projects",
            "interview_questions",
            "career_suggestions"

        ]

        for field in array_fields:

            if not isinstance(parsed[field], list):

                parsed[field] = []

        # -------------------------------------------------
        # Make sure text fields are strings
        # -------------------------------------------------

        if not isinstance(parsed["summary"], str):
            parsed["summary"] = str(parsed["summary"])

        if not isinstance(parsed["ats_analysis"], str):
            parsed["ats_analysis"] = str(
                parsed["ats_analysis"]
            )

        print("\nAI ANALYSIS READY")

        print(
            "Summary:",
            bool(parsed["summary"])
        )

        print(
            "Strengths:",
            len(parsed["strengths"])
        )

        print(
            "Weaknesses:",
            len(parsed["weaknesses"])
        )

        print(
            "Missing Skills:",
            len(parsed["missing_skills"])
        )

        print(
            "Improvements:",
            len(parsed["improvements"])
        )

        print(
            "Projects:",
            len(parsed["recommended_projects"])
        )

        print(
            "Interview Questions:",
            len(parsed["interview_questions"])
        )

        print(
            "Career Suggestions:",
            len(parsed["career_suggestions"])
        )

        print("====================================\n")

        # Return dictionary directly
        return parsed

    except Exception as error:

        print("\n====================================")
        print("OPENAI ERROR")
        print("====================================")

        print(
            repr(error)
        )

        print("====================================\n")

        raise