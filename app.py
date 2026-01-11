import os
import hashlib
import pandas as pd
import streamlit as st
import pymupdf  # PyMuPDF per llegir PDF
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

# Configuració de l'API
os.environ["GOOGLE_API_KEY"] = 'AIxxx'

chat_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.9,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# Funció per extreure text del PDF
def extract_text_from_pdf(pdf_file):
    pdf_document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Funció per generar tasques i preguntes basades en el contingut
def generate_work_from_text(text, num_tasks):
    prompt = f"""
    Ets un expert en educació secundària. A continuació tens el contingut d’una unitat didàctica sobre un tema específic.
    A partir d’aquest contingut, crea un conjunt de {num_tasks} preguntes de comprensió, activitats i tasques per als estudiants.
    Aquestes tasques han de ser adequades per a alumnes de secundària, basades en la informació del text, i han d’ajudar els estudiants a aprendre de manera efectiva.

    Text de la unitat didàctica:
    {text}

    Tasques i preguntes:
    """
    return chat_model.predict(prompt)

# Interfície de Streamlit
st.title("📚 Generador de Treballs per a Estudiants a partir d'una Unitat Didàctica")

# Pujar arxiu PDF
uploaded_pdf = st.file_uploader("Si us plau, puja un arxiu PDF amb una unitat didàctica", type=["pdf"])

# Seleccionar el nombre de tasques a generar
num_tasks = st.selectbox("Quantes tasques o preguntes vols generar?", [5, 10, 15], 0)

# Crear un espai per mostrar els resultats generats
if uploaded_pdf:
    # Extreure el text del PDF
    pdf_text = extract_text_from_pdf(uploaded_pdf)

    # Mostrar una part del text extret per confirmar que s’ha carregat correctament
    st.write("### Text extret de la unitat didàctica:")
    st.write(pdf_text[:1500])

    # Botó per generar el treball basat en el text extret
    if st.button("Generar tasques i preguntes per als estudiants"):
        with st.spinner("Generant tasques..."):
            work = generate_work_from_text(pdf_text, num_tasks)
            st.write("### Tasques i preguntes generades:")
            st.write(work)

    # Exportar les tasques generades com a fitxer de text
    if st.button("Exportar tasques a un fitxer de text"):
        if 'work' in locals():
            st.download_button(
                label="Descarregar fitxer de tasques",
                data=work,
                file_name="tasques_estudiants.txt",
                mime="text/plain"
            )
else:
    st.write("Si us plau, puja un arxiu PDF amb la unitat didàctica per començar.")
