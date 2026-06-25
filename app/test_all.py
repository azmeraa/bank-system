import requests

BASE_URL = "http://127.0.0.1:5000"

# =====================
# REGISTER
# =====================
print("\n=== REGISTER ===")

register_data = {
    "full_name": "Azmera",
    "email": "azmera@test.com",
    "password": "123456"
}

response = requests.post(
    f"{BASE_URL}/register",
    json=register_data
)

print(response.status_code)
print(response.json())

# =====================
# LOGIN
# =====================
print("\n=== LOGIN ===")

login_data = {
    "email": "azmera@test.com",
    "password": "123456"
}

response = requests.post(
    f"{BASE_URL}/login",
    json=login_data
)

print(response.status_code)
print(response.json())

token = response.json()["token"]

headers = {
    "Authorization": token
}

# =====================
# DEPOSIT
# =====================
print("\n=== DEPOSIT ===")

response = requests.post(
    f"{BASE_URL}/deposit",
    json={"amount": 1000},
    headers=headers
)

print(response.status_code)
print(response.json())

# =====================
# WITHDRAW
# =====================
print("\n=== WITHDRAW ===")

response = requests.post(
    f"{BASE_URL}/withdraw",
    json={"amount": 200},
    headers=headers
)

print(response.status_code)
print(response.json())

# =====================
# TRANSACTIONS
# =====================
print("\n=== TRANSACTIONS ===")

response = requests.get(
    f"{BASE_URL}/transactions",
    headers=headers
)

print(response.status_code)
print(response.json())