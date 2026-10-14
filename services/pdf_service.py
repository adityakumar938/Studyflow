from pypdf import PdfReader


def extract_text(pdf_path):
    """Return all text from a PDF. Raises ValueError if no text is found."""
    reader = PdfReader(pdf_path)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    if not text.strip():
        raise ValueError("No text found. The PDF may be a scanned image.")
    return text