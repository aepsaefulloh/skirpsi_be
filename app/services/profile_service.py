# app/services/profile_service.py
import jwt
from flask import request, jsonify
from app.database import get_db_connection
from app.utils.auth import jwt_required

SECRET_KEY = "your_secret_key"

@jwt_required
def get_profile(user_id, *args, **kwargs):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, username, fullname, email, role FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify({"user": user}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400