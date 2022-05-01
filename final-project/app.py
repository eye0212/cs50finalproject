from ast import BinOp
import os

# test

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from PIL import Image 
import PIL 
import os, sys

from helpers import apology, login_required, convertToBinaryData

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")
        age = request.form.get("age")
        location = request.form.get("location")
        name = request.form.get("name")

        #photo = request.form.get('photo')
        #print(type(photo))

        if not username or not password or not confirmation or not email or not age or not location or not name:
            return apology("All fields are required.", 400)
        if password != confirmation:
            return apology("Passwords do not match.", 400)
        for profile in db.execute("SELECT username FROM users"):
            if profile["username"] == username:
                return apology("This username is taken.", 400)
        for profile in db.execute("SELECT email FROM users"):
            if profile["email"] == email:
                return apology("This email is already associated with an account.", 400)
        #print(os.getcwd())
        #photo.save(f"/photos/{username}.png")
        db.execute("INSERT INTO users (username, hash, email, age, location, name) VALUES (?, ?, ?, ?, ?, ?)", username, generate_password_hash(password), email, age, location, name)
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]
        return redirect("/")


@app.route("/musicians", methods=["GET", "POST"])
@login_required
def musicians():
    """Show eligible musicians"""
    if request.method == "GET":
        mus_list = db.execute("SELECT * FROM users")
        return render_template("musicians.html", mus_list=mus_list)
    else:
        age = request.form.get("age")
        location = request.form.get("location")
        name = request.form.get("name")
        if not age:
            age = "%%"
        if not location:
            location = "%%"
        if not name:
            name = "%%"
        else: 
            name = f"%{name}%"
        mus_list = db.execute("SELECT * FROM users WHERE name LIKE ? AND age LIKE ? AND location LIKE ?", name, age, location)
        return render_template("musicians.html", mus_list=mus_list)



@app.route("/musicquiz")
@login_required
def musicquiz():
    """Test template for now"""

    mus_list = db.execute("SELECT * FROM users")
    return render_template("musicquiz.html", mus_list=mus_list)
