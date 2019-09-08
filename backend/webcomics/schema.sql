DROP TABLE IF EXISTS comics;
DROP TABLE IF EXISTS strips;
DROP TABLE IF EXISTS reads;

CREATE TABLE IF NOT EXISTS comics (
    name TEXT PRIMARY KEY NOT NULL,
    author TEXT NOT NULL,
    link TEXT
);

CREATE TABLE IF NOT EXISTS strips (
    id INTEGER PRIMARY KEY,  -- alias for rowid
    title TEXT NOT NULL,
    link TEXT NOT NULL,
    datePublished TEXT NOT NULL,
    description TEXT,
    imgUrl TEXT,
    comic TEXT REFERENCES comics(name)
);

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS reads (
    stripId INTEGER REFERENCES strips(id),
    userId INTEGER REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
