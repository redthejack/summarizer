import streamlit as st
from openai import OpenAI
import sqlite3
import hashlib
import datetime
from datetime import datetime

# ====== 🗃️ DATABASE SETUP ======
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Create tables if they don't exist
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
    input_text TEXT,
    summary TEXT,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')
conn.commit()

# ====== 🔐 AUTH FUNCTIONS ======
def create_user(username, password, email):
    try:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        c.execute('INSERT INTO users (username, password, email, signup_date) VALUES (?, ?, ?, ?)',
                 (username, hashed_pw, email, datetime.datetime.now().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute('SELECT id, username, plan FROM users WHERE username=? AND password=?',
             (username, hashed_pw))
    return c.fetchone()

# ====== 💰 SUBSCRIPTION PLANS ======
PLANS = {
    "free": {
        "monthly_cost": 0,
        "max_summaries": 10,
        "model": "gpt-3.5-turbo"
    },
    "pro": {
        "monthly_cost": 9.99,
        "max_summaries": 100,
        "model": "gpt-4-turbo"
    },
    "enterprise": {
        "monthly_cost": 29.99,
        "max_summaries": 1000,
        "model": "gpt-4-turbo"
    }
}

# ====== 🤖 AI SETUP ======
@st.cache_resource
def init_client():
    return OpenAI(api_key=st.secrets["openai"]["api_key"])

client = init_client()

# ====== 🖥️ AUTH PAGES ======
def login_page():
    st.title("🔒 Login to Summarizer Pro")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            user = verify_user(username, password)
            if user:
                st.session_state.user = {
                    "id": user[0],
                    "username": user[1],
                    "plan": user[2]
                }
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    if st.button("Create Account"):
        st.session_state.page = "signup"
        st.rerun()

def signup_page():
    st.title("🚀 Create Account")
    
    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        plan = st.selectbox("Plan", list(PLANS.keys()), format_func=lambda x: f"{x.capitalize()} (${PLANS[x]['monthly_cost']}/mo)")
        
        submitted = st.form_submit_button("Sign Up")
        
        if submitted:
            if create_user(username, password, email):
                st.success("Account created! Please login")
                st.session_state.page = "login"
                st.rerun()
            else:
                st.error("Username/email already exists")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# ====== 📊 PROFILE PAGE ======
def profile_page():
    st.title(f"👤 {st.session_state.user['username']}'s Profile")
    
    # User stats
    c.execute('SELECT COUNT(*) FROM summaries WHERE user_id=?', (st.session_state.user['id'],))
    summary_count = c.fetchone()[0]
    
    with st.expander("📊 Usage Stats"):
        col1, col2 = st.columns(2)
        col1.metric("Current Plan", st.session_state.user['plan'].capitalize())
        col2.metric("Summaries This Month", f"{summary_count}/{PLANS[st.session_state.user['plan']]['max_summaries']}")
        
        st.progress(summary_count / PLANS[st.session_state.user['plan']]['max_summaries'])
    
    # Plan upgrade
    with st.expander("💎 Upgrade Plan"):
        current_plan = st.session_state.user['plan']
        for plan, details in PLANS.items():
            if plan != current_plan:
                if st.button(f"Upgrade to {plan.capitalize()} (${details['monthly_cost']}/mo)"):
                    c.execute('UPDATE users SET plan=? WHERE id=?', 
                             (plan, st.session_state.user['id']))
                    conn.commit()
                    st.session_state.user['plan'] = plan
                    st.success(f"Upgraded to {plan} plan!")
                    st.rerun()
    
    if st.button("Logout"):
        del st.session_state.user
        st.session_state.page = "login"
        st.rerun()

# ====== ✂️ MAIN APP ======
def summarizer_page():
    st.title("✂️ AI Summarizer Pro")
    st.write(f"Welcome back, {st.session_state.user['username']}!")
    
    # Check usage limits
    c.execute('SELECT COUNT(*) FROM summaries WHERE user_id=? AND created_at > date("now", "-30 days")',
             (st.session_state.user['id'],))
    monthly_usage = c.fetchone()[0]
    
    if monthly_usage >= PLANS[st.session_state.user['plan']]['max_summaries']:
        st.error("You've reached your monthly summary limit! Upgrade to continue.")
        return
    
    # Summarizer UI
    input_text = st.text_area("Enter text to summarize:", height=200)
    
    if st.button("Generate Summary"):
        with st.spinner("Creating summary..."):
            try:
                response = client.chat.completions.create(
                    model=PLANS[st.session_state.user['plan']]['model'],
                    messages=[{
                        "role": "user",
                        "content": f"Create a concise summary:\n\n{input_text}"
                    }]
                )
                summary = response.choices[0].message.content
                
                # Save to database
                c.execute('INSERT INTO summaries (user_id, input_text, summary, created_at) VALUES (?, ?, ?, ?)',
                         (st.session_state.user['id'], input_text, summary, datetime.datetime.now().isoformat()))
                conn.commit()
                
                st.subheader("Summary")
                st.write(summary)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ====== 🚀 APP FLOW ======
if 'page' not in st.session_state:
    st.session_state.page = "login"

if 'user' not in st.session_state:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
else:
    # Authenticated routes
    tab1, tab2 = st.tabs(["Summarizer", "Profile"])
    
    with tab1:
        summarizer_page()
    
    with tab2:
        profile_page()
