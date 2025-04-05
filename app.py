import streamlit as st
from openai import OpenAI

# ====== 🖤 INITIALIZE ONCE ======
if "client" not in st.session_state:
    st.session_state.client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# ====== 🤖 AI FUNCTION ======
def generate_summary(text, style, detail):
    prompt = f"""
    Create a {detail.lower()}-detail {style.lower()} summary in Russian:
    - Preserve key facts
    - Maintain historical accuracy
    - Output in bullet points
    
    Text: {text}
    """
    response = st.session_state.client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# ====== 🚀 APP LAYOUT ======
st.markdown('<h1 class="neon-title">NEO SUMMARIZER</h1>', unsafe_allow_html=True)

# Unique widget keys prevent duplication
with st.expander("⚙️ SETTINGS", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox(
            "OUTPUT STYLE", 
            ["Technical", "Concise", "Bullet Points"],
            key="style_select"  # Unique key
        )
    with col2:
        level = st.select_slider(
            "DETAIL LEVEL", 
            ["Low", "Medium", "High"],
            key="detail_slider"  # Unique key
        )

input_text = st.text_area(
    "INPUT TEXT:", 
    height=250, 
    key="text_input"  # Unique key
)

if st.button("⚡ PROCESS TEXT", key="process_btn"):
    if not input_text:
        st.warning("Input field empty!")
    else:
        with st.spinner("DECRYPTING CONTENT..."):
            try:
                summary = generate_summary(input_text, style, level)
                
                st.markdown(f"""
                <div class="cyber-card">
                    <h3>📡 ANALYSIS COMPLETE</h3>
                    <p>{summary}</p>
                    <div style="color: var(--accent); margin-top: 1rem;">
                        ⚙️ Compression: {len(input_text)} → {len(summary)} chars
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Quantum processor overload: {str(e)}")
