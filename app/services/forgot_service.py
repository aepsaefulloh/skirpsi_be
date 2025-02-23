# app/services/forgot_service.py
import bcrypt
from app.database import get_db_connection

def forgot_password(username, last_four_nisn, new_password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT nisn FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        
        if not user:
            return {"error": "User not found"}, 404
        
        nisn_str = str(user["nisn"])
        if nisn_str[-4:] != str(last_four_nisn):
            return {"error": "Invalid NISN verification"}, 401
        
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        cursor.execute('UPDATE users SET password = %s WHERE username = %s', (hashed_password, username))
        conn.commit()
        
        cursor.close()
        conn.close()
        return {"message": "Password reset successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 400
