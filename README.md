# SpendWise.

This website was built using Python and Flask. You can log in your income and expenses and view where you're spending your money, what you have left of your monthly budget as well as if any of your categories are over the limit.

Demo link: [https://niralpatel.pythonanywhere.com/?msg=budget]

I created this as part of my first week project for Hack Club Terra.

## Why I created this
I wanted an easier way to track my money rather than using a spreadsheet. I also wanted to play around with charts.

## Features and How to use
Adding transactions

1. Click on the 'Add Transaction' card. Select either 'Expense' or 'Income'.
2. Enter the details of your transaction including its name, value and date (defaults to today).
3. If it is an expense category, select a category. No categories are needed for income.
4. Press 'Add'. A prompt will appear and the balance and charts will also be updated.
Editing/deletions

Press ✏️ to edit any row. After editing press 'Save changes'.
To delete, press 🗑️ and it will ask to confirm.
Searching

Search for a transaction using the search bar.
Clicking on any category chip (🍔 Food, 🚌 Transport etc) will filter to just that category. To view all swipe left/right on the row.
Clicking on the month drop down will allow you to view just one month. This will also change the balance, income and spent cards.
Clicking 'Clear Filters' will return you to all.

Understanding Charts
The pie chart will show you how much you have spent in each category. The total can be seen in the centre.
Hover/tap on any slice to highlight it. Use the legend at the bottom to see precise values.
Setting Budgets

Type in the amount you want your budget to be for the month in the budget card and click 'Set'.
The bar will fill up as you spend. If you go over it will turn red with 'Over by...'.

Setting Category Limits
Click on 🎯 Set category limits.
Enter in a limit for any category. Leave the rest blank. Click 'Save limits'.
Each category will have its own little bar. This will show your limit for the month displayed in the budget card. Click on the drop down to change the month.

Exporting Data
Click on ⬇️ Export CSV to download all of your transactions.

## Code breakdown
`app.py` contains the routes, filtering, data for the chart and saving.
`templates/index.html` is the main page. `templates/edit.html` is the edit page.
`static/style.css` has all of the styling.
`data.json`, `budget.json` and `limits.json` are automatically created when using this.
This was built using Python, Flask, Jinja, HTML, CSS and JavaScript. Chart.js was used for the chart. The website is hosted on PythonAnywhere.

## Things to know
There are no accounts so anyone viewing the live demo will see the same list. Please don't input any personal information.
As it is free to host, I need to renew it each month. This means that the demo may go down if I don't remember.
JSON files are good for a small project but would not work for many users.

## What I learnt
How routing works in Flask. How to use dynamic URLs such as '/edit/3'.
How to include filters in the URL (e.g. ?month=2026-11&cat=food) and then read them in Python.
How to send data from Python to JavaScript so that Chart.js can display it.
How to create a downloadable file in Flask.
How to read a traceback from the bottom up. Most of my bugs were small errors. For example, if I had a replace all function and replaced 'categories' with 'CATEGORIES' it broke my templates.

It took a few attempts to deploy. When I deployed FocusList for the first time on Vercel, it didn't work as it can't save files. So I decided to use PythonAnywhere from the start.

## What I would improve
Dark mode
Private list for each visitor
Chart comparing income and spend each month.
Actual database instead of JSON files

-------
 Niral