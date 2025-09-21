def process_pdf_file(path: str):
    """
    Your heavy ingestion code here.
    This is where memory usage can spike.
    """

    from PyPDF2 import PdfReader
    reader = PdfReader(path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    
    # simulate long processing
    print(f"[Worker] Processed {len(text)} chars from {path}")
