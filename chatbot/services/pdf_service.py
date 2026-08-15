import fitz
import os
import re

from dotenv import load_dotenv
from google import genai
from .rag_service import search_pdf

load_dotenv()


def extract_text_from_pdf(pdf_file):

    document = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    text = ""

    for page_number, page in enumerate(
        document,
        start=1
    ):
        page_text = page.get_text()

        text += (
            f"\n\n--- Page {page_number} ---\n\n"
            + page_text
        )

    document.close()

    return text


def summarize_pdf(text):

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    prompt = f"""
You are an AI Study Assistant.

Summarize the following study material.

IMPORTANT:
- Use ONLY the provided study material.
- Do not add information from outside the material.
- If something is unclear or missing, say so.
- Make the explanation easy for a student.

Create the summary using this structure:

1. 📚 Overview
2. 🎯 Important Concepts
3. 📌 Important Definitions
4. 📝 Exam Important Points
5. 🧮 Important Formulas
6. ❓ Possible Exam Questions
7. 🧠 Simple Explanation

STUDY MATERIAL:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

def ask_question_from_pdf(
    pdf_id,
    user_id,
    question
):

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    relevant_chunks = search_pdf(
        pdf_id,
        user_id,
        question,
        top_k=4
    )

    if not relevant_chunks:

        return (
            "This information is not available "
            "in the uploaded PDF."
        )

    context = "\n\n".join(
        relevant_chunks
    )

    prompt = f"""
You are an AI Study Assistant.

Answer the student's question using ONLY
the provided study material.

Rules:

1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not supported by the
   provided material, say:
   "This information is not available
   in the uploaded PDF."
4. Explain in simple student-friendly language.
5. Give a clear and useful answer.

Relevant study material:

{context}

Student question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

def create_chunks(text, chunk_size=4000):

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        # कोशिश करें कि chunk sentence के बीच में न कटे
        if end < len(text):

            last_break = max(
                chunk.rfind("\n"),
                chunk.rfind(". "),
                chunk.rfind("। ")
            )

            if last_break > chunk_size * 0.6:
                end = start + last_break + 1
                chunk = text[start:end]

        chunks.append(chunk.strip())

        start = end

    return chunks

def find_relevant_chunks(text, question, max_chunks=3):

    chunks = create_chunks(text)

    question_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            question.lower()
        )
    )

    scored_chunks = []

    for chunk in chunks:

        chunk_words = set(
            re.findall(
                r"\b[a-zA-Z0-9]+\b",
                chunk.lower()
            )
        )

        score = len(
            question_words.intersection(
                chunk_words
            )
        )

        scored_chunks.append(
            (score, chunk)
        )

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    relevant = [
        chunk
        for score, chunk in scored_chunks[:max_chunks]
        if score > 0
    ]

    return relevant

