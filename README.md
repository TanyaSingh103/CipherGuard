# CipherGuard

A secure and interactive file encryption and decryption platform, developed using **Python** and the **Streamlit** framework, to ensure data confidentiality and integrity through advanced cryptographic algorithms.

---
## Overview

CipherGuard provides an easy-to-use interface for encrypting and decrypting various file types, including **CSV**, **DOC**, **PDF**, and **images**. With support for multiple encryption algorithms, it ensures flexible and secure file handling, protecting sensitive data with password-protected encryption keys.

---

## Features

- **Multi-File Support**: Encrypt and decrypt files of type CSV, DOC, PDF, and images.
- **Algorithm Selection**: Choose from **DES**, **AES**, **3DES**, and **Blowfish** encryption algorithms.
- **Password-Protected Keys**: Input encryption keys securely in a password field.
- **Secure Downloads**: Download encrypted files safely.
- **Data Integrity**: Retrieve original files during decryption if the correct key is provided.
- **Streamlit-Based UI**: Provides a seamless, interactive, and visually appealing interface.

---

## Tech Stack

- **Framework**: Streamlit (Python)
- **Core Language**: Python
- **Encryption Algorithms**:
  - **AES** (Advanced Encryption Standard)
  - **DES** (Data Encryption Standard)
  - **3DES** (Triple DES)
  - **Blowfish**

---

## How It Works

1. **File Upload**:
   Upload any supported file type (CSV, DOC, PDF, image).

2. **Select Algorithm**:
   Choose an encryption algorithm from **DES**, **AES**, **3DES**, or **Blowfish**.

3. **Enter Key**:
   - Provide a secure encryption key in the password field.
   - The same key is required for decryption.

4. **Encrypt File**:
   - Click the **Encrypt** button to generate the encrypted file.
   - Download the encrypted file securely.

5. **Decrypt File**:
   - Upload the encrypted file.
   - Choose the algorithm and provide the same key used for encryption.
   - Retrieve the original file if the key matches.

---

## Security Considerations

- Always use strong and unique keys to ensure data confidentiality.
- Keep the encryption key confidential, as it is essential for decrypting files.
- This application leverages robust cryptographic libraries, but the security of your data also depends on protecting the keys and encrypted files.
  
---

Enjoy secure and reliable file encryption with CipherGuard!

