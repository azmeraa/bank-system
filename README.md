# 🏦 Banking System API (Flask + JWT + Admin Role System)

A secure backend banking system built with **Flask**, featuring authentication, role-based authorization, and full banking operations (deposit, withdraw, transfer, transaction history) with Swagger API documentation.

---

## 🚀 Features

### 🔐 Authentication
- User registration
- Login with JWT token
- Secure password handling

### 👤 Authorization
- Role-based access control
- User vs Admin roles
- Protected routes using JWT

### 💰 Banking System
- Deposit money
- Withdraw money
- Transfer funds between users
- Transaction history tracking

### 👑 Admin Features
- View all users
- View all transactions
- Admin-only access control

### 📚 API Documentation
- Swagger UI available at `/docs`
- OpenAPI 3.0 specification
- Fully documented endpoints

---

## 🧱 Tech Stack

- Python 🐍
- Flask 🌶️
- SQLite 🗄️
- JWT Authentication 🔐
- Flask Swagger UI 📚
- Dotenv ⚙️

---

## 📁 Project Structure
  backend/
     └── app/
        ├── routes/ # API endpoints
        ├── services/ # Business logic
        ├── utils/ # Security (JWT, decorators)
        ├── models.py # Database models
        ├── database.py # DB connection/setup
        ├── main.py # App entry point


---

##Installation & Setup

### 1️#Clone repository
```bash
git clone https://github.com/your-username/bank-system.git
cd bank-system/backend/app
 2️#Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️#Install dependencies
 ----bash
pip install -r requirements.txt
4#Run application
----bash
python main.py

🌐 API Endpoints
🔐 Auth
POST /register → Register user
POST /login → Login & get JWT
💰 Banking
POST /deposit → Deposit money
POST /withdraw → Withdraw money
POST /transfer → Transfer funds
GET /transactions → Transaction history
👑 Admin
GET /admin/users → View all users
GET /admin/transactions → View all transactions
📚 API Documentation (Swagger)

After running the project:

http://127.0.0.1:5000/docs
🔐 Security Features
JWT authentication
Role-based access control
Admin-only decorators
Protected banking routes
🧠 System Design

This project follows a layered backend architecture:

Routes → API layer
Services → Business logic
Utils → Security logic
Models → Database layer