import streamlit as st
import pandas as pd
from utils.data_processing import load_and_preprocess_data, get_department_data
from utils.database import init_db, replace_department_data
from tabs.dashboard import render_dashboard
from tabs.ai_insights import render_ai_insights
from tabs.outliers import render_outliers
from tabs.leaderboard import render_leaderboard
from tabs.data_assistant import render_data_assistant

# Initialize Database on Startup
init_db()

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
    # Load dataset from SQLite
    full_df = load_and_preprocess_data()
    
    if full_df.empty:
        st.warning("Data could not be loaded. Please check the database.")
    else:
        # Filter for the logged in department automatically
        dept_df = get_department_data(full_df, st.session_state["department"])
        
        # ---- IMPORT / MANAGE DATA SECION ----
        with st.expander("📥 Manage Department Data"):
            manage_tab1, manage_tab2 = st.tabs(["📝 Edit Current Data", "📤 Upload New CSV"])
            
            with manage_tab1:
                st.write("Modify existing records or add new students for your department here:")
                
                # We show only editable columns to prevent breaking calculated fields if any.
                # Preprocessed fields like avg_cgpa shouldn't be edited directly.
                # For simplicity, we can let them edit the original df columns.
                editable_df = st.data_editor(
                    dept_df.drop(columns=['avg_cgpa', 'performance_trend', 'sem1_cgpa_display', 'sem2_cgpa_display', 'sem3_cgpa_display'], errors='ignore'), 
                    num_rows="dynamic", 
                    use_container_width=True,
                    key="data_editor"
                )
                
                if st.button("Save Changes", type="primary"):
                    # user's edits are stored in editable_df
                    replace_department_data(st.session_state["department"], editable_df)
                    st.success("Data successfully updated!")
                    st.cache_data.clear()
                    st.rerun()

            with manage_tab2:
                st.write("Upload a entirely new CSV file to replace your current department's data:")
                uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
                
                if uploaded_file is not None:
                    if st.button("Replace Department Data", type="primary"):
                        try:
                            # Read uploaded file
                            new_data_df = pd.read_csv(uploaded_file)
                            # Ensure columns match (rudimentary check)
                            if 'student_id' not in new_data_df.columns:
                                st.error("Invalid CSV format. Missing 'student_id' column.")
                            else:
                                replace_department_data(st.session_state["department"], new_data_df)
                                st.success("Department data successfully replaced!")
                                st.cache_data.clear()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error processing file: {e}")
        # ---- END IMPORT / MANAGE DATA SECTION ----
        
        st.divider()

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
