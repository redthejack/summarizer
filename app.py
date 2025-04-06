import streamlit as st
from openai import OpenAI
import os
import tempfile
from datetime import datetime

# ====== 🛠️ INITIALIZATION ======
@st.cache_resource
def init_client():
    try:
        # Check for API key in secrets (Streamlit Cloud) or environment (local)
        api_key = (
            st.secrets["openai"]["api_key"]
            if "openai" in st.secrets
            else os.getenv("OPENAI_API_KEY")
        )
        
        if not api_key:
            st.error("🔑 API key not found in secrets or environment variables")
            return None
            
        client = OpenAI(api_key=api_key)
        
        # Quick connection test
        client.models.list()
        return client
        
    except Exception as e:
        st.error(f"🚨 Failed to initialize OpenAI: {str(e)}")
        return None

client = init_client()
if not client:
    st.stop()

# ====== 🎨 THEME ======
st.markdown("""
<style>
    :root {
        --bg: #0f0f15;
        --card: #1a1a25;
        --text: #e0e0e0;
        --primary: #8a63f8;
    }
    [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--text);
    }
    .stTextArea textarea {
        background: #252525 !important;
        color: white !important;
        border-radius: 10px !important;
    }
    .stButton>button {
        background: var(--primary) !important;
        color: white !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== 🤖 CORE FUNCTIONS ======
def summarize(text, style="concise", language="auto"):
    prompt = f"""
    Create a {style} summary in {language if language != "auto" else "the text's original language"}:
    - Key facts only
    - {"Bullet points" if style == "technical" else "Paragraph format"}
    - Preserve important numbers/dates
    
    Text: {text}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ Summarization failed: {str(e)}")
        return None

# ====== 🖥️ UI ======
st.title("✨ Ultimate AI Summarizer")
st.write("Paste text and get instant summaries")

# Input
tab1, tab2 = st.tabs(["📝 Text", "📂 File"])
input_text = ""

with tab1:
    input_text = st.text_area("Paste content here:", height=200)

with tab2:
    uploaded_file = st.file_uploader("Upload TXT/PDF/DOCX", type=["txt", "pdf", "docx"])
    if uploaded_file:
        if uploaded_file.type == "text/plain":
            input_text = str(uploaded_file.read(), "utf-8")
        else:
            st.warning("File processing requires PyPDF2/python-docx")

# Options
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox("Style", ["concise", "technical", "detailed"])
with col2:
    language = st.selectbox("Language", ["auto", "English", "Russian", "Spanish"])

# Processing
if st.button("Generate Summary"):
    if input_text:
        with st.spinner("🔍 Analyzing..."):
            summary = summarize(input_text, style, language)
            
            if summary:
                st.subheader("📝 Summary")
                st.write(summary)
                
                # Download
                st.download_button(
                    "Download Summary",
                    summary,
                    file_name=f"summary_{datetime.now().strftime('%Y%m%d')}.txt"
                )
    else:
        st.warning("Please enter some text first")

# Footer
st.divider()
st.caption("⚡ Powered by OpenAI GPT-3.5 Turbo")
