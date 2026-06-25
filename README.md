
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-API-black)
![JWT](https://img.shields.io/badge/Auth-JWT-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)

# 🏦 Banking System API (Flask + JWT + Role-Based Access)

A secure backend banking system built with **Flask**, featuring JWT authentication, role-based access control (Admin/User), and modular API architecture.

---

## 🚀 Features

- 👤 User registration & login
- 🔐 JWT authentication system
- 🛡️ Role-based access control (Admin / User)
- 💳 Banking operations API (deposit, withdraw, balance, transfer)
- 🔒 Secure endpoints with authorization middleware
- 🧱 Clean modular backend structure
- 📊 Scalable REST API design

---

## 🛠 Tech Stack

- Python 🐍
- Flask 🌶️
- Flask-JWT-Extended 🔐
- SQLite (or database used)
- RESTful API design

---

## 📁 Project Structure

bank-system/
│
├── app/
│ ├── routes/ # API endpoints
│ ├── models/ # Database models
│ ├── utils/ # Helper functions
│ ├── services/ # Business logic
│
├── main.py # Application entry point
├── requirements.txt # Dependencies
├── .gitignore
└── README.md
---

## ▶️ How to Run

```bash
git clone https://github.com/azmeraa/bank-system.git
cd bank-system
pip install -r requirements.txt
python main.py

## 📌 API Endpoints

### 🔐 Auth
- `POST /register` → Create new user  
## 📌 API Request Examples

### 🔐 Register User
```bash
POST /register
Content-Type: application/json

{
  "username": "john",
  "password": "1234"
}
- `POST /login` → Login and get JWT token  
POST /login
Content-Type: application/json

{
  "username": "john",
  "password": "1234"
}
{
  "token": "eyJhbGciOiJIUzI1NiIs..."
}

### 💳 Banking
- `GET /balance` → View account balance  
- `POST /deposit` → Add money  
POST /deposit
Authorization: Bearer <token>

{
  "amount": 1000
}
- `POST /withdraw` → Withdraw money  
- `POST /transfer` → Transfer money  

---

# 🧠 3. ARCHITECTURE SECTION (INTERVIEW GOLD)

Add this:

```md id="arch"
## 🧠 System Architecture

This project follows a **modular layered backend architecture**:

- **Routes Layer** → Handles API endpoints
- **Services Layer** → Business logic (banking operations)
- **Models Layer** → Database structure
- **Utils Layer** → Helper functions (JWT, validation)

### 🔁 Request Flow

Client → Flask Route → Service Layer → Database → Response

This separation ensures:
- Clean code
- Scalability
- Easy debugging
- Maintainability

## 💼 What I Learned

- Building REST APIs with Flask
- Implementing JWT authentication
- Role-based access control (RBAC)
- Structuring backend projects professionally
- Writing modular and scalable code
- Handling secure financial operations logic