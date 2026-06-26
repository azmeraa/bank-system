from flask import Blueprint, request, jsonify
from app.database import get_connection
from app.services.bank_service import BankService

from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime
import os
from functools import wraps

auth = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "bank-secret-key-123")


# ====================================
# TOKEN DECORATOR
# ====================================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401

        try:
            data = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = data

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


# ====================================
# REGISTER
# ====================================
@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (full_name,email,password,balance)
            VALUES (?,?,?,?)
            """,
            (full_name, email, hashed_password, 0),
        )

        conn.commit()

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400

    finally:
        conn.close()


# ====================================
# LOGIN
# ====================================
@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password"}), 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "email": user["email"],
            "is_admin": user["is_admin"],
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(hours=2),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify({
        "message": "Login successful",
        "token": token
    })


# ====================================
# BALANCE
# ====================================
@auth.route("/balance", methods=["GET"])
@token_required
def balance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE id=?",
        (request.user["user_id"],),
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "balance": user["balance"]
    })


# ====================================
# PROFILE
# ====================================
@auth.route("/profile", methods=["GET"])
@token_required
def profile():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,
               full_name,
               email,
               balance,
               is_admin
        FROM users
        WHERE id=?
        """,
        (request.user["user_id"],),
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user))


# ====================================
# DEPOSIT
# ====================================
@auth.route("/deposit", methods=["POST"])
@token_required
def deposit():

    data = request.get_json()

    try:
        amount = float(data["amount"])
    except:
        return jsonify({"error": "Invalid amount"}), 400

    result = BankService.deposit(
        request.user["user_id"],
        amount
    )

    return jsonify({
        "message": "Deposit successful",
        "new_balance": result
    })


# ====================================
# WITHDRAW
# ====================================
@auth.route("/withdraw", methods=["POST"])
@token_required
def withdraw():

    data = request.get_json()

    try:
        amount = float(data["amount"])
    except:
        return jsonify({"error": "Invalid amount"}), 400

    result = BankService.withdraw(
        request.user["user_id"],
        amount
    )

    if result == "INSUFFICIENT_FUNDS":
        return jsonify({"error": "Insufficient funds"}), 400

    return jsonify({
        "message": "Withdraw successful",
        "new_balance": result
    })


# ====================================
# TRANSACTIONS
# ====================================
@auth.route("/transactions", methods=["GET"])
@token_required
def transactions():

    rows = BankService.get_transactions(
        request.user["user_id"]
    )

    return jsonify([dict(r) for r in rows])


# ====================================
# TRANSFER
# ====================================
@auth.route("/transfer", methods=["POST"])
@token_required
def transfer():

    data = request.get_json()

    receiver_email = data.get("receiver_email")

    try:
        amount = float(data["amount"])
    except:
        return jsonify({"error": "Invalid amount"}), 400

    result = BankService.transfer(
        request.user["user_id"],
        receiver_email,
        amount
    )

    if result == "RECEIVER_NOT_FOUND":
        return jsonify({"error": "Receiver not found"}), 404

    if result == "SENDER_NOT_FOUND":
        return jsonify({"error": "Sender not found"}), 404

    if result == "INSUFFICIENT_FUNDS":
        return jsonify({"error": "Insufficient funds"}), 400

    return jsonify({
        "message": "Transfer successful",
        "new_balance": result
    })