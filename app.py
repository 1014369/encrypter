# app.py
import os
import streamlit as st
from datetime import datetime
from pdf_utils import extract_text_from_pdf_bytes, create_pdf_from_text
from keypad_cipher import encrypt_keypad, decrypt_keypad

# ---------------------------
# Directories
# ---------------------------
UPLOAD_DIR = "uploaded_pdfs"
GENERATED_DIR = "generated_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GENERATED_DIR, exist_ok=True)

# ---------------------------
# UI: Simple email "login"
# ---------------------------
st.set_page_config(page_title="Secure PDF Store", layout="centered")
st.title("🔒 Secure PDF Upload & Keypad Encryption")

st.markdown("Enter your email to continue. Admin can upload PDFs; allowed user can view decrypted content.")
user_email = st.text_input("Your email")

if not user_email:
    st.info("Enter your email to continue.")
    st.stop()

user_email = user_email.strip().lower()

# ---------------------------
# Secrets (replace with your own)
# ---------------------------
ADMIN_EMAIL = "admin@gmail.com"
ALLOWED_EMAIL = "admin@gmail.com"

# ---------------------------
# ADMIN SECTION
# ---------------------------
if user_email == ADMIN_EMAIL:
    st.subheader("Admin — Upload or Encrypt New PDF/Text")
    uploaded = st.file_uploader("Upload PDF", type=["pdf"])
    paste_text = st.text_area("Or paste text to encrypt")

    if st.button("Encrypt & Save"):
        if uploaded is None and not paste_text.strip():
            st.error("Provide a PDF or some text.")
            st.stop()

        if uploaded:
            raw = uploaded.read()
            extracted = extract_text_from_pdf_bytes(raw).strip()
            plaintext = extracted or ""
        else:
            plaintext = paste_text.strip()

        if not plaintext:
            st.error("No readable text found.")
            st.stop()

        # Encrypt
        encrypted_text = encrypt_keypad(plaintext)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        out_name = f"encrypted_{timestamp}.pdf"
        out_path = os.path.join(GENERATED_DIR, out_name)

        pdf_buf = create_pdf_from_text(f"Encrypted Payload ({timestamp})", encrypted_text)
        with open(out_path, "wb") as f:
            f.write(pdf_buf.getvalue())

        st.success(f"Encrypted PDF saved: {out_name}")
        st.download_button("⬇️ Download Encrypted PDF", data=pdf_buf, file_name=out_name, mime="application/pdf")

# ---------------------------
# FILE LIST SECTION
# ---------------------------
st.subheader("📄 Available Encrypted PDFs")
files = sorted(os.listdir(GENERATED_DIR), reverse=True)
if not files:
    st.info("No PDFs uploaded yet.")
else:
    for fname in files:
        path = os.path.join(GENERATED_DIR, fname)
        with open(path, "rb") as f:
            pdf_bytes = f.read()
        encrypted_text = extract_text_from_pdf_bytes(pdf_bytes).strip()

        with st.expander(fname):
            st.text_area("Encrypted preview:", encrypted_text[:200] + ("..." if len(encrypted_text) > 200 else ""))

            if user_email == ALLOWED_EMAIL:
                decrypted_text = decrypt_keypad(encrypted_text)
                pdf_buf = create_pdf_from_text(f"Decrypted: {fname}", decrypted_text)

                st.download_button("⬇️ Download Decrypted PDF", data=pdf_buf, file_name=fname.replace(".pdf", "_decrypted.pdf"), mime="application/pdf")
                st.download_button("⬇️ Download Decrypted Text", data=decrypted_text.encode(), file_name=fname.replace(".pdf", "_decrypted.txt"), mime="text/plain")

            else:
                st.download_button("⬇️ Download Encrypted PDF", data=pdf_bytes, file_name=fname, mime="application/pdf")
