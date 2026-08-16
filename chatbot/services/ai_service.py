import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================
# NORMAL AI CHAT
# =========================

def ask_ai(question):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are an AI Study Assistant.

Student Question:
{question}

Rules:

1. Explain in simple language.
2. Use Markdown formatting.
3. Use headings where useful.
4. Use bullet points for lists.
5. For mathematics, show step-by-step calculations.
6. Use LaTeX for mathematical formulas.
7. Use $$...$$ for important/display equations.
8. Use $...$ for inline equations.
9. Give the final answer clearly.
10. Give one practice question at the end.
11. Do not unnecessarily make the answer very long.
"""
    )

    return response.text


# =========================
# PDF QUESTION ANSWERING
# =========================

def ask_question_from_context(question, context):

    prompt = f"""
You are an AI Study Assistant.

You must answer the student's question ONLY using the
provided study material.

=========================
STUDY MATERIAL
=========================

{context}

=========================
STUDENT QUESTION
=========================

{question}

=========================
RULES
=========================

1. Answer using only the study material above.
2. Do not invent information.
3. If the answer is not present in the material, say:

   "This information is not available in the provided PDF."

4. Explain in simple student-friendly language.
5. Use Markdown formatting.
6. Use headings where useful.
7. Use bullet points for lists.
8. For mathematics, show step-by-step calculations.
9. Use LaTeX for formulas.
10. Keep the answer concise but useful.
11. Give an example if the PDF supports one.
12. Do not use outside knowledge.

Answer:
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# =========================
# PDF QUESTION
# =========================

def ask_question_from_pdf(pdf_id, user_id, question):

    # Import here to avoid circular import problems
    from .pdf_service import search_pdf

    # Get relevant chunks from ChromaDB
    documents = search_pdf(
        pdf_id=pdf_id,
        user_id=user_id,
        question=question,
        top_k=5
    )

    # No relevant material found
    if not documents:

        return (
            "This information is not available "
            "in the provided PDF."
        )

    # Combine chunks
    context = "\n\n".join(documents)

    # Ask Gemini using PDF context
    answer = ask_question_from_context(
        question=question,
        context=context
    )

    return answer