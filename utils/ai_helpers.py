import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Initialize API Key
API_KEY = os.getenv("GEMINI_API_KEY")

@st.cache_resource
def get_gemini_client():
    """Initializes and caches the Gemini client."""
    if not API_KEY:
        return None
    try:
        # Assuming the new google-genai package
        return genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")
        return None

def generate_student_summary(student_data: dict) -> str:
    """Generates a brief 2-line summary of a student's strengths and weaknesses."""
    client = get_gemini_client()
    if not client:
        return "⚠️ Gemini API key not found. Add it to .env. Expected: A 2-line summary of this student's performance."

    prompt = f"""
    You are an expert educational advisor. Based on the following student data, provide a very brief (exactly 2 lines) summary highlighting their key strength and one potential area of weakness/improvement.
    
    Student Data:
    - Name: {student_data.get('name')}
    - Attendance: {student_data.get('attendance_pct')}%
    - UT1 Marks: {student_data.get('ut1_marks')} (Out of 25)
    - UT2 Marks: {student_data.get('ut2_marks')} (Out of 25)
    - Sem 1 CGPA: {student_data.get('sem1_cgpa_display')}
    - Sem 2 CGPA: {student_data.get('sem2_cgpa_display')}
    - Sem 3 CGPA: {student_data.get('sem3_cgpa_display')}
    - Total KTs: {student_data.get('total_kts')}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error generating summary: {e}"

def generate_class_insights(class_averages: dict, top_students: list, bottom_students: list) -> str:
    """Generates dynamic AI insights based on class extremes and averages."""
    client = get_gemini_client()
    if not client:
        return "⚠️ Gemini API key missing. Cannot generate insights."

    prompt = f"""
    Analyze this class data and identify the 3 most significant trends or anomalies. Do not limit to gender or attendance; look for anything interesting (e.g., 'Students who failed Sem 1 are now topping the class' or 'High UT1 scorers are dropping in UT2').
    Present these as "AI Intelligence Briefs" with bullet points.
    
    Class Averages:
    {class_averages}
    
    Top Performing Students:
    {top_students}
    
    Bottom Performing Students:
    {bottom_students}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error generating class insights: {e}"

def chat_with_bot(messages, class_summary_stats: str) -> str:
    """Returns the bot's response given a chat history and the class statistics context."""
    client = get_gemini_client()
    if not client:
        return "⚠️ Gemini API key not found. Cannot connect to Data Assistant."

    # Prepend the system prompt to the messages
    system_instruction = f"""
    You are a Data Assistant Context-Aware AI Bot for an Edu-Tech platform. 
    You are currently analyzing the following class statistics:
    {class_summary_stats}
    
    Answer the user's questions strictly based on this context or general knowledge related to data analysis. Be concise and helpful.
    """
    
    formatted_messages = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        formatted_messages.append({"role": role, "parts": [{"text": msg["content"]}]})
        
    try:
        # Create a new format compatible with google-genai or use normal text concatenation if easier
        # Easiest way with basic generate_content is to pass the history as part of the prompt
        # since keeping a persistent chat session might drop state across Streamlit reruns.
        conversation_history = system_instruction + "\n\nConversation History:\n"
        for msg in messages:
            conversation_history += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
        conversation_history += "Model:"

        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=conversation_history,
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error communicating with assistant: {e}"
