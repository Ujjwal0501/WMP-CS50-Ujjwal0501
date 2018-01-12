from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    # get cash
    try :
        cash = float(db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])[0]["cash"])
    except :
        return apology("Could not get cash")

    # get shares
    try :
        shares = db.execute("SELECT symbol,SUM(shares) AS shares,price,date,SUM(amount) AS amount FROM transactions WHERE "+
                            "symbol IS NOT NULL AND id = :userid GROUP BY symbol", userid=session["user_id"])
    except :
        return apology("Could not get shares")

    total = 0.0
    for row in shares :
        name, row["price"], symbol = lookup(row["symbol"])
        total = total + row["amount"]
        row["amount"] = usd(float(row["amount"]))
        row["price"] = usd(float(row["price"]))
    total = total + cash

    return render_template("index.html", rows=shares, cash=usd(cash), total=usd(total))

@app.route("/buy", methods=["GET", "POST"])
#@login_required
def buy():
    """Buy shares of stock."""

    # show webpage if method is GET
    if request.method == "GET" :
        return render_template("buy.html")

    # look share rate if method is POST
    if request.method == "POST" :

        # ensure symbol was submitted
        if not request.form.get("symbol") :
            flash("Must enter symbol")
            return render_template("buy.html")

        # ensure share is submitted
        if not request.form.get("shares") :
            flash("Must enter share")
            return render_template("buy.html")

        # store symbol
        symbol = request.form.get("symbol")

        # perform lookup of share price
        name, price, symbol = symbol.upper(), 0.0, symbol.upper()
        try :
            name, price, symbol = lookup(symbol)
        except :
            return apology("LOOKUP FAILED")

        shares = int(request.form.get("shares"))

        # extract user details
        row = ""
        try :
            row = db.execute("SELECT * FROM users WHERE id = :userid", userid=session["user_id"])
        except :
            return apology("Could not retrieve user data")

        # ensure user has enough balance
        if float(row[0]["cash"]) < (price*shares) :
            flash("You do not have sufficent balance")
            return render_template("buy.html")

        try :
            # update user's balance
            db.execute("UPDATE users SET cash=cash-:cost WHERE id=:userid", cost=price*shares, userid=session["user_id"])
        except :
            # show error if update fails
            return apology("Could not update user info")

        try :
            # log transaction details
            db.execute("INSERT INTO transactions VALUES(:userid, :smbl, :share, :prc, 'BUY', CURRENT_TIMESTAMP, :cost)",
                            userid=session["user_id"], smbl=symbol, share=shares, prc=price, cost=price*shares)
        except :
            # revert shares and balance update
            db.execute("UPDATE users SET cash=cash+:cost WHERE id=:userid", cost=price*shares, userid=session["user_id"])
            return apology("Could not log transaction details")


        # redirect to home page
        flash("Bought")
        return redirect(url_for('index'))

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    try:
        # retrieve history
        rows = db.execute("SELECT * FROM transactions WHERE symbol IS NOT NULL AND id = :userid", userid=session["user_id"])
    except :
        return apology("Could not retrieve data")

    # render history
    return render_template("history.html", rows=rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # show webpage if method is GET
    if request.method == "GET" :
        return render_template("quote.html")

    # look share rate if method is POST
    if request.method == "POST" :

        # ensure symbol was submitted
        if not request.form.get("symbol") :
            flash("Must enter symbol")
            return render_template("quote.html")

        # store symbol
        symbol = request.form.get("symbol")

        # perform lookup of share price
        try :
            name, price, symbol = lookup(symbol)
        except :
            return apology("LOOKUP FAILED")

        # try rendering output
        try :
            price = usd(float(price))
            return render_template("quoted.html", name=name, symbol=symbol, price=price)

        # show ERROR in case of exception
        except :
            return apology("LOOKUP FAILED")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # show page if method is get
    if request.method == "GET" :
        return render_template("register.html")

    # proceed registration when method is post
    elif request.method == "POST" :

        # ensure username was submitted
        if not request.form.get("username") :
            flash("Must provide username!")
            return render_template("register.html")

        # ensure password was submitted
        if not request.form.get("password") :
            flash("Must provide password!")
            return render_template("register.html")

        # ensure passwords match
        if not request.form.get("cpassword") :
            flash("Must confirm password!")
            return render_template("register.html")

        row = ""
        try :
            # confirm uniqueness of username
            rows = db.execute("SELECT * FROM users WHERE username LIKE :username", username=request.form.get("username"))
        except :
            return apology("Could not retrieve User Details")

        if len(rows) != 0 :
            flash("username already exists!")
            return render_template("register.html")

        # register only if username is available
        else :

            # register only if passwords match
            if request.form.get("password") == request.form.get("cpassword") :
                db.execute("INSERT INTO users (username, hash) VALUES(:username, :password)",
                            username=request.form.get("username"), password=pwd_context.hash(request.form.get("password")))
                flash("Register Success!")
                return redirect(url_for("login"))
            else :
                flash("Passwords do not match")
                return render_template("register.html")
    else :
        return render_template("login.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    # show webpage if method is GET
    if request.method == "GET" :
        rows = ""

        try:
            # retrieve symbol of bought stocks
            rows = db.execute("SELECT DISTINCT symbol FROM transactions WHERE symbol IS NOT NULL AND id = :userid",
                                userid=session["user_id"])
        except :
            # show error if retrieve fails
            return apology("Could not retrieve bought stocks")

        # handle empty symbol list
        if len(rows) == 0 :
            flash("You have not bought any stocks yet")
            return redirect(url_for('index'))

        # render sell page with symbols
        return render_template("sell.html", symbols=rows)

    # proceed to change password if method id POST
    if request.method == "POST" :

        # ensure symbol was selected
        if not request.form.get("symbol") :
            flash("Must select a symbol")
            return render_template("sell.html")

        # ensure share was submitted
        if not request.form.get("shares") :
            flash("Must provide shares")
            return render_template("sell.html")

        # store symbol, share and price
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        name, price, symbol = lookup(symbol)

        # retrieve share details of selected symbol
        rows = ""
        try :
            rows = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE id = :userid AND "+
                                "symbol = :smbl GROUP BY symbol", userid=session["user_id"], smbl=symbol)
        except :
            # show error if retrieve fails
            return apology("Could not retrieve shares\' details")

        # ensure user has enough shares to sell
        if shares > rows[0]["shares"] :
            flash("You do not possess enough shares of this symbol to sell")
            return redirect(url_for('index'))

        try :
            # add cash to account
            db.execute("UPDATE users SET cash=cash+:amount WHERE id = :userid", amount=price*shares, userid=session["user_id"])
        except :
            return apology("Could not update cash\nSell aborted")

        try :
            # log sell details
            db.execute("INSERT INTO transactions VALUES(:userid, :smbl, :share, :prc, 'SELL', CURRENT_TIMESTAMP, :amount)",
                        userid=session["user_id"], smbl=symbol, share=-shares, prc=price, amount=-price*shares)
        except :
            db.execute("UPDATE users SET cash=cash-:amount WHERE id = :userid", amount=price*shares, userid=session["user_id"])
            return apology("Could not log transaction details\nSell aborted")

        # show sold message and redirect to home page
        flash("Sold!")
        return redirect(url_for('index'))

@app.route("/change", methods=["GET","POST"])
@login_required
def change():
    """change password"""

    # show webpage if method is GET
    if request.method == "GET" :
        return render_template("change.html")

    # proceed to change password if method id POST
    if request.method == "POST" :

        # ensure old password was submitted
        if not request.form.get("opassword") :
            flash("Must provide old password")
            return render_template("change.html")

        # ensure new password was submitted
        if not request.form.get("password") :
            flash("Must provide new password")
            return render_template("change.html")

        # ensure password was retyped
        if not request.form.get("cpassword") :
            flash("Must confirm new password")
            return render_template("change.html")

        # ensure passwords match
        if request.form.get("password") != request.form.get("cpassword") :
            flash("New passwords do not match")
            return render_template("change.html")

        try :
            # retrieve user info
            rows = db.execute("SELECT * FROM users WHERE id = :userid", userid=session["user_id"])
        except :
            # show error if retrieve fails
            return apology("Could not retrieve User Details")

        # verify old password
        if not pwd_context.verify(request.form.get("opassword"), rows[0]["hash"]):
            return apology("Invalid old password")

        try :
            # save new hash
            db.execute("UPDATE users SET hash = :password WHERE id = :userid",
                            password=pwd_context.hash(request.form.get("password")), userid=session["user_id"])
        except :

            # show error if update fails
            return apology("SORRY!!\nPassword not changed")

        # log out current user
        session.clear()

        # redirect to login page
        return redirect(url_for('login'))

@app.route("/credit", methods=["GET", "POST"])
@login_required
def credit():
    """add cash"""

    # show web page if method is GET
    if request.method == "GET" :
        return render_template("credit.html")

    # proceed to add cash if method is POST
    if request.method == "POST" :

        # ensure amount was submitted
        if not request.form.get("amount") :
            flash("Must provide amount")
            return render_template("credit.html")

        # retrieve user info
        row = db.execute("SELECT * FROM users WHERE id = :userid", userid=session["user_id"])

        try :

            # ensure credit was success
            db.execute("UPDATE users SET cash = cash + :amount WHERE id = :userid", amount=int(request.form.get("amount")),
                            userid=session["user_id"])
        except :

            # show error if credit fails
            return apology("Could not add cash")

        try:

            # log credit details
            db.execute("INSERT INTO transactions VALUES(:userid, NULL, NULL, NULL, \'CREDIT\', CURRENT_TIMESTAMP, :amount)",
                        userid=session["user_id"], amount=int(request.form.get("amount")))
        except :

            # undo credit if logging fails
            db.execute("UPDATE users SET cash = cash - :amount WHERE id = :userid", amount=int(request.form.get("amount")),
                        userid=session["user_id"])
            return apology("Could not log transaction details")

        # redirect to home page
        return redirect(url_for('index'))