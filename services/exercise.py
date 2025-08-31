import database.db as db

def get_user_exercises(user_id):
    sql = """SELECT e.id, e.title, s.weight, s.set_amount, s.rep_amount
             FROM exercises e
             JOIN stats s ON e.id = s.exercise_id
             WHERE s.user_id = ?
             """
    exercises = db.query(sql, [user_id])
    return exercises

def create_exercise(user_id, title, set_amount, rep_amount, weight, description):
    sql = """INSERT INTO exercises (title, description, goal_weight, goal_set_amount, goal_rep_amount, user_id) 
             VALUES (?, ?, ?, ?, ?, ?)
             """
    db.execute(sql, [title, description, weight, set_amount, rep_amount, user_id])
    return db.last_insert_id()