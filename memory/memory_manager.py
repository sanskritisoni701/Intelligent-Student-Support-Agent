
import sqlite3
from pathlib import Path


# Locate the memory database
DB_FILE = (
    Path(__file__).resolve().parent / "memory.db"
)


# Information categories that can be remembered
ALLOWED_CATEGORIES = {
    "programme",
    "preferred_language",
    "response_preference",
    "learning_preference"
}


def get_connection():

    return sqlite3.connect(DB_FILE)


# 1. Initialize the database
def initialize_memory():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            category TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, category)
        )
    """)

    connection.commit()
    connection.close()


# 2. Save useful information
def save_memory(student_id, category, value):

    # Validate student ID
    if not student_id or not student_id.strip():
        return {
            "success": False,
            "message": "Student ID is required."
        }

    # Only allow approved memory categories
    if category not in ALLOWED_CATEGORIES:
        return {
            "success": False,
            "message": "This information category cannot be stored."
        }

    if not isinstance(value, str) or not value.strip():
        return {
            "success": False,
            "message": "Memory value cannot be empty."
        }

    if len(value) > 200:
        return {
            "success": False,
            "message": "Memory value is too long."
        }

    # Store the information
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO student_memory
        (student_id, category, value)
        VALUES (?, ?, ?)

        ON CONFLICT(student_id, category)
        DO UPDATE SET value = excluded.value
    """, (student_id, category, value.strip()))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Memory saved successfully."
    }


# 3. Retrieve saved information
def get_memories(student_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT category, value
        FROM student_memory
        WHERE student_id = ?
    """, (student_id,))

    records = cursor.fetchall()

    connection.close()

    return {
        category: value
        for category, value in records
    }


# 4. Clear a student's saved memory
def clear_memories(student_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM student_memory
        WHERE student_id = ?
    """, (student_id,))

    connection.commit()
    connection.close()

    return {
        "success": True,
        "message": "Student memory cleared."
    }


# Initialize database when this module is loaded
initialize_memory()
