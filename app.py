import streamlit as st
import streamlit.components.v1 as components
import easyocr
import io
import tempfile
import os

from PIL import Image
from googletrans import Translator

st.title('extt', anchor=False)
st.caption('tool for extracting and translating text from image based in [EasyOCR](https://github.com/JaidedAI/EasyOCR) and a [implementation of Google Translate API](https://github.com/ssut/py-googletrans)')

uploaded_files = st.file_uploader('upload files', help='we do not store your files', accept_multiple_files=True)

col1, col2 = st.columns(2)

with col1:
    from_lang = st.selectbox(
        'from lang',
        ('en', 'ru', 'pt', 'es', 'fr'))

with col2:
    to_lang = st.selectbox(
        'to lang',
        ('en', 'ru', 'pt', 'es', 'fr'))

_, colb, _ = st.columns(3)
with colb:
    button = st.button('extract and translate', type='primary')

st.divider()

if button:

    def translate(text, from_lang=from_lang, to_lang=to_lang):
        translator = Translator()
        translate = translator.translate((text), src=from_lang, dest=to_lang)
        return translate.text

    temp_dir = tempfile.TemporaryDirectory()

    reader = easyocr.Reader([from_lang])

    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

        image = Image.open(io.BytesIO(bytes_data))

        temp_image_path = os.path.join(temp_dir.name, uploaded_file.name)
        image.save(temp_image_path)

        result = reader.readtext(temp_image_path)

        colimg, coltext = st.columns(2)

        with colimg:
            st.image(temp_image_path)

        with coltext:
            st.subheader(f'{uploaded_file.name}', anchor=False, divider='rainbow')
            for (_, coord, _) in result:
                try:
                    st.write(f'''
                    {coord}

                    **translation:** {translate(coord)}
                    ''')
                    st.divider()
                except TypeError as e:
                    st.error(f'error: Unable to translate "{coord}"')
                    st.divider()