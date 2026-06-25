from functools import wraps
from flask import request, jsonify


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # Check if user is logged in via jwt_required
        if not hasattr(request, "user_id"):
            return jsonify({"message": "Unauthorized"}), 401

        # Check admin role
        if getattr(request, "is_admin", 0) != 1:
            return jsonify({"message": "Admin access required"}), 403

        return f(*args, **kwargs)

    return decorated