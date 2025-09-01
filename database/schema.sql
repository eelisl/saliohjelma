CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    label TEXT
);

CREATE TABLE exercises (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    goal_weight INTEGER,
    goal_set_amount INTEGER,
    goal_rep_amount INTEGER,
    user_id INTEGER REFERENCES users,
    category_id INTEGER REFERENCES categories
);

CREATE TABLE stats (
    id INTEGER PRIMARY KEY,
    weight INTEGER,
    set_amount INTEGER,
    rep_amount INTEGER,
    completed_at TEXT,
    user_id INTEGER REFERENCES users,
    exercise_id INTEGER REFERENCES exercises
);