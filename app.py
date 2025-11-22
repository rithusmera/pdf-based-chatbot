import streamlit as st
from Core import chunker
from Core import embedder
from Core import pipeline

st.title("PDF Chatbot")

if st.button("Clear PDF"):
    st.session_state.pop('chunks', None)
    st.session_state.pop('embeddings', None)
    st.rerun()

uploaded_file = st.file_uploader("Upload a PDF", type = ['pdf'])
if uploaded_file:
    if 'embeddings' not in st.session_state:
        with st.spinner("Processing PDF..."):
            pages = pipeline.process_pdf(uploaded_file)
            chunks = chunker.create_chunks(pages) 
            embeddings = embedder.create_embeddings(chunks)
            summary = pipeline.create_summary(pages)

            st.session_state['chunks'] = chunks
            st.session_state['embeddings'] = embeddings
            st.session_state['global_summary'] = summary
            st.success(f"PDF processed! {len(chunks)} chunks created.")

    embeddings = st.session_state['embeddings']


    query = st.text_input("Ask a question about the PDF:")
    if query.strip():
        prompt = pipeline.create_prompt(query, embeddings)
        with st.spinner("Generating answer..."):
            answer = pipeline.query_llm(prompt)

        st.markdown("**Answer:**")
        st.write(answer)
