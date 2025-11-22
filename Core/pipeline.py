import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def process_pdf(file):
    pages = []
    file.seek(0)
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    
    return pages

def create_summary(pages):
    full_text = '\n\n'.join(pages)

    prompt = (
        "Summarize the following document in 250–300 words. Focus on the main ideas and overall purpose.\n\n"
        f"{full_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You summarize documents."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.2
    )

    return response['choices'][0]['message']['content'].strip()

def create_prompt(query, embeddings, global_summary):
    vectors = np.array([e['embedding'] for e in embeddings])
    query_vec = model.encode(query).reshape(1, -1)

    similarity = cosine_similarity(vectors, query_vec).ravel()
    valid_indices = [i for i, sim in enumerate(similarity) if sim>= 0.35]

    if valid_indices:
        top_idx = sorted(valid_indices, key=lambda i: similarity[i], reverse=True)[:3]
        top_embs = [embeddings[idx] for idx in top_idx]
        top_txts = [emb['text'] for emb in top_embs]

        context = '\n\n'.join(top_txts)

    else:
        context = global_summary

    final_prompt = f"Answer the following question based on the context:\n\n{context}\n\nQuestion: {query}"

    return final_prompt

def query_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant answering questions based on the provided context."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.2
    )
    return response['choices'][0]['message']['content']