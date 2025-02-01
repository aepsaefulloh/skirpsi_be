# app/services/register_service.py
import bcrypt
from app.database import get_db_connection

def register_user(username, password, fullname, email, date_of_birth, nisn):
    try:
        # Validasi panjang NISN
        nisn = str(nisn)
        if not nisn.isdigit() or len(nisn) != 10:
            return {"error": "Invalid NISN. It must be a 10-digit number."}, 400

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, fullname, email, date_of_birth, nisn) VALUES (%s, %s, %s, %s, %s, %s)',
            (username, hashed_password, fullname, email, date_of_birth, int(nisn))
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "User registered successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 400
