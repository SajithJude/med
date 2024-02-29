import streamlit as st
import fitz  # PyMuPDF
import os

# Create a data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Title of the app
st.title('PDF Upload and Save App')

# File uploader widget
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Display the details of the uploaded file
    st.write("Filename:", uploaded_file.name)
    st.write("File size:", uploaded_file.size, "bytes")

    # Save the PDF to the data folder
    file_path = os.path.join('data', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved in {file_path}")

    # Here you can add more functionality, such as displaying the PDF content
    # For example, to display the text of the first page
    try:
        # Open the saved PDF file
        doc = fitz.open(file_path)
        page = doc.load_page(0)  # Assuming we want the text from the first page
        text = page.get_text()
        st.write("Text extracted from the first page of the PDF:")
        st.text_area("Extracted Text", text, height=250)
    except Exception as e:
        st.error("Error processing PDF file: " + str(e))
