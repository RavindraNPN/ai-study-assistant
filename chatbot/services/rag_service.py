import os

import chromadb
from sentence_transformers import SentenceTransformer


# =========================================================
# 1. EMBEDDING MODEL
# =========================================================

_embedding_model = None


def get_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        print("Loading embedding model...")

        _embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded successfully.")

    return _embedding_model


# =========================================================
# 2. CHROMADB
# =========================================================

CHROMA_PATH = os.path.join(
    "media",
    "chroma"
)


chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = chroma_client.get_or_create_collection(
    name="study_material"
)


# =========================================================
# 3. CREATE TEXT CHUNKS
# =========================================================

def create_chunks(
    text,
    chunk_size=4000
):

    if not text:
        return []

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        # Try to avoid cutting sentences/paragraphs
        if end < len(text):

            last_break = max(
                chunk.rfind("\n"),
                chunk.rfind(". "),
                chunk.rfind("। "),
                chunk.rfind("? "),
                chunk.rfind("! ")
            )

            if last_break > chunk_size * 0.60:

                end = start + last_break + 1

                chunk = text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        start = end

    return chunks


# =========================================================
# 4. DELETE OLD PDF INDEX
# =========================================================

def delete_pdf_index(
    pdf_id,
    user_id
):

    try:

        collection.delete(
            where={
                "$and": [
                    {
                        "pdf_id": str(pdf_id)
                    },
                    {
                        "user_id": str(user_id)
                    }
                ]
            }
        )

        print(
            f"Old index deleted for PDF {pdf_id}"
        )

    except Exception as e:

        print(
            f"Could not delete old index: {e}"
        )


# =========================================================
# 5. INDEX PDF
# =========================================================

def index_pdf(
    pdf_id,
    user_id,
    text
):

    # Create chunks
    chunks = create_chunks(text)

    if not chunks:

        print(
            f"PDF {pdf_id} has no text to index."
        )

        return 0

    # Remove previous index
    delete_pdf_index(
        pdf_id,
        user_id
    )

    ids = []

    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"pdf_{pdf_id}_user_{user_id}_chunk_{index}"
        )

        metadatas.append(
            {
                "pdf_id": str(pdf_id),
                "user_id": str(user_id),
                "chunk_index": index,
            }
        )

    # Generate embeddings locally
    model = get_embedding_model()

    embeddings = model.encode(
        chunks,
        show_progress_bar=False
    ).tolist()

    # Store everything in ChromaDB
    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(
        f"PDF {pdf_id} indexed successfully "
        f"with {len(chunks)} chunks."
    )

    return len(chunks)


# =========================================================
# 6. SEARCH PDF
# =========================================================

def search_pdf(
    pdf_id,
    user_id,
    question,
    top_k=5
):

    if not question:

        return []

    question = question.strip()

    if not question:

        return []

    # Generate question embedding
    model = get_embedding_model()

    question_embedding = model.encode(
        [question],
        show_progress_bar=False
    ).tolist()

    # Search only inside this user's PDF
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=top_k,
        where={
            "$and": [
                {
                    "pdf_id": str(pdf_id)
                },
                {
                    "user_id": str(user_id)
                }
            ]
        }
    )

    documents = results.get(
        "documents",
        []
    )

    if not documents:

        return []

    # Chroma returns list of lists
    documents = documents[0]

    return [
        document
        for document in documents
        if document
    ]


# =========================================================
# 7. GET RELEVANT CONTEXT
# =========================================================

def get_pdf_context(
    pdf_id,
    user_id,
    question,
    top_k=5
):

    documents = search_pdf(
        pdf_id=pdf_id,
        user_id=user_id,
        question=question,
        top_k=top_k
    )

    if not documents:

        return ""

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        context_parts.append(
            f"""
--- Relevant Section {index} ---

{document}
"""
        )

    return "\n".join(
        context_parts
    )