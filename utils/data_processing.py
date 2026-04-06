import pandas as pd
import streamlit as st
import os
from utils.database import get_all_data

@st.cache_data
def load_and_preprocess_data() -> pd.DataFrame:
    """Loads and preprocesses the student performance dataset from database."""
    try:
        df = get_all_data()
    except Exception as e:
        st.error(f"Error loading database: {str(e)}")
        return pd.DataFrame()

    # Create original cgpa columns to preserve 'FAIL' string for display
    df['sem1_cgpa_display'] = df['sem1_cgpa']
    df['sem2_cgpa_display'] = df['sem2_cgpa']
    df['sem3_cgpa_display'] = df['sem3_cgpa']

    # Convert to numeric, errors='coerce' turns "FAIL" and others into NaN
    # Then fill NaN with 0.0
    for col in ['sem1_cgpa', 'sem2_cgpa', 'sem3_cgpa']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # Calculate average CGPA across 3 semesters as a new feature
    df['avg_cgpa'] = df[['sem1_cgpa', 'sem2_cgpa', 'sem3_cgpa']].mean(axis=1)

    # Add trend detection: positive if ut2 > ut1, negative if ut2 < ut1, neutral if equal
    def determine_trend(row):
        if row['ut2_marks'] > row['ut1_marks']:
            return "Improving"
        elif row['ut2_marks'] < row['ut1_marks']:
            return "Declining"
        else:
            return "Stable"

    df['performance_trend'] = df.apply(determine_trend, axis=1)

    return df

def get_department_data(df: pd.DataFrame, department: str) -> pd.DataFrame:
    """Filters data for a specific department."""
    if department == "Admin":
        return df # Full access
    return df[df['department'] == department].copy()
