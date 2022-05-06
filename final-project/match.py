from ast import BinOp
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
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



def categorize(username):

    # note to fill answer table as well as user table with ids every time new person is made

    # get all answers from current user 
    user_q1 = db.execute("SELECT q1 FROM answers WHERE username LIKE ?", username)
    user_q2 = db.execute("SELECT q2 FROM answers WHERE id LIKE ?", username)
    user_q3 = db.execute("SELECT q3 FROM answers WHERE id LIKE ?", username)
    user_q4 = db.execute("SELECT q4 FROM answers WHERE id LIKE ?", username)
    user_q5 = db.execute("SELECT q5 FROM answers WHERE id LIKE ?", username)
    user_q6 = db.execute("SELECT q6 FROM answers WHERE id LIKE ?", username)
    user_q7 = db.execute("SELECT q7 FROM answers WHERE id LIKE ?", username)
    user_q8 = db.execute("SELECT q8 FROM answers WHERE id LIKE ?", username)
    user_q9 = db.execute("SELECT q9 FROM answers WHERE id LIKE ?", username)
    user_q10 = db.execute("SELECT q10 FROM answers WHERE id LIKE ?", username)

    # put answers into a list for easier processing 
    answers = [
        user_q1,
        user_q2,
        user_q3,
        user_q4,
        user_q5,
        user_q6,
        user_q7,
        user_q8,
        user_q9,
        user_q10
    ]

    score = [0, 0]

    for answer in answers:
        if answer == "a":
            score[0] += 1
        if answer == "b":
            score[0] += 1
            score[1] += 1
        if answer == "c":
            score[1] = score[1] - 1
        if answer == "d":
            score[0] = score[0] - 1
            score[1] = score[1] - 1

    return score
