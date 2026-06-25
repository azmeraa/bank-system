from flask import Blueprint, request, jsonify
from utils.jwt_required import jwt_required
from services.bank_service import BankService

banking = Blueprint("banking", __name__)


# =========================
# 💰 DEPOSIT MONEY
# =========================
@banking.route("/deposit", methods=["POST"])
@jwt_required
def deposit():
    data = request.get_json()

    if not data or "amount" not in data:
        return jsonify({"message": "Amount is required"}), 400

    try:
        amount = float(data["amount"])
    except:
        return jsonify({"message": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"message": "Amount must be greater than 0"}), 400

    result = BankService.deposit(request.user_id, amount)

    if not result:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "message": "Deposit successful",
        "new_balance": result
    })


# =========================
# 💸 WITHDRAW MONEY
# =========================
@banking.route("/withdraw", methods=["POST"])
@jwt_required
def withdraw():
    data = request.get_json()

    if not data or "amount" not in data:
        return jsonify({"message": "Amount is required"}), 400

    try:
        amount = float(data["amount"])
    except:
        return jsonify({"message": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"message": "Amount must be greater than 0"}), 400

    result = BankService.withdraw(request.user_id, amount)

    if result == "INSUFFICIENT_FUNDS":
        return jsonify({"message": "Insufficient funds"}), 400

    if not result:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "message": "Withdraw successful",
        "new_balance": result
    })


# =========================
# 📊 TRANSACTION HISTORY
# =========================
@banking.route("/transactions", methods=["GET"])
@jwt_required
def transactions():
    rows = BankService.get_transactions(request.user_id)

    return jsonify([
        {
            "type": r["transaction_type"],
            "amount": r["amount"],
            "balance_after": r["balance_after"],
            "timestamp": r["timestamp"]
        }
        for r in rows
    ])


# =========================
# 💸 TRANSFER MONEY (NEW)
# =========================
@banking.route("/transfer", methods=["POST"])
@jwt_required
def transfer():
    data = request.get_json()

    if not data or "email" not in data or "amount" not in data:
        return jsonify({"message": "email and amount are required"}), 400

    try:
        amount = float(data["amount"])
    except:
        return jsonify({"message": "Invalid amount"}), 400

    if amount <= 0:
        return jsonify({"message": "Amount must be greater than 0"}), 400

    result = BankService.transfer(
        request.user_id,
        data["email"],
        amount
    )

    if result == "RECEIVER_NOT_FOUND":
        return jsonify({"message": "Receiver not found"}), 404

    if result == "SENDER_NOT_FOUND":
        return jsonify({"message": "Sender not found"}), 404

    if result == "INSUFFICIENT_FUNDS":
        return jsonify({"message": "Insufficient funds"}), 400

    return jsonify({
        "message": "Transfer successful",
        "new_balance": result
    })