# app/services/login_service.py
import bcrypt
import jwt
import datetime
from app.database import get_db_connection

SECRET_KEY = "your_secret_key"

def login_user(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            token = jwt.encode({
                "user_id": user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24*7)
            }, SECRET_KEY, algorithm="HS256")
            return {"token": token}, 200
        else:
            return {"error": "Invalid username or password"}, 401
    except Exception as e:
        return {"error": str(e)}, 400
