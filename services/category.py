"""Categories service"""
from database import db

def get_categories():
    """Get all categories"""
    sql = """SELECT c.label, c.id
             FROM categories c
             """
    exercises = db.query(sql)
    return exercises
