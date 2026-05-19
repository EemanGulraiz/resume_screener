# No spaCy needed — we use simple keyword matching instead

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
    """Compare skills in resume vs job description."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    return {
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "resume_skills": sorted(list(resume_skills)),
        "jd_skills": sorted(list(jd_skills)),
    }