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
<img width="1912" height="889" alt="Screenshot 2025-09-11 112209" src="https://github.com/user-attachments/assets/dabb06ea-777e-4c5c-bc42-e6e0af8bc077" />
*Then,use portfolio in the website to calculate the total amount:http://127.0.0.1:8000/portfolio/
*you will get a web page like this:
<img width="1802" height="896" alt="Screenshot 2025-09-11 115504" src="https://github.com/user-attachments/assets/15bc1859-cac7-477b-b499-308e350a055f" />


