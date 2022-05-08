from ast import BinOp
import os


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import datetime
from PIL import Image 
import PIL 
import os, sys

from helpers import login_required, allowed_file
from match import categorize, match

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Prepare app.py for file upload
UPLOAD_FOLDER = '/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
            flash('must provide username')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('must provide password')
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('invalid username and/or password')
            return render_template("login.html")


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

@app.route("/register", methods=["GET", "POST"]) ## Some code adapted from https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
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
        file = request.files['file']

        # Check that all fields are completed
        if not username or not password or not confirmation or not email or not age or not location or not name or not file:
            flash('All fields are required')
            return render_template("register.html")
        # Check that passwords match
        if password != confirmation:
            flash('Passwords do not match.')
            return render_template("register.html")
        # Check that username is unique
        for profile in db.execute("SELECT username FROM users"):
            if profile["username"] == username:
                flash('This username is taken.')
                return render_template("register.html")
        # Check that email is unique
        for profile in db.execute("SELECT email FROM users"):
            if profile["email"] == email:
                flash('This username is already associated with an account.')
                return render_template("register.html")

        # Check to make sure file is right format:
        if not allowed_file(file.filename):
            flash('not allowed file')
            return render_template("login.html")
    
        # Set session to user ID
        db.execute("INSERT INTO users (username, hash, email, age, location, name) VALUES (?, ?, ?, ?, ?, ?)", username, generate_password_hash(password), email, age, location, name)
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", username)[0]["id"]

        # Upload file to server (while protecting against malicious users)
        filename = secure_filename(f'{session["user_id"]}.png')
        file.save(os.path.join(app.root_path, 'static', 'images', filename))

        # Redirect to music quiz
        return render_template("musicquiz_2.html")


@app.route("/musicians", methods = ["GET", "POST"])
@login_required
def musicians():
    # Show a list of musicians who aren't the user
    if request.method == "GET":
        
        # Calculate match scores
        input = categorize(session["user_id"])
        match_scores = match(input)

        # Retrieve list
        mus_list = db.execute("SELECT * FROM users WHERE id <> ?", session["user_id"])

        # Render template
        return render_template("musicians.html", mus_list = mus_list, match_scores = match_scores)
    else:
        # get age, location, and name from current user
        age = request.form.get("age")
        location = request.form.get("location")
        name = request.form.get("name")

        # If not specified, search for anything
        if not age:
            age = "%%"
        if not location:
            location = "%%"
        if not name:
            name = "%%"
        else: 
            name = f"%{name}%"

        # Upload match scores and filter info to HTML and render musicians page
        input = categorize(session["user_id"])
        match_scores = match(input)
        mus_list = db.execute("SELECT * FROM users WHERE name LIKE ? AND age LIKE ? AND location LIKE ? AND id <> ?", name, age, location, session["user_id"])
        return render_template("musicians.html", mus_list = mus_list, match_scores = match_scores)

@app.route("/profile", methods = ["GET"])
@login_required
def profile():
    if request.method == "GET":

        # Display only information about current user
        mus_list = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        return render_template("profile.html", mus_list = mus_list)


@app.route("/musicquiz", methods=['POST', 'GET'])
@login_required
def musicquiz():
    if request.method == 'GET':
        return render_template("musicquiz.html")
    else:
        # get responses form current user when they take the musician quiz
        q1_response = request.form.get('q1')
        q2_response = request.form.get('q2')
        q3_response = request.form.get('q3')
        q4_response = request.form.get('q4')
        q5_response = request.form.get('q5')
        q6_response = request.form.get('q6')
        q7_response = request.form.get('q7')
        q8_response = request.form.get('q8')
        q9_response = request.form.get('q9')
        q10_response = request.form.get('q10')

        # insert answers into sql database   
        db.execute("UPDATE users SET q1 = ?, q2 = ?, q3 = ?, q4 = ?, q5 = ?, q6 = ?, q7 = ?, q8 = ?, q9 = ?, q10 = ? WHERE id = ?", q1_response, q2_response, q3_response, q4_response, q5_response, q6_response, q7_response, q8_response, q9_response, q10_response, session["user_id"])
        
        # run categorize and match functions from match.py
        input = categorize(session["user_id"])
        match_scores = match(input)

        # Upload match scores and filter info to HTML and render musicians page
        mus_list = db.execute("SELECT * FROM users WHERE id <> ?", session["user_id"])
        print(mus_list)
        print(match_scores)
        return render_template("musicians.html", mus_list = mus_list, match_scores = match_scores)
