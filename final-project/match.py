from ast import BinOp
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import os, sys

import pandas as pd
import random
import numpy as np

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


@app.route("/musicquiz")
@login_required
def musicquiz():
    """Test template for now"""

    q1 = request.form.get("q1")
    q2 = request.form.get("q2")
    q3 = request.form.get("q3")
    q4 = request.form.get("q4")
    q5 = request.form.get("q5")
    q6 = request.form.get("q6")
    q7 = request.form.get("q7")
    q8 = request.form.get("q8")
    q9 = request.form.get("q9")
    q10 = request.form.get("q10")

    mus_list = db.execute("INSERT INTO answers (q1, q2, q3, q4, q5, q6, q7, q8, q9, q10) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", q1, q2, q3, q4, q5, q6, q7, q8, q9, q10)





    return render_template("musicquiz.html", mus_list=mus_list)



def match():
    name = request.form.get("name")

    username = "SELECT * FROM users WHERE name LIKE ?", name)

    username = db.execute("SELECT username FROM users ")

    name = db.execute("SELECT name FROM answers")



    q1 = db.execute("SELECT q1 FROM answers")





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