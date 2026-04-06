import sqlite3
import pandas as pd
import os

DB_PATH = "students.db"
CSV_FALLBACK = "student_performance_analysis.csv"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initializes the database from the fallback CSV if it doesn't exist or is empty."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if table 'students' exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        if os.path.exists(CSV_FALLBACK):
            df = pd.read_csv(CSV_FALLBACK)
            df.to_sql("students", conn, if_exists="replace", index=False)
        else:
            # Create an empty table if even the CSV isn't there
            # with default schema
            schema = pd.DataFrame(columns=[
                "student_id", "name", "email", "gender", "department", 
                "year_of_study", "attendance_percent", "sem1_cgpa", 
                "sem2_cgpa", "sem3_cgpa", "ut1_marks", "ut2_marks", 
                "assignments_completed", "active_participation", 
                "extracurricular_activities", "library_books_issued", "library_hours_spent"
            ])
            schema.to_sql("students", conn, if_exists="replace", index=False)
    
    conn.close()

def get_all_data() -> pd.DataFrame:
    """Fetches all student data from the database."""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

def get_department_data(department: str) -> pd.DataFrame:
    """Fetches data for a specific department."""
    conn = get_connection()
    if department == "Admin":
        df = pd.read_sql("SELECT * FROM students", conn)
    else:
        df = pd.read_sql("SELECT * FROM students WHERE department = ?", conn, params=(department,))
    conn.close()
    return df

def replace_department_data(department: str, new_df: pd.DataFrame):
    """
    Replaces all records for a specific department with the provided DataFrame.
    Other departments remain untouched.
    """
    # Ensure all rows in new_df belong to this department
    new_df = new_df.copy()
    new_df['department'] = department
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Delete existing rows for this department
    cursor.execute("DELETE FROM students WHERE department = ?", (department,))
    
    # 2. Append the new_df to the table
    new_df.to_sql("students", conn, if_exists="append", index=False)
    
    conn.commit()
    conn.close()
