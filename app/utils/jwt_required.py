from functools import wraps
from flask import request, jsonify
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "bank-secret-key-123")


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # Bearer TOKEN
            except:
                return jsonify({"message": "Token format invalid"}), 401

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # =========================
            # 🔐 Attach user info to request
            # =========================
            request.user_id = data.get("user_id")
            request.is_admin = data.get("is_admin", 0)

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 401

        return f(*args, **kwargs)

    return decorated