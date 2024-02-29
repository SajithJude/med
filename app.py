# import streamlit as st
# import fitz  # PyMuPDF
# import os
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
      captiolist = []
      with fitz.open(filepath) as doc:
          for page_index in range(len(doc)):
              page = doc[page_index]

              for image_index, img in enumerate(page.get_images(full=True), start=1):
                  xref = img[0]
                  base_image = doc.extract_image(xref)
                  image_bytes = base_image["image"]
                  image_ext = base_image["ext"]
                  image = Image.open(io.BytesIO(image_bytes))
                  img_rect = page.get_image_rects(xref)[0]
                  # Create a surrounding box that's 1.5 times the image area
                  new_rect = fitz.Rect(
                      img_rect.x0 - 0.25 * img_rect.width,
                      img_rect.y0 - 0.25 * img_rect.height,
                      img_rect.x1 + 0.25 * img_rect.width,
                      img_rect.y1 + 0.25 * img_rect.height
                  )

                  imgfilepath = os.path.join("data", img_path, f"page_{page_index}_{image_index}.{image_ext}")
                  # Extract text in the surrounding box
                  text = page.get_text("text", clip=new_rect)
                  captiolist.append({"Image_path":imgfilepath , "surroundingText": text})
                  # If the image is in CMYK mode, invert the channels
                  if image.mode == 'CMYK':
                      inverted_channels = [channel.point(lambda p: 255 - p) for channel in image.split()]
                      image = Image.merge('CMYK', inverted_channels)
                      image = image.convert('RGB')

                  image.save(os.path.join(img_path, f"page_{page_index}_{image_index}.{image_ext}"))
                  img_rect = page.get_image_rects(xref)[0]

       
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
        extract_images_from_pdf(file_path,"data")
        st.success(f"ezracted saved in {file_path}")

        zip_path = os.path.join('data', 'images.zip')
        shutil.make_archive(base_name="data", format='zip', root_dir="data")
        
        # Provide a button to download the ZIP file
        with open(zip_path, "rb") as fp:
            btn = st.download_button(
                label="Download Images as ZIP",
                data=fp,
                file_name='images.zip',
                mime='application/zip'
            )
        # st.write("Text extracted from the first page of the PDF:")
        # st.text_area("Extracted Text", text, height=250)
    except Exception as e:
        st.error("Error processing PDF file: " + str(e))
