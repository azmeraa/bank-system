from app.database import get_connection


class BankService:

    @staticmethod
    def deposit(user_id, amount):

        if amount <= 0:
            return "INVALID_AMOUNT"

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance FROM users WHERE id = ?",
                (user_id,)
            )

            user = cursor.fetchone()

            if not user:
                return "USER_NOT_FOUND"

            new_balance = user["balance"] + amount

            cursor.execute(
                "UPDATE users SET balance = ? WHERE id = ?",
                (new_balance, user_id)
            )

            cursor.execute("""
                INSERT INTO transactions
                (user_id, transaction_type, amount, balance_after)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                "deposit",
                amount,
                new_balance
            ))

            conn.commit()

            return new_balance

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()


    @staticmethod
    def withdraw(user_id, amount):

        if amount <= 0:
            return "INVALID_AMOUNT"

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance FROM users WHERE id = ?",
                (user_id,)
            )

            user = cursor.fetchone()

            if not user:
                return "USER_NOT_FOUND"

            if user["balance"] < amount:
                return "INSUFFICIENT_FUNDS"

            new_balance = user["balance"] - amount

            cursor.execute(
                "UPDATE users SET balance = ? WHERE id = ?",
                (new_balance, user_id)
            )

            cursor.execute("""
                INSERT INTO transactions
                (user_id, transaction_type, amount, balance_after)
                VALUES (?, ?, ?, ?)
            """, (
                user_id,
                "withdraw",
                amount,
                new_balance
            ))

            conn.commit()

            return new_balance

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()


    @staticmethod
    def get_transactions(user_id):

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    transaction_type,
                    amount,
                    balance_after,
                    timestamp
                FROM transactions
                WHERE user_id = ?
                ORDER BY timestamp DESC
            """, (user_id,))

            return cursor.fetchall()

        finally:
            conn.close()


    @staticmethod
    def transfer(sender_id, receiver_email, amount):

        if amount <= 0:
            return "INVALID_AMOUNT"

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT balance FROM users WHERE id = ?",
                (sender_id,)
            )

            sender = cursor.fetchone()

            if not sender:
                return "SENDER_NOT_FOUND"

            if sender["balance"] < amount:
                return "INSUFFICIENT_FUNDS"

            cursor.execute(
                "SELECT id, balance FROM users WHERE email = ?",
                (receiver_email,)
            )

            receiver = cursor.fetchone()

            if not receiver:
                return "RECEIVER_NOT_FOUND"

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

            cursor.execute("""
                INSERT INTO transactions
                (user_id, transaction_type, amount, balance_after)
                VALUES (?, ?, ?, ?)
            """, (
                sender_id,
                "transfer_out",
                amount,
                sender_new_balance
            ))

            cursor.execute("""
                INSERT INTO transactions
                (user_id, transaction_type, amount, balance_after)
                VALUES (?, ?, ?, ?)
            """, (
                receiver["id"],
                "transfer_in",
                amount,
                receiver_new_balance
            ))

            conn.commit()

            return sender_new_balance

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()