CREATE DATABASE sample;
CREATE USER IF NOT EXISTS 'web_user'@'%' IDENTIFIED WITH mysql_native_password BY 'dev';
GRANT ALL PRIVILEGES ON sample . * TO 'web_user'@'%';