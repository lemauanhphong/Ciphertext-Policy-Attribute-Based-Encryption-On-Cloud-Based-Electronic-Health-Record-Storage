CREATE DATABASE cloud;

USE cloud;

CREATE TABLE
  health_records (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGBLOB,
    uid INT NOT NULL,
    PRIMARY KEY (id)
  );

CREATE TABLE
  person_profiles (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGBLOB,
    address VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    uid INT NOT NULL,
    PRIMARY KEY (id)
  );

CREATE TABLE
  researches (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGBLOB,
    PRIMARY KEY (id)
  );

CREATE TABLE
  financials (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    description VARCHAR(255) NOT NULL,
    data LONGBLOB,
    uid INT NOT NULL,
    PRIMARY KEY (id)
  );
