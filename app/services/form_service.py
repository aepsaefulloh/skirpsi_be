# app/services/form_service.py
from flask import request, jsonify
import json
from app.database import get_db_connection
from app.services.knn_service import predict_kejuruan
from app.utils.auth import jwt_required


@jwt_required
def create_form(user_id, title, questions):
    try:
        data = request.json  
        status = data.get("status", 0) 

        conn = get_db_connection()
        cursor = conn.cursor()

        if status not in [0, 1]:
            return jsonify({"error": "Invalid status value. Must be 0 or 1"}), 400

        cursor.execute("INSERT INTO forms (title, status) VALUES (%s, %s)", (title, status))
        form_id = cursor.lastrowid

        for question in questions:
            options = json.dumps(question.get("options")) if "options" in question else None
            cursor.execute("INSERT INTO form_questions (form_id, question_text, category, options, status) VALUES (%s, %s, %s, %s, %s)",
                           (form_id, question["question_text"], question["category"], options, question.get("status", status)))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Form created successfully", "form_id": form_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@jwt_required
def update_form(user_id, form_id, title=None, questions=None, status=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if title:
            cursor.execute("UPDATE forms SET title = %s WHERE id = %s", (title, form_id))
        if status is not None:
            cursor.execute("UPDATE forms SET status = %s WHERE id = %s", (status, form_id))
        
        print(status)

        if questions:
            for question in questions:
                if "id" in question:
                    options = json.dumps(question.get("options")) if "options" in question and isinstance(question["options"], list) else None
                    cursor.execute(
                        "UPDATE form_questions SET question_text = %s, category = %s, options = %s, status = %s WHERE id = %s",
                        (question["question_text"], question["category"], options, question.get("status", 1), question["id"])
                    )
                else:
                    cursor.execute(
                        "INSERT INTO form_questions (form_id, question_text, category, options, status) VALUES (%s, %s, %s, %s, %s)",
                        (
                            form_id,
                            question["question_text"],
                            question["category"],
                            json.dumps(question.get("options")),
                            question.get("status", 1),
                        )
                    )

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Form updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def delete_form(user_id, form_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM forms WHERE id = %s", (form_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Form deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_forms(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        status = request.args.get("status")

        if status is not None:
            try:
                status = int(status)
                if status not in [0, 1]:
                    return jsonify({"error": "Invalid status value. Must be 0 or 1"}), 400
                query = "SELECT * FROM forms WHERE status = %s"
                cursor.execute(query, (status,))
            except ValueError:
                return jsonify({"error": "Invalid status parameter"}), 400
        else:
            query = "SELECT * FROM forms"
            cursor.execute(query)
        
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
        
        cursor.execute("SELECT * FROM forms WHERE id = %s", (form_id,))
        form = cursor.fetchone()
        
        if not form:
            return jsonify({"error": "Form not found"}), 404
        
        cursor.execute("SELECT * FROM form_questions WHERE form_id = %s", (form_id,))
        questions = cursor.fetchall()
        
        for question in questions:
            raw_options = json.loads(question["options"])
            question["options"] = [{"id": i, "title": option} for i, option in enumerate(raw_options)]

        form["questions"] = questions
        cursor.close()
        conn.close()
        return jsonify(form), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@jwt_required
def submit_answers(user_id, form_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        data = request.get_json()
        answers = data.get("answers", [])

        if not answers:
            return jsonify({"error": "No answers provided"}), 400

        for answer in answers:
            question_id = answer.get("question_id")
            answer_text = answer.get("answer_text")
            answer_index = answer.get("answer_index")

            if not question_id or not answer_text:
                continue  

            cursor.execute("""
                INSERT INTO form_answers (form_id, question_id, user_id, answer_text, answer_index) 
                VALUES (%s, %s, %s, %s, %s)
            """, (form_id, question_id, user_id, answer_text, answer_index))

        conn.commit()

        user_answers = {ans["question_id"]: ans["answer_text"] for ans in answers}

        prediction = predict_kejuruan(user_answers)

        if prediction is None:
            return jsonify({
                "message": "Answers submitted successfully", 
                "predicted_kejuruan": "No prediction available. Please submit more data."
            }), 200

        cursor.execute("""
            INSERT INTO kejuruan_answers (user_id, kejuruan) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE kejuruan = VALUES(kejuruan)
        """, (user_id, prediction))

        cursor.execute("""
            UPDATE form_answers 
            SET kejuruan = %s 
            WHERE user_id = %s AND form_id = %s
        """, (prediction, user_id, form_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Answers submitted successfully", 
            "predicted_kejuruan": prediction
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jwt_required
def fetch_users_with_filled_forms(*args):
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DISTINCT u.id AS user_id, u.fullname, u.username, u.email, u.nisn, 
                            f.id AS form_id, f.title AS form_title
            FROM users u
            INNER JOIN form_answers fa ON u.id = fa.user_id
            INNER JOIN forms f ON fa.form_id = f.id
            ORDER BY u.id, f.id
        """
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        if not data:
            return jsonify({"error": "No users found with filled forms"}), 404

        users_dict = {}
        for row in data:
            user_id = row["user_id"]
            if user_id not in users_dict:
                users_dict[user_id] = {
                    "id": row["user_id"],
                    "fullname": row["fullname"],
                    "username": row["username"],
                    "email": row["email"],
                    "nisn": row["nisn"],
                    "forms": []
                }
            
            users_dict[user_id]["forms"].append({
                "form_id": row["form_id"],
                "form_title": row["form_title"]
            })

        return jsonify({"users": list(users_dict.values())}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_answers_by_user_form(requested_user_id, form_id, *args):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query_user = "SELECT id FROM users WHERE id = %s"
        cursor.execute(query_user, (requested_user_id,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404

        query_answers = """
            SELECT answer_text, (
                SELECT question_text FROM form_questions WHERE form_questions.id = form_answers.question_id
            ) AS question_text, (
                SELECT title FROM forms WHERE forms.id = form_answers.form_id
            ) AS title
            FROM form_answers 
            WHERE form_id = %s AND user_id = %s 
        """
        print(f"Executing query: {query_answers} with values ({requested_user_id}, {form_id})")
        cursor.execute(query_answers, (requested_user_id, form_id))
        tempAnswer = cursor.fetchall()

        print(f"Query result: {tempAnswer}")  

        cursor.close()
        conn.close()

        if not tempAnswer:
            return jsonify({"error": "No answers found"}), 404
        
        answers = []
        title = tempAnswer[0]["title"]
        
        for answer in tempAnswer:
            answers.append({
                "question_text": answer["question_text"].strip(),
                "answer_text": answer["answer_text"].strip()
            })
            
        return jsonify({
            "title": title,
            "answers": answers
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def predict_skill_level(user_id):
    try:
        data = request.json
        answers = data.get("answers", {})

        if not answers:
            return jsonify({"error": "No answers provided"}), 400

        prediction = predict_level(answers)

        return jsonify({"predicted_user_id": prediction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400






