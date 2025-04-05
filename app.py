import streamlit as st
from openai import OpenAI
import time

# ====== 🖤 ULTIMATE DARK MODE ======
st.markdown("""
<style>
    :root {
        --bg: #0f0f15;
        --card: #1a1a25;
        --text: #e0e0e0;
        --primary: #9d7aff;
        --secondary: #7a5eff;
        --accent: #6a8eff;
        --neon: 0 0 10px rgba(157, 122, 255, 0.5);
    }
    
    /* Main container */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, #0a0a12 0%, var(--bg) 100%);
        color: var(--text);
    }
    
    /* Text input - Matrix style */
    .stTextArea textarea {
        background: rgba(30, 30, 45, 0.8) !important;
        color: #f0f0f0 !important;
        border: 1px solid #33334d !important;
        border-radius: 8px !important;
        font-family: monospace;
    }
    
    /* Cyberpunk button */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%) !important;
        color: black !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: var(--neon);
        transition: all 0.3s !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(157, 122, 255, 0.8);
    }
    
    /* Glowing card */
    .cyber-card {
        background: var(--card);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 3px solid var(--primary);
        box-shadow: var(--neon);
        margin: 1rem 0;
        transition: transform 0.3s;
    }
    
    .cyber-card:hover {
        transform: translateY(-3px);
    }
    
    /* Special title effect */
    .neon-title {
        color: var(--primary);
        text-shadow: 0 0 8px rgba(157, 122, 255, 0.7);
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# ====== 🚀 APP CODE ======
st.markdown('<h1 class="neon-title">NEO SUMMARIZER</h1>', unsafe_allow_html=True)
st.caption("AI-powered text condensation in cyber-dark theme")

with st.expander("⚙️ SETTINGS", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("OUTPUT STYLE", 
                           ["Technical", "Concise", "Bullet Points"])
    with col2:
        level = st.select_slider("DETAIL LEVEL", 
                               ["Low", "Medium", "High"])

input_text = st.text_area("INPUT TEXT:", height=250, 
                         placeholder="Enter text to summarize...")

if st.button("⚡ PROCESS TEXT"):
    if not input_text:
        st.warning("Input field empty!")
    else:
        with st.spinner("DECRYPTING CONTENT..."):
            # Simulate high-tech processing
            progress_bar = st.progress(0)
            for percent in range(100):
                time.sleep(0.02)
                progress_bar.progress(percent + 1)
            
            # Mock AI response (replace with real API call)
            mock_summary = f"""🔍 {style.upper()} SUMMARY ({level} DETAIL):
            
            - Core concept extracted from {len(input_text)} characters
            - Key points condensed using quantum algorithms
            - Ready for neural assimilation"""
            
            st.markdown(f"""
            <div class="cyber-card">
                <h3>📡 ANALYSIS COMPLETE</h3>
                <p>{mock_summary}</p>
                <div style="color: var(--accent); margin-top: 1rem;">
                    ⚙️ Compression: {len(input_text)} → {int(len(input_text)*0.3)} chars
                </div>
            </div>
            """, unsafe_allow_html=True)

# ====== 🕶️ CREDITS ======
st.divider()
st.caption("""
NEO SUMMARIZER v2.0 | [TERMS] | [PRIVACY] | 
""")
