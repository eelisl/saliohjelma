import database.db as db
import datetime

def get_exercises(query, page_size, page):
    sql = """SELECT e.id, e.title, e.description, e.goal_weight, e.goal_set_amount, e.goal_rep_amount, e.category_id, c.label as category_label
             FROM exercises e
             JOIN categories c ON c.id = e.category_id
             """
    if query:
        sql += "WHERE e.title LIKE ?"
    sql += "LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    exercises = db.query(sql, [f"%{query}%", limit, offset] if query else [limit, offset])
    return exercises

def count_exercises(query):
    sql = """SELECT COUNT(*) AS total
             FROM exercises e
             """
    if query:
        sql += "WHERE e.title LIKE ? "
    count = db.query(sql, [f"%{query}%"] if query else [])
    return count[0][0]

def get_user_exercises(user_id, query):
    sql = """SELECT e.id, e.title, e.description, e.goal_weight, e.goal_set_amount, e.goal_rep_amount, e.category_id, c.label as category_label
             FROM exercises e
             JOIN categories c ON c.id = e.category_id
             WHERE e.user_id = ?
             """
    if query:
        sql += " AND e.title LIKE ?"
    exercises = db.query(sql, [user_id] if not query else [user_id, f"%{query}%"])
    return exercises

def get_exercise(exercise_id, user_id):
    sql = """SELECT e.id, e.title, e.goal_weight, e.goal_set_amount, e.goal_rep_amount, e.description, e.category_id, c.label as category_label
             FROM exercises e
             JOIN categories c ON c.id = e.category_id
             WHERE e.user_id = ? AND e.id = ?
             """
    print(sql)
    exercises = db.query(sql, [user_id, exercise_id])
    return exercises[0]

def create_exercise(user_id, title, set_amount, rep_amount, weight, description, category_id):
    sql = """INSERT INTO exercises (title, description, goal_weight, goal_set_amount, goal_rep_amount, user_id, category_id) 
             VALUES (?, ?, ?, ?, ?, ?, ?)
             """
    db.execute(sql, [title, description, weight, set_amount, rep_amount, user_id, category_id])
    return db.last_insert_id()

def edit_exercise(exercise_id, user_id, title, set_amount, rep_amount, weight, description, category_id):
    sql = """UPDATE exercises 
             SET title = ?, description = ?, goal_weight = ?, goal_set_amount = ?, goal_rep_amount = ?, category_id = ?
             WHERE id = ? AND user_id = ?
             """
    db.execute(sql, [title, description, weight, set_amount, rep_amount, category_id, exercise_id, user_id])
    return True

def delete_exercise(exercise_id, user_id):
    sql = "DELETE FROM exercises WHERE id = ? AND user_id = ?"
    db.execute(sql, [exercise_id, user_id])
    return True

def get_user_exercises_with_stats(user_id, query, page_size, page):
    sql = """SELECT s.set_amount, s.rep_amount, s.completed_at, e.id, e.title, e.description, e.goal_weight, e.goal_set_amount, e.goal_rep_amount
             FROM stats s
             JOIN exercises e
                ON s.exercise_id = e.id 
                AND s.user_id = e.user_id
             WHERE e.user_id = ?
             """
    if query:
        sql += " AND e.title LIKE ? "
    sql += "LIMIT ? OFFSET ?"
    limit = page_size
    offset = page_size * (page - 1)
    exercises = db.query(sql, [user_id, f"%{query}%", limit, offset] if query else [user_id, limit, offset])
    return exercises

def count_user_exercises_with_stats(user_id, query):
    sql = """SELECT COUNT(*) AS total
             FROM stats s
             JOIN exercises e
               ON s.exercise_id = e.id 
              AND s.user_id = e.user_id
             WHERE e.user_id = ?"""
    if query:
        sql += " AND e.title LIKE ? "
    count = db.query(sql, [user_id, f"%{query}%"] if query else [user_id])
    return count[0][0]


def get_user_exercises_with_today_stats(user_id, query):
    sql = """SELECT 
                e.id, e.title, e.goal_weight, e.goal_set_amount, e.goal_rep_amount,
                s.weight, s.set_amount, s.rep_amount, s.completed_at,
                (
                    SELECT COUNT(*) FROM stats s2
                    WHERE s2.exercise_id = e.id
                    AND s2.user_id = e.user_id
                    AND DATE(s2.completed_at) = DATE('now', 'localtime')
                ) AS completed_count_today
             FROM exercises e
             LEFT JOIN stats s 
                ON s.exercise_id = e.id 
                AND s.user_id = e.user_id
                AND DATE(s.completed_at) = DATE('now', 'localtime')
             WHERE e.user_id = ?
             """
    if query:
        sql += " AND e.title LIKE ?"
    exercises = db.query(sql, [user_id] if not query else [user_id, f"%{query}%"])
    return exercises

def add_exercise_stats(user_id, exercise_id, set_amount, rep_amount, weight):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = """INSERT INTO stats (set_amount, rep_amount, weight, completed_at, user_id, exercise_id)
             VALUES (?, ?, ?, ?, ?, ?)
             """
    db.execute(sql, [set_amount, rep_amount, weight, now, user_id, exercise_id])
    return db.last_insert_id()

def get_profile_stats(user_id):
    sql = """SELECT 
                (
                    SELECT COUNT(DISTINCT DATE(s1.completed_at)) 
                    FROM stats s1
                    WHERE s1.user_id = ?
                      AND DATE(s1.completed_at) BETWEEN DATE('now', '-7 days', 'localtime') AND DATE('now', 'localtime')
                ) as count_training_days_week,
                (
                    SELECT COUNT(DISTINCT s2.exercise_id)
                    FROM stats s2
                    WHERE s2.user_id = ?
                        AND DATE(s2.completed_at) = DATE('now', 'localtime')
                ) as count_exercises_today
             """
    stats = db.query(sql, [user_id, user_id])
    print(stats)
    return stats[0] if stats else None

def edit_category(exercise_id, category_id):
    sql = """UPDATE exercises
             SET category_id = ?
             WHERE id = ?
             """
    db.execute(sql, [category_id, exercise_id])
    return True