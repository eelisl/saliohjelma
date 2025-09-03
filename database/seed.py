"""Seed file for database"""
import random
import sqlite3
from werkzeug.security import generate_password_hash

db = sqlite3.connect("database.db")

db.execute("DELETE FROM stats")
db.execute("DELETE FROM exercises")
db.execute("DELETE FROM categories")
db.execute("DELETE FROM users")

USER_COUNT = 100
CATEGORY_COUNT = 10
EXERCISE_COUNT = 200
STAT_COUNT = 1000

# Seed users
for i in range(1, USER_COUNT + 1):
    PASSWORD = f"user{i}_password"
    password_hash = generate_password_hash(PASSWORD)
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               [f"user{i}", password_hash])

# Seed categories
for i in range(1, CATEGORY_COUNT + 1):
    db.execute("INSERT INTO categories (label) VALUES (?)",
               [f"category{i}"])

# Seed exercises for user1 and collect their IDs
user1_exercise_ids = []
for i in range(1, 11):
    category_id = random.randint(1, CATEGORY_COUNT)
    db.execute("""INSERT INTO
                    exercises (title, description, goal_weight, goal_set_amount, goal_rep_amount, user_id, category_id)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
               [
                   f"user1_exercise{i}",
                   f"description{i}",
                   random.randint(20, 100),
                   random.randint(1, 5),
                   random.randint(5, 20),
                   1,
                   category_id
                ]
    )
    user1_exercise_ids.append(db.execute("SELECT last_insert_rowid()").fetchone()[0])

# Seed remaining exercises
for i in range(11, EXERCISE_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    category_id = random.randint(1, CATEGORY_COUNT)
    db.execute("""INSERT INTO
                    exercises (title, description, goal_weight, goal_set_amount, goal_rep_amount, user_id, category_id)
                  VALUES (?, ?, ?, ?, ?, ?, ?)""",
               [
                   f"exercise{i}",
                   f"description{i}",
                   random.randint(20, 100),
                   random.randint(1, 5),
                   random.randint(5, 20),
                   user_id,
                   category_id
                ]
    )

# Seed stats (random users)
for i in range(1, STAT_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    exercise_id = random.randint(1, EXERCISE_COUNT)
    db.execute("""INSERT INTO
                    stats (weight, set_amount, rep_amount, completed_at, user_id, exercise_id)
                  VALUES (?, ?, ?, datetime('now', ? || ' days'), ?, ?)""",
               [
                   random.randint(20, 100),
                   random.randint(1, 5),
                   random.randint(5, 20),
                   str(-random.randint(0, 365)),
                   user_id,
                   exercise_id
                ]
    )

# Seed 1000 stats for user1, distributed among their 10 exercises
for i in range(1, 1001):
    exercise_id = random.choice(user1_exercise_ids)
    db.execute("""INSERT INTO
                    stats (weight, set_amount, rep_amount, completed_at, user_id, exercise_id)
                  VALUES (?, ?, ?, datetime('now', ? || ' days'), ?, ?)""",
               [
                   random.randint(20, 100),
                   random.randint(1, 5),
                   random.randint(5, 20),
                   str(-random.randint(0, 365)),
                   1,
                   exercise_id
                ]
    )

db.commit()
db.close()
