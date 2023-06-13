CREATE DATABASE cloud;

USE cloud;

CREATE TABLE
  person_profiles (
    id INT NOT NULL,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    data LONGTEXT,
    address VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    description VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
  );

CREATE TABLE
  health_records (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    uid INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    data LONGTEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (uid) REFERENCES person_profiles (id)
  );

CREATE TABLE
  researches (
    id INT NOT NULL AUTO_INCREMENT,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    data LONGTEXT,
    PRIMARY KEY (id)
  );

CREATE TABLE
  financials (
    id INT NOT NULL AUTO_INCREMENT,
    uid INT NOT NULL,
    uploader_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    data LONGTEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (uid) REFERENCES person_profiles (id)
  );
