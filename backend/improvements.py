def generate_improvements(text, score):

    improvements = []

    text_lower = text.lower()

    # Contact information
    if "@" not in text:
        improvements.append(
            "Add a professional email address to your resume."
        )

    # Phone
    if not any(char.isdigit() for char in text):
        improvements.append(
            "Add your contact phone number."
        )

    # Objective / Summary
    if "objective" not in text_lower and "summary" not in text_lower:
        improvements.append(
            "Add a short professional summary or career objective."
        )

    # Education
    if "education" not in text_lower and "qualification" not in text_lower:
        improvements.append(
            "Clearly mention your education and qualifications."
        )

    # Experience
    if "experience" not in text_lower:
        improvements.append(
            "Add your work experience with job role and responsibilities."
        )

    # Projects
    if "project" not in text_lower:
        improvements.append(
            "Add 2-3 relevant projects to demonstrate your practical skills."
        )

    # Skills
    if "skill" not in text_lower:
        improvements.append(
            "Create a dedicated Skills section."
        )

    # Resume score
    if score < 50:
        improvements.append(
            "Your resume needs significant improvement. Add relevant skills, projects and experience."
        )

    elif score < 75:
        improvements.append(
            "Your resume is good, but adding projects and stronger skill descriptions can improve it."
        )

    else:
        improvements.append(
            "Your resume is strong. Keep your skills and projects updated."
        )

    return improvements