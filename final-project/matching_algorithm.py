from ast import BinOp
import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from PIL import Image 
import PIL 
import os, sys


@app.route("/login", methods=["GET", "POST"])
def match():

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


















import pandas as pd
import random
import numpy as np

# Creating a Dataset of men and women
men = pd.DataFrame()

women = pd.DataFrame()

# Number of users
num = 1000

# Dating profile questions for each
qs = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']

# Answers to profile questions
ans = ['A', 'B', 'C', 'D', 'E']

for q in qs:
    
    # Making them categorical for preprocessing later
    men[q] = pd.Categorical(random.choices(ans, k=num), categories=ans)
    
    women[q] = pd.Categorical(random.choices(ans, k=num), categories=ans)
    
    # IDs
    men['id'] = ["m"+str(i) for i in range(num)]
    
    women['id'] = ["w"+str(i) for i in range(num)]
    
# Setting index
men.set_index('id', inplace=True)

women.set_index('id', inplace=True)

# Creating match status between users
ratings = pd.DataFrame(index=men.index, columns=women.index)

for i in ratings.columns:
    ratings[i] = random.choices([0,1,"unseen"], k=num)


m_user = ratings.T.apply(pd.Series.value_counts).T.sort_values(
    by="unseen", 
    ascending=False
).iloc[0]


m_nrate = ratings.T[ratings.T[m_user.name]=="unseen"].index

n_men = men.apply(lambda x: x.cat.codes)

m_sim = n_men.T.corrwith(
    n_men.T[m_user.name]
).sort_values(
    ascending=False
)[1:11]

msim_rate = ratings.loc[list(m_sim.index)][m_nrate]


# Man predictions
m_predict = pd.DataFrame()
# Replacing the unseen values with NaNs for calculation purposes
msim_rate.replace(
    "unseen", 
    np.nan, 
    inplace=True
)
# Average
m_predict['avg'] = msim_rate.mean()
# Frequency
m_predict['freq'] = msim_rate.mode().T[0]
# Median
m_predict['median'] = msim_rate.median()





def matchMan(men_df, women_df, ratings, new_man_answers, num_sim=10):
    """
    This function will return the most likely compatible women based on a few given
    dataframes for a new male user.  Will use the top N similar users' compatibility 
    ratings to find the potentially most compatible women.
    """
    
    # First need to replace the DF answers with their numerical values
    men_df = men_df.apply(lambda x: x.cat.codes)

    women_df = women_df.apply(lambda x: x.cat.codes)
    
    # Dataframe of new user
    new_man = pd.DataFrame(
        [new_man_answers],
        columns=men_df.columns,
        index=['m'+str(int(men_df.index[-1][1:])+1)] # Getting the new man's id 
    )
    
    # Categorical answers to the profile questions
    ans = ['A', 'B', 'C', 'D', 'E']
    
    # Categorizing the answers
    new_man = new_man.apply(
        lambda x: pd.Categorical(x, categories=ans)
    ).apply(
        lambda x: x.cat.codes, axis=1
    )
        
    # Getting the top N similar users
    sim_men = men_df.corrwith(
        new_man.iloc[0], 
        axis=1
    ).sort_values(ascending=False)[:num_sim].index
    
    # Getting the similar users' ratings
    sim_rate = ratings.T[sim_men]
    
    # Filling in unseen values with nan for calculation purposes
    sim_rate.replace("unseen", np.nan, inplace=True)
    
    # The potentially most compatible women for the new man
    most_comp = sim_rate.mean(axis=1).sort_values(ascending=False)
    
    return most_comp


ans = ['A', 'B', 'C', 'D', 'E']
# Randomly picking answers
new_man_answers = random.choices(ans, k=5)
# Running the function
recs = matchMan(
    men, 
    women, 
    ratings, 
    new_man_answers, 
    num_sim=10
)
# Finding the top 20 most potentially compatible
recs[:20]



