-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS corvus_test_db;
CREATE USER IF NOT EXISTS 'corvus_test'@'localhost' IDENTIFIED BY 'c0rvus';
GRANT ALL PRIVILEGES ON `corvus_test_db`.* TO 'corvus_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'corvus_test'@'localhost';
FLUSH PRIVILEGES;
