from flask import request, jsonify
from flask_cors import CORS  # Import CORS
from app.services.register_service import register_user
from app.services.login_service import login_user
from app.services.profile_service import get_profile
from app.services.forgot_service import forgot_password
from app.services.form_service import get_forms, create_form, update_form, delete_form, get_form, submit_answers
from app.services.user_service import get_all_users, get_user_by_id, update_user
def init_routes(app):
    CORS(app)  # Enable CORS for all routes

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
    @app.route('/users', methods=['GET'])
    def users():
        return get_all_users()

    @app.route('/user/<int:user_id>', methods=['GET'])
    def user_by_id(user_id):
        return get_user_by_id(user_id)
    
    @app.route('/user/<int:user_id>', methods=['PUT'])
    def update_user_route(user_id):
        try:
            data = request.get_json()
            if not data:
                return {"error": "Missing request body"}, 400
            return update_user(user_id, data.get("fullname"), data.get("email"), data.get("date_of_birth"), data.get("nisn"), data.get("role"))
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/forms', methods=['GET'])
    def forms():
        return get_forms()
    
    @app.route('/forms', methods=['POST'])
    def add_form():
        try:
            data = request.get_json()
            if not data or "title" not in data or "questions" not in data:
                return {"error": "Missing required fields"}, 400
            return create_form(data["title"], data["questions"])
        except Exception as e:
            return {"error": str(e)}, 500
        
    @app.route('/form/<int:form_id>', methods=['PUT'])
    def update_form_route(form_id):
        try:
            data = request.get_json()
            if not data:
                return {"error": "Missing request body"}, 400
            return update_form(form_id, data.get("title"), data.get("questions"), data.get("status"))
        except Exception as e:
            return {"error": str(e)}, 500
        
    @app.route('/form/<int:form_id>', methods=['DELETE'])
    def delete_form_route(form_id):
        try:
            return delete_form(form_id)
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/form/<int:form_id>', methods=['GET'])
    def form_by_id(form_id):
        return get_form(form_id)

    @app.route('/form/<int:form_id>/submit', methods=['POST'])
    def submit_form_answers(form_id):
        try:
            data = request.get_json()
            if not data or "answers" not in data:
                return {"error": "Missing required fields"}, 400
            return submit_answers(form_id, data["answers"])
        except Exception as e:
            return {"error": str(e)}, 500

        
