Title: Crypto Price Tracker
problem:
"Tracking cryptocurrency investments manually is difficult because prices change every second."

solution:
"This project is a Crypto Portfolio Tracker that fetches live prices from CoinGecko API and automatically calculates the total value of a user’s portfolio."

Features (What it does)
*Fetches real-time crypto prices using the CoinGecko API.
*Users can enter how many coins they own (e.g., 2 BTC, 5 ETH).
*The system multiplies the number of coins with live price to show:
  Current price of each coin
  Value of user’s holdings per coin
  Total portfolio value in USD
*All this updates dynamically with live market prices.

Tech Stack (How it is built)
*Backend: Django (Python) – handles requests, fetches live prices.
*Frontend: HTML templates (Jinja in Django) – displays portfolio, prices, and total value.
*API: CoinGecko (for live crypto data).
*Database: Stores cryptocurrency details (name, symbol, CoinGecko ID).

how to run:
*In the root folder terminal,give the command:py manage.py runserver
*then,you will see the web page:
<img width="1776" height="869" alt="Screenshot 2025-09-11 214324" src="https://github.com/user-attachments/assets/5ae72bef-9736-4964-9e67-4fd57ea4f44b" />
*Then,when you navigate to portfolio tab
*you will get a web page like this:
<img width="1852" height="878" alt="Screenshot 2025-09-11 214353" src="https://github.com/user-attachments/assets/80fa0f19-f0d9-4e35-840f-9e3a3ab55c10" />
where you can calculate your total amount.

