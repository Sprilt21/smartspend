CREATE DATABASE IF NOT EXISTS smartspendapp;

USE smartspendapp;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS user_keys;
DROP TABLE IF EXISTS budgets;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id int not null AUTO_INCREMENT,
    username varchar(64) not null,
    pwdhash varchar(512) not null,
    firstname varchar(64) not null,
    lastname varchar(64) not null,
    PRIMARY KEY (user_id),
    UNIQUE (username)
);

ALTER TABLE users AUTO_INCREMENT = 20001;

CREATE TABLE budgets (
    budget_id int not null AUTO_INCREMENT,
    user_id int not null,
    budget_name varchar(64) not null,
    budget_amt decimal(10,2) not null,
    current_amt decimal(10,2) not null,
    PRIMARY KEY (budget_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

ALTER TABLE budgets AUTO_INCREMENT = 1001;

CREATE TABLE transactions (
    transaction_id int not null AUTO_INCREMENT,
    user_id int not null,
    budget_id int not null,
    transaction_amt decimal(10,2) not null,
    transaction_desc varchar(256) not null,
    transaction_date date not null,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (budget_id) REFERENCES budgets(budget_id)
);

ALTER TABLE transactions AUTO_INCREMENT = 1001;

CREATE TABLE user_keys (
    key_id int not null AUTO_INCREMENT,
    user_id int not null,
    key_str varchar(256) not null,
    PRIMARY KEY (key_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Insert some data to test with

ALTER TABLE user_keys AUTO_INCREMENT = 1001;

-- pwd = password123
INSERT INTO users(username, pwdhash, firstname, lastname) 
values ('Taliyah21', 'gAAAAABnULYeSWZAJCrp1cn9RXx4b2IWOiZhAAAFK-0DWpy5QdoilCCqTIIfguPxIsb7IEngnPLjSsb1p9SVK_QCVFlVfcjpYQ==', 'Taliyah', 'Stoneweaver');

INSERT INTO user_keys(user_id, key_str) values (20001, 'K0eYJeOJZ1C9SamxjTxL_xeyWvsirOcu-bQ-B8Xf2Kw=');

INSERT INTO budgets(user_id, budget_name, budget_amt, current_amt) values (20001, 'Groceries', 200.00, 0.00);

-- user accounts for db access
DROP USER IF EXISTS 'smartspendapp-read-only';
DROP USER IF EXISTS 'smartspendapp-read-write';

CREATE USER 'smartspendapp-read-only' IDENTIFIED BY 'abc123!!';
CREATE USER 'smartspendapp-read-write' IDENTIFIED BY 'def456!!';

GRANT SELECT, SHOW VIEW ON smartspendapp.* 
    TO 'smartspendapp-read-only';
GRANT SELECT, SHOW VIEW, INSERT, UPDATE, DELETE, DROP, CREATE, ALTER ON smartspendapp.* 
    TO 'smartspendapp-read-write';

FLUSH PRIVILEGES;