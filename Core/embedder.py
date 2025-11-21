from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(chunks, model):
    embeddings = []

    for chunk in chunks:
        embedding = model.encode(chunk)
        embeddings.append(embedding)

    return embeddings

