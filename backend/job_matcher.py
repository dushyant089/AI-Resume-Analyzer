def calculate_job_match(resume_skills, job_description):

    job_text = job_description.lower()

    matched_skills = []
    missing_skills = []

    for skill in resume_skills:

        if skill.lower() in job_text:
            matched_skills.append(skill)

    # Common skills list
    common_skills = [
        "python",
        "java",
        "javascript",
        "html",
        "css",
        "react",
        "node.js",
        "express",
        "mongodb",
        "mysql",
        "sql",
        "git",
        "github",
        "c++",
        "c",
        "php",
        "machine learning",
        "artificial intelligence",
        "data science",
        "excel",
        "word",
        "powerpoint",
        "autocad",
        "solidworks",
        "computer",
        "communication",
        "teamwork"
    ]

    for skill in common_skills:

        if skill in job_text and skill not in resume_skills:
            missing_skills.append(skill)

    total_required = len(matched_skills) + len(missing_skills)

    if total_required > 0:
        match_percentage = round(
            (len(matched_skills) / total_required) * 100
        )
    else:
        match_percentage = 0

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }