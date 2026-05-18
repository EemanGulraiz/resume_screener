from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model once (this takes a few seconds on first run)
# It will auto-download (~80MB) the first time only
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_match_score(resume_text, jd_text):
    """
    Compare resume text vs job description text.
    Returns a score from 0 to 100.
    """
    # Convert both texts into vectors (embeddings)
    embeddings = model.encode([resume_text, jd_text])

    # Calculate how similar the two vectors are
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    # Convert to percentage and round to 2 decimal places
    return round(float(score) * 100, 2)


# ── TEST IT ──
if __name__ == "__main__":
    resume = """
    I am a software engineer with 2 years of experience.
    Skills: Python, Django, REST APIs, PostgreSQL, Git.
    Education: BS Computer Science.
    """

    job_description = """
    We are looking for a Python developer with experience in Django
    and REST APIs. Knowledge of SQL databases is a plus.
    Bachelor's degree in Computer Science required.
    """

    score = get_match_score(resume, job_description)
    print(f"Match Score: {score}%")