import streamlit as st
import pandas as pd
from utils.ai_helpers import chat_with_bot

def render_data_assistant(df: pd.DataFrame):
    st.header("Data Assistant (Context-Aware AI)")
    st.write("Chat with Gemini about your class performance.")
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": f"Hello! I am your AI assistant for the {st.session_state['department']} department. Keep in mind I have context of your class statistics. How can I help you today?"}
        ]
        
    # Generate Context Summary
    avg_att = df['attendance_pct'].mean()
    avg_cgpa = df['avg_cgpa'].mean()
    total_stu = len(df)
    total_kts = df['total_kts'].sum()
    improving_count = len(df[df['performance_trend'] == 'Improving'])
    declining_count = len(df[df['performance_trend'] == 'Declining'])
    
    class_summary_stats = f"""
    Department: {st.session_state['department']}
    Total Students: {total_stu}
    Average Attendance: {avg_att:.1f}%
    Average CGPA: {avg_cgpa:.2f}
    Total Class KTs: {total_kts}
    Students Improving (UT2 > UT1): {improving_count}
    Students Declining (UT2 < UT1): {declining_count}
    
    Here is the complete data for all students in this class:
{df.to_csv(index=False)}
    """

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask about your class... (e.g., 'Who is the most improved student?')"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_bot(st.session_state.messages, class_summary_stats)
            st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
