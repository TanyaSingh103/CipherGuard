import streamlit as st
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from PyPDF2 import PdfReader, PdfWriter
import docx
import os

# File uploader
def show_uploader(choice):
    uploaded_file = None
    if choice == 1:
        uploaded_file = st.file_uploader("Choose your .csv file", type="csv")
    elif choice == 2:
        uploaded_file = st.file_uploader("Choose your .docx file", type="docx")
    elif choice == 3:
        uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")
    elif choice == 4:
        uploaded_file = st.file_uploader("Choose your .jpg file", type="jpg")
    else:
        st.write("Invalid choice.")
    return uploaded_file

# Encryption
def encrypt_file(file, algorithm, file_type):
    key = b"encryptionkey12"  # 16-byte key for AES/3DES/Blowfish
    backend = default_backend()
    iv = os.urandom(16)

    # Select algorithm
    if algorithm == "AES":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    elif algorithm == "Blowfish":
        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=backend)
    elif algorithm == "3DES":
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    else:
        st.error("Unsupported algorithm for encryption.")
        return

    encryptor = cipher.encryptor()
    padded_data = pad_data(file.read())
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    return save_temp_file(encrypted_data, file_type)

# Decryption
def decrypt_file(file, algorithm, file_type):
    key = b"encryptionkey12"
    backend = default_backend()
    iv = os.urandom(16)

    if algorithm == "AES":
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    elif algorithm == "Blowfish":
        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=backend)
    elif algorithm == "3DES":
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=backend)
    else:
        st.error("Unsupported algorithm for decryption.")
        return

    decryptor = cipher.decryptor()
    encrypted_data = file.read()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return save_temp_file(decrypted_data, file_type)

# Padding helper
def pad_data(data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    return padder.update(data) + padder.finalize()

# Save file to temp
def save_temp_file(data, file_type):
    extension = {1: "csv", 2: "docx", 3: "pdf", 4: "jpg"}[file_type]
    temp_file = f"temp.{extension}"
    with open(temp_file, "wb") as f:
        f.write(data)
    return temp_file

# File download link
def download_file(file_path, action):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/octet-stream;base64,{b64}" download="{action}_{os.path.basename(file_path)}">Download {action.title()} File</a>'
    st.markdown(href, unsafe_allow_html=True)
