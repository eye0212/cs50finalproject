# cs50finalproject

**Subito** is a web app implemented using Flask, jinja, and bootstrap that matches users based on their classical music preferences - designed to bring musicians together online. Our website includes a quiz designed to characterize users’ preferences as a function of 4 key variables, and then provides them with scores ranking the compatibility of their tastes with respect to other users.

![index page](final-project/static/images/readme3.png?raw=true)

## **User Instructions**

#### Accessing Subito:

To access our website, in your codespace set your current directory to "final-project". Then, into the terminal, type flask run and command + click on the link that appears. This will open your browser, taking you to subito's Log In page. 


![index page](final-project/static/images/readme1.png?raw=true)


#### Register and Login:

Create a new account by the "register" button on the nav-bar. This will direct you to a new page where you must fill out your information to become a user. Fill out all the required fields, including uploading a .jpg .jpeg or .png profile picture.


![index page](final-project/static/images/readme2.png?raw=true)


#### Taking the Musician Quiz:

Immediately after making a new account, the web app will direct you to a page with a ten question quiz to fill out. This quiz is how the web app learns about your musical preferences and will internally assign you a score. Fill out all the required boxes and submit the form.


![index page](final-project/static/images/readme4.png?raw=true)


#### Musicians Page:

After taking the musician quiz, the web app will direct you to the musicians page where you can see the information of every other user. Here, you have access to their name, age, location, email, compatability score, and a head shot. The compatability score is a number from 0-100 that represents how compatible the current user is to another user based on the results from the musician quiz. On the musicians page, you can filter the results by name, age, and location.


![index page](final-project/static/images/readme5.png?raw=true)


#### My Profile:

In this page, the user can see their own information including their name, age, location, email, and head shot.


![index page](final-project/static/images/readme6.png?raw=true)


#### Log Out:

This button logs the user out of their current session.