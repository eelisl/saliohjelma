from flask import Flask, render_template, session, redirect
import config
import sqlite3
import os
import database.db as db

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def require_login():
    if "user_id" not in session:
        return redirect("/login")

@app.route('/', methods=['GET'])
def front_page():
    require_login()
    login_check = require_login()
    if login_check:
        return login_check
    return render_template("index.html")

@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html", hide_navigation=True)

# TODO: not an actual route yet
@app.route('/login', method="POST")
def login():
    return render_template("login.html", hide_navigation=True)

@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html", hide_navigation=True)

# TODO: not an actual route yet
@app.route('/register', methods=['POST'])
def register():
    return render_template("register.html", hide_navigation=True)

if __name__ == '__main__':
    app.run(debug=True)