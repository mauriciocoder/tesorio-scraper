DROP TABLE IF EXISTS REPOSITORY;
DROP TABLE IF EXISTS USER;

CREATE TABLE REPOSITORY (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  NAME TEXT UNIQUE NOT NULL,
  FULL_NAME TEXT,
  DESCRIPTION TEXT,
  LANGUAGE TEXT,
  HTML_URL TEXT,
  FORKS INTEGER,
  CREATED_AT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UPDATED_AT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE USER (
  ID INTEGER PRIMARY KEY AUTOINCREMENT,
  LOGIN TEXT UNIQUE NOT NULL
);

CREATE TABLE REPOSITORY_USER (
  REPOSITORY_ID INTEGER,
  USER_ID INTEGER
);