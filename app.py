import os  # Per gestionar variables d'entorn (p. ex. la clau API)
import streamlit as st  # Llibreria per crear la interfície web amb Streamlit
import pymupdf  # PyMuPDF per llegir i extreure text de PDFs
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI  # Model de xat de Google via LangChain

# ==========================
# CONFIGURACIÓ DE L'API / MODEL
# ==========================

# Definim la clau de l'API com a variable d'entorn perquè el client la pugui llegir
os.environ["GOOGLE_API_KEY"] = 'AIxxx'

# Creem la instància del model de xat
chat_model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",  # Nom del model a utilitzar
    temperature=0.9,                # Creativitat: més alt = respostes més variades
    max_tokens=None,                # Límit de tokens de sortida (None = el que permeti el model/config)
    timeout=None,                   # Temps d'espera màxim (None = per defecte)
    max_retries=2                   # Reintents si falla la petició
)

# Creem una variable per a guardar la última resposta generada
if "work" not in st.session_state:
    st.session_state.work = ""

# ==========================
# FUNCIONS AUXILIARS
# ==========================

def extract_text_from_pdf(pdf_file):
    """
    Llegeix un PDF pujat per Streamlit i n'extreu el text de totes les pàgines.
    
    Args:
        pdf_file: objecte file-like retornat per st.file_uploader
    
    Returns:
        str: text concatenat de totes les pàgines del PDF
    """
    # Obrim el PDF a partir del contingut binari (stream) que Streamlit proporciona
    pdf_document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")

    text = ""  # Aquí acumularem el text extret

    # Iterem per totes les pàgines del PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Carreguem la pàgina
        text += page.get_text()                  # N'extraiem el text i l'afegim al total

    return text  # Retornem el text complet del PDF


def generate_work_from_text(text, num_tasks, question_types, generate_answers, retry=False):
    """
    Genera preguntes/activitats a partir del text extret del PDF, segons el nombre i el tipus seleccionats.

    Args:
        text (str): contingut de la unitat didàctica
        num_tasks (int): nombre de tasques/preguntes a generar
        question_types (list[str]): llista amb tipus seleccionats (p. ex. ["Tipus test", "Teòriques"])
        generate_answers (str): si ha de generar la resposta o no

    Returns:
        str: resposta del model (tasques generades)
    """
    # Convertim la llista d'opcions en una cadena readable
    tipus = ", ".join(question_types)

    if generate_answers == "Sí":
        answers_instruction = "Has de generar també les respostes de totes les preguntes."
    else:
        answers_instruction = "NO has de generar les respostes, només les preguntes."
    # Prompt que enviem al model: defineix rol, instruccions i el text font
    prompt = f"""
Ets un expert en educació secundària.

A continuació tens el contingut d’una unitat didàctica.
A partir d’aquest contingut, crea un conjunt de {num_tasks} activitats o preguntes.

🔹 Tipus de preguntes que has de generar:
SOLAMENT POTS GENERAR PREGUNTES DE {tipus}

🔹 Instruccions específiques:
- Les preguntes han de ser adequades per a alumnes de secundària
- Han d’estar basades exclusivament en la informació del text
- Si hi ha preguntes tipus test, inclou 4 opcions
- Si hi ha preguntes pràctiques, planteja situacions o exercicis aplicats
- Si hi ha preguntes teòriques, demana explicacions clares i raonades
- {answers_instruction}

Text de la unitat didàctica:
{text}

Tasques i preguntes:
"""

    # Fem la crida al model i retornem el text generat
    response = chat_model.invoke(prompt)
    try:
        return response.content[0].get("text", "Sin respuesta")
    except Exception as e:
        # Si dona error una vegada, ho reintentem
        print(e)
        return generate_work_from_text(text, num_tasks, question_types, generate_answers, retry=True)

# ==========================
# INTERFÍCIE D'USUARI (STREAMLIT)
# ==========================

# Títol principal de l'app
st.title("📚 Generador de Treballs per a Estudiants a partir d'una Unitat Didàctica")

# Widget per pujar un PDF (només accepta .pdf)
uploaded_pdf = st.file_uploader(
    "Si us plau, puja un arxiu PDF amb una unitat didàctica",
    type=["pdf"]
)

# Selector del nombre de tasques/preguntes a generar
# (0 indica que el valor per defecte és el primer de la llista: 5)
num_tasks = st.selectbox(
    "Quantes tasques o preguntes vols generar?",
    [5, 10, 15],
    0
)

# Selector per a obtindre les respostes tambe
generate_answers = st.selectbox(
    "Vols que també es generin les respostes?",
    ["No", "Sí"],
    index=0
)

# Selector (multi) del tipus de preguntes:
# - multiselect permet triar més d'una opció
# - default indica quina opció ve marcada inicialment
question_types = st.multiselect(
    "Quin tipus de preguntes vols generar?",
    ["Tipus test", "Teòriques", "Pràctiques"],
    default=["Teòriques"]
)

# ==========================
# LÒGICA PRINCIPAL
# ==========================

# Si l'usuari ha pujat un PDF...
if uploaded_pdf:
    # Extraiem el text del PDF
    pdf_text = extract_text_from_pdf(uploaded_pdf)

    # Mostrem un fragment inicial per verificar que el PDF s'ha carregat correctament
    st.write("### Text extret de la unitat didàctica:")
    st.markdown(
        f"""
        <div style="
            font-size: 10px;
            line-height: 1.2;
            color: #555;
            background-color: #f7f7f7;
            padding: 10px;
            border-radius: 6px;
            max-height: 250px;
            overflow-y: auto;
            white-space: pre-wrap;
        ">
            {pdf_text[:150]}
        </div>
        """,
        unsafe_allow_html=True
    ) # Només mostrem els primers 1500 caràcters (per no saturar la UI)

    # Botó per demanar al model que generi les tasques/preguntes
    if st.button("Generar tasques i preguntes per als estudiants"):
        # Validació: l'usuari ha de seleccionar almenys un tipus de pregunta
        if not question_types:
            st.warning("Selecciona almenys un tipus de pregunta.")
        else:
            # Spinner mentre s'està generant el contingut (millora l'experiència d'usuari)
            with st.spinner("Generant tasques..."):
                # Generem el contingut cridant al model
                st.session_state.work = ""
                st.session_state.work  = generate_work_from_text(
                    pdf_text,
                    num_tasks,
                    question_types,
                    generate_answers
                )
                # Mostrem el resultat a la pantalla
                st.write("### Tasques i preguntes generades:")
                st.write(st.session_state.work)

    # Botó per exportar les tasques a un fitxer de text
    # IMPORTANT: aquest botó només funcionarà si "work" existeix (si abans s'ha generat)
    if st.button("Exportar tasques a un fitxer de text"):
        # Comprovem si 'work' existeix a l'espai local (és una manera simple, però millor usar st.session_state)
        if st.session_state.work != "":
            st.download_button(
                label="Descarregar fitxer de tasques",  # Text del botó de descàrrega
                data=st.session_state.work or "",                              # Contingut que es descarregarà
                file_name="tasques_estudiants.txt",     # Nom del fitxer
                mime="text/plain"                       # Tipus MIME
            )
        else:
            # Si encara no s'ha generat res, avisem l'usuari
            st.warning("Primer has de generar les tasques abans d'exportar-les.")
else:
    # Si no s'ha pujat cap PDF, mostrem un missatge d'instrucció
    st.write("Si us plau, puja un arxiu PDF amb la unitat didàctica per començar.")
