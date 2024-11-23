import streamlit as st
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from io import BytesIO
import os

def show_uploader(choice):
    uploaded_file = None
    if choice == 1:
        uploaded_file = st.file_uploader("Choose your CSV file", type="csv")
    elif choice == 2:
        uploaded_file = st.file_uploader("Choose your DOC file", type="doc")
    elif choice == 3:
        uploaded_file = st.file_uploader("Choose your PDF file", type="pdf")
    elif choice == 4:
        uploaded_file = st.file_uploader("Choose your JPG file", type="jpg")
    else:
        st.write("Please choose a valid option (1-4).")
    return uploaded_file

def pad_key(key: bytes, length: int) -> bytes:
    """Pad the key to make it the required length for AES."""
    while len(key) < length:
        key += b"0"  # Add padding
    return key[:length]

def encrypt_file(file, algorithm, key, file_type):
    """Encrypt the uploaded file."""
    backend = default_backend()
    iv = os.urandom(16)
    key = pad_key(key.encode(), 32)  # AES requires key size of 16, 24, or 32 bytes

    if algorithm == "AES":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    else:
        st.error(f"{algorithm} is not supported yet.")
        return None

    encryptor = cipher.encryptor()
    padder = PKCS7(128).padder()
    padded_data = padder.update(file.read()) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    output_file = BytesIO(encrypted_data + iv)  # Append IV for decryption
    return output_file

def decrypt_file(file, algorithm, key, file_type):
    """Decrypt the uploaded file."""
    backend = default_backend()
    content = file.read()
    key = pad_key(key.encode(), 32)  # AES requires key size of 16, 24, or 32 bytes

    iv = content[-16:]  # Extract the last 16 bytes as the IV
    encrypted_data = content[:-16]

    if algorithm == "AES":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    else:
        st.error(f"{algorithm} is not supported yet.")
        return None

    decryptor = cipher.decryptor()
    unpadder = PKCS7(128).unpadder()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    output_file = BytesIO(decrypted_data)
    return output_file
