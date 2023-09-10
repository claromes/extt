import streamlit as st
import easyocr
from PIL import Image
import io
import tempfile
import os
from googletrans import Translator

FROM_LANG = 'ru'

def translate(text, from_lang=FROM_LANG, to_lang='en'):
    translator = Translator()
    translate = translator.translate(text, src=from_lang, dest=to_lang)
    return translate.text

st.title('extt')

uploaded_files = st.file_uploader('upload a picture', help='we do not store your file', accept_multiple_files=True)
st.empty()
button = st.button('extract and translate', type='primary')

temp_dir = tempfile.TemporaryDirectory()

if button:
    reader = easyocr.Reader([FROM_LANG])

    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

        image = Image.open(io.BytesIO(bytes_data))

        temp_image_path = os.path.join(temp_dir.name, uploaded_file.name)
        image.save(temp_image_path)

        result = reader.readtext(temp_image_path)

        for (_, coord, _) in result:
            st.write(coord)
            st.write(f'translation: {translate(coord)}')
            st.divider()