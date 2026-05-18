import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Our skills vocabulary — you can keep adding to this list!
SKILLS_LIST = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "sql",
    "html", "css", "php", "swift", "kotlin", "go", "rust", "scala",

    # Frameworks & Libraries
    "django", "flask", "fastapi", "react", "angular", "vue", "node.js",
    "spring", "tensorflow", "pytorch", "keras", "scikit-learn", "pandas",
    "numpy", "opencv", "bootstrap",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "redis", "firebase",
    "oracle", "sql server",

    # Tools & Platforms
    "git", "github", "docker", "kubernetes", "aws", "azure", "gcp",
    "linux", "rest api", "graphql", "postman", "jira", "figma",

    # AI / Data
    "machine learning", "deep learning", "natural language processing",
    "nlp", "computer vision", "data analysis", "data science",
    "neural networks", "llm", "transformers",

    # Soft Skills
    "communication", "teamwork", "leadership", "problem solving",
    "project management", "agile", "scrum",
]

def extract_skills(text):
    """Find all skills mentioned in a piece of text."""
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILLS_LIST:
        if skill in text_lower:
            found_skills.add(skill)

    return found_skills

def get_skill_gap(resume_text, jd_text):
    """
    Compare skills in resume vs job description.
    Returns matched skills and missing skills.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills & jd_skills      # skills in both
    missing = jd_skills - resume_skills      # skills in JD but not resume

    return {
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "resume_skills": sorted(list(resume_skills)),
        "jd_skills": sorted(list(jd_skills)),
    }


# ── TEST IT ──
if __name__ == "__main__":
    resume = """
    Experienced Python developer with knowledge of Django, REST API,
    PostgreSQL, and Git. Worked with machine learning and scikit-learn.
    Good communication and teamwork skills.
    """

    jd = """
    Looking for a Python developer with Django and Flask experience.
    Must know Docker, AWS, and PostgreSQL. Experience with machine learning
    and deep learning is preferred. Strong communication skills required.
    """

    result = get_skill_gap(resume, jd)

    print("✅ Matched Skills:")
    for skill in result["matched"]:
        print(f"   - {skill}")

    print("\n❌ Missing Skills:")
    for skill in result["missing"]:
        print(f"   - {skill}")