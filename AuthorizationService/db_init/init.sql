CREATE DATABASE IF NOT EXISTS authorization_db;
USE authorization_db;

CREATE TABLE IF NOT EXISTS `users` (
  username VARCHAR(255) PRIMARY KEY,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL
);

INSERT INTO `users` (username, password, role) VALUES ('admin', 'password', 'admin');
INSERT INTO `users` (username, password, role) VALUES ('employee', 'password', 'employee');