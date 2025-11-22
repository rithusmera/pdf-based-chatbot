from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks, model= model):
    embeddings = []

    for chunk in chunks:
        text = chunk['text']
        embedding = model.encode(text)
        embeddings.append({'chunk_id': chunk['chunk_id'], 'page': chunk['page'], 'text': text, 'embedding': embedding})

    return embeddings