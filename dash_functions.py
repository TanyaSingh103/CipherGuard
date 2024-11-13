import streamlit as st

def show_uploader(choice):
    uploaded_file = None

    if choice == 1:
        uploaded_file = st.file_uploader("Choose your .csv file", type="csv")
        if uploaded_file is not None:
            st.write("CSV file uploaded.")
            # Further processing of CSV file can go here, such as reading with pandas.
            
    elif choice == 2:
        uploaded_file = st.file_uploader("Choose your .doc file", type="doc")
        if uploaded_file is not None:
            st.write("DOC file uploaded.")
            # Use appropriate libraries to read DOC files, such as python-docx.
            
    elif choice == 3:
        uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")
        if uploaded_file is not None:
            st.write("PDF file uploaded.")
            # Use libraries like PyMuPDF or pdfplumber to read PDF files.
            
    elif choice == 4:
        uploaded_file = st.file_uploader("Choose your .jpg file", type="jpg")
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    else:
        st.write("Please choose a valid option (1-4).")
    
    return uploaded_file
