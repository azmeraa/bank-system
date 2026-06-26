from flask import Flask, jsonify
import os

# =========================
# App Imports
# =========================
from app.models import create_tables
from app.routes.auth import auth
from app.routes.banking import banking
from app.routes.admin import admin

from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# =========================
# Load environment variables
# =========================
load_dotenv()

# =========================
# Secret Key
# =========================
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "bank-secret-key-123"
)

# =========================
# Database setup
# =========================
with app.app_context():
    print("Creating database tables...")
    create_tables()
    print("Database ready!")

# =========================
# Register Blueprints
# =========================
app.register_blueprint(auth)
app.register_blueprint(banking)
app.register_blueprint(admin)

# =========================
# Swagger UI
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
# Swagger JSON
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
            "/": {
                "get": {
                    "summary": "Health Check"
                }
            },
            "/register": {
                "post": {
                    "summary": "Register User"
                }
            },
            "/login": {
                "post": {
                    "summary": "Login User"
                }
            },
            "/deposit": {
                "post": {
                    "summary": "Deposit Money",
                    "security": [{"bearerAuth": []}]
                }
            },
            "/withdraw": {
                "post": {
                    "summary": "Withdraw Money",
                    "security": [{"bearerAuth": []}]
                }
            },
            "/transfer": {
                "post": {
                    "summary": "Transfer Money",
                    "security": [{"bearerAuth": []}]
                }
            },
            "/transactions": {
                "get": {
                    "summary": "Transaction History",
                    "security": [{"bearerAuth": []}]
                }
            },
            "/admin/users": {
                "get": {
                    "summary": "Get All Users",
                    "security": [{"bearerAuth": []}]
                }
            },
            "/admin/transactions": {
                "get": {
                    "summary": "Get All Transactions",
                    "security": [{"bearerAuth": []}]
                }
            }
        },
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
# Home Route
# =========================
@app.route("/")
def home():
    return jsonify({
        "message": "Bank System API is running"
    })


# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)