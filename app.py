import streamlit as st
from PIL import Image  # For logo (optional)

# ======== 🎀 Custom Styling ========
st.set_page_config(
    page_title="AI Summarizer Pro",
    page_icon="✂️",
    layout="centered"
)

# Inject custom CSS
st.markdown("""
<style>
    .stTextArea [data-baseweb=textarea] {
        background-color: #f9f9f9;
        border-radius: 12px;
    }
    .stButton button {
        background: linear-gradient(90deg, #6e48aa 0%, #9d50bb 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 12px;
    }
    .stButton button:hover {
        opacity: 0.9;
    }
    .summary-box {
        background: #f0f2f6;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ======== 🏗️ App Layout ========
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("✂️ AI Summarizer Pro")
with col2:
    st.write("")  # Spacer
    st.markdown("`v1.0 | Demo Mode`")

st.subheader("Paste any text, article, or lecture notes")

# ======== 📝 Input Area ========
input_text = st.text_area(
    "**Your text:**",
    height=250,
    placeholder="Paste content here... (Demo mode shows truncated text)"
)

# ======== ✨ Generate Button ========
if st.button("✨ Generate Summary", type="primary"):
    if input_text:
        with st.spinner("Processing..."):
            # Mock summary (replace with OpenAI API later)
            mock_summary = f"**Demo Summary:**\n\n{input_text[:150]}... [truncated in demo mode]"
            
            # Fancy result box
            st.markdown(f"""
            <div class="summary-box">
                📝 <b>Original length:</b> {len(input_text)} characters<br>
                ✨ <b>Summary length:</b> {min(150, len(input_text))} characters<br><br>
                {mock_summary}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please enter text first!")

# ======== 📊 Demo Stats ========
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg. Summary Time", "2.4s")
with col2:
    st.metric("Accuracy", "92%", "-8% in demo")
with col3:
    st.metric("Chars Reduced", "75%")

# ======== ℹ️ How It Works ========
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. Paste text in the box above  
    2. Click **Generate Summary**  
    3. Get instant condensed version  
    *Real AI integration coming soon!*
    """)

st.markdown("""
<style>
    @media (prefers-color-scheme: dark) {
        .summary-box {
            background: #1e1e1e;
        }
    }
</style>
""", unsafe_allow_html=True)

# ======== 📱 Mobile-Friendly Footer ========
st.divider()
st.caption("© 2024 AI Summarizer Pro | [Contact Support](mailto:support@example.com)")
