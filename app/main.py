from flask import Flask, jsonify
from models import create_tables
from routes.auth import auth
from routes.banking import banking
from routes.admin import admin   # 👑 ADDED (admin system)

from dotenv import load_dotenv
import os

from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# =========================
# Load environment variables
# =========================
load_dotenv()

# =========================
# SECRET KEY (JWT)
# =========================
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "bank-secret-key-123")

# =========================
# Database setup
# =========================
with app.app_context():
    print("Creating database tables...")
    create_tables()
    print("Database ready!")

# =========================
# Register blueprints
# =========================
app.register_blueprint(auth)
app.register_blueprint(banking)
app.register_blueprint(admin)   # 👑 ADDED

# =========================
# Swagger UI Setup
# =========================
SWAGGER_URL = "/docs"
API_URL = "/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Bank System API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# =========================
# Swagger JSON (API documentation)
# =========================
@app.route("/swagger.json")
def swagger_json():
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Banking System API",
            "version": "1.0",
            "description": "Secure Banking Backend API using Flask + JWT + Admin System"
        },

        "paths": {

            # =========================
            # 🏠 HEALTH CHECK
            # =========================
            "/": {
                "get": {
                    "summary": "Health check",
                    "responses": {
                        "200": {
                            "description": "API is running"
                        }
                    }
                }
            },

            # =========================
            # 👤 AUTH
            # =========================
            "/register": {
                "post": {
                    "summary": "Register new user"
                }
            },

            "/login": {
                "post": {
                    "summary": "Login user and return JWT token"
                }
            },

            # =========================
            # 💰 BANKING
            # =========================
            "/deposit": {
                "post": {
                    "summary": "Deposit money",
                    "security": [{"bearerAuth": []}]
                }
            },

            "/withdraw": {
                "post": {
                    "summary": "Withdraw money",
                    "security": [{"bearerAuth": []}]
                }
            },

            "/transfer": {
                "post": {
                    "summary": "Transfer money to another user",
                    "security": [{"bearerAuth": []}]
                }
            },

            "/transactions": {
                "get": {
                    "summary": "Get transaction history",
                    "security": [{"bearerAuth": []}]
                }
            },

            # =========================
            # 👑 ADMIN
            # =========================
            "/admin/users": {
                "get": {
                    "summary": "Get all users (Admin only)",
                    "security": [{"bearerAuth": []}]
                }
            },

            "/admin/transactions": {
                "get": {
                    "summary": "Get all transactions (Admin only)",
                    "security": [{"bearerAuth": []}]
                }
            }
        },

        # =========================
        # 🔐 JWT SECURITY
        # =========================
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }


# =========================
# 🏠 Home route
# =========================
@app.route("/")
def home():
    return jsonify({"message": "Bank System API is running"})


if __name__ == "__main__":
    app.run(debug=True)