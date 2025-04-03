import streamlit as st
import openai

# Set OpenAI API key
openai.api_key = "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"  # Replace with your OpenAI key

# Website title
st.title("🤖 AI Summarizer")
st.write("Paste any text, and I'll summarize it for you!")

# Input box
input_text = st.text_area("Enter your text here:", height=200)

# Summarize button
if st.button("Summarize"):
    if input_text:
        # Call OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI that summarizes text concisely."},
                {"role": "user", "content": f"Summarize this in 3 sentences or less:\n\n{input_text}"}
            ]
        )
        summary = response.choices[0].message['content']
        st.success("✅ Summary:")
        st.write(summary)
    else:
        st.warning("⚠️ Please enter some text first!")
