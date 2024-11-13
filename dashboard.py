import streamlit as st
import pandas as pd
import dash_functions as fns

st.title('CipherGuard')
st.write('Encrypt and decrypt files using an encryption of your choice ')

st.write('1. csv \n 2. doc \n 3. pdf \n 4. jpg')
choice = st.text_input('Enter file type to upload : ')

if(choice):
    uploaded_file = fns.show_uploader(int(choice))