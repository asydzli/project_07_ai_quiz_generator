import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

from utils import read_pdf
from utils import read_docx
from utils import read_pptx

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY tidak ditemukan.")
    st.stop()

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI Quiz Generator from Documents")

st.write(
    "Upload materi lalu biarkan AI membuat soal latihan secara otomatis."
)

uploaded_file = st.file_uploader(
    "Upload Materi",
    type=["pdf", "docx", "pptx"]
)

col1, col2, col3 = st.columns(3)

with col1:
    total = st.slider(
        "Jumlah Soal",
        5,
        20,
        10
    )

with col2:
    difficulty = st.selectbox(
        "Kesulitan",
        [
            "Mudah",
            "Sedang",
            "Sulit"
        ]
    )

with col3:
    quiz_type = st.selectbox(
        "Jenis Soal",
        [
            "Pilihan Ganda",
            "Essay",
            "Benar / Salah"
        ]
    )

if st.button("🚀 Generate Quiz", use_container_width=True):

    if uploaded_file is None:

        st.warning("Silakan upload file terlebih dahulu.")

    else:

        extension = uploaded_file.name.split(".")[-1]

        if extension == "pdf":
            text = read_pdf(uploaded_file)

        elif extension == "docx":
            text = read_docx(uploaded_file)

        elif extension == "pptx":
            text = read_pptx(uploaded_file)

        else:
            text = ""

        prompt = f"""
Berikut adalah materi pembelajaran.

{text}

Buatkan:

{total} soal

Jenis soal:

{quiz_type}

Tingkat kesulitan:

{difficulty}

Gunakan Bahasa Indonesia.

Jika pilihan ganda,
berikan 4 opsi.

Setelah setiap soal,
berikan jawaban yang benar.

Format harus rapi.
"""

        with st.spinner("AI sedang membuat soal..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.success("Quiz berhasil dibuat!")

                st.markdown(response.text)

            except Exception as e:

                st.error(e)