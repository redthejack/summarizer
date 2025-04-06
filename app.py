import streamlit as st
from openai import OpenAI
import PyPDF2
import docx
import pytesseract
from PIL import Image
import tempfile
import datetime
import base64
import sqlite3
import hashlib

# ====== 🗃️ DATABASE SETUP ======
conn = sqlite3.connect('academic_users.db', check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE,
    plan TEXT DEFAULT 'free',
    signup_date TEXT,
    last_login TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    content TEXT,
    summary TEXT,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')
conn.commit()

# ====== 🎓 ACADEMIC PRESETS ======
ACADEMIC_MODES = {
    "Lecture Notes": {
        "prompt": "Convert these lecture notes into: 1) Key concepts 2) Definitions 3) Examples 4) Potential exam questions",
        "icon": "📝"
    },
    "Research Paper": {
        "prompt": "Extract: 1) Research question 2) Methodology 3) Findings 4) Limitations 5) Future work",
        "icon": "🔬"
    },
    "Textbook Chapter": {
        "prompt": "Summarize with: 1) Chapter objectives 2) Key theorems (boxed) 3) Important diagrams 4) Practice problems",
        "icon": "📚"
    },
    "Case Study": {
        "prompt": "Analyze: 1) Core problem 2) Stakeholders 3) Solutions proposed 4) Best alternative",
        "icon": "💼"
    }
}

CITATION_STYLES = {
    "APA": "American Psychological Association",
    "MLA": "Modern Language Association",
    "Chicago": "Chicago Manual of Style",
    "IEEE": "Institute of Electrical and Electronics Engineers"
}

# ====== 🔐 AUTHENTICATION ======
def create_user(username, password, email):
    try:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        c.execute('''
            INSERT INTO users (username, password, email, signup_date)
            VALUES (?, ?, ?, ?)
        ''', (username, hashed_pw, email, datetime.datetime.now().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute('''
        SELECT id, username, plan FROM users WHERE username=? AND password=?
    ''', (username, hashed_pw))
    return c.fetchone()

# ====== 🤖 AI PROCESSING ======
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_academic_summary(text, mode, citation_style):
    prompt = f'''
    As a university professor, create a {mode} summary:
    
    {ACADEMIC_MODES[mode]['prompt']}
    
    Additional Requirements:
    - Use {citation_style} citation style
    - Bold key terms (**term**)
    - Box important formulas [\boxed{{x = y}}]
    - Add "Discussion Questions" section
    - Include "Further Reading" suggestions
    
    Text: {text}
    '''
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

def generate_flashcards(summary):
    prompt = f'''
    Convert this summary into 10 Anki-style flashcards:
    - Front: Question/term
    - Back: Definition/answer
    - Format: Q: ... | A: ...
    
    Summary: {summary}
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

# ====== 📂 FILE PROCESSING ======
def process_file(file):
    if file.type == "application/pdf":
        text = ""
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif file.type.startswith("image/"):
        img = Image.open(file)
        return pytesseract.image_to_string(img)
    
    return file.read().decode("utf-8")

# ====== 🖥️ STREAMLIT UI ======
st.set_page_config(page_title="Academic AI Suite", layout="wide", page_icon="🎓")

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "login"

# ====== 🚀 PAGES ======
def login_page():
    st.title("University Login")
    
    with st.form("login_form"):
        username = st.text_input("Student/Faculty ID")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            user = verify_user(username, password)
            if user:
                st.session_state.user = {
                    "id": user[0],
                    "username": user[1],
                    "plan": user[2]
                }
                st.session_state.page = "summarizer"
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

def signup_page():
    st.title("Academic Account Registration")
    
    with st.form("signup_form"):
        username = st.text_input("Create Username", help="Use your university email")
        email = st.text_input("Institutional Email")
        password = st.text_input("Create Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        
        if st.form_submit_button("Register"):
            if password != confirm:
                st.error("Passwords don't match!")
            elif len(password) < 8:
                st.error("Password must be 8+ characters")
            elif create_user(username, password, email):
                st.success("Account created! Please login")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username/email already exists")
    
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

def summarizer_page():
    # Header
    st.title(f"{ACADEMIC_MODES[st.session_state.mode]['icon']} Academic AI Suite")
    st.caption(f"Logged in as {st.session_state.user['username']} | Plan: {st.session_state.user['plan'].capitalize()}")
    
    # Main Columns
    input_col, config_col = st.columns([3, 1])
    
    with config_col:
        st.subheader("Academic Settings")
        st.session_state.mode = st.selectbox(
            "Document Type",
            list(ACADEMIC_MODES.keys()),
            format_func=lambda x: f"{ACADEMIC_MODES[x]['icon']} {x}"
        )
        st.session_state.citation = st.selectbox(
            "Citation Style",
            list(CITATION_STYLES.keys()),
            format_func=lambda x: f"{x} ({CITATION_STYLES[x]})"
        )
        
        st.divider()
        st.checkbox("Generate Flashcards", True, key="gen_flashcards")
        st.checkbox("Create Quiz Questions", False, key="gen_quiz")

        if 'user' not in st.session_state:
           st.session_state.user = None  # Proper initialization
        
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
    
    with input_col:
        # Input Methods
        input_method = st.radio(
            "Input Method",
            ["Text", "File Upload", "Scan/Photo"],
            horizontal=True
        )
        
        text = ""
        if input_method == "Text":
            text = st.text_area("Paste academic content:", height=300)
        else:
            file = st.file_uploader(
                "Upload Document",
                type=["pdf", "docx", "txt", "png", "jpg", "jpeg"],
                accept_multiple_files=False
            )
            if file:
                with st.spinner("Processing document..."):
                    text = process_file(file)
                    st.success("File processed!")
        
        # Processing
        if st.button("Generate Academic Summary"):
            if text:
                with st.spinner("Creating enhanced summary..."):
                    # Save original
                    title = f"{st.session_state.mode} - {datetime.datetime.now().strftime('%Y-%m-%d')}"
                    summary = generate_academic_summary(
                        text,
                        st.session_state.mode,
                        st.session_state.citation
                    )
                    
                    # Save to database
                    c.execute('''
                        INSERT INTO summaries (user_id, title, content, summary, created_at)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        st.session_state.user['id'],
                        title,
                        text[:500] + ("..." if len(text) > 500 else ""),
                        summary,
                        datetime.datetime.now().isoformat()
                    ))
                    conn.commit()
                    
                    # Display
                    st.subheader("Academic Summary")
                    st.markdown(summary)
                    
                    # Study Tools
                    if st.session_state.gen_flashcards:
                        st.divider()
                        st.subheader("📚 Flashcards")
                        flashcards = generate_flashcards(summary)
                        st.download_button(
                            "Download Flashcards",
                            flashcards,
                            file_name=f"flashcards_{title}.txt"
                        )
                        st.text_area("Flashcard Preview", flashcards, height=200)
                    
                    # Export
                    st.divider()
                    export_col1, export_col2 = st.columns(2)
                    with export_col1:
                        st.download_button(
                            "Download Summary",
                            summary,
                            file_name=f"summary_{title}.md"
                        )
                    with export_col2:
                        st.download_button(
                            "Save to References",
                            f"# {title}\n\n{summary}",
                            file_name=f"references_{title}.md"
                        )
            else:
                st.warning("Please input content first")

# ====== 🚀 APP FLOW ======
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "signup":
    signup_page()
else:
    if 'mode' not in st.session_state:
        st.session_state.mode = "Lecture Notes"
    if 'citation' not in st.session_state:
        st.session_state.citation = "APA"
    summarizer_page()

# ====== 🏁 FOOTER ======
st.divider()
st.caption("""
🎓 **Academic AI Suite** | Supports all disciplines | 
[Terms] | [Privacy] | v2.5
""")
