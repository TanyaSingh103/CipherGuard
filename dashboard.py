import streamlit as st
import pandas as pd
import dash_functions as fns


import streamlit as st

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
    st.write('Encrypt and decrypt files using an encryption of your choice ')
    st.write('1. csv \n 2. doc \n 3. pdf \n 4. jpg')
    choice = st.text_input('Enter file type to upload : ')

    if(choice):
        uploaded_file = fns.show_uploader(int(choice))

        st.write('Do you want to encrypt or decrypt?')
        if st.button("Encrypt"):
            fns.encrypt()
        elif st.button("Decrypt"):
            fns.decrypt()

elif nav_option == "About":
    st.title("About Us")
    st.write("Information about the application or organization.")

elif nav_option == "Services":
    st.title("Our Services")
    st.write("Details about the services provided.")

elif nav_option == "Contact":
    st.title("Contact Us")
    st.write("Contact details and form to reach out.")

st.markdown("</div>", unsafe_allow_html=True)


