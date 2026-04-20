CREATE TABLE IF NOT EXISTS sensor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

CREATE TABLE IF NOT EXISTS measurement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location_id INT,
    sensor_id INT,
    value FLOAT,
    unit VARCHAR(20),
    datetime DATETIME
);