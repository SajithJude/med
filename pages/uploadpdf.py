import qdrant_client
import streamlit as st
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.schema import ImageDocument
from PIL import Image
import os
import fitz
import base64
# from b64encode import BytesIO
import io
# from llama_index.core.response.notebook_utils import display_source_node
from llama_index.core.schema import ImageNode

from llama_index.multi_modal_llms.openai import OpenAIMultiModal

openai_mm_llm = OpenAIMultiModal(
    model="gpt-4-vision-preview", api_key=st.secrets["OPENAI_API_KEY"], max_new_tokens=9500
)


def extract_images_from_pdf(filepath, file_dir):

    
      img_path = os.path.join(file_dir, "pages")
      os.makedirs(img_path, exist_ok=True)
      filelist = [ f for f in os.listdir(img_path) if f.endswith(".png") ]
      for f in filelist:
        os.remove(os.path.join(img_path, f))

      captiolist = []
      with fitz.open(filepath) as doc:
          for page in doc:  # iterate through the pages
            pix = page.get_pixmap()  # render page to an image
            pix.save(os.path.join(img_path,"page-%i.png" % page.number))  # store image as a PNG

            #    = page.get_image_rects(xref)[0]

imageupload = st.file_uploader("Choose a PDF file", type="pdf")

if imageupload is not None:
    # Display the uploaded image
    # st.image(imageupload, caption='Uploaded Image.', use_column_width=True)
    st.write("Filename:", imageupload.name)
    st.write("File size:", imageupload.size, "bytes")

    # Save the PDF to the data folder
    file_path = os.path.join('data', imageupload.name)
    with open(file_path, "wb") as f:
        f.write(imageupload.getbuffer())
    st.success(f"File saved in {file_path}")
    extract_images_from_pdf(file_path,'data')
    dirs = os.listdir('data/pages')
    st.write(dirs)

    image_documents = [
        ImageDocument(image_path="data/pages/"+image_path) for image_path in dirs
    ]


    response = openai_mm_llm.complete(
        prompt="Generate MCQ Questions that can be answered with the images, for MBBS graduates, with solutions",
        image_documents=image_documents,
    )


if response:

    response