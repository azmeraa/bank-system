from flask import Blueprint, request, jsonify
from app.database import get_connection

from werkzeug.security import generate_password_hash, check_password_hash
from services.bank_service import BankService

import jwt
import datetime
import os
from functools import wraps

auth = Blueprint('auth', __name__)

# ✅ USE ENV SECRET (Render safe)
SECRET_KEY = os.getenv("SECRET_KEY", "bank-secret-key-123")

# =========================
# REGISTER
# =========================
@auth.route('/register', methods=['POST'])
def register():
    data = request.json

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not all([full_name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (full_name, email, password, balance)
            VALUES (?, ?, ?, ?)
        """, (full_name, email, hashed_password, 0))

        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        conn.close()

# =========================
# LOGIN
# =========================
@auth.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Login successful", "token": token}), 200

# =========================
# TOKEN DECORATOR
# =========================
def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except:
            return jsonify({"error": "Invalid or expired token"}), 401

        return func(*args, **kwargs)

    return wrapper

# =========================
# BALANCE
# =========================
@auth.route('/balance', methods=['GET'])
@token_required
def balance():
    user_id = request.user["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"balance": user["balance"]}), 200

# =========================
# PROFILE
# =========================
@auth.route('/profile', methods=['GET'])
@token_required
def profile():
    user_id = request.user["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, full_name, email, balance
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user)), 200

# =========================
# DEPOSIT
# =========================
@auth.route('/deposit', methods=['POST'])
@token_required
def deposit():
    data = request.json

    try:
        amount = float(data.get("amount", 0))
    except:
        return jsonify({"error": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be > 0"}), 400

    new_balance = BankService.deposit(request.user["user_id"], amount)

    return jsonify({
        "message": "Deposit successful",
        "new_balance": new_balance
    })

# =========================
# WITHDRAW
# =========================
@auth.route('/withdraw', methods=['POST'])
@token_required
def withdraw():
    data = request.json

    try:
        amount = float(data.get("amount", 0))
    except:
        return jsonify({"error": "Invalid amount"}), 400

    result = BankService.withdraw(request.user["user_id"], amount)

    if result == "INSUFFICIENT_FUNDS":
        return jsonify({"error": "Insufficient funds"}), 400

    return jsonify({
        "message": "Withdraw successful",
        "new_balance": result
    })

# =========================
# TRANSACTIONS
# =========================
@auth.route('/transactions', methods=['GET'])
@token_required
def transactions():
    rows = BankService.get_transactions(request.user["user_id"])

    return jsonify([
        dict(r) for r in rows
    ])

# =========================
# TRANSFER
# =========================
@auth.route('/transfer', methods=['POST'])
@token_required
def transfer():
    data = request.json

    receiver_email = data.get("receiver_email")

    try:
        amount = float(data.get("amount", 0))
    except:
        return jsonify({"error": "Invalid amount"}), 400

    if not receiver_email:
        return jsonify({"error": "receiver_email required"}), 400

    sender_id = request.user["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (sender_id,))
    sender = cursor.fetchone()

    cursor.execute("SELECT * FROM users WHERE email = ?", (receiver_email,))
    receiver = cursor.fetchone()

    if not receiver:
        return jsonify({"error": "Receiver not found"}), 404

    if sender["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    sender_new = sender["balance"] - amount
    receiver_new = receiver["balance"] + amount

    cursor.execute("UPDATE users SET balance=? WHERE id=?", (sender_new, sender_id))
    cursor.execute("UPDATE users SET balance=? WHERE id=?", (receiver_new, receiver["id"]))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Transfer successful",
        "sender_balance": sender_new
    })