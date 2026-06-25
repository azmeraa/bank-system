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
- `POST /login` → Login and get JWT token  

### 💳 Banking
- `GET /balance` → View account balance  
- `POST /deposit` → Add money  
- `POST /withdraw` → Withdraw money  
- `POST /transfer` → Transfer money  