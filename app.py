import streamlit as st
import pandas as pd
from utils.data_processing import load_and_preprocess_data, get_department_data
from tabs.dashboard import render_dashboard
from tabs.ai_insights import render_ai_insights
from tabs.outliers import render_outliers
from tabs.leaderboard import render_leaderboard
from tabs.data_assistant import render_data_assistant

# Page Setup
st.set_page_config(
    page_title="Edu-Tech Student Performance Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal CSS for Edu-Tech vibe
st.markdown("""
    <style>
    .stMetric {
        background-color: rgba(240, 242, 246, 0.5);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    div[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #dee2e6;
    }
    </style>
""", unsafe_allow_html=True)

# Authentication state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["department"] = None

# Sidebar Authentication
st.sidebar.title("🔐 Educator Login")

# Mock database of users
USERS = {
    "Data Science": "ds123",
    "CSE": "cse123",
    "AIML": "aiml123",
    "IT": "it123"
}

if not st.session_state["logged_in"]:
    st.sidebar.write("Please log in to access your department data.")
    st.sidebar.caption("Passwords are <dept_code>123 (e.g. ds123)")
    username = st.sidebar.selectbox("Department", options=list(USERS.keys()))
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        if password == USERS.get(username):
            st.session_state["logged_in"] = True
            st.session_state["department"] = username
            st.rerun()
        else:
            st.sidebar.error("Incorrect password.")
            
else:
    st.sidebar.success(f"Logged in as {st.session_state['department']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["department"] = None
        st.rerun()

# Main Application logic
if st.session_state["logged_in"]:
    # Load dataset
    filepath = "student_performance_analysis.csv"
    full_df = load_and_preprocess_data(filepath)
    
    if full_df.empty:
        st.warning("Data could not be loaded. Please ensure the CSV file is present.")
    else:
        # Filter for the logged in department automatically
        dept_df = get_department_data(full_df, st.session_state["department"])
        
        # Tabs Layout
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", 
            "🧠 AI Insights", 
            "⚠️ Outliers", 
            "🏆 Leaderboard", 
            "🤖 Data Assistant"
        ])
        
        with tab1:
            render_dashboard(dept_df)
            
        with tab2:
            render_ai_insights(dept_df)
            
        with tab3:
            render_outliers(dept_df)
            
        with tab4:
            # The leaderboard is globally accessible by design
            render_leaderboard(full_df)
            
        with tab5:
            render_data_assistant(dept_df)
else:
    st.title("🎓 Student Performance Analyzer")
    st.markdown("### Welcome!")
    st.write("This robust Streamlit web application allows educators to seamlessly track, analyze, and gain AI-powered insights into student performance.")
    st.info("👈 Please use the sidebar to log in and select your department.")
