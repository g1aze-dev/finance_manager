import requests

API_URL = "http://localhost:5000/api/transactions"

def get_transactions():
    response = requests.get(API_URL)
    return response.json()

def add_transaction(amount, category, date, transaction_type, description=""):
    requests.post(API_URL, json={
        "amount": amount,
        "category": category,
        "date": date,
        "type": transaction_type,
        "description": description
    })

def delete_transaction(category, date, transaction_type):
    requests.delete(API_URL, json={
        "category": category,
        "date": date,
        "type": transaction_type,
        
    })