import pdfplumber

def load_pdf(path):
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            pages.append(text)
    
    return pages