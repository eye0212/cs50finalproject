from ast import BinOp

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

import math
from sklearn import preprocessing

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


def categorize(id):

    # note to fill answer table as well as user table with ids every time new person is made

    # get all answers from current user 
    user_q1 = db.execute("SELECT q1 FROM users WHERE id = ?", id)
    user_q2 = db.execute("SELECT q2 FROM users WHERE id = ?", id)
    user_q3 = db.execute("SELECT q3 FROM users WHERE id = ?", id)
    user_q4 = db.execute("SELECT q4 FROM users WHERE id = ?", id)
    user_q5 = db.execute("SELECT q5 FROM users WHERE id = ?", id)
    user_q6 = db.execute("SELECT q6 FROM users WHERE id = ?", id)
    user_q7 = db.execute("SELECT q7 FROM users WHERE id = ?", id)
    user_q8 = db.execute("SELECT q8 FROM users WHERE id = ?", id)
    user_q9 = db.execute("SELECT q9 FROM users WHERE id = ?", id)
    user_q10 = db.execute("SELECT q10 FROM users WHERE id = ?", id)

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

    score = [0, 0, 0, 0]

    for answer in answers:
        if answer == "a":
            score[0] += 1
        if answer == "b":
            score[1] += 1
        if answer == "c":
            score[2] += 1
        if answer == "d":
            score[3] += 1

    # this function assigns every person a score in R4 and returns it after putting it into the SQL 
    # database table called answers

    db.execute("UPDATE users SET score_x = ?, score_y = ?, score_z = ?, score_t = ? WHERE id = ?", score[0], score[1], score[2], score[3], id)
    return score

def match(score):

    #number of users

    users_num = db.execute("SELECT COUNT(*) FROM users")

    ids = list(db.execute("SELECT id FROM users"))

    compatability = []

    # get the compatability scores for each person relative to user by taking distance 
    for i in range(users_num):
        Px = score[0]
        Py = score[1]
        Pz = score[2]
        Pt = score[3]

        Qx = db.execute("SELECT score_x FROM users WHERE id = ?", ids[i])
        Qy = db.execute("SELECT score_y FROM users WHERE id = ?", ids[i])
        Qz = db.execute("SELECT score_z FROM users WHERE id = ?", ids[i])
        Qt = db.execute("SELECT score_t FROM users WHERE id = ?", ids[i])

        eDistance = math.dist([Px, Py, Pz, Pt], [Qx, Qy, Qz, Qt])
        compatability.append(eDistance)

    # normalize compatability_scores to get value between 0 and 1
    normalized = preprocessing.normalize(compatability)

    # organize usernames and compatability into a dictionary to better represent data
    compatability_dict = {}
    
    for i in range(len(id)):
        compatability_dict[id[i]] = int(100 * (1 - normalized[i]))

    # this function returns a dictionary that has every user and the compatability score assigned with that user

    return compatability_dict