def create_chunks(pages, max_len=300):
    chunks = []
    page_no = 0
    counter = 0

    for page in pages:
        page_no += 1
        paragraphs = page.split('\n\n')

        for para in paragraphs:
            para = para.strip()
            words = para.split()

            if len(words) < 10:
                continue
            
            if len(words) <= max_len:
                counter+=1
                chunks.append({'chunk_id': counter, 'page': page_no, 'text': para})
            else:
                start = 0
                while start < len(words):
                    chunk_words = words[start: start+max_len]
                    chunk_text = ' '.join(chunk_words).strip()
                    counter+=1
                    chunks.append({'chunk_id': counter, 'page': page_no, 'text': chunk_text})
                    start += max_len

    return chunks