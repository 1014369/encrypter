# crypto_utils.py
# Simple AES-GCM encrypt/decrypt helpers (server-side symmetric key)
# Key must be 32 bytes (256-bit). We store it base64 in secrets.

import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key_bytes():
    return os.urandom(32)

def key_bytes_to_b64(key_bytes: bytes) -> str:
    return base64.b64encode(key_bytes).decode("utf-8")

def key_b64_to_bytes(b64: str) -> bytes:
    return base64.b64decode(b64)

def aes_encrypt(plaintext_bytes: bytes, key_bytes: bytes) -> str:
    """
    Returns package string: base64(nonce):base64(ciphertext)
    Safe to embed as text into PDFs.
    """
    aesgcm = AESGCM(key_bytes)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext_bytes, None)
    return f"{base64.b64encode(nonce).decode('utf-8')}:{base64.b64encode(ct).decode('utf-8')}"

def aes_decrypt(package_str: str, key_bytes: bytes) -> bytes:
    nonce_b64, ct_b64 = package_str.split(":")
    nonce = base64.b64decode(nonce_b64)
    ct = base64.b64decode(ct_b64)
    aesgcm = AESGCM(key_bytes)
    return aesgcm.decrypt(nonce, ct, None)
