from crypt import methods
from decimal import Decimal
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_fontawesome import FontAwesome

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

fa = FontAwesome(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mylittlestore.db")

cart_items = []

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    products = db.execute("Select * from products;")
    if products is not None:
        return render_template("index.html", data = products)
    return apology("test")

@app.route("/add", methods=["GET","POST"])
def add():
    product_id = request.args.get("product_id")
    quantity = request.args.get("quantity")
    flag = request.args.get("flag")

    if not request.args.get("product_id"):
         return apology("something's wrong", 403)

    row = db.execute("SELECT id, name, price, img_url FROM products WHERE id = ?", product_id)

    for x in cart_items:
        if int(x["id"]) == int(product_id):
            if flag != "from_cart":
                quantity = int(x["quantity"]) + int(quantity)
            cart_items.remove(x)

    subtotal = int(quantity) * float(row[0]["price"])

    cart_item = {"id": row[0]["id"], "name": row[0]["name"], "price": row[0]["price"], "img_url": row[0]["img_url"], "quantity": quantity, "subtotal" : subtotal}

    cart_items.append(cart_item)
    
    return jsonify(cart_items = cart_items, quantity = quantity, subtotal = subtotal)

@app.route("/cart", methods=["GET"])
def cart():
    grand_total = 0
    if cart_items:
        for item in cart_items:
            grand_total = grand_total + float(item["subtotal"])
        return render_template("cart.html", cart_items = cart_items, count = len(cart_items), grand_total = grand_total)
    return render_template("cart.html")

@app.route("/get_times", methods=["GET"])
def get_times():
    date_value = request.args.get("date_value")
    available_times = db.execute("SELECT time FROM delivery_slots WHERE date = ? order by date asc", date_value)
    return jsonify(available_times = available_times)

@app.route("/get_dates", methods=["GET"])
def get_dates():
    available_dates = db.execute("SELECT DISTINCT date from delivery_slots")
    return jsonify(available_dates = available_dates)

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        """Register user"""
        if not request.form.get("username"):
            return apology("must provide username", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            return apology("username already exists", 400)

        if not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provide password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password not matched", 400)

        pwd = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        insertQuery = "INSERT INTO users(username, hash) VALUES('" + request.form.get("username") + "', '" + pwd + "') "
        db.execute(insertQuery)

        return redirect("/login")
    return render_template("register.html")

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
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

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