import streamlit as st
from Crypto.Cipher import AES, DES, DES3, Blowfish
from Crypto.Util.Padding import pad, unpad
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
    """Pad the key to make it the required length for specific algorithms."""
    while len(key) < length:
        key += b"0"  # Add padding
    return key[:length]

def encrypt_file(file, algorithm, key, file_type):
    """Encrypt the uploaded file."""
    content = file.read()
    iv = os.urandom(8 if algorithm in ["DES", "Blowfish"] else 16)  # IV size depends on the algorithm
    encrypted_data = None

    if algorithm == "AES":
        cipher = AES.new(pad_key(key.encode(), 32), AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(content, AES.block_size))
    elif algorithm == "DES":
        cipher = DES.new(pad_key(key.encode(), 8), DES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(content, DES.block_size))
    elif algorithm == "3DES":
        cipher = DES3.new(pad_key(key.encode(), 24), DES3.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(content, DES3.block_size))
    elif algorithm == "Blowfish":
        cipher = Blowfish.new(pad_key(key.encode(), 16), Blowfish.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(content, Blowfish.block_size))
    else:
        st.error(f"{algorithm} is not supported.")
        return None

    # Combine encrypted data with the IV and file type metadata
    output = BytesIO()
    output.write(file_type.encode() + b":" + iv + encrypted_data)
    output.seek(0)
    return output

def decrypt_file(file, algorithm, key):
    """Decrypt the uploaded file."""
    content = file.read()
    file_type, content = content.split(b":", 1)
    iv = content[:8 if algorithm in ["DES", "Blowfish"] else 16]
    encrypted_data = content[8 if algorithm in ["DES", "Blowfish"] else 16:]
    decrypted_data = None

    if algorithm == "AES":
        cipher = AES.new(pad_key(key.encode(), 32), AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    elif algorithm == "DES":
        cipher = DES.new(pad_key(key.encode(), 8), DES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)
    elif algorithm == "3DES":
        cipher = DES3.new(pad_key(key.encode(), 24), DES3.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), DES3.block_size)
    elif algorithm == "Blowfish":
        cipher = Blowfish.new(pad_key(key.encode(), 16), Blowfish.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
    else:
        st.error(f"{algorithm} is not supported.")
        return None

    # Output the decrypted file with its original type
    output = BytesIO(decrypted_data)
    output.name = file_type.decode()
    output.seek(0)
    return output
