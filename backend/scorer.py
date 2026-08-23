def calculate_resume_score(text, skills):
    text_lower = text.lower()

    score = 0

    # 1. Contact Information - 10 marks
    contact_score = 0

    if "@" in text:
        contact_score += 5

    if any(char.isdigit() for char in text):
        contact_score += 5

    score += contact_score

    # 2. Education - 20 marks
    education_score = 0

    education_keywords = [
        "education",
        "qualification",
        "degree",
        "bachelor",
        "master",
        "diploma",
        "polytechnic",
        "iti",
        "10th",
        "12th"
    ]

    education_found = any(
        keyword in text_lower
        for keyword in education_keywords
    )

    if education_found:
        education_score = 20

    score += education_score

    # 3. Skills - 20 marks
    skill_score = min(len(skills) * 5, 20)

    score += skill_score

    # 4. Experience - 20 marks
    experience_score = 0

    experience_keywords = [
        "experience",
        "worked",
        "working",
        "job",
        "internship"
    ]

    if any(
        keyword in text_lower
        for keyword in experience_keywords
    ):
        experience_score = 20

    score += experience_score

    # 5. Projects - 20 marks
    project_score = 0

    project_keywords = [
        "project",
        "projects",
        "developed",
        "application",
        "website",
        "system"
    ]

    if any(
        keyword in text_lower
        for keyword in project_keywords
    ):
        project_score = 20

    score += project_score

    # 6. Objective / Summary - 10 marks
    objective_score = 0

    objective_keywords = [
        "objective",
        "summary",
        "career objective",
        "profile"
    ]

    if any(
        keyword in text_lower
        for keyword in objective_keywords
    ):
        objective_score = 10

    score += objective_score

    return {
        "total": score,
        "contact": contact_score,
        "education": education_score,
        "skills": skill_score,
        "experience": experience_score,
        "projects": project_score,
        "objective": objective_score
    }