import streamlit as st
from openai import OpenAI
import os
import tempfile
from PyPDF2 import PdfReader
from docx import Document
from pydub import AudioSegment
import whisper
import base64
from datetime import datetime

# ====== 🔧 CONFIGURATION ======
THEME = "dark"  # or "light"
MAX_TOKENS = 4096  # Adjust based on model limits

# ====== 🎨 THEME & STYLING ======
def apply_theme(theme):
    if theme == "dark":
        st.markdown("""
        <style>
            :root { --bg: #0f0f15; --card: #1a1a25; --text: #e0e0e0; }
            [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
            .stTextArea textarea { background: #252525 !important; color: white !important; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            :root { --bg: #f5f5f5; --card: #ffffff; --text: #333333; }
            [data-testid="stAppViewContainer"] { background: var(--bg); color: var(--text); }
        </style>
        """, unsafe_allow_html=True)

# ====== 🤖 AI FUNCTIONS ======
@st.cache_resource
def init_client():
    return OpenAI(api_key=st.secrets["openai"]["api_key"])

def summarize(text, style="concise", language="en"):
    prompt = f"""
    Create a {style} summary in {language}:
    - Key facts only
    - { "Bullet points" if style == "technical" else "Paragraph format" }
    - Max 3 sentences if "concise"
    
    Text: {text}
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=MAX_TOKENS
    )
    return response.choices[0].message.content

# ====== 📂 FILE PROCESSING ======
def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return " ".join([para.text for para in doc.paragraphs])
    elif file.type.startswith("audio/"):
        audio = AudioSegment.from_file(file)
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            audio.export(tmp.name, format="wav")
            model = whisper.load_model("base")
            return model.transcribe(tmp.name)["text"]
    return None

# ====== 🖥️ UI LAYOUT ======
apply_theme(THEME)
client = init_client()

st.title("🚀 Ultimate Summarizer Pro")
st.sidebar.header("Settings")

# Input Options
input_method = st.radio("Input Method:", ["Text", "File Upload"], key="input_method")
text = ""
if input_method == "Text":
    text = st.text_area("Paste text here:", height=200)
else:
    file = st.file_uploader("Upload PDF/DOCX/Audio", type=["pdf", "docx", "mp3", "wav"])
    if file:
        text = extract_text(file)

# Customization
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Style", ["Concise", "Technical", "Detailed"], key="style")
with col2:
    language = st.selectbox("Language", ["en", "ru", "es", "fr", "de"], key="lang")

# Processing
if st.button("✨ Generate Summary", type="primary"):
    if text:
        with st.spinner("Processing..."):
            summary = summarize(text, style.lower(), language)
            
            # Save to history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "input": text[:100] + "...",
                "summary": summary
            })
            
            # Display
            st.subheader("📝 Summary")
            st.write(summary)
            
            # Export
            st.download_button("📥 Download", summary, file_name="summary.txt")
    else:
        st.warning("Please provide input!")

# History Panel
if "history" in st.session_state and st.session_state.history:
    st.sidebar.subheader("History")
    for i, item in enumerate(st.session_state.history):
        with st.sidebar.expander(f"{item['date']}: {item['input']}"):
            st.write(item["summary"])
            if st.button(f"❌ Delete #{i+1}", key=f"del_{i}"):
                del st.session_state.history[i]
                st.rerun()
