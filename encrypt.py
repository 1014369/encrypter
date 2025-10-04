import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def create_pdf(title, text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)  # no unpacking needed

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 742, title)  # letter height is 792, leave margin
    c.setFont("Helvetica", 12)

    y = 700
    for line in text.split('\n'):
        c.drawString(50, y, line)
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer

# --- Keypad mapping logic ---
keys = {
    2: "ABC",
    3: "DEF",
    4: "GHI",
    5: "JKL",
    6: "MNO",
    7: "PQRS",
    8: "TUV",
    9: "WXYZ"
}

# Build encryption map
encrypt_map = {}
for digit, letters in keys.items():
    for idx, letter_char in enumerate(letters, start=1):
        encrypt_map[letter_char] = f"{digit}{idx}"
encrypt_map[' '] = '00'

# Build decryption map
decrypt_map = {v: k for k, v in encrypt_map.items()}

# --- Encryption / Decryption ---
def encrypt(text):
    return ' '.join(encrypt_map.get(char.upper(), char) for char in text)

def decrypt(code):
    parts = code.split()
    return ''.join(decrypt_map.get(part, part) for part in parts)

# --- PDF generation ---
def create_pdf(title, text):
    buffer = io.BytesIO()
    page_size = letter  # Use letter as a tuple
    width, height = tuple(page_size)  # Safe unpacking

    c = canvas.Canvas(buffer, pagesize=page_size)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, title)
    c.setFont("Helvetica", 12)

    y = height - 100
    for line in text.split('\n'):
        c.drawString(50, y, line)
        y -= 20

    c.save()
    buffer.seek(0)
    return buffer

# --- Streamlit UI ---
st.title("📱 Phone Keypad Encrypt/Decrypt App")

text_input = st.text_area("Enter text:", "")

if text_input:
    encrypted_text = encrypt(text_input)
    decrypted_text = decrypt(encrypted_text)

    st.subheader("🔐 Encrypted Text")
    st.code(encrypted_text)

    st.subheader("🗝 Decrypted Text")
    st.code(decrypted_text)

    # Generate PDFs
    pdf_encrypted = create_pdf("Encrypted Text", encrypted_text)
    pdf_decrypted = create_pdf("Decrypted Text", decrypted_text)

    # Download buttons
    st.download_button(
        label="📥 Download Encrypted PDF",
        data=pdf_encrypted,
        file_name="encrypted_text.pdf",
        mime="application/pdf"
    )

    st.download_button(
        label="📥 Download Decrypted PDF",
        data=pdf_decrypted,
        file_name="decrypted_text.pdf",
        mime="application/pdf"
    )
