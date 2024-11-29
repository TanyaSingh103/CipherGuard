import streamlit as st
from Crypto.Cipher import AES, DES, DES3, Blowfish
from Crypto.Util.Padding import pad, unpad
from io import BytesIO
import os

def show_uploader(choice):
    """Show the file uploader based on the choice."""
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
        key += b"0" 
    return key[:length]

def encrypt_file(file, algorithm, key, file_type):
    """Encrypt the uploaded file."""
    content = file.read()
    
    # Ensure IV length is correct
    if algorithm == "Blowfish":
        iv = os.urandom(8)  # Blowfish uses 8-byte IV
    else:
        iv = os.urandom(8 if algorithm in ["3DES", "DES", "Blowfish"] else 16)  # Use 8 bytes for DES/Blowfish, 16 for AES/3DES

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

    output = BytesIO()
    output.write(file_type.encode() + b":" + iv + encrypted_data)
    output.seek(0)
    return output

def decrypt_file(file, algorithm, key):
    """Decrypt the uploaded file."""
    content = file.read()
    file_type, content = content.split(b":", 1)
    
    # Ensure IV length is correct
    if algorithm == "Blowfish":
        iv = content[:8]  # Blowfish uses 8-byte IV
    else:
        iv = content[:8 if algorithm in ["3DES", "DES", "Blowfish"] else 16]  # Use 8 bytes for DES/Blowfish, 16 for AES/3DES
    
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

    output = BytesIO(decrypted_data)
    output.name = file_type.decode()
    output.seek(0)
    return output

# Streamlit UI
st.title("File Encryption & Decryption")
st.subheader("Secure your files using encryption algorithms.")

# File Type Selection
file_type = st.radio("Select File Type:", ["CSV", "DOC", "PDF", "JPG"], index=0)

# File Upload
uploaded_file = show_uploader([1, 2, 3, 4][["CSV", "DOC", "PDF", "JPG"].index(file_type)])

# Algorithm Selection
if uploaded_file:
    algorithm = st.selectbox("Choose Encryption Algorithm:", ["AES", "DES", "3DES", "Blowfish"])

    # Key Input
    key = st.text_input("Enter encryption key (password):", type="password")

    if key and st.button("Submit"):
        operation = st.radio("Select Operation:", ["Encrypt", "Decrypt"])

        if operation == "Encrypt":
            encrypted_file = encrypt_file(uploaded_file, algorithm, key, file_type)
            if encrypted_file:
                st.success("File encrypted successfully")
                st.download_button("Download Encrypted File", encrypted_file.getvalue(), "encrypted_file.enc")
        elif operation == "Decrypt":
            decrypted_file = decrypt_file(uploaded_file, algorithm, key)
            if decrypted_file:
                st.success("File decrypted successfully")
                st.download_button("Download Decrypted File", decrypted_file.getvalue(), "decrypted_file")
