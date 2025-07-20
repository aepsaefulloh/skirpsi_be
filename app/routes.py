from flask import request, jsonify
from flask_cors import CORS
import numpy as np
from app.services.register_service import register_user
from app.services.login_service import login_user
from app.services.profile_service import get_profile
from app.services.forgot_service import forgot_password
from app.services.form_service import get_forms, create_form, update_form, delete_form, get_form, submit_answers, fetch_users_with_filled_forms, get_answers_by_user_form
from app.services.user_service import get_all_users, get_user_by_id, update_user
from app.services.setting_service import (
    get_all_setting, get_setting_by_id, create_setting, update_setting, delete_setting
)
from app.services.knn_service import predict_kejuruan

from app.utils.train_knn_from_csv import predict_kejuruan_from_csv

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
        return submit_answers(form_id)
    
    @app.route('/users/filled-forms', methods=['GET'])
    def get_users_with_filled_forms():
        return fetch_users_with_filled_forms()
    
    @app.route('/form/<int:requested_user_id>/answers/<int:form_id>', methods=['GET'])
    def get_form_answers_by_user(requested_user_id, form_id):
        return get_answers_by_user_form(requested_user_id, form_id)

    @app.route('/settings', methods=['GET'])
    def get_settings(): 
        return get_all_setting()

    @app.route('/settings/<int:setting_id>', methods=['GET'])
    def get_single_setting(setting_id):
        return get_setting_by_id(setting_id)

    @app.route('/settings', methods=['POST'])
    def create_new_setting():
        try:
            data = request.get_json()
            if not data or "url" not in data:
                return {"error": "Missing required fields"}, 400
            return create_setting()
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/settings/<int:setting_id>', methods=['PUT'])
    def update_existing_setting(setting_id):
        try:
            data = request.get_json()
            if not data or "url" not in data:
                return {"error": "Missing required fields"}, 400
            return update_setting(setting_id)
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/settings/<int:setting_id>', methods=['DELETE'])
    def delete_existing_setting(setting_id):
        try:
            return delete_setting(setting_id)
        except Exception as e:
            return {"error": str(e)}, 500
    
    @app.route('/predict-kejuruan-db', methods=['POST'])
    def predict_kejuruan_db_api():
        """ API untuk prediksi kejuruan berdasarkan data dari database """
        try:
            data = request.get_json()
            if not data or "answers" not in data:
                return jsonify({"error": "Invalid JSON atau field 'answers' tidak ada"}), 400

            user_answers = data["answers"]
            if len(user_answers) < 1:
                return jsonify({"error": "Jawaban tidak boleh kosong"}), 400

            prediction = predict_kejuruan(user_answers)

            if prediction is None:
                return jsonify({"error": "Model belum siap, harap latih ulang dengan lebih banyak data"}), 400

            return jsonify({"predicted_kejuruan": prediction}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/predict-kejuruan', methods=['POST'])
    def predict_kejuruan_api():
        """ API untuk prediksi kejuruan """
        try:
            data = request.get_json()
            if not data or "answers" not in data:
                return jsonify({"error": "Invalid JSON or missing 'answers' field"}), 400

            user_answers = data["answers"]
            if len(user_answers) != 6:  # Sesuaikan jumlah fitur dengan dataset
                return jsonify({"error": "Jumlah jawaban tidak sesuai dengan dataset"}), 400

            prediction = predict_kejuruan_from_csv(user_answers)

            return jsonify({"predicted_kejuruan": prediction}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500




    

        
