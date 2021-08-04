import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Selects unique SYMBOLS from history.db to use lookup() function in each one.
    symbols = db.execute("SELECT DISTINCT symbol FROM history WHERE user_id = ?", session["user_id"])
    shares = {}  # [{'symbol': 'AAPL'}, {'symbol': 'FB'}]
    print(symbols)
    # Use lookup() function in each distinct symbol to get the current price and store it in prices = {} dict, shares and names.
    prices = {}
    names = {}
    totals = {}
    totalCash = 0.0
    for i in range(len(symbols)):
        # updates prices dictionary with keys = symbols from query.
        symbol = symbols[i]["symbol"]
        quote = lookup(symbol)
        price = quote["price"]  # float
        prices[symbol] = price

        # updates shares dictionary with keys = symbols from query.
        quantity = db.execute("SELECT SUM(shares) FROM history WHERE symbol = ? AND user_id = ?",
                              quote["symbol"], session["user_id"])  # Gives back a list with a single dict "[{'SUM(shares)': 4.0}]""
        shares[symbol] = int(quantity[0]["SUM(shares)"])  # Gets the value of the single dict above.

        # updates totals dictionary with keys = symbol
        totals[symbol] = float(price * shares[symbol])

        # updates names dictionary with keys = symbol
        name = quote["name"]
        names[symbol] = name

        totalCash = totalCash + totals[symbol]  # tfoot in the index.html sum the total

    # print(prices)   # {'AAPL': 145.11, 'FB': 350.42}
    # print(shares)   # {'AAPL': 3.0, 'FB': 3.0}
    # print(names)    # {'AAPL': 'Apple Inc', 'FB': 'Facebook Inc - Class A'}
    # print(totals)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    totalCash = totalCash + cash[0]["cash"]
    return render_template("index.html", prices=prices, shares=shares, names=names, symbols=symbols, cash=cash, totals=totals, totalCash=totalCash)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares")

        # Ensure shares submitted is valid
        shares = request.form.get("shares")
        # Defines a function to check if the string (shares) typed by the user is a float or integer

        def is_integer(n):
            try:
                float(n)
            except ValueError:
                return False
            else:
                return float(n).is_integer()
        # Ensure shares submitted is a positive integer
        if not is_integer(shares):
            return apology("a share must be a positive integer")

        # After validating above, gets number of shares from the user as an integer
        shares = int(shares)
        # Ensure shares is bigger than 0
        if shares <= 0:
            return apology("a share must be a positive integer")

        # Ensure user has those shares
        # Gets quantity from history.db
        quantity = db.execute("SELECT SUM(shares) FROM history WHERE symbol = ? AND user_id = ?",
                              request.form.get("symbol"), session["user_id"])  # Gives back a list with a single dict "[{'SUM(shares)': 4.0}]""
        # Ensure user has any share from that symbol
        if not quantity:
            return apology("you don't have shares from this company")
        # Ensure user has more than he's selling
        quantity = int(quantity[0]["SUM(shares)"])
        if shares > quantity:
            return apology("You dont have that many shares from this company")
        # Look up the stock’s current price
        quote = lookup(request.form.get("symbol"))
        name = quote["name"]  # string
        price = quote["price"]  # float
        symbol = quote["symbol"]  # string

        # Calculates the sale price as a float
        sp = float(price * shares)
        # Select how much cash the user currently has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = float(cash[0]["cash"])

        # Updates cash variable adding sp (sale price)
        cash = cash + sp
        # Updates the amount of cash this user has after the sale in the database finance.db
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        # SQL DATE: TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
        # Gets the date and time of the purchase using datetime() imported from datetime library.
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formats as desired: seconds being integer not float.
        # Updates history TABLE from finance.db with name (companyname), price of 1 share, symbol, shares sold (-), datetime and user_id.
        # Transform shares sold in a negative number in the database so we can track is history.db and history.html what is a buy and what is a sell.
        shares = shares * (-1)
        db.execute("INSERT INTO history (user_id, name, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], name, symbol, shares, price, date)

    # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Selects unique SYMBOLS from history.db to pass to the select form in sell.html
        symbols = db.execute("SELECT DISTINCT symbol FROM history WHERE user_id = ?", session["user_id"])
        shares = {}  # [{'symbol': 'AAPL'}, {'symbol': 'FB'}]
        print(symbols)
        # to exclude from select (sell.html) stocks that user have bought but sold all.
        for i in range(len(symbols)):
            symbol = symbols[i]["symbol"]
            quantity = db.execute("SELECT SUM(shares) FROM history WHERE symbol = ? AND user_id = ?",
                                  symbol, session["user_id"])  # Gives back a list with a single dict "[{'SUM(shares)': 4.0}]""
            shares[symbol] = int(quantity[0]["SUM(shares)"])  # Gets the value of the single dict above.

        return render_template("sell.html", symbols=symbols, shares=shares)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        quote = lookup(request.form.get("symbol"))
        # Ensure symbol submitted is valid
        if not quote:
            return apology("invalid symbol")

        # Ensure shares was submitted
        if not request.form.get("shares"):
            return apology("must provide shares")

        # Ensure shares submitted is valid
        shares = request.form.get("shares")
        # Defines a function to check if the string (shares) typed by the user is a float or integer

        def is_integer(n):
            try:
                float(n)
            except ValueError:
                return False
            else:
                return float(n).is_integer()
        # Ensure shares submitted is a positive integer
        if not is_integer(shares):
            return apology("a share must be a positive integer")

        # After validating above, gets number of shares from the user as an integer
        shares = int(shares)
        # Ensure shares is bigger than 0
        if shares <= 0:
            return apology("a share must be a positive integer")

        # Look up the stock’s current price
        name = quote["name"]  # string
        price = quote["price"]  # float
        symbol = quote["symbol"]  # string

        # Calculates the purchase price as a float
        pp = float(price * shares)
        # Select how much cash the user currently has
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = float(cash[0]["cash"])
        # Ensure user has the money to buy those shares at that purchase price
        if pp > cash:
            return apology("cannot afford the number of shares at the current price")
        # Updates cash variable subtracting pp (purchase price)
        cash = cash - pp
        # Updates the amount of cash this user has after the purchase in the database finance.db
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        # SQL DATE: TEXT as ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS").
        # Gets the date and time of the purchase using datetime() imported from datetime library.
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formats as desired: seconds being integer not float.
        # Updates history TABLE from finance.db with name (companyname), price of 1 share, symbol, shares purchased (+), datetime and user_id.
        db.execute("INSERT INTO history (user_id, name, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], name, symbol, shares, price, date)

    # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT symbol, shares, price, date FROM history WHERE user_id = ?", session["user_id"])
    print(history)
    print(type(history))
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        quote = lookup(request.form.get("symbol"))
        # Ensure symbol submitted is valid
        if not quote:
            return apology("invalid symbol")
        name = quote["name"]
        value = quote["price"]
        symbol = quote["symbol"]

        return render_template("quoted.html", name=name, value=value, symbol=symbol)
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure username does not exist in database
        x = db.execute("SELECT * FROM users WHERE username =?", request.form.get("username"))
        if int(len(x)) > 0:
            return apology("username already exists", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure that confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure that confirmation matches password
        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Password does not match", 400)

        # Register user in the database
        username = request.form.get("username")

        password = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)

        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
