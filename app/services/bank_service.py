from database import get_connection


class BankService:

    # =========================
    # 💰 DEPOSIT
    # =========================
    @staticmethod
    def deposit(user_id, amount):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return None

        new_balance = user["balance"] + amount

        cursor.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (new_balance, user_id)
        )

        cursor.execute("""
            INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
            VALUES (?, ?, ?, ?)
        """, (user_id, "deposit", amount, new_balance))

        conn.commit()
        conn.close()

        return new_balance


    # =========================
    # 💸 WITHDRAW
    # =========================
    @staticmethod
    def withdraw(user_id, amount):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            return None

        current_balance = user["balance"]

        if current_balance < amount:
            conn.close()
            return "INSUFFICIENT_FUNDS"

        new_balance = current_balance - amount

        cursor.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (new_balance, user_id)
        )

        cursor.execute("""
            INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
            VALUES (?, ?, ?, ?)
        """, (user_id, "withdraw", amount, new_balance))

        conn.commit()
        conn.close()

        return new_balance


    # =========================
    # 📊 TRANSACTION HISTORY
    # =========================
    @staticmethod
    def get_transactions(user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT transaction_type, amount, balance_after, timestamp
            FROM transactions
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()

        return rows


    # =========================
    # 💸 TRANSFER MONEY (NEW)
    # =========================
    @staticmethod
    def transfer(sender_id, receiver_email, amount):
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Get sender
        cursor.execute("SELECT balance FROM users WHERE id = ?", (sender_id,))
        sender = cursor.fetchone()

        if not sender:
            conn.close()
            return "SENDER_NOT_FOUND"

        # 2. Check sender balance
        if sender["balance"] < amount:
            conn.close()
            return "INSUFFICIENT_FUNDS"

        # 3. Get receiver
        cursor.execute("SELECT id, balance FROM users WHERE email = ?", (receiver_email,))
        receiver = cursor.fetchone()

        if not receiver:
            conn.close()
            return "RECEIVER_NOT_FOUND"

        # 4. Update balances
        sender_new_balance = sender["balance"] - amount
        receiver_new_balance = receiver["balance"] + amount

        cursor.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (sender_new_balance, sender_id)
        )

        cursor.execute(
            "UPDATE users SET balance = ? WHERE id = ?",
            (receiver_new_balance, receiver["id"])
        )

        # 5. Log sender transaction
        cursor.execute("""
            INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
            VALUES (?, ?, ?, ?)
        """, (sender_id, "transfer_out", amount, sender_new_balance))

        # 6. Log receiver transaction
        cursor.execute("""
            INSERT INTO transactions (user_id, transaction_type, amount, balance_after)
            VALUES (?, ?, ?, ?)
        """, (receiver["id"], "transfer_in", amount, receiver_new_balance))

        conn.commit()
        conn.close()

        return sender_new_balance