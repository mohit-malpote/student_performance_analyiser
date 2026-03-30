import streamlit as st
import pandas as pd
import plotly.express as px

def render_outliers(df: pd.DataFrame):
    st.header("Outliers & Extremes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("High Achievers 🌟")
        # Top 5 students with highest CGPA and 0 KTs
        high_achievers = df[df['total_kts'] == 0].nlargest(5, 'avg_cgpa')
        st.dataframe(high_achievers[['student_id', 'name', 'attendance_pct', 'avg_cgpa']], 
                     use_container_width=True, hide_index=True)
                     
    with col2:
        st.subheader("At-Risk Students ⚠️")
        # Students with (attendance_pct < 75%) OR (total_kts > 1) OR (ut2_marks < ut1_marks)
        at_risk = df[(df['attendance_pct'] < 75) | 
                     (df['total_kts'] > 1) | 
                     (df['performance_trend'] == 'Declining')]
        
        # Displaying only top 5 at-risk to avoid clutter, sorted by lowest attendance first
        st.dataframe(at_risk.sort_values('attendance_pct').head(5)[['student_id', 'name', 'attendance_pct', 'performance_trend', 'total_kts']], 
                     use_container_width=True, hide_index=True)

    st.divider()
    
    st.subheader("Statistical Spread & Outliers")
    st.write("Box plots visualize the distribution and point out statistical outliers.")
    
    # Melt dataframe for Box Plot
    df_melt = pd.melt(df, id_vars=['name'], value_vars=['ut1_marks', 'ut2_marks'], 
                      var_name='Unit Test', value_name='Marks')
                      
    fig_spread = px.box(df_melt, x='Unit Test', y='Marks', points="all", hover_data=['name'],
                        title="Distribution of Unit Test Marks", color='Unit Test')
    st.plotly_chart(fig_spread, use_container_width=True)
