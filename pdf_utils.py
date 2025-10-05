# pdf_utils.py
import io
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file given as bytes."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []
    for p in reader.pages:
        pages.append(p.extract_text() or "")
    return "\n".join(pages)

def create_pdf_from_text(title: str, text: str) -> io.BytesIO:
    """Create a PDF from text, returns BytesIO."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin_left = 50
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_left, y, title)
    y -= 28

    c.setFont("Helvetica", 10)
    line_height = 12
    for line in text.split("\n"):
        for chunk in [line[i:i+90] for i in range(0, len(line), 90)]:
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
            c.drawString(margin_left, y, chunk)
            y -= line_height

    c.save()
    buffer.seek(0)
    return buffer
