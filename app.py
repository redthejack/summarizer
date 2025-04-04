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

# ========== 🎨 Custom Styling ==========
st.set_page_config(
    page_title="AI Summarizer Pro",
    page_icon="✂️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    .stTextArea textarea {
        background: rgba(255,255,255,0.9) !important;
        border-radius: 12px !important;
    }
    .summary-card {
        background: rgba(255,255,255,0.95);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6e48aa 0%, #9d50bb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
    }
    .stMarkdown h1 {
        color: #4a2c82;
    }
</style>
""", unsafe_allow_html=True)

# ========== 🖼️ Header Section ==========
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("✂️ AI Summarizer Pro")
    st.caption("Transform long texts into concise summaries with GPT-4")
with col2:
    # Add your logo (replace with actual image)
    st.image("https://via.placeholder.com/120x40?text=Your+Logo", width=120)

# ========== 📝 Main Input Area ==========
input_text = st.text_area(
    "**Paste your text here:**",
    height=250,
    placeholder="Paste article, report, or lecture notes...",
    help="Supports 10+ languages automatically"
)

# ========== ⚙️ Settings ==========
with st.expander("⚙️ Advanced Options"):
    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox(
            "Summary Length",
            ("Short (1-2 sentences)", "Medium (3-5 sentences)", "Detailed (5+ sentences)")
        )
    with col2:
        style = st.selectbox(
            "Style",
            ("Academic", "Casual", "Bullet Points", "Executive Summary")
        )

# ========== 🚀 Generate Button ==========
if st.button("✨ Generate Summary", type="primary"):
    if not input_text:
        st.warning("Please enter text to summarize")
    elif not client:
        st.error("API connection failed - check your key")
    else:
        with st.spinner("🧠 Analyzing content..."):
            try:
                # Dynamic prompt based on user selection
                length_map = {
                    "Short": "1-2 concise sentences",
                    "Medium": "3-5 informative sentences",
                    "Detailed": "5+ comprehensive sentences"
                }
                
                prompt = f"""
                Create a {length_map[length.split(' ')[0]]} summary in {style} style:
                - Preserve key facts and numbers
                - Maintain original meaning
                - Output in the same language as the text
                
                Text: {input_text}
                """
                
                response = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                
                summary = response.choices[0].message.content
                
                # Display results
                st.markdown(f"""
                <div class="summary-card">
                    <h3>📝 Summary ({length.split(' ')[0]}, {style})</h3>
                    <p>{summary}</p>
                    <div style="margin-top: 1rem; font-size: 0.8rem; color: #666;">
                        Original: {len(input_text)} chars → Summary: {len(summary)} chars 
                        (Reduced by {round((1-len(summary)/len(input_text))*100}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Generation failed: {str(e)}")

# ========== 📱 Mobile-Friendly Footer ==========
st.divider()
st.caption("""
🔒 Secure processing | 🌍 15+ languages supported | 
[Terms](https://example.com) | [Privacy](https://example.com)
""")
