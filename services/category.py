import database.db as db

def get_categories():
    sql = """SELECT c.label, c.id
             FROM categories c
             """
    exercises = db.query(sql)
    return exercises