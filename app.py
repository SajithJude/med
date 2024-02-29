import streamlit as st
import fitz  # PyMuPDF
import os
import shutil
from PIL import Image
import io

# Create a data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Title of the app
st.title('PDF Upload and Save App')

def extract_images_from_pdf(filepath, file_dir):
    img_path = os.path.join(file_dir, "pages")
    os.makedirs(img_path, exist_ok=True)
    captionlist = []
    with fitz.open(filepath) as doc:
        for page_index in range(len(doc)):
            page = doc[page_index]

            for image_index, img in enumerate(page.get_images(full=True), start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
                
                imgfilepath = os.path.join(img_path, f"page_{page_index}_{image_index}.{image_ext}")
                captionlist.append({"Image_path": imgfilepath, "surroundingText": ""})  # Example placeholder
                
                if image.mode == 'CMYK':
                    image = image.convert('RGB')

                image.save(imgfilepath)
    
    return captionlist, img_path

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

    try:
        # Extract images and get the path where images are saved
        _, img_path = extract_images_from_pdf(file_path, "data")
        
        # Create a ZIP file of the images folder
        zip_path = os.path.join('data', 'images.zip')
        shutil.make_archive(base_name=img_path, format='zip', root_dir=img_path)
        
        # Provide a button to download the ZIP file
        with open(zip_path , "rb") as fp:
            btn = st.download_button(
                label="Download Images as ZIP",
                data=fp,
                file_name='images.zip',
                mime='application/zip'
            )
    except Exception as e:
        st.error(f"Error processing PDF file: {e}")
