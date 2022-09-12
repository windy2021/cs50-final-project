from crypt import methods
import datetime
from decimal import Decimal
from email import message
import json
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

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

@app.route("/history")
def history():
    transactions = []
    get_customer_id = db.execute("select customers.id as customer_id from customers inner join users where customers.customer_user_id = users.id and users.id = ?", session["user_id"])
    if len(get_customer_id) == 0:
        return render_template("history.html")
    transactions_query_rows = db.execute("SELECT * FROM transactions where customer_id = ?", get_customer_id[0]["customer_id"])
    
    if transactions_query_rows is not None:
        now = datetime.datetime.now()
        for transaction in transactions_query_rows:
            transaction_details = db.execute("select product_id, quantity, subtotal from transaction_details where transaction_id = ?", transaction["id"])

            status = "In progress"
            # order_date = transaction["transaction_date_time"]
            # datetime_object = datetime.datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')

            delivery_datetime = str(transaction["delivery_date"]) + " " + str(transaction["delivery_time"])
            datetime_object = datetime.datetime.strptime(delivery_datetime, '%Y-%m-%d %H:%M:%S')

            if now > datetime_object:
                status = "Completed"

            transaction = {"id" : transaction["id"], "datetime": transaction["transaction_date_time"], "total": float(transaction["total"]), "status": status}

            transactions.append(transaction)
        return render_template("history.html", transactions = transactions)
    return render_template("history.html")

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
    user_details ={
        "fullname": "",
        "email": "",
        "mobile": ""
    }
    grand_total = 0
    if len(cart_items) != 0:
        for item in cart_items:
            grand_total = grand_total + float(item["subtotal"])
        if "user_id" in session:
            user_details_row = db.execute("SELECT fullname, email, mobile, address FROM users WHERE id = ?", session["user_id"])
            user_details["fullname"] = user_details_row[0]["fullname"]
            user_details["email"] = user_details_row[0]["email"]
            user_details["mobile"] = user_details_row[0]["mobile"]
        return render_template("cart.html", cart_items = cart_items, count = len(cart_items), grand_total = grand_total, user_details = user_details)
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

@app.route("/delete_from_cart", methods=["GET"])
def delete_from_cart():
    product_id = request.args.get("product_id")
    if cart_items:
        for x in cart_items:
            if int(x["id"]) == int(product_id):
                cart_items.remove(x)
                break
    return jsonify(cart_items = cart_items)

@app.route("/pay", methods=["GET", "POST"])
def pay():
    # For Transactions Table
    date = request.form.get("date")
    time = str(request.form.get("time")) + ":00"
    method = request.form.get("method")
    address = request.form.get("address")
    customer_id = None

    # For New Customer in Customers
    name = "GUEST"
    user_id = None

    if method == "PICKUP":
        address = "PICKUP"
    
    if not address:
        return jsonify({"message": "must provide delivery address"})

    delivery_slot_row = db.execute("SELECT * from delivery_slots where date = ? and time = ? ", date, time)
    if len(delivery_slot_row) == 0:
        return jsonify({"message": "select another slot"})

    if 'user_id' in session:
        user_id = session['user_id']

        get_username_query = db.execute("SELECT username FROM users WHERE id = ?", user_id)
        name = get_username_query[0]["username"]

        get_user_customer_id = db.execute("SELECT id FROM customers WHERE customer_user_id = ?", user_id)
        if len(get_user_customer_id) != 0:
            customer_id = get_user_customer_id[0]["id"]

    if customer_id is None:
        customer_id = db.execute("INSERT INTO customers(name, customer_user_id) values(?, ?)", name, user_id)
    
    grand_total = 0
    if cart_items:
        for item in cart_items:
            grand_total = grand_total + float(item["subtotal"])

    insert_transaction_query = db.execute("INSERT INTO transactions(total, customer_id, delivery_date, delivery_time, delivery_type, address) VALUES(?, ?, ?, ?, ?, ?)", grand_total, customer_id, delivery_slot_row[0]["date"], delivery_slot_row[0]["time"], method, address)

    for item in cart_items:
        insert_transaction_details_query = db.execute("INSERT INTO transaction_details(transaction_id, product_id, quantity, subtotal) VALUES(?, ?, ?, ?)", insert_transaction_query, item['id'], item['quantity'], item['subtotal'])

    delete_delivery_slot = db.execute("DELETE FROM delivery_slots WHERE id = ?", delivery_slot_row[0]["id"])
    cart_items.clear()
    messages = "Thank you for your order!"
    return jsonify({"message": messages})

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

        insertQuery = "INSERT INTO users(username, hash, fullname, email, mobile) VALUES('" + request.form.get("username") + "', '" + pwd + "', '"+ request.form.get("fullname") +"', '"+ request.form.get("email") +"', '"+ request.form.get("mobile") +"') "
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
        session["username"] = rows[0]["username"]

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

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        admin_date = request.args.get("admin_date")
        admin_time = request.args.get("admin_time")
        db.execute("insert into delivery_slots(date, time) values(?, ?)", admin_date, admin_time)
    return render_template("admin.html")