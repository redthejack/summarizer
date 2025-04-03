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
