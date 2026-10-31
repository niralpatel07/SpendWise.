from datetime import date
from flask import Flask, render_template

app = Flask(__name__)

CURRENCY = "$"

CATEROGIES = {
    "food":       {"label":  "Food",      "emoji":  "🍔", "color": "#f97316"},
    "transport":  {"label":  "Transport", "emoji":  "🚌", "color": "#3b82f6"},
    "fun":        {"label":  "Fun",       "emoji":  "🎮", "color": "#a855f7"},
    "shopping":   {"label":  "Shopping",  "emoji":  "🛍️", "color": "#ec4899"},
    "bills":      {"label":  "Bills",     "emoji":  "🧾", "color": "#eab308"},
    "income":     {"label":  "Income",    "emoji":  "💰", "color": "#16a34a"},
}

SAMPLE = [
    {"id": 1, "title": "Paycheck",    "amount": 220.00, "type": "income",  "category": "income",     "date": "2026-10-30"},
    {"id": 2, "title": "Groceries",   "amount": 42.50,  "type": "expense", "category": "food",       "date": "2026-10-31"},
    {"id": 3, "title": "Presto Card", "amount": 30.00,  "type": "expense", "category": "transport",  "date": "2026-11-01"},
    {"id": 4, "title": "Movie night", "amount": 18.75,  "type": "expense", "category": "fun",        "date": "2026-11-02"},
    {"id": 5, "title": "Phone bill",  "amount": 18.75,  "type": "expense", "category": "bills",      "date": "2026-11-03"},
]

def totals(items):
    income = sum(t["amount"] for t in items if t["type"] == "income")
    spent = sum(t["amount"] for t in items if t["type"] == "expense")
    return income, spent, income - spent

@app.route("/")
def home():
    income, spent, balance = totals(SAMPLE)
    recent = sorted(SAMPLE, key = lambda t: t["date"], reverse=True)
    return render_template( 
        "index.html",
        transactions=recent,
        categories=CATEROGIES,
        currency=CURRENCY,
        income=income,
        spent=spent,
        balance=balance,
        month=date.today().strftime("%B %Y"),
    ) 

if __name__ == "__main__":
    app.run(debug=True)
