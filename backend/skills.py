SKILLS = [
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


def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return found_skills