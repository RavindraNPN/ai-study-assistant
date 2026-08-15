import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_ai(question):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
You are an AI Study Assistant.

Your job is to teach students clearly.

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

For example:

### Concept

Explain the concept.

### Formula

$$F = m \\times a$$

### Example

Step 1: ...

### Final Answer

...

### Practice Question

...
"""    )

    return response.text