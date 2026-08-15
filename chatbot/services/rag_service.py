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

chroma_client = chromadb.PersistentClient(
    path="media/chroma"
)


collection = chroma_client.get_or_create_collection(
    name="study_material"
)


# =========================================================
# 3. CREATE TEXT CHUNKS
# =========================================================

def create_chunks(text, chunk_size=4000):

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        # Try not to cut the text in the middle
        if end < len(text):

            last_break = max(
                chunk.rfind("\n"),
                chunk.rfind(". "),
                chunk.rfind("। ")
            )

            if last_break > chunk_size * 0.6:

                end = start + last_break + 1

                chunk = text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        start = end

    return chunks


# =========================================================
# 4. INDEX PDF
# =========================================================

def index_pdf(pdf_id, user_id, text):

    chunks = create_chunks(text)

    if not chunks:

        return 0

    ids = []

    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(
            f"pdf_{pdf_id}_chunk_{index}"
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

    # Store in ChromaDB
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
# 5. SEARCH RELEVANT PDF CONTENT
# =========================================================

def search_pdf(
    pdf_id,
    user_id,
    question,
    top_k=4
):

    # Generate embedding for question
    model = get_embedding_model()

    question_embedding = model.encode(
        [question],
        show_progress_bar=False
    ).tolist()

    # Search ChromaDB
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
        [[]]
    )[0]

    return documents