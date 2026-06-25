from flask import Blueprint, request, jsonify
from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from services.bank_service import BankService
import jwt
import datetime
from functools import wraps

auth = Blueprint('auth', __name__)

SECRET_KEY = "bank-secret-key-123"

# =========================
# REGISTER
# =========================
@auth.route('/register', methods=['POST'])
def register():
    data = request.json

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
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
# LOGIN (TOKEN)
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
# TOKEN CHECKER
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

    cursor.execute(
        "SELECT balance FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user_id,
        "balance": user["balance"]
    }), 200


# =========================
# PROFILE (NEW)
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

    return jsonify({
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "balance": user["balance"]
    }), 200


# =========================
# DEPOSIT
# =========================
@auth.route('/deposit', methods=['POST'])
@token_required
def deposit():
    data = request.json
    amount = data.get("amount")

    user_id = request.user["user_id"]

    new_balance = BankService.deposit(user_id, amount)

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
    amount = data.get("amount")

    user_id = request.user["user_id"]

    new_balance = BankService.withdraw(user_id, amount)

    if new_balance is None:
        return jsonify({"error": "Insufficient balance"}), 400

    return jsonify({
        "message": "Withdraw successful",
        "new_balance": new_balance
    })


# =========================
# TRANSACTIONS
# =========================
@auth.route('/transactions', methods=['GET'])
@token_required
def transactions():
    user_id = request.user["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify({
        "transactions": [
            {
                "transaction_type": r["transaction_type"],
                "amount": r["amount"],
                "balance_after": r["balance_after"],
                "timestamp": r["timestamp"]
            }
            for r in rows
        ]
    })


# =========================
# TRANSFER
# =========================
@auth.route('/transfer', methods=['POST'])
@token_required
def transfer():
    data = request.json

    receiver_email = data.get("receiver_email")
    amount = data.get("amount")

    if not receiver_email or amount is None:
        return jsonify({"error": "receiver_email and amount are required"}), 400

    sender_id = request.user["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (sender_id,))
    sender = cursor.fetchone()

    cursor.execute("SELECT * FROM users WHERE email = ?", (receiver_email,))
    receiver = cursor.fetchone()

    if not receiver:
        conn.close()
        return jsonify({"error": "Receiver not found"}), 404

    if sender["balance"] < amount:
        conn.close()
        return jsonify({"error": "Insufficient balance"}), 400

    sender_new = sender["balance"] - amount
    receiver_new = receiver["balance"] + amount

    cursor.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (sender_new, sender_id)
    )

    cursor.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (receiver_new, receiver["id"])
    )

    cursor.execute("""
        INSERT INTO transactions
        (user_id, transaction_type, amount, balance_after)
        VALUES (?, ?, ?, ?)
    """, (
        sender_id,
        "transfer_sent",
        amount,
        sender_new
    ))

    cursor.execute("""
        INSERT INTO transactions
        (user_id, transaction_type, amount, balance_after)
        VALUES (?, ?, ?, ?)
    """, (
        receiver["id"],
        "transfer_received",
        amount,
        receiver_new
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Transfer successful",
        "sender_balance": sender_new
    }), 200