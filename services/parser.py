from PyPDF2 import PdfReader

def extract_pdf_text(filepath):
    reader = PdfReader(filepath)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text