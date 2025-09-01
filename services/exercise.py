import database.db as db
import datetime

def get_user_exercises(user_id, query):
    sql = """SELECT e.id, e.title, e.goal_weight, e.goal_set_amount, e.goal_rep_amount
             FROM exercises e
             WHERE e.user_id = ?
             """
    if query:
        sql += " AND e.title LIKE ?"
    exercises = db.query(sql, [user_id] if not query else [user_id, query])
    return exercises

def get_exercise(exercise_id, user_id):
    sql = """SELECT e.id, e.title, e.goal_weight, e.goal_set_amount, e.goal_rep_amount, e.description
             FROM exercises e
             WHERE e.user_id = ? AND e.id = ?
             """
    print(sql)
    exercises = db.query(sql, [user_id, exercise_id])
    return exercises[0]

def create_exercise(user_id, title, set_amount, rep_amount, weight, description):
    sql = """INSERT INTO exercises (title, description, goal_weight, goal_set_amount, goal_rep_amount, user_id) 
             VALUES (?, ?, ?, ?, ?, ?)
             """
    db.execute(sql, [title, description, weight, set_amount, rep_amount, user_id])
    return db.last_insert_id()

def edit_exercise(exercise_id, user_id, title, set_amount, rep_amount, weight, description):
    sql = """UPDATE exercises 
             SET title = ?, description = ?, goal_weight = ?, goal_set_amount = ?, goal_rep_amount = ?
             WHERE id = ? AND user_id = ?
             """
    db.execute(sql, [title, description, weight, set_amount, rep_amount, exercise_id, user_id])
    return True

def delete_exercise(exercise_id, user_id):
    sql = "DELETE FROM exercises WHERE id = ? AND user_id = ?"
    db.execute(sql, [exercise_id, user_id])
    return True

def get_user_exercises_with_stats(user_id):
    sql = """SELECT e.id, e.title, e.goal_weight, e.goal_set_amount, e.goal_rep_amount, 
             FROM exercises e
             LEFT JOIN stats s 
                ON s.exercise_id = e.id 
                AND s.user_id = e.user_id
             WHERE e.user_id = ?
             """
    exercises = db.query(sql, [user_id])
    return exercises

def get_user_exercises_with_today_stats(user_id):
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
    exercises = db.query(sql, [user_id])
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
    return stats[0] if stats else None
