# app/routes.py
from flask import request, jsonify
from app.services.register_service import register_user
from app.services.login_service import login_user
from app.services.profile_service import get_profile
from app.services.forgot_service import forgot_password
from app.services.question_service import create_question, get_questions, get_question_by_id, delete_question

def init_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            if not data:
                return {"error": "Missing request body"}, 400

            required_fields = ["username", "password", "nisn", "fullname", "email", "date_of_birth"]
            for field in required_fields:
                if field not in data:
                    return {"error": f"Missing field: {field}"}, 400

            return register_user(data["username"], data["password"], data["fullname"], data["email"], data["date_of_birth"], data["nisn"])
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            if not data or "username" not in data or "password" not in data:
                return {"error": "Missing username or password"}, 400
            return login_user(data["username"], data["password"])
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/forgot-password', methods=['POST'])
    def forgot_password_route():
        try:
            data = request.get_json()
            if not data or "username" not in data or "last_four_nisn" not in data or "new_password" not in data:
                return {"error": "Missing required fields"}, 400
            return forgot_password(data["username"], data["last_four_nisn"], data["new_password"])
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/profile', methods=['GET'])
    def profile():
        try:
            token = request.headers.get("Authorization")
            if not token:
                return {"error": "Token is missing"}, 401
            return get_profile(token.split(" ")[1])
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/questions', methods=['GET'])
    def questions():
        status = request.args.get('status')  # Ambil parameter status jika ada
        return get_questions(status=status)

    @app.route('/question', methods=['GET', 'POST'])
    def question():
        if request.method == 'GET':
            status = request.args.get('status')  # Ambil parameter status jika ada
            return get_questions(status=status)
        elif request.method == 'POST':
            try:
                data = request.get_json()
                if not data or "question_text" not in data or "category" not in data or "status" not in data:
                    return {"error": "Missing required fields"}, 400
                return create_question(data["question_text"], data["category"], data["status"])
            except Exception as e:
                return {"error": str(e)}, 500
    @app.route('/question/<int:question_id>', methods=['GET'])
    def question_by_id(question_id):
        return get_question_by_id(question_id)

    @app.route('/question/<int:question_id>', methods=['DELETE'])
    def remove_question(question_id):
        return delete_question(question_id)
