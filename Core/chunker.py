def chunk_text(pages, max_len):
    chunks = []
    page_no = 0
    
    for page in pages:
        page_no += 1
        paragraphs = page.split('\n\n')

        for para in paragraphs:
            para = para.strip()
            if len(para) < 50:
                continue
            
            words = para.split()
            if len(words) <= max_len:
                chunks.append({'page': page_no, 'text': para})
            else:
                start = 0
                while start < len(words):
                    chunk_words = words[start: start+max_len]
                    chunk_text = ' '.join(chunk_words).strip()
                    chunks.append({'page': page_no, 'text': chunk_text})
                    start += max_len

    return chunks