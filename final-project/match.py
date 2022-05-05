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



def match(user_id):

    user_q1 = db.execute("SELECT q1 FROM answers WHERE id LIKE ?", user_id)
    user_q2 = db.execute("SELECT q2 FROM answers WHERE id LIKE ?", user_id)
    user_q3 = db.execute("SELECT q3 FROM answers WHERE id LIKE ?", user_id)
    user_q4 = db.execute("SELECT q4 FROM answers WHERE id LIKE ?", user_id)
    user_q5 = db.execute("SELECT q5 FROM answers WHERE id LIKE ?", user_id)
    user_q6 = db.execute("SELECT q6 FROM answers WHERE id LIKE ?", user_id)
    user_q7 = db.execute("SELECT q7 FROM answers WHERE id LIKE ?", user_id)
    user_q8 = db.execute("SELECT q8 FROM answers WHERE id LIKE ?", user_id)
    user_q9 = db.execute("SELECT q9 FROM answers WHERE id LIKE ?", user_id)
    user_q10 = db.execute("SELECT q10 FROM answers WHERE id LIKE ?", user_id)

    all_q1 = db.execute("SELECT q1 FROM answers")

    qs = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']

    ans = ['1', '2', '3', '4', '5']

    sql_query = pd.read_sql_query (''' SELECT * FROM answers ''', db)

    df = pd.DataFrame(sql_query, columns = ['id', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10'])

    answers = pd.DataFrame(index=men.index, columns=women.index)

    for i in ratings.columns:
        ratings[i] = random.choices([0,1,"unseen"], k=num)

    return redirect("/")