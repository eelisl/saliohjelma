import database.db as db
import sqlite3
from flask import session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

def hash_password(password):
    return generate_password_hash(password)

def create_user(username, password_hash):
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        flash("Rekisteröityminen onnistui! Kirjaudu sisään.", "success")
        return redirect("/login")
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu", "error")
        return redirect("/register")
    
def get_user(username, password):
    try:
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        query = db.query(sql, [username])
        password_hash = query[0][1]
        user_id = query[0][0]
        print(password_hash, user_id)
    except IndexError:
        flash("VIRHE: tapahtui virhe. Tarkista käyttäjätunnus ja salasana.", "error")
        return redirect("/login")

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        flash("VIRHE: tapahtui virhe. Tarkista käyttäjätunnus ja salasana.", "error")
        return redirect("/login")