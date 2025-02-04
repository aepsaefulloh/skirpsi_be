from flask import request, jsonify
import json
from app.database import get_db_connection
from app.utils.auth import jwt_required  # Middleware JWT

@jwt_required
def create_form(user_id, title, questions):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert form data
        cursor.execute("INSERT INTO forms (title) VALUES (%s)", (title,))
        form_id = cursor.lastrowid
        
        # Insert questions
        for question in questions:
            options = json.dumps(question.get("options")) if "options" in question else None
            cursor.execute("INSERT INTO form_questions (form_id, question_text, category, options, status) VALUES (%s, %s, %s, %s, %s)",
                           (form_id, question["question_text"], question["category"], options, question.get("status", 1)))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Form created successfully", "form_id": form_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_forms(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM forms")
        forms = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return jsonify({"forms": forms}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@jwt_required
def get_form(user_id, form_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get form details
        cursor.execute("SELECT * FROM forms WHERE id = %s", (form_id,))
        form = cursor.fetchone()
        
        if not form:
            return jsonify({"error": "Form not found"}), 404
        
        # Get form questions
        cursor.execute("SELECT * FROM form_questions WHERE form_id = %s", (form_id,))
        questions = cursor.fetchall()
        
        form["questions"] = questions
        cursor.close()
        conn.close()
        return jsonify(form), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def submit_answers(user_id, form_id, answers):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert answers
        for answer in answers:
            cursor.execute("INSERT INTO form_answers (form_id, question_id, user_id, answer_text) VALUES (%s, %s, %s, %s)",
                           (form_id, answer["question_id"], user_id, answer["answer_text"]))
        
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Answers submitted successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
