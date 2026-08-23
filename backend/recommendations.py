def generate_recommendations(missing_skills, resume_score):

    recommendations = []

    # Missing skills
    if missing_skills:

        for skill in missing_skills[:5]:

            recommendations.append(
                f"Learn and practice {skill} to improve your job match."
            )

    # Resume score
    if resume_score < 60:

        recommendations.append(
            "Your resume score is low. Add more relevant skills, projects and experience."
        )

    elif resume_score < 80:

        recommendations.append(
            "Your resume is good, but adding relevant projects can make it stronger."
        )

    else:

        recommendations.append(
            "Your resume is strong. Keep your skills and projects updated."
        )

    # Projects
    recommendations.append(
        "Add 2-3 relevant projects related to the target job."
    )

    # General improvement
    recommendations.append(
        "Use clear and professional descriptions for your experience."
    )

    return recommendations