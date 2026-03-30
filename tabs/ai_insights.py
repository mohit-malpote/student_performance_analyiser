import streamlit as st
import pandas as pd
from utils.ai_helpers import generate_class_insights

def render_ai_insights(df: pd.DataFrame):
    st.header("Dynamic AI Insights")
    st.write("Generates deep contextual analysis identifying trends and anomalies for this class.")
    
    if st.button("Generate Insights via Gemini 3.1 Pro"):
        with st.spinner("Analyzing class data and generating intelligence brief..."):
            # Compute Class Averages
            avg_attendance = df['attendance_pct'].mean()
            avg_ut1 = df['ut1_marks'].mean()
            avg_ut2 = df['ut2_marks'].mean()
            avg_sem1 = df['sem1_cgpa'].mean()
            avg_sem2 = df['sem2_cgpa'].mean()
            avg_sem3 = df['sem3_cgpa'].mean()
            
            class_averages = {
                "Attendance": f"{avg_attendance:.2f}%",
                "UT1 Marks": f"{avg_ut1:.2f}",
                "UT2 Marks": f"{avg_ut2:.2f}",
                "Sem 1 CGPA": f"{avg_sem1:.2f}",
                "Sem 2 CGPA": f"{avg_sem2:.2f}",
                "Sem 3 CGPA": f"{avg_sem3:.2f}"
            }
            
            # Find Top 3 and Bottom 3 Students (based on avg_cgpa)
            sorted_df = df.sort_values(by='avg_cgpa', ascending=False)
            
            top_students = []
            for _, row in sorted_df.head(3).iterrows():
                top_students.append(f"{row['name']} (Attendance: {row['attendance_pct']}%, Sem 1: {row['sem1_cgpa_display']}, Sem 2: {row['sem2_cgpa_display']}, Sem 3: {row['sem3_cgpa_display']}, KTs: {row['total_kts']})")
                
            bottom_students = []
            for _, row in sorted_df.tail(3).iterrows():
                bottom_students.append(f"{row['name']} (Attendance: {row['attendance_pct']}%, Sem 1: {row['sem1_cgpa_display']}, Sem 2: {row['sem2_cgpa_display']}, Sem 3: {row['sem3_cgpa_display']}, KTs: {row['total_kts']})")
                
            insights = generate_class_insights(class_averages, top_students, bottom_students)
            
            st.success("Analysis Complete")
            st.markdown(insights)
    else:
        st.info("Click the button above to evaluate class data through Gemini.")
