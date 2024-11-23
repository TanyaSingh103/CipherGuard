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
    st.write('Encrypt and decrypt files using an encryption of your choice')
    st.write('1. csv \n2. docx \n3. pdf \n4. jpg')
    choice = st.text_input('Enter file type to upload (1-4):')

    if choice.isdigit() and int(choice) in [1, 2, 3, 4]:
        uploaded_file = fns.show_uploader(int(choice))
        if uploaded_file:
            action = st.radio("Select Action:", ["Encrypt", "Decrypt"], horizontal=True)
            algorithm = st.selectbox("Select Algorithm:", ["AES", "RSA", "Blowfish", "3DES"])
            
            if st.button("Process File"):
                if action == "Encrypt":
                    encrypted_file = fns.encrypt_file(uploaded_file, algorithm, int(choice))
                    st.success("File encrypted successfully!")
                    fns.download_file(encrypted_file, "encrypted")
                elif action == "Decrypt":
                    decrypted_file = fns.decrypt_file(uploaded_file, algorithm, int(choice))
                    st.success("File decrypted successfully!")
                    fns.download_file(decrypted_file, "decrypted")
    else:
        st.warning("Please enter a valid choice (1-4).")

elif nav_option == "About":
    st.title("About Us")
    st.write("CipherGuard is an application for file encryption and decryption using multiple algorithms.")

elif nav_option == "Services":
    st.title("Our Services")
    st.write("We offer secure file encryption and decryption services for various file formats.")

elif nav_option == "Contact":
    st.title("Contact Us")
    st.write("Reach out to us at support@cipherguard.com")

st.markdown("</div>", unsafe_allow_html=True)
