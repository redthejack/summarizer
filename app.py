import streamlit as st
from openai import OpenAI
import os

# ====== 🌑 DARK MODE CONFIG ======
st.markdown("""
<style>
    :root {
        --bg: #0e1117;
        --card-bg: #1e1e1e;
        --text: #f0f0f0;
        --primary: #8a63f8;
        --secondary: #6e48aa;
        --accent: #4776E6;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
    }
    
    .stTextArea textarea {
        background-color: #252525 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
    }
    
    /* Dark mode buttons */
    .stButton>button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(138, 99, 248, 0.3) !important;
    }
    
    /* Cards */
    .summary-card {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 4px solid var(--accent);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Headers */
    .stMarkdown h1 {
        color: var(--primary);
        font-weight: 700;
    }
    
    /* Tabs */
    .stTabs [role="tablist"] {
        background: #252525 !important;
    }
    
    /* Select boxes */
    .stSelectbox div {
        background: #252525 !important;
    }
</style>
""", unsafe_allow_html=True)

# ====== 🤖 AI FUNCTIONALITY ======
@st.cache_resource
def init_client():
    return OpenAI(api_key=st.secrets["openai"]["api_key"])

# ====== 🖥️ APP LAYOUT ======
st.title("🌙 Dark Mode Summarizer")
st.write("Paste text for an AI-powered summary in sleek dark theme")

input_text = st.text_area("Your text:", height=250)

if st.button("Generate Summary"):
    if input_text:
        with st.spinner("Analyzing..."):
            try:
                client = init_client()
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{
                        "role": "user", 
                        "content": f"Summarize this in 3 sentences:\n\n{input_text}"
                    }]
                )
                summary = response.choices[0].message.content
                
                st.markdown(f"""
                <div class="summary-card">
                    <h3>✨ Summary</h3>
                    <p>{summary}</p>
                    <div style="color: #aaa; font-size: 0.8rem; margin-top: 1rem;">
                        Reduced from {len(input_text)} to {len(summary)} chars
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter text first")

# ====== 🏁 FOOTER ======
st.divider()
st.caption("🔮 Dark Mode AI Summarizer | v1.0")
