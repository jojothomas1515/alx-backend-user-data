-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS test@localhost IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON my_db.* TO 'test'@'localhost';

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email VARCHAR(256)
);

INSERT INTO users(email) VALUES ("bob@dylan.com");
INSERT INTO users(email) VALUES ("bib@dylan.com");

--  PERSONAL_DATA_DB_USERNAME=test PERSONAL_DATA_DB_PASSWORD=test PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./main.py
