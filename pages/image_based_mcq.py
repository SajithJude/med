import streamlit as st
import requests
import base64
import os

# Assuming OPENAI_API_KEY is set in your environment variables
api_key = os.environ.get('OPENAI_API_KEY')

# Function to encode the image file uploaded
def encode_image(uploaded_image):
    return base64.b64encode(uploaded_image.getvalue()).decode('utf-8')

st.title("Image Upload for OpenAI Response")

uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    
    # Encode the uploaded image for the API request
    base64_image = encode_image(uploaded_image=uploaded_file)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Generate questions that can be asked from the image, to be answered by looking at the image"
                    },
                    {
                        "type": "image",
                        "data": f"data:image/jpeg;base64,{base64_image}"
                    }
                ]
            }
        ],
        "max_tokens": 3000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response:
        st.write(response.json())

    if response.status_code == 200:
        st.write("Response from OpenAI:")
        st.write(response.json())
    else:
        st.write("Failed to get response from OpenAI API. Status code: " + str(response))

