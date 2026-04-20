
USE openaq;

-- 🌍 Country
CREATE TABLE country (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- 🏙️ City
CREATE TABLE city (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_id INT,
    FOREIGN KEY (country_id) REFERENCES country(id)
);

-- 📍 Location (mittauspaikka)
CREATE TABLE location (
    id INT PRIMARY KEY, -- OpenAQ location_id
    name VARCHAR(255),
    city_id INT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    FOREIGN KEY (city_id) REFERENCES city(id)
);

-- 🌡️ Sensor (pm25, pm10, no2 jne)
CREATE TABLE sensor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 📊 Measurement (mittausdata)
CREATE TABLE measurement (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    location_id INT,
    sensor_id INT,
    value FLOAT,
    unit VARCHAR(20),
    datetime DATETIME,

    FOREIGN KEY (location_id) REFERENCES location(id),
    FOREIGN KEY (sensor_id) REFERENCES sensor(id),

    INDEX (location_id),
    INDEX (sensor_id),
    INDEX (datetime)
);