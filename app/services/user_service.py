# app/services/user_service.py
from flask import jsonify, request
from app.database import get_db_connection
from app.utils.auth import jwt_required

@jwt_required
def get_all_users(user_id, *args, **kwargs):
    """
    Get all users from the users table.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, fullname, email, date_of_birth, nisn, role, created_at FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def get_user_by_id(user_id, requested_user_id, *args, **kwargs):
    """
    Get a specific user by their ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, fullname, email, date_of_birth, nisn, role, created_at FROM users WHERE id = %s", (requested_user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify({"user": user}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@jwt_required
def update_user(user_id, requested_user_id, *args, **kwargs):
    """
    Update a specific user by their ID.
    """
    try:
        # Validasi input data
        data = request.get_json()
        required_fields = ["fullname", "email", "date_of_birth"]
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({"error": f"{field} is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Cek role pengguna
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404

        role = user["role"]

        # Role-based authorization
        if role == 99:
            return jsonify({"error": "Guest users are not allowed to update user data"}), 403
        elif role != 1 and int(user_id) != int(requested_user_id):
            # Selain superadmin, hanya bisa mengupdate data dirinya sendiri
            cursor.close()
            conn.close()
            return jsonify({"error": "You are not authorized to update this user"}), 403

        # Update user data
        cursor.execute(
            "UPDATE users SET fullname = %s, email = %s, date_of_birth = %s WHERE id = %s",
            (data["fullname"], data["email"], data["date_of_birth"], requested_user_id)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


