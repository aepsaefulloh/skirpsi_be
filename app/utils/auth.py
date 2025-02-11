# app/utils/auth.py
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
            
            # Dapatkan role pengguna dari database
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT role FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if not user:
                return jsonify({"error": "User not found"}), 404
            
            # Role-based handling
            if user["role"] == 99:
                return jsonify({"error": "Guest users are not allowed to access this resource"}), 403
            elif user["role"] == 1:
                print(f"Superadmin access granted for user_id: {user_id}")  # Contoh logging tambahan
            
            return f(user_id, *args, **kwargs) 
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return decorated_function
