![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-API-black)
![JWT](https://img.shields.io/badge/Auth-JWT-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

# 🏦 Banking System API (Flask + JWT + RBAC)

A secure backend banking system built with Flask featuring JWT authentication, role-based access control (Admin/User), and modular architecture.

---

## 🚀 Features

- 👤 User registration & login
- 🔐 JWT authentication system
- 🛡️ Role-based access control (Admin / User)
- 💳 Banking operations (deposit, withdraw, transfer, balance)
- 🔒 Protected routes with middleware security
- 🧱 Modular backend architecture
- 📊 RESTful API design



## 🛠 Tech Stack

- Python 🐍
- Flask 🌶️
- Flask-JWT-Extended 🔐
- SQLite 🗄️
- REST API architecture


## 📁 Project Structure


bank-system/
│
├── app/
│ ├── routes/ # API endpoints
│ ├── models/ # Database models
│ ├── services/ # Business logic
│ ├── utils/ # Helper functions
│
├── main.py # Entry point
├── requirements.txt
├── .gitignore
└── README.md


## ▶️ How to Run

```bash
git clone https://github.com/azmeraa/bank-system.git
cd bank-system
pip install -r requirements.txt
python main.py
📌 API Endpoints
🔐 Authentication
Register User
POST /register
Content-Type: application/json

{
  "username": "john",
  "password": "1234"
}
Login User
POST /login
Content-Type: application/json

{
  "username": "john",
  "password": "1234"
}

Response:

{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
💳 Banking Operations
Get Balance
GET /balance
Authorization: Bearer <token>
Deposit Money
POST /deposit
Authorization: Bearer <token>

{
  "amount": 1000
}
Withdraw Money
POST /withdraw
Authorization: Bearer <token>

{
  "amount": 500
}
Transfer Money
POST /transfer
Authorization: Bearer <token>

{
  "to_user": "john",
  "amount": 200
}
🧠 System Architecture

This project follows a modular layered architecture:

Routes Layer → API endpoints
Services Layer → Business logic
Models Layer → Database schema
Utils Layer → JWT & helpers
🔁 Request Flow

Client → Route → Service → Database → Response

💼 Key Learnings
Flask REST API development
JWT authentication system
Role-based access control (RBAC)
Backend architecture design
Secure financial transaction logic
