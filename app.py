import streamlit as st
import streamlit.components.v1 as components
import easyocr
import io
import tempfile
import os

from PIL import Image
from googletrans import Translator

text_input_disabled = False

st.title('extt', anchor=False)
st.caption('tool for extracting and translating text from image based in [EasyOCR OSS](https://github.com/JaidedAI/EasyOCR) and a [implementation of Google Translate API](https://github.com/ssut/py-googletrans)')

uploaded_files = st.file_uploader('upload files', help='we do not store your files', accept_multiple_files=True)

st.write('or')

if uploaded_files:
    text_input_disabled = True

url = st.text_input('paste an image link', disabled=text_input_disabled)

col1, col2 = st.columns(2)

with col1:
    from_lang = st.selectbox(
        'from lang',
        ('en', 'ru', 'pt', 'es', 'fr'))

with col2:
    to_lang = st.selectbox(
        'to lang',
        ('en', 'ru', 'pt', 'es', 'fr'))

_, colbtn, _ = st.columns(3)

with colbtn:
    button = st.button('extract and translate', type='primary')

st.divider()

if button:
    def translate(text, from_lang=from_lang, to_lang=to_lang):
        translator = Translator()
        translate = translator.translate((text), src=from_lang, dest=to_lang)
        return translate.text

    def show_result(source):
        _, colimg, _ = st.columns([1, 10, 1])
        colsrc, coltrans = st.columns(2)

        with colimg:
            if source == 'url':
                st.caption(url)
            if source == 'uploaded_files':
                st.image(temp_image_path, caption=uploaded_file.name)

        with colsrc:
            st.caption('source:')
            for r in result:
                st.write(r)

        with coltrans:
            st.caption('translation:')
            for r in result:
                try:
                    st.write(translate(r))
                except TypeError:
                    st.write(f':red[error: unable to translate "{r}"]')

        st.divider()

    temp_dir = tempfile.TemporaryDirectory()

    reader = easyocr.Reader([from_lang])

    if url:
        result = reader.readtext(url, detail=0, paragraph=True)

        show_result('url')

    if uploaded_files:
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()

            image = Image.open(io.BytesIO(bytes_data))

            temp_image_path = os.path.join(temp_dir.name, uploaded_file.name)
            image.save(temp_image_path)

            result = reader.readtext(temp_image_path, detail=0, paragraph=True)

            show_result('uploaded_files')
