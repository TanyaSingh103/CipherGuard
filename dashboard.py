import streamlit as st
import dash_functions as fns

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
        padding-top: 60px;  /* Offset for the fixed navbar */
    }
    </style>
    <div class="topnav">
      <a href="#home" class="active">Home</a>
      <a href="#about">About</a>
      <a href="#services">Services</a>
      <a href="#contact">Contact</a>
    </div>
    <div class="content">
    """,
    unsafe_allow_html=True,
)

nav_option = st.radio("", ["Home", "About", "Services", "Contact"], index=0, horizontal=True, label_visibility="collapsed")

if nav_option == "Home":
    st.title('CipherGuard')
    st.write('Encrypt and decrypt files using an encryption algorithm of your choice.')
    st.write('Supported file types:\n1. CSV \n2. DOC \n3. PDF \n4. JPG')
    choice = st.text_input('Enter file type to upload (1-4): ')

    if choice:
        uploaded_file = fns.show_uploader(int(choice))  # File uploader based on type

        if uploaded_file:
            algorithm = st.selectbox("Choose an encryption algorithm", ["AES", "DES", "RSA"])
            operation = st.radio("Choose an operation:", ["Encrypt", "Decrypt"], horizontal=True)
            key = st.text_input("Enter your key (AES: 16/24/32 chars)")

            if key and st.button("Submit"):
                if operation == "Encrypt":
                    encrypted_file = fns.encrypt_file(uploaded_file, algorithm, key, int(choice))
                    if encrypted_file:
                        st.success("File encrypted successfully!")
                        st.download_button("Download Encrypted File", encrypted_file.getvalue(), "encrypted_file")
                elif operation == "Decrypt":
                    decrypted_file = fns.decrypt_file(uploaded_file, algorithm, key, int(choice))
                    if decrypted_file:
                        st.success("File decrypted successfully!")
                        st.download_button("Download Decrypted File", decrypted_file.getvalue(), "decrypted_file")

elif nav_option == "About":
    st.title("About Us")
    st.write("CipherGuard is a secure file encryption and decryption tool.")

elif nav_option == "Services":
    st.title("Our Services")
    st.write("Secure encryption and decryption for various file types.")

elif nav_option == "Contact":
    st.title("Contact Us")
    st.write("Email: contact@cipherguard.com")

st.markdown("</div>", unsafe_allow_html=True)
