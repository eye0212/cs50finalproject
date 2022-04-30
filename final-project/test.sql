ALTER TABLE users
ADD email varchar(255);



CREATE TABLE IF NOT EXISTS 'users'
(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, email TEXT NOT NULL, hash TEXT NOT NULL, age int, location char(255), name varchar(255));
CREATE UNIQUE INDEX email ON users (email);