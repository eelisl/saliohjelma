import database.db as db

def get_user_exercises(user_id):
    sql = """SELECT e.id, e.title, e.goal_weight, e.goal_set_amount, e.goal_rep_amount
             FROM exercises e
             WHERE e.user_id = ?
             """
    exercises = db.query(sql, [user_id])
    return exercises

def get_user_stats(user_id):
    sql = """SELECT e.id, e.title, e.goal_weight, e.goal_set_amount, e.goal_rep_amount
             FROM exercises e
             JOIN stats s ON e.id = s.exercise_id
             WHERE s.user_id = ?
             """
    exercises = db.query(sql, [user_id])
    print(exercises)
    return exercises

def create_exercise(user_id, title, set_amount, rep_amount, weight, description):
    sql = """INSERT INTO exercises (title, description, goal_weight, goal_set_amount, goal_rep_amount, user_id) 
             VALUES (?, ?, ?, ?, ?, ?)
             """
    db.execute(sql, [title, description, weight, set_amount, rep_amount, user_id])
    return db.last_insert_id()

def edit_exercise(exercise_id, user_id, title, set_amount, rep_amount, weight, description):
    sql = """UPDATE exercises 
             SET title = ?, description = ?, goal_weight = ?, goal_set_amount = ?, goal_rep_amount = ?, user_id = ?
             WHERE id = ?
             """
    result = db.execute(sql, [title, description, weight, set_amount, rep_amount, user_id, exercise_id])
    return result.rowcount > 0

def delete_exercise(exercise_id, user_id):
    sql = "DELETE FROM exercises WHERE id = ? AND user_id = ?"
    db.execute(sql, [exercise_id, user_id])
    return True