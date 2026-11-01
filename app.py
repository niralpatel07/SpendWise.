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

MESSAGES = {
    "added": "Transaction added successfully!✅",
    "saved": "Changes saved ☑️",
    "deleted": "Deleted 🗑",
}

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

def find(tid):
    for t in transactions:
        if t["id"] == tid:
            return t
    return None

def read_form(): 
    title = request.form.get("title", "").strip()
    try:
        amount = round(float(request.form.get("amount", 0)), 2)
    except ValueError:
        amount = 0 
    kind = "income" if request.form.get("type") == "income" else "expense"
    category = "income" if kind == "income" else request.form.get("category", "food")
    when = request.form.get("date") or date.today().isoformat()

    if title and amount > 0 and category in CATEROGIES:
        return {"title": title, "amount": amount, "type": kind,
                "category": category, "date": when}
    return None

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
        toast=MESSAGES.get(request.args.get("msg")),
    ) 

@app.route("/add", methods=["POST"])
def add():
    global next_id
    data = read_form()
    if data:
        data["id"] = next_id
        next_id += 1
        transactions.append(data)
        save_data()
        return redirect(url_for("home", msg="added"))
    return redirect(url_for("home", msg="invalid"))

@app.route("/edit/<int:tid>", methods=["GET", "POST"])
def edit(tid):
    t = find(tid)
    if t is None:
        return redirect(url_for("home"))
    if request.method == "POST":
        data = read_form()
        if data:
            t.update(data)
            save_data()
            return redirect(url_for("home", msg="saved"))
    return render_template(
        "edit.html",
        t=t,
        categories=CATEROGIES,
        expense_cats=EXPENSE_CATS,
    )

@app.route("/delete/<int:tid>", methods=["POST"])
def delete(tid):
    global transactions
    transactions = [t for t in transactions if t["id"] != tid]
    save_data()
    return redirect(url_for("home", msg="deleted"))
    
if __name__ == "__main__":
    app.run(debug=True)
