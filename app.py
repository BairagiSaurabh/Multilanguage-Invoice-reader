import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Load Gemini pro vision

model = genai.GenerativeModel("gemini-pro-vision")

def get_final_response(system_prompt,input_image,user_prompt):
    response = model.generate_content([system_prompt,input_image[0],user_prompt])
    for candidate in response.candidates:
        return [part.text for part in candidate.content.parts][0]
    #return response.text

def image_processing(upload_file):
    """
    This function converts the image in bytes
    """

    if upload_file is not None:
        data_bytes = upload_file.getvalue()
        image_parts = [
            {
                "mime_type" : upload_file.type,
                "data" : data_bytes
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded.")
    
system_prompt  = """

You are a professional Invoice reader with high expertise in multiple languages. 
Once the image of invoice or any other document image is uploaded, you will correctly 
answer the questions asked based on the uploaded file. If you do not find any answer just say 
that "Answer cannot be found in the given file." 

"""

## Stremlit code:
    
st.set_page_config(page_title="Gemini Image Analysis")

st.header("Multilanguage Invoice/Image reader")
input = st.text_input("Input Prompt: ", key= "user_prompt")
upload_file = st.file_uploader("Upload your invoice image", type = ["jpg", "jpeg", "png"])
submit = st.button("Click here to Get Answer...")

image = ""

if submit:
    image_data = image_processing(upload_file)
    response =  get_final_response(system_prompt,image_data,input)
    st.success(f"Answer : {response}")

if upload_file is not None:
     image = Image.open(upload_file)
     st.image(image, caption = "Uploaded image")




