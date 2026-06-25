from flask import Blueprint, jsonify
from app.database import get_connection
from app.utils.jwt_required import jwt_required
from app.utils.admin_required import admin_required

admin = Blueprint("admin", __name__)


# =========================
# 👥 ALL USERS
# =========================
@admin.route("/admin/users", methods=["GET"])
@jwt_required
@admin_required
def get_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, full_name, email, balance FROM users")
    users = cursor.fetchall()

    conn.close()

    return jsonify([dict(u) for u in users])


# =========================
# 📊 ALL TRANSACTIONS
# =========================
@admin.route("/admin/transactions", methods=["GET"])
@jwt_required
@admin_required
def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        ORDER BY timestamp DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return jsonify([dict(t) for t in data])


# =========================
# 👤 SINGLE USER DETAILS
# =========================
@admin.route("/admin/user/<int:user_id>", methods=["GET"])
@jwt_required
@admin_required
def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(dict(user))