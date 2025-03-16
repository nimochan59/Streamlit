import streamlit as st
from PIL import Image
import numpy as np
import cv2

st.title("Image Converter")
  
uploaded_file = st.file_uploader('Upload your image file.')
  
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = np.array(image)

    st.subheader('Uploaded image')
    st.image(image)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    st.subheader('Converted image')
    st.image(gray_image)
