CREATE DATABASE authority_server;

USE authority_server;

CREATE TABLE
  users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    attributes VARCHAR(255) NOT NULL,
    UNIQUE (username),
    PRIMARY KEY (id)
  );

INSERT INTO
  users (username, password, attributes)
VALUES
  (
    "admin",
    "22690f3254ccce4ff47abb8cf09785addc7a55e3b13c61b4b6a09bc5a3df2288",
    '{"ROLES": ["ADMIN"]}'
  );

-- admin account
INSERT INTO
  users (username, password, attributes)
VALUES
  (
    "patient",
    "22690f3254ccce4ff47abb8cf09785addc7a55e3b13c61b4b6a09bc5a3df2288",
    '{"ROLES": ["PATIENT"]}'
  );
