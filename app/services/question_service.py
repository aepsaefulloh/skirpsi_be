# app/services/question_service.py
import jwt
from flask import request, jsonify
from app.database import get_db_connection
from app.utils.auth import jwt_required  # Import middleware JWT

SECRET_KEY = "your_secret_key"

@jwt_required
def get_user_profile(user_id, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, username, fullname, email FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify({"user": user}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def create_question(user_id, question_text, category, status, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO m_questions (question_text, category, status) VALUES (%s, %s, %s)',
            (question_text, category, status)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Question added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_questions(user_id, status=None, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if status is not None:
            cursor.execute('SELECT * FROM m_questions WHERE status = %s', (status,))
        else:
            cursor.execute('SELECT * FROM m_questions')
        questions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"questions": questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_question_by_id(user_id, question_id, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM m_questions WHERE id = %s', (question_id,))
        question = cursor.fetchone()
        cursor.close()
        conn.close()
        if question:
            return jsonify({"question": question}), 200
        else:
            return jsonify({"error": "Question not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def delete_question(user_id, question_id, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM m_questions WHERE id = %s', (question_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Question deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400