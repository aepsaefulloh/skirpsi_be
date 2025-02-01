# app/database.py
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            nisn BIGINT(50),
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            date_of_birth DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS m_questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question_text TEXT NOT NULL,
                category VARCHAR(100) NOT NULL,
                status SMALLINT(2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.commit()
    cursor.close()
    conn.close()