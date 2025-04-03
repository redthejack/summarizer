import streamlit as st
import openai

openai.api_key = "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"  # 🔑 Replace with your OpenAI key

st.title("🤖 AI Summarizer")
input_text = st.text_area("Paste text here:")
if st.button("Summarize"):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize this in 3 sentences:\n{input_text}"}]
    )
    st.write(response.choices[0].message['content'])
