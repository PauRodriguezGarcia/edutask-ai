# 📚 Generador de Tasques per a Estudiants a partir d’Unitats Didàctiques (PDF)

Aquesta aplicació permet pujar una unitat didàctica en format PDF i generar automàticament preguntes, activitats i tasques per a alumnes de secundària utilitzant intel·ligència artificial.

Està pensada per a docents que volen crear material educatiu de manera ràpida i personalitzada.

---

## 🚀 Funcionalitats

- Pujada d’arxius PDF amb unitats didàctiques.
- Extracció automàtica del text del PDF.
- Generació de tasques i preguntes educatives mitjançant IA (Google Gemini).
- Selecció del nombre de tasques (5, 10 o 15).
- Exportació del resultat en un fitxer `.txt`.

---

## 🛠️ Tecnologies utilitzades

- **Python 3.10+**
- **Streamlit** – interfície web
- **PyMuPDF (pymupdf)** – lectura de PDFs
- **LangChain + Google Gemini API**

---

## 📦 Instal·lació

Clona el repositori i instal·la les dependències:

```bash
git clone https://github.com/PauRodriguezGarcia/edutask-ai.git
cd edutask-ai
pip install -r requirements.txt
```

### Dependències principals

```bash
pip install streamlit pymupdf pandas langchain-google-genai
```

---

## 🔐 Configuració de l’API de Google Gemini

Afegeix la teva clau d’API com a variable d’entorn:

**Windows (PowerShell):**
```powershell
setx GOOGLE_API_KEY "LA_TEVA_API_KEY"
```

**Linux / MacOS:**
```bash
export GOOGLE_API_KEY="LA_TEVA_API_KEY"
```

---

## ▶️ Execució de l’aplicació

```bash
streamlit run app.py
```

S’obrirà automàticament al navegador:  
`http://localhost:8501`

---

## 🧪 Exemple d’ús

1. Puja un PDF amb una unitat didàctica.
2. Tria quantes tasques vols generar.
3. Prem **"Generar tasques i preguntes per als estudiants"**.
4. Descarrega el fitxer amb les activitats.

---

## 📁 Estructura del projecte

```
.
├── app.py
├── README.md
├── requirements.txt
```

---

## ⚠️ Notes importants

- El PDF ha de contenir **text seleccionable** (no només imatges).
- La qualitat de les preguntes depèn de la qualitat del contingut del PDF.
- Evita PDFs molt llargs per no saturar el model.

---

## 👨‍🏫 Pensat per a

- Professors de secundària  
- Centres educatius  
- Projectes d’innovació educativa  

---

✨ Desenvolupat per facilitar la creació de material educatiu amb IA.
