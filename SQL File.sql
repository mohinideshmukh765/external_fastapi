CREATE DATABASE diabetes_db;

USE diabetes_db;

CREATE TABLE predictions(
id INT AUTO_INCREMENT PRIMARY KEY,
pregnancies INT,
glucose FLOAT,
bloodpressure FLOAT,
skinthickness FLOAT,
insulin FLOAT,
bmi FLOAT,
pedigree FLOAT,
age INT,
prediction VARCHAR(50)
);

ALTER TABLE predictions
ADD COLUMN prediction_time TIMESTAMP
DEFAULT CURRENT_TIMESTAMP;