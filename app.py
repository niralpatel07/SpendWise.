import csv
import io
import json
import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, Response

app = Flask(__name__)

CURRENCY = "$"
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
BUDGET_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "budget.json")

LIMITS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "limits.json")

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
    "budget": "Budget updated 💰",
    "limits": "Category limits saved 🚨",
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

def load_budget():
    try:
        with open(BUDGET_FILE, "r") as f:
            return float(json.load(f)["budget"])
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
        return 200.0

def save_budget(value):
    with open(BUDGET_FILE, "w") as f:
        json.dump({"budget": value}, f)
def month_options():
    keys = sorted({t["date"][:7] for t in transactions}, reverse=True)
    result = []
    for key in keys:
        year, month = key.split("-")
        label = date(int(year), int(month), 1).strftime("%B %Y")
        result.append({"key": key, "label": label})
    return result

def load_limits():
    try:
        with open(LIMITS_FILE, "r") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_limits(limits):
    with open(LIMITS_FILE, "w") as f:
        json.dump(limits, f)

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

    f_month = request.args.get("month", "all")
    f_cat = request.args.get("cat", "all")
    q = request.args.get("q", "").strip()
    by_cat = {}
    for t in transactions:
        if t["type"] == "expense" and (f_month == "all" or t["date"].startswith(f_month)):
            by_cat[t["category"]] = by_cat.get(t["category"], 0) + t["amount"]
    chart_data = [
        {
            "label": CATEROGIES[k]["label"],
            "emoji": CATEROGIES[k]["emoji"],
            "color": CATEROGIES[k]["color"],
            "amount": round(v, 2),
        }
        for k, v in sorted(by_cat.items(), key=lambda kv: kv[1], reverse=True)
    ]
    chart_total = round(sum(d["amount"] for d in chart_data), 2)
    months_sorted = sorted({t["date"][:7] for t in transactions})[-6:]
    bar_labels,bar_income, bar_spent = [], [], []
    for key in months_sorted:
        yy, mm = key.split("-")
        bar_labels.append(date(int(yy), int(mm), 1).strftime("%b"))
        inc,sp, _ = totals([t for t in transactions if t["date"].startswith(key)])
        bar_income.append(round(inc, 2))
        bar_spent.append(round(sp, 2))

    b_key = f_month if f_month != "all" else date.today().strftime("%Y-%m")
    b_year, b_mon = b_key.split("-")
    b_label = date(int(b_year), int(b_mon), 1).strftime("%B")
    b_spent = totals([t for t in transactions if t["date"].startswith(b_key)])[1]
    budget = load_budget()
    budget_pct = min(round(b_spent / budget * 100), 100)
    budget_over = b_spent > budget
    limits = load_limits()
    limit_rows = []
    for key in EXPENSE_CATS:
        lim = limits.get(key)
        if lim:
            sp = sum(t["amount"] for t in transactions
                    if t["type"] == "expense" and t["category"] == key and t["date"].startswith(b_key))
            limit_rows.append({
                "label": CATEROGIES[key]["label"],
                "emoji": CATEROGIES[key]["emoji"],
                "spent": round(sp, 2),
                "limit": lim,
                "pct": min(round(sp / lim * 100), 100),                    
                "over": sp > lim,
            })
                    
    in_month = [t for t in transactions if f_month == "all" or t["date"].startswith(f_month)]
    income, spent, balance = totals(in_month)
    if f_month == "all":
        hero_label = "All time"
    else:
        y, m = f_month.split("-")
        hero_label = date(int(y), int(m), 1).strftime("%B %Y")


    shown = sorted(transactions, key=lambda t: (t["date"], t["id"]), reverse=True)
    if f_month != "all":
        shown = [t for t in shown if t["date"].startswith(f_month)]
    if f_cat != "all":
        shown = [t for t in shown if t["category"] == f_cat]
    if q:
        shown = [t for t in shown if q.lower() in t["title"].lower()]

    shown_income, shown_spent, shown_net = totals(shown)
    filtered = f_month != "all" or f_cat != "all" or bool(q)

    return render_template( 
        "index.html",
        transactions=shown,
        categories=CATEROGIES,
        expense_cats=EXPENSE_CATS,
        currency=CURRENCY,
        income=income,
        spent=spent,
        balance=balance,
        month=date.today().strftime("%B %Y"),
        hero_label=hero_label,
        today=date.today().isoformat(),
        toast=MESSAGES.get(request.args.get("msg")),
        months=month_options(),
        f_month=f_month,
        f_cat=f_cat,
        q=q,
        chart_data=chart_data,
        chart_total=chart_total,
        bar_labels=bar_labels,
        bar_income=bar_income,
        bar_spent=bar_spent,
        b_label=b_label,
        b_spent=b_spent,
        budget=budget,
        budget_pct=budget_pct,
        budget_over=budget_over,
        limits=limits,
        limit_rows=limit_rows,
        filtered=filtered,
        shown_spent=shown_spent,
        shown_income=shown_income,
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
    
@app.route("/budget", methods=["POST"])
def set_budget():
    try:
        value = round(float(request.form.get("budget", 0)), 2)
    except ValueError:
        value = 0
    if value > 0:
        save_budget(value)
        return redirect(url_for("home", msg="budget"))
    return redirect(url_for("home"))

@app.route("/limits", methods=["POST"])
def set_limits():
    limits = {}
    for key in EXPENSE_CATS:
        try:
            value = round(float(request.form.get(key, "")), 2)
        except ValueError:
            continue
        if value > 0:
            limits[key] = value
    save_limits(limits)
    return redirect(url_for("home", msg="limits"))

@app.route("/export.csv")
def export_csv():
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["Date", "Title", "Category", "Type", "Amount"])
    for t in sorted(transactions, key=lambda t: (t["date"], t["id"])):
        title = t["title"]
        if title.startswith(("=", "+", "-", "@")):
            title = "'" + title
        writer.writerow([t["date"], title, CATEROGIES[t["category"]]["label"], t["type"], "%.2f" % t["amount"]])
    return Response(
        out.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"}
    )

if __name__ == "__main__":
    app.run(debug=True)
