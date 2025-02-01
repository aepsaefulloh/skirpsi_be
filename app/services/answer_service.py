# app/services/answer_service.py
from flask import request, jsonify
from app.database import get_db_connection
from app.utils.auth import jwt_required  # Import middleware JWT

@jwt_required
def create_answer(user_id, title, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO m_answers (title) VALUES (%s)',
            (title,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Answer added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_answers(user_id, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM m_answers')
        answers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"answers": answers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_answer_by_id(user_id, answer_id, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM m_answers WHERE id = %s', (answer_id,))
        answer = cursor.fetchone()
        cursor.close()
        conn.close()
        if answer:
            return jsonify({"answer": answer}), 200
        else:
            return jsonify({"error": "Answer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def delete_answer(user_id, answer_id, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM m_answers WHERE id = %s', (answer_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Answer deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
