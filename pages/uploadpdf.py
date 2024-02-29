import qdrant_client
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.schema import ImageDocument

from llama_index.core.response.notebook_utils import display_source_node
from llama_index.core.schema import ImageNode

from llama_index.multi_modal_llms.openai import OpenAIMultiModal

openai_mm_llm = OpenAIMultiModal(
    model="gpt-4-vision-preview", api_key=OPENAI_API_TOKEN, max_new_tokens=1500
)


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

imageupload = st.file_uploader("Choose a PDF file", type="pdf")

if imageupload is not None:
    # Display the uploaded image
    st.image(imageupload, caption='Uploaded Image.', use_column_width=True)
    st.write("Filename:", uploaded_file.name)
    st.write("File size:", uploaded_file.size, "bytes")

    # Save the PDF to the data folder
    file_path = os.path.join('data', uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved in {file_path}")
    extract_images_from_pdf(file_path,'data')
    dirs = os.listdir('data')
    st.write(dirs)

    # image_documents = [
    #     ImageDocument(image_path=image_path) for image_path in retrieved_images
    # ]


    # response = openai_mm_llm.complete(
    #     prompt="Compare llama2 with llama1?",
    #     image_documents=image_documents,
    # )


# if response:

#     response