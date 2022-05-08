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
    user_q1 = db.execute("SELECT q1 FROM users WHERE id = ?", id)[0]["q1"]
    user_q2 = db.execute("SELECT q2 FROM users WHERE id = ?", id)[0]["q2"]
    user_q3 = db.execute("SELECT q3 FROM users WHERE id = ?", id)[0]["q3"]
    user_q4 = db.execute("SELECT q4 FROM users WHERE id = ?", id)[0]["q4"]
    user_q5 = db.execute("SELECT q5 FROM users WHERE id = ?", id)[0]["q5"]
    user_q6 = db.execute("SELECT q6 FROM users WHERE id = ?", id)[0]["q6"]
    user_q7 = db.execute("SELECT q7 FROM users WHERE id = ?", id)[0]["q7"]
    user_q8 = db.execute("SELECT q8 FROM users WHERE id = ?", id)[0]["q8"]
    user_q9 = db.execute("SELECT q9 FROM users WHERE id = ?", id)[0]["q9"]
    user_q10 = db.execute("SELECT q10 FROM users WHERE id = ?", id)[0]["q10"]

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

    users_num = db.execute("SELECT COUNT(*) FROM users")[0]["COUNT(*)"]

    lis = db.execute("SELECT id FROM users")
    ids = []
    for id in lis:
        ids.append(id["id"])

    compatability = []

    # get the compatability scores for each person relative to user by taking distance 
    for i in range(users_num):
        Px = score[0]
        Py = score[1]
        Pz = score[2]
        Pt = score[3]

        Qx = db.execute("SELECT score_x FROM users WHERE id = ?", ids[i])[0]["score_x"]
        Qy = db.execute("SELECT score_y FROM users WHERE id = ?", ids[i])[0]["score_y"]
        Qz = db.execute("SELECT score_z FROM users WHERE id = ?", ids[i])[0]["score_z"]
        Qt = db.execute("SELECT score_t FROM users WHERE id = ?", ids[i])[0]["score_t"]

        eDistance = math.dist([Px, Py, Pz, Pt], [Qx, Qy, Qz, Qt])
        compatability.append(eDistance)

    # normalize compatability_scores to get value between 0 and 1
    print(compatability)
    normalized = preprocessing.normalize([compatability])[0]
    # print('GJK', normalized)

    # organize usernames and compatability into a dictionary to better represent data
    compatability_dict = {}

    for i in range(len(ids)):
        compatability_dict[ids[i]] = int(100 * math.sqrt((1 - normalized[i])))

    # this function returns a dictionary that has every user and the compatability score assigned with that user (between 0 and 100)
    return compatability_dict