# backend/extractor.py

import pdfplumber
from docx import Document
import re

def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a PDF file using pdfplumber.
    Returns extracted text as a string.
    """
    try:
        full_text = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
        return "\n".join(full_text).strip()

    except Exception as e:
        print(f"[ERROR] Failed to extract PDF: {e}")
        return ""


def extract_text_from_docx(path: str) -> str:
    """
    Extracts text from a DOCX file using python-docx.
    """
    try:
        doc = Document(path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        print(f"[ERROR] Failed to extract DOCX: {e}")
        return ""


def extract_text(file_path: str) -> str:
    """
    Auto-detect file type and extract text accordingly.
    Supports PDF and DOCX formats.
    """
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)
    
    elif file_path.lower().endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            print(f"[ERROR] Failed to read TXT: {e}")
            return ""

    else:
        print(f"Unsupported file type: {file_path}")
        return ""