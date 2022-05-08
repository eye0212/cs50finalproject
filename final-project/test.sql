ALTER TABLE users
ADD email varchar(255);



CREATE TABLE IF NOT EXISTS 'users'
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL, age int, location char(255), name varchar(255));
CREATE UNIQUE INDEX email ON users (email);

CREATE TABLE IF NOT EXISTS 'users' (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, age int, location char(255), email varchar(255), name varchar(255), 'q1' varchar(255), 'q2' varchar(255), 'q3' varchar(255), 'q4' varchar(255), 'q5' varchar(255), 'q6' varchar(255), 'q7' varchar(255), 'q8' varchar(255), 'q9' varchar(255), 'q10' varchar(255), 'score_x' INTEGER, 'score_y' INTEGER, 'score_z' INTEGER, 'score_t' INTEGER);


CREATE TABLE IF NOT EXISTS 'users' (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, age int, location char(255), email varchar(255), name varchar(255));
CREATE TABLE IF NOT EXISTS 'answers' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT, 'q1' TEXT, 'q2' TEXT, 'q3' TEXT, 'q4' TEXT, 'q5' TEXT, 'q6' TEXT, 'q7' TEXT, 'q8' TEXT, 'q9' TEXT, 'q10' TEXT, 'score_x' INTEGER, 'score_y' INTEGER, score_z INTEGER, score_t INTEGER);