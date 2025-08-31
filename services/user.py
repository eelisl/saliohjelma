import database.db as db
import sqlite3
from flask import session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash

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
        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]
    except IndexError:
        flash("VIRHE: tapahtui virhe. Tarkista käyttäjätunnus ja salasana.", "error")
        return redirect("/login")

    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        flash("VIRHE: tapahtui virhe. Tarkista käyttäjätunnus ja salasana.", "error")
        return redirect("/login")