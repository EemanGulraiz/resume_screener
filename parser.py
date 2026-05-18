import pdfplumber
import re

def extract_text(pdf_path):
    """Extract raw text from a PDF resume."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def clean_text(text):
    """Clean up the extracted text."""
    # Remove extra whitespace and blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove special characters but keep letters, numbers, punctuation
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def parse_resume(pdf_path):
    """Main function — extract and clean text from a resume PDF."""
    raw_text = extract_text(pdf_path)
    clean = clean_text(raw_text)
    return clean

# ── TEST IT ──
if __name__ == "__main__":
    # Put any sample resume PDF in your sample_resumes folder
    # and change the filename below to match
    result = parse_resume("sample_resumes/resume1.pdf")
    print(result[:500])  # Print first 500 characters