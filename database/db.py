"""DB service"""

import sqlite3
from flask import g

# We need to give some params, so let's ignore the pylint errors here
# pylint: disable=W0102:dangerous-default-value
def get_connection():
    """Connection startup"""
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    """Execute query"""
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    """Return last insert id, that is stored in global"""
    return g.last_insert_id    

def query(sql, params=[]):
    """DB query function"""
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
