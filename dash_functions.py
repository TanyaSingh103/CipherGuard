import streamlit as st
from Crypto.Cipher import AES, DES, DES3, Blowfish
from Crypto.Util.Padding import pad, unpad
from io import BytesIO
import os


def show_uploader(file_types):
    """Show the file uploader for encryption or decryption."""
    return st.file_uploader("Choose your file", type=file_types)


def pad_key(key: bytes, length: int) -> bytes:
    """Pad the key to make it the required length for specific algorithms."""
    while len(key) < length:
        key += b"0"
    return key[:length]


def encrypt_file(file, algorithm, key, file_type):
    """Encrypt the uploaded file."""
    content = file.read()
    iv = os.urandom(16 if algorithm == "AES" else 8)  # AES uses 16-byte IV, others use 8-byte
    encrypted_data = None

    try:
        if algorithm == "AES":
            cipher = AES.new(pad_key(key.encode(), 32), AES.MODE_CBC, iv)
            encrypted_data = cipher.encrypt(pad(content, AES.block_size))
        elif algorithm == "DES":
            cipher = DES.new(pad_key(key.encode(), 8), AES.MODE_CBC, iv)
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
        # Save the file_type, IV length, IV, and encrypted data
        output.write(file_type.encode() + b":" + len(iv).to_bytes(4, 'big') + iv + encrypted_data)
        output.seek(0)
        return output
    except Exception as e:
        st.error(f"Encryption failed: {e}")
        return None


def decrypt_file(file, algorithm, key):
    """Decrypt the uploaded encrypted file."""
    content = file.read()

    try:
        # Extract file type and IV length
        file_type_end = content.find(b":")
        file_type = content[:file_type_end].decode()  # Decode file type to a string
        iv_len = int.from_bytes(content[file_type_end + 1:file_type_end + 5], 'big')
        iv_start = file_type_end + 5
        iv = content[iv_start:iv_start + iv_len]
        encrypted_data = content[iv_start + iv_len:]

        # Validate IV length
        if algorithm == "AES" and len(iv) != 16:
            raise ValueError("Incorrect IV length for AES (must be 16 bytes).")
        elif algorithm in ["DES", "3DES", "Blowfish"] and len(iv) != 8:
            raise ValueError("Incorrect IV length for DES/3DES/Blowfish (must be 8 bytes).")

        # Decrypt the data
        if algorithm == "AES":
            cipher = AES.new(pad_key(key.encode(), 32), AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        elif algorithm == "DES":
            cipher = DES.new(pad_key(key.encode(), 8), AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), DES.block_size)
        elif algorithm == "3DES":
            cipher = DES3.new(pad_key(key.encode(), 24), AES.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), DES3.block_size)
        elif algorithm == "Blowfish":
            cipher = Blowfish.new(pad_key(key.encode(), 16), Blowfish.MODE_CBC, iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
        else:
            st.error(f"{algorithm} is not supported.")
            return None, None

        # Prepare decrypted file for download
        decrypted_file = BytesIO(decrypted_data)
        decrypted_file.seek(0)
        return file_type, decrypted_file

    except Exception as e:
        st.error(f"Decryption failed: {e}")
        return None, None
