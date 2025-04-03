import streamlit as st
from openai import OpenAI  # New import style

# Initialize the client with your API key
client = OpenAI(api_key="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")  # 🔑 Replace with your actual key

st.title("🤖 AI Summarizer")
st.write("Paste any text and get an instant summary!")

input_text = st.text_area("Enter text to summarize:", height=200)

if st.button("Summarize"):
    if input_text:
        with st.spinner("Generating summary..."):
            try:
                # New API syntax
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant that summarizes text concisely."},
                        {"role": "user", "content": f"Summarize this in 3 sentences or less:\n\n{input_text}"}
                    ]
                )
                summary = response.choices[0].message.content
                st.success("✅ Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter some text first!")
