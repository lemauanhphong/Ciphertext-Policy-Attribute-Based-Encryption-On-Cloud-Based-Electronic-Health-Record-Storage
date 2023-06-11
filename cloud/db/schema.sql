CREATE DATABASE cloud;

USE cloud;

CREATE TABLE
  person_profiles (
    uid INT NOT NULL,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGTEXT,
    address VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    PRIMARY KEY (uid)
  );

CREATE TABLE
  health_records (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGTEXT,
    uid INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (uid) REFERENCES person_profiles (uid)
  );

CREATE TABLE
  researches (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGTEXT,
    PRIMARY KEY (id)
  );

CREATE TABLE
  financials (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGTEXT,
    uid INT NOT NULL,
    PRIMARY KEY (id)
  );
