import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.ai_helpers import generate_student_summary

def render_dashboard(df: pd.DataFrame):
    st.title(f"Dashboard: {st.session_state['department']} Department")
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    avg_attendance = df['attendance_pct'].mean()
    avg_sem3 = df['sem3_cgpa'].mean()
    total_students = len(df)
    total_kts = df['total_kts'].sum()
    
    with col1:
        st.metric("Avg Attendance", f"{avg_attendance:.1f}%")
    with col2:
        st.metric("Avg Sem 3 CGPA", f"{avg_sem3:.2f}")
    with col3:
        st.metric("Total Students", total_students)
    with col4:
        st.metric("Class KT Count", total_kts)
    
    # Main Charts
    st.subheader("Class Overview")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Scatter Plot - Attendance vs Marks (UT Avg)
        df['avg_ut_marks'] = (df['ut1_marks'] + df['ut2_marks']) / 2
        fig_scatter = px.scatter(df, x='attendance_pct', y='avg_ut_marks', hover_name='name', 
                                 title="Attendance vs Avg UT Marks",
                                 labels={'attendance_pct': 'Attendance %', 'avg_ut_marks': 'Avg UT Marks'},
                                 color_discrete_sequence=['#636EFA'])
        fig_scatter.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with chart_col2:
        # Histogram of Class CGPAs
        fig_hist = px.histogram(df, x='avg_cgpa', nbins=15, title="Distribution of Average CGPA",
                                labels={'avg_cgpa': 'Average CGPA'}, color_discrete_sequence=['#EF553B'])
        fig_hist.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_hist, use_container_width=True)
    
    st.divider()
    
    # Interactive Table for Student Selection
    st.subheader("Student Directory")
    st.write("Select a student row to view their detailed profile.")
    
    # Select columns to display in table
    display_cols = ['student_id', 'name', 'attendance_pct', 'avg_ut_marks', 'sem1_cgpa_display', 'sem2_cgpa_display', 'sem3_cgpa_display', 'total_kts', 'performance_trend']
    display_df = df[display_cols].copy()
    
    event = st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    selected_indices = event.selection.rows
    
    # Drill-down view
    if selected_indices:
        st.markdown("---")
        idx = selected_indices[0]
        student = display_df.iloc[idx]
        # Match original full row for detailed plotting
        full_student_row = df.iloc[idx].to_dict()
        
        st.subheader(f"🎓 Student Profile: {student['name']} ({student['student_id']})")
        
        col_summary, col_charts = st.columns([1, 2])
        
        with col_summary:
            st.markdown("### AI Summary")
            with st.spinner("Generating AI Summary..."):
                summary = generate_student_summary(full_student_row)
            st.info(summary)
            
            st.markdown("### Details")
            st.write(f"**Attendance:** {student['attendance_pct']}%")
            st.write(f"**Total KTs:** {student['total_kts']}")
            st.write(f"**Trend:** {student['performance_trend']}")
            
        with col_charts:
            # Visual 1: Line Chart
            cgpa_vals = [full_student_row['sem1_cgpa'], full_student_row['sem2_cgpa'], full_student_row['sem3_cgpa']]
            semesters = ['Sem 1', 'Sem 2', 'Sem 3']
            fig_line = px.line(x=semesters, y=cgpa_vals, markers=True, 
                               title="CGPA Progress (FAIL=0.0)", labels={'x': 'Semester', 'y': 'CGPA'})
            fig_line.update_yaxes(range=[0, 10])
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Visual 2: Grouped Bar Chart
            ut_vals = [full_student_row['ut1_marks'], full_student_row['ut2_marks']]
            ut_labels = ['UT 1', 'UT 2']
            fig_bar = px.bar(x=ut_labels, y=ut_vals, title="UT Marks Comparison", labels={'x': 'Unit Test', 'y': 'Marks (Out of 25)'})
            fig_bar.update_yaxes(range=[0, 25])
            st.plotly_chart(fig_bar, use_container_width=True)
