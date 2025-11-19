# backend/parser.py

import re
import spacy

# Load the spaCy model we installed
# If you get an error here, make sure we ran:
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# Regex patterns
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(\+?\d{1,3}[-.\s]?)?(\d{10}|\d{5}[-.\s]\d{5})"


def clean_text(text: str) -> str:
    """Basic cleanup: remove extra spaces and line breaks."""
    text = text.replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_email(text: str):
    match = re.search(EMAIL_REGEX, text)
    return match.group(0) if match else None


def extract_phone(text: str):
    match = re.search(PHONE_REGEX, text)
    return match.group(0) if match else None


def extract_name(text: str):
    """
    Uses spaCy NER to extract the first PERSON entity
    Assumes candidate's name appears near the top.
    """
    doc = nlp(text[:300])  # Only check top section for speed
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Simple check to avoid matching "LinkedIn" or other false positives
            if len(ent.text.split()) < 4:
                return ent.text.strip()
    return None


def parse_basic_info(text: str) -> dict:
    """
    Returns a dictionary of extracted basic info:
    - name
    - email
    - phone
    """
    cleaned = clean_text(text)

    return {
        "name": extract_name(cleaned),
        "email": extract_email(cleaned),
        "phone": extract_phone(cleaned),
    }