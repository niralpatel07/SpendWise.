import json
import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

CURRENCY = "$"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

CATEROGIES = {
    "food":       {"label":  "Food",      "emoji":  "🍔", "color": "#f97316"},
    "transport":  {"label":  "Transport", "emoji":  "🚌", "color": "#3b82f6"},
    "fun":        {"label":  "Fun",       "emoji":  "🎮", "color": "#a855f7"},
    "shopping":   {"label":  "Shopping",  "emoji":  "🛍️", "color": "#ec4899"},
    "bills":      {"label":  "Bills",     "emoji":  "🧾", "color": "#eab308"},
    "income":     {"label":  "Income",    "emoji":  "💰", "color": "#16a34a"},
}
EXPENSE_CATS = [key for key in CATEROGIES if key != "income"]

DEFAULT_TRANSACTIONS = [
    {"id": 1, "title": "Paycheck",    "amount": 220.00, "type": "income",  "category": "income",     "date": "2026-10-30"},
    {"id": 2, "title": "Groceries",   "amount": 42.50,  "type": "expense", "category": "food",       "date": "2026-10-31"},
    {"id": 3, "title": "Presto Card", "amount": 30.00,  "type": "expense", "category": "transport",  "date": "2026-11-01"},
    {"id": 4, "title": "Movie night", "amount": 18.75,  "type": "expense", "category": "fun",        "date": "2026-11-02"},
    {"id": 5, "title": "Phone bill",  "amount": 18.75,  "type": "expense", "category": "bills",      "date": "2026-11-03"},
]

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data["transactions"], data["next_id"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return [dict(t) for t in DEFAULT_TRANSACTIONS], 6

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"transactions": transactions, "next_id": next_id}, f, indent=2)

transactions, next_id = load_data()

def totals(items):
    income = sum(t["amount"] for t in items if t["type"] == "income")
    spent = sum(t["amount"] for t in items if t["type"] == "expense")
    return income, spent, income - spent

@app.route("/")
def home():
    income, spent, balance = totals(transactions)
    recent = sorted(transactions, key = lambda t: (t["date"], t["id"]), reverse=True)
    return render_template( 
        "index.html",
        transactions=recent,
        categories=CATEROGIES,
        expense_cats=EXPENSE_CATS,
        currency=CURRENCY,
        income=income,
        spent=spent,
        balance=balance,
        month=date.today().strftime("%B %Y"),
        today=date.today().isoformat(),
    ) 

@app.route("/add", methods=["POST"])
def add():
    global next_id
    title = request.form.get("title", "").strip()
    try:
        amount = round(float(request.form.get("amount", 0)), 2)
    except ValueError:
        amount = 0 
    kind = request.form.get("type", "expense")
    category = request.form.get("category", "food")
    when = request.form.get("date") or date.today().isoformat()

    if kind == "income":
        category = "income"
    else:
        kind = "expense"

    if title and amount > 0 and category in CATEROGIES:
        transactions.append({
            "id": next_id,
            "title": title,
            "amount": amount,
            "type": kind,
            "category": category,
            "date": when,
        })
        next_id += 1
        save_data()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
