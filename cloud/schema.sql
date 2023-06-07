CREATE DATABASE cloud;

USE cloud;

CREATE TABLE
  health_records (
    id INT NOT NULL AUTO_INCREMENT,
    uid INT NOT NULL,
    creator INT NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    file_location VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
  );

CREATE TABLE
  person_profiles (
    id INT NOT NULL AUTO_INCREMENT,
    uid INT NOT NULL,
    creator INT NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    file_location VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE,
    address VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
  );

CREATE TABLE
  research (
    id INT NOT NULL AUTO_INCREMENT,
    uid INT NOT NULL,
    creator INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    file_location VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id)
  );

CREATE TABLE
  financials (
    id INT NOT NULL AUTO_INCREMENT,
    uid INT NOT NULL,
    creator INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    file_location VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id)
  );
