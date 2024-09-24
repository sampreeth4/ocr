#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
from PIL import Image
import pytesseract
import re

# Set the path to the tesseract executable (for Windows users)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path as needed
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
# Title of the web app
st.title("Hindi and English OCR Web Application")

# File upload
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)
    
    # Display the image in the app
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Perform OCR with Tesseract (support for both Hindi and English)
    with st.spinner('Performing OCR...'):
        extracted_text = pytesseract.image_to_string(image, lang='hin+eng')
    
    # Display extracted text
    st.subheader("Extracted Text")
    st.write(extracted_text)

    # Input for searching keywords
    search_query = st.text_input("Enter keyword(s) to search in the text")

    if search_query:
        # Search the keyword(s) in the extracted text
        # Highlighting search results
        def highlight_keywords(text, keyword):
            # Create a regex pattern for the keyword
            pattern = re.escape(keyword)
            # Highlight matching keywords using HTML span
            highlighted_text = re.sub(f"({pattern})", r'<span style="color:red; font-weight:bold;">\1</span>', text, flags=re.IGNORECASE)
            return highlighted_text
        
        highlighted_text = highlight_keywords(extracted_text, search_query)
        
        # Display search results
        st.subheader("Search Results")
        if search_query.lower() in extracted_text.lower():
            st.write(f"Matches found for '{search_query}':")
            st.markdown(f'<div style="white-space: pre-wrap;">{highlighted_text}</div>', unsafe_allow_html=True)
        else:
            st.write(f"No matches found for '{search_query}'.")

else:
    st.write("Please upload an image file to start the OCR process.")

