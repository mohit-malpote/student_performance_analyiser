import streamlit as st
import pandas as pd
import plotly.express as px

def render_leaderboard(df: pd.DataFrame):
    st.header("Inter-Class Leaderboard 🏆")
    st.write("Comparing all 4 departments across multiple performance metrics.")
    
    # We aggregate the full dataframe
    # Calculate metrics for each department
    agg_df = df.groupby('department').agg(
        avg_attendance=('attendance_pct', 'mean'),
        avg_cgpa=('avg_cgpa', 'mean'),
        total_students=('student_id', 'count')
    ).reset_index()
    
    # Calculate % of students with 0 KTs per department
    def zero_kt_pct(group):
        zero_kts = len(group[group['total_kts'] == 0])
        total = len(group)
        return (zero_kts / total) * 100 if total > 0 else 0
        
    zero_kt_df = df.groupby('department').apply(zero_kt_pct, include_groups=False).reset_index(name='pct_zero_kts')
    
    # Merge
    dept_stats = pd.merge(agg_df, zero_kt_df, on='department')
    
    # Calculate a combined ranking score (arbitrary simple formula for demo)
    # Give weight to CGPA, Attendance, and Zero KT %
    dept_stats['combined_score'] = (dept_stats['avg_cgpa'] * 10) + (dept_stats['avg_attendance'] * 0.5) + (dept_stats['pct_zero_kts'] * 0.5)
    
    # Sort by score
    dept_stats = dept_stats.sort_values('combined_score', ascending=False).reset_index(drop=True)
    dept_stats['Rank'] = dept_stats.index + 1
    
    # Display the Ranking Table First
    st.subheader("Department Rankings")
    
    # Format for display
    display_stats = dept_stats[['Rank', 'department', 'avg_attendance', 'avg_cgpa', 'pct_zero_kts', 'combined_score']].copy()
    display_stats['avg_attendance'] = display_stats['avg_attendance'].round(1).astype(str) + '%'
    display_stats['avg_cgpa'] = display_stats['avg_cgpa'].round(2)
    display_stats['pct_zero_kts'] = display_stats['pct_zero_kts'].round(1).astype(str) + '%'
    display_stats['combined_score'] = display_stats['combined_score'].round(1)
    
    st.dataframe(display_stats, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("Performance Comparison")
    
    # Grouped Bar Chart
    fig_bar = px.bar(
        dept_stats, 
        x="department", 
        y=["avg_attendance", "pct_zero_kts"], 
        title="Department Attendance vs % Zero KTs",
        barmode='group',
        labels={'value': 'Percentage', 'variable': 'Metric'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)
