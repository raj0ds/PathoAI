from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

st.set_page_config(page_title="Multilingual Pathologist", page_icon=":female-doctor:")

# Prompt user for API key
google_api_key = st.text_input("Enter your Google API Key:")
if not google_api_key:
    st.error("Please enter your Google API Key.")
    st.stop()

# Configure genai with the entered API key
# genai.configure(api_key=google_api_key)
genai.configure(api_key=google_api_key)
# Load gemini pro vision 
model = genai.GenerativeModel("gemini-pro-vision")

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        byte_data = uploaded_file.getvalue()
        image_part = {
                "mime_type":uploaded_file.type,
                "data": byte_data
                }
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")
def get_gemini_response(input, image, user_prompt):
    response = model.generate_content([input, image, user_prompt]) # in Gemini pro we can pass parameter as list
    return response.text

st.header("Patho-AI :female-doctor:")
input = st.text_input("Input Prompt", key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice....", type=["jpg", "jpeg", "pdf", "docx","png", "image/png"])
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", use_column_width=True)
    
submit=st.button("Generate answer")
input_prompt = """You are an expert pathologist. We will upload an image of medical test report
you will have to see the report and analyse that report either is normal or is it some issue in case of issue you have to point out the possible reasons of that and steps to increase or decrease that also give suggestions about how patient should improve that condition using diet, medicine etc """

if submit:
    image_data=input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is : ")
    st.write(response)