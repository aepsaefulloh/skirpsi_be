import jwt
from flask import request, jsonify
from functools import wraps
from app.database import get_db_connection

SECRET_KEY = "your_secret_key"

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization token is missing"}), 401
        
        try:
            token = auth_header.split(" ")[1]
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_token["user_id"]
            return f(user_id, *args, **kwargs)  # Mengirim user_id ke fungsi endpoint
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
    
    return decorated_function
