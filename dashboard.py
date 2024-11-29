import streamlit as st
import dash_functions as fns

# Custom Navbar Styling
st.markdown(
    """
    <style>
    .topnav {
        background-color: #333;
        overflow: hidden;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 100;
    }
    .topnav a {
        float: left;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        font-size: 17px;
    }
    .topnav a:hover {
        background-color: #ddd;
        color: black;
    }
    .topnav a.active {
        background-color: #04AA6D;
        color: white;
    }
    .content {
        padding-top: 70px;  /* Offset for the fixed navbar */
    }
    footer {
        text-align: center;
        position: fixed;
        bottom: 0;
        width: 100%;
        background: #333;
        color: white;
        padding: 10px 0;
    }
    footer a {
        color: #04AA6D;
        text-decoration: none;
    }
    footer a:hover {
        text-decoration: underline;
    }
    </style>
    <div class="topnav">
        <a href="#home" class="active">Home</a>
        <a href="#about">About</a>
        <a href="#contact">Contact</a>
    </div>
    <div class="content">
    """,
    unsafe_allow_html=True,
)

# Navigation Options
nav_option = st.radio("", ["Home", "About", "Contact"], index=0, horizontal=True, label_visibility="collapsed")

if nav_option == "Home":
    st.title('CipherGuard: Secure Your Files')
    st.subheader('Encrypt and decrypt files effortlessly.')
    st.markdown("**Supported file types:** CSV, DOC, PDF, JPG")

    # Dropdown for File Type
    file_type = st.selectbox("Select File Type to Upload:", ["CSV", "DOC", "PDF", "JPG"])

    # File Upload Component
    uploaded_file = st.file_uploader(f"Upload your {file_type} file:", type=file_type.lower())

    # Algorithm Selection
    if uploaded_file:
        st.write("**File Uploaded Successfully!**")
        algorithm = st.selectbox("Choose Encryption Algorithm:", ["AES", "DES", "3DES", "Blowfish"])
        operation = st.radio("Select Operation:", ["Encrypt", "Decrypt"], horizontal=True)

        # Key Input
        key = st.text_input(
            "Enter your encryption key:",
            help="AES: 16/24/32 chars, DES: 8 chars, 3DES: 24 chars, Blowfish: 16 chars",
        )

        if key and st.button("Submit"):
            if len(key) not in [8, 16, 24, 32]:
                st.error("Invalid key length! Please check the key requirements.")
            else:
                if operation == "Encrypt":
                    encrypted_file = fns.encrypt_file(uploaded_file, algorithm, key, uploaded_file.name.split('.')[-1])
                    if encrypted_file:
                        st.success("File encrypted successfully! 🎉")
                        st.download_button("Download Encrypted File", encrypted_file.getvalue(), "encrypted_file.enc")
                elif operation == "Decrypt":
                    decrypted_file = fns.decrypt_file(uploaded_file, algorithm, key)
                    if decrypted_file:
                        st.success("File decrypted successfully! 🎉")
                        st.download_button("Download Decrypted File", decrypted_file.getvalue(), decrypted_file.name)

elif nav_option == "About":
    st.title("About CipherGuard")
    st.markdown(
        """
        CipherGuard is a secure file encryption and decryption tool that simplifies the process for users of all skill levels.

        ### Features:
        - **File Support**: CSV, DOC, PDF, JPG
        - **Algorithms**: AES, DES, 3DES, Blowfish
        - **Ease of Use**: Simple upload and download interface.

        ### How It Works:  
        1. Upload your file.  
        2. Choose an encryption algorithm and operation.  
        3. Provide the key to encrypt or decrypt.  
        """
    )

elif nav_option == "Contact":
    st.title("Contact Us")
    st.write("**For inquiries, reach out to us at:**")
    st.markdown("[kavyabhatia198@gmail.com](mailto:kavyabhatia198@gmail.com)")
    st.markdown("[tanya.103.singh@gmail.com](mailto:tanya.103.singh@gmail.com)")


st.markdown("</div>", unsafe_allow_html=True)
