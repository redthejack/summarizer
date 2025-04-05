import streamlit as st
from openai import OpenAI
import os
from PIL import Image  # For logo

# ========== 🔐 Initialize OpenAI Client ==========
@st.cache_resource
def init_client():
    try:
        client = OpenAI(api_key=st.secrets["openai"]["api_key"])
        # Verify connection
        client.models.list()
        return client
    except Exception as e:
        st.error(f"🔴 API Connection Error: {str(e)}")
        return None

client = init_client()

# ====== 1. GLOBAL STYLE ======
st.markdown("""
<style>
    :root {
        --primary: #6e48aa;
        --secondary: #9d50bb;
        --accent: #4776E6;
        --light: #f8f9fa;
        --dark: #212529;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    .stTextArea textarea {
        background: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Gradient buttons */
    .stButton>button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(110, 72, 170, 0.3) !important;
    }
    
    /* Cards */
    .summary-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid var(--accent);
        margin: 1rem 0;
    }
    
    /* Headers */
    .stMarkdown h1 {
        color: var(--primary);
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stMarkdown h2 {
        color: var(--secondary);
        border-bottom: 2px solid #eee;
        padding-bottom: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# ====== 2. SAMPLE UI ======
st.title("✨ Summarizer Pro")
st.header("Generate Summary", divider="rainbow")

input_text = st.text_area("Paste your content here:", height=250)

if st.button("Magic Summarize 🎩"):
    with st.expander("🔍 See Summary", expanded=True):
        st.markdown("""
        <div class="summary-card">
            <h3>This is a color-enhanced summary card!</h3>
            <p>Notice the smooth gradients, elegant shadows, and cohesive color scheme.</p>
        </div>
        """, unsafe_allow_html=True)

# ====== 3. FOOTER ======
st.divider()
st.markdown("""
<span style="color: var(--secondary); font-size: 0.9rem">
    🔒 <strong>Privacy First</strong> | 🌈 <strong>Color-Optimized</strong> | 
    🚀 <strong>Powered by AI</strong>
</span>
""", unsafe_allow_html=True)
