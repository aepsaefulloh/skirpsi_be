# app/services/setting_service.py
from flask import jsonify, request
from app.database import get_db_connection
from app.utils.auth import jwt_required  # Middleware JWT

@jwt_required
def get_all_setting(user_id, *args, **kwargs):
    """
    Get all settings from the setting table.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, url FROM setting")
        settings = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"settings": settings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_setting_by_id( setting_id, *args, **kwargs):
    """
    Get a specific setting by ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, url FROM setting WHERE id = %s", (setting_id,))
        setting = cursor.fetchone()
        cursor.close()
        conn.close()

        if not setting:
            return jsonify({"error": "Setting not found"}), 404

        return jsonify({"setting": setting}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jwt_required
def create_setting(user_id, *args, **kwargs):
    """
    Create a new setting.
    """
    try:
        data = request.get_json()
        required_fields = ["url"]
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({"error": f"{field} is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO setting (url) VALUES (%s)", (data["url"],))
        conn.commit()
        setting_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"message": "Setting created successfully", "id": setting_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jwt_required
def update_setting(user_id, setting_id, *args, **kwargs):
    """
    Update a specific setting by its ID.
    """
    try:
        data = request.get_json()
        required_fields = ["url"]
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({"error": f"{field} is required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Cek apakah setting ada
        cursor.execute("SELECT id FROM setting WHERE id = %s", (setting_id,))
        setting = cursor.fetchone()

        if not setting:
            cursor.close()
            conn.close()
            return jsonify({"error": "Setting not found"}), 404

        # Update setting data
        cursor.execute("UPDATE setting SET url = %s WHERE id = %s", (data["url"], setting_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Setting updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jwt_required
def delete_setting(user_id, setting_id, *args, **kwargs):
    """
    Delete a specific setting by its ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Cek apakah setting ada
        cursor.execute("SELECT id FROM setting WHERE id = %s", (setting_id,))
        setting = cursor.fetchone()

        if not setting:
            cursor.close()
            conn.close()
            return jsonify({"error": "Setting not found"}), 404

        # Hapus setting
        cursor.execute("DELETE FROM setting WHERE id = %s", (setting_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Setting deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
