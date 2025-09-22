"""User service"""

import secrets
import sqlite3
from flask import session, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

def hash_password(password):
    """Util to hash password"""
    return generate_password_hash(password)

def create_user(username, password_hash):
    """Create user, throw error if user already registered"""
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        flash("Rekisteröityminen onnistui! Kirjaudu sisään.", "success")
        return redirect(f"/login?username={username}")
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu", "error")
        return redirect("/register")

def get_user(username, password):
    """Get user, throw error if there are users in the database that have malformed data"""
    try:
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        query = db.query(sql, [username])
        password_hash = query[0][1]
        user_id = query[0][0]
    except IndexError:
        flash("VIRHE: tapahtui virhe. Tarkista käyttäjätunnus ja salasana.", "error")
        return redirect(f"/login?username={username}")

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    flash("VIRHE: tapahtui virhe. Tarkista käyttäjätunnus ja salasana.", "error")
    return redirect(f"/login?username={username}")
