CREATE DATABASE sample;
CREATE USER IF NOT EXISTS 'web_user'@'%' IDENTIFIED BY 'dev';
GRANT ALL PRIVILEGES ON sample . * TO 'web_user'@'%';