# SpendWise.

# SpendWise

This website was built using Python and Flask. You can log in your income and expenses and view where you're spending your money, what you have left of your monthly budget as well as if any of your categories are over the limit.

Live demo: [Paste your PythonAnywhere link here]

I created this as part of my first week project for Hack Club Terra.

## Why I created this
I wanted an easier way to track my money rather than using a spreadsheet. I also wanted to play around with charts.
## Features

Add income and expenses with a title, value, date and category.
Edit or delete any transaction.
Search by title, filter by category and change month.
The balance, income and spend cards update based on the chosen month.
See a doughnut chart showing what you've spent in each category. This includes a colour legend.
View your monthly budget with a bar that fills up. If you go over you'll see it turn red.
You can set optional limits on your categories (e.g. Food = $30). Each category will have its own bar.
Export data into a CSV file.
Data is stored in JSON files so it doesn't get lost when restarting.
## Code breakdown

`app.py` contains the routes, filtering, data for the chart and saving.
`templates/index.html` is the main page. `templates/edit.html` is the edit page.
`static/style.css` has all of the styling.
`data.json`, `budget.json` and `limits.json` are automatically created when using this.
## Technologies used

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

## How I built this
I coded this using my iPad. I used Claude (AI assistant) as my teacher to help me code. I also used it to help me write and debug my code. I tested, fixed and deployed it myself.

## What I would improve
Dark mode
Private list for each visitor
Chart comparing income and spend each month.
Actual database instead of JSON files

-------
 Niral