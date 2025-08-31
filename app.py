from flask import Flask, render_template, session, redirect, request, flash
import config
import services.user as userService
import services.exercise as exerciseService

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def require_login():
    if "user_id" not in session:
        return redirect("/login")

@app.route("/", methods=["GET"])
def front_page():
    login_check = require_login()
    if login_check:
        return login_check
    
    exercises = exerciseService.get_user_exercises(session["user_id"])
    return render_template("index.html", excersises=exercises)

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html", hide_navigation=True)


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html", hide_navigation=True)

@app.route("/logout", methods=["GET"])
def logout():
    del session["user_id"]
    return redirect("/")

@app.route("/api/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    return userService.get_user(username, password)

@app.route("/api/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password1"]
    password_again = request.form["password2"]

    if password != password_again:
        flash("VIRHE: salasanat eivät ole samat", "error")
        return redirect("/register")
    
    return userService.create_user(username, userService.generate_password_hash(password))

if __name__ == "__main__":
    app.run(debug=True)