import streamlit as st
from model_helper import predict


st.title("Satellite Image Detection")

uploaded_img = st.file_uploader("Upload the image", type = ['jpg','png','jpeg','bmp','gif','webp',])

if uploaded_img:
    image_path = "temp_file.jpg"
    with open(image_path, 'wb') as f:
        f.write(uploaded_img.getbuffer())
    st.image(uploaded_img, caption='Uploaded file', use_container_width=True )
    prediction = predict(image_path)
    st.info(f"predicted Class: {prediction}")
        