import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


MODEL_NAME = "gemini-2.5-flash"


def load_api_key() -> str | None:
    """Membaca API key Gemini dari file .env atau environment variable."""
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def build_prompt(topic: str, level: str, total_questions: int, quiz_type: str) -> str:
    """Menyusun prompt agar Gemini membuat quiz yang mudah dipakai belajar."""
    return f"""
Anda adalah pembuat quiz untuk programmer pemula hingga intermediate.

Buat {total_questions} soal quiz berdasarkan detail berikut:
- Topik: {topic}
- Level: {level}
- Jenis soal: {quiz_type}
- Bahasa: Indonesia

Aturan output:
- Gunakan penomoran 1 sampai {total_questions}.
- Untuk pilihan ganda, berikan opsi A sampai D.
- Tulis kunci jawaban setelah semua soal.
- Tambahkan pembahasan singkat untuk setiap jawaban.
- Pastikan soal menguji pemahaman, bukan hafalan saja.
"""


def generate_quiz(api_key: str, prompt: str) -> str:
    """Mengirim prompt ke Gemini dan mengembalikan quiz."""
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text or ""


def main() -> None:
    st.set_page_config(
        page_title="AI Quiz Generator",
        page_icon="AI",
        layout="centered",
    )

    st.title("AI Quiz Generator")
    st.caption("Buat quiz latihan lengkap dengan kunci jawaban dan pembahasan.")

    api_key = load_api_key()
    if not api_key:
        st.error("GEMINI_API_KEY belum ditemukan. Buat file .env dari .env.example.")
        st.stop()

    with st.sidebar:
        st.header("Pengaturan")
        level = st.selectbox("Level soal", ["Pemula", "Intermediate", "Campuran"])
        quiz_type = st.selectbox("Jenis soal", ["Pilihan ganda", "Benar atau salah", "Jawaban singkat"])
        total_questions = st.slider("Jumlah soal", min_value=3, max_value=15, value=5)
        st.info("Model: gemini-2.5-flash")

    with st.form("quiz_form"):
        topic = st.text_input(
            "Topik quiz",
            placeholder="Contoh: Python function, Git, SQL dasar, machine learning",
        )
        submitted = st.form_submit_button("Buat Quiz")

    if submitted:
        clean_topic = topic.strip()

        if not clean_topic:
            st.warning("Masukkan topik quiz terlebih dahulu.")
            st.stop()

        if len(clean_topic) < 3:
            st.warning("Topik terlalu pendek. Gunakan minimal 3 karakter.")
            st.stop()

        prompt = build_prompt(clean_topic, level, total_questions, quiz_type)

        with st.spinner("Gemini sedang membuat quiz..."):
            try:
                result = generate_quiz(api_key, prompt)
            except Exception as error:
                st.error(f"Terjadi error saat menghubungi Gemini: {error}")
                st.stop()

        if not result.strip():
            st.warning("Gemini tidak mengembalikan quiz. Coba lagi.")
            st.stop()

        st.subheader("Quiz")
        st.markdown(result)


if __name__ == "__main__":
    main()
