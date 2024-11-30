import streamlit as st
import dash_functions as fns
from io import BytesIO
from PIL import Image
import pandas as pd

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
nav_option = st.radio(
    "Navigation options (hidden):",
    ["Home", "About", "Contact"],
    index=0,
    horizontal=True,
    label_visibility="collapsed"
)

if nav_option == "Home":
    st.title('CipherGuard: Secure Your Files')
    st.subheader('Encrypt and decrypt files effortlessly.')
    st.markdown("**Supported file types:** CSV, DOC, PDF, JPG")

    file_type = st.radio("Select File Type to Upload:", ["CSV", "DOC", "PDF", "JPG"])

    st.subheader("Upload Your File")
    uploaded_file = fns.show_uploader([file_type.lower()])

    if uploaded_file:
        st.success("File uploaded successfully!")

        # display file preview
        if file_type.lower() in ["jpg", "jpeg", "png"]:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True) 

        elif file_type.lower() == "pdf":
            st.write("PDF file preview:")
            st.download_button("Download PDF", uploaded_file)

        elif file_type.lower() == "csv":
            df = pd.read_csv(uploaded_file)
            st.write("CSV file preview:")
            st.dataframe(df.head())  

        else:
            st.write("File preview is not available for this type.")

        operation = st.radio("Select Operation:", ["Encrypt", "Decrypt"], index=0)

        if operation == "Encrypt":
            st.markdown(
                """
                ### Encryption Key Requirements:
                - **AES**: Key length must be 16, 24, or 32 characters.
                - **DES**: Key length must be exactly 8 characters.
                - **3DES**: Key length must be 24 characters.
                - **Blowfish**: Key length must be 16 characters.
                """
            )
            algorithm = st.selectbox("Choose Encryption Algorithm:", ["AES", "DES", "3DES", "Blowfish"])
            key = st.text_input("Enter encryption key (password):", type="password")

            if key and st.button("Encrypt"):
                encrypted_file = fns.encrypt_file(uploaded_file, algorithm, key, file_type)
                if encrypted_file:
                    st.success("File encrypted successfully!")
                    st.download_button("Download Encrypted File", encrypted_file.getvalue(), "encrypted_file.enc")

        elif operation == "Decrypt":
            st.markdown(
                """
                ### Decryption Key Requirements:
                - Ensure the key matches the encryption algorithm's requirements.
                """
            )
            # Decrypt section only appears if user has uploaded an encrypted file (with .enc extension)
            uploaded_enc_file = fns.show_uploader(["enc"])  # Allow only .enc files

            if uploaded_enc_file:
                algorithm = st.selectbox("Choose Decryption Algorithm:", ["AES", "DES", "3DES", "Blowfish"])
                key = st.text_input("Enter decryption key (password):", type="password")

                if key and st.button("Decrypt"):
                    decrypted_file_type, decrypted_content = fns.decrypt_file(uploaded_enc_file, algorithm, key)
                    if decrypted_content:
                        st.success("File decrypted successfully!")
                        decrypted_file = BytesIO(decrypted_content)
                        decrypted_file.name = f"decrypted_file.{decrypted_file_type.lower()}"
                        st.download_button(f"Download Decrypted {decrypted_file_type} File", decrypted_file.getvalue(), decrypted_file.name)

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
    st.markdown("[surbhidkumar@gmail.com](mailto:surbhidkumar@gmail.com)")
    st.markdown("[tanya.103.singh@gmail.com](mailto:tanya.103.singh@gmail.com)")

st.markdown("</div>", unsafe_allow_html=True)
