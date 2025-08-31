from functools import wraps
from flask import Flask, render_template, session, redirect, request, flash
import config
import services.user as userService
import services.exercise as exerciseService

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def require_login(f):
    @wraps(f)
    def check_id(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return check_id
##
# PAGES
##

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

@app.route("/", methods=["GET"])
@require_login
def front_page():
    try:
        exercises = exerciseService.get_user_exercises(session["user_id"])
        print(exercises)
    except:
        exercises = []

    return render_template("index.html", exercises=exercises)

@app.route("/uusi", methods=["GET"])
@require_login
def new_exercise_page():
    return render_template("new_exercise.html")

@app.route("/harjoitteet/<int:exercise_id>/muokkaa", methods=["GET"])
@require_login
def edit_exercise_page(exercise_id):
    try:
        print(exercise_id, session["user_id"])
        exercise = exerciseService.get_exercise(exercise_id, session["user_id"])
        return render_template("edit_exercise.html", exercise=exercise)
    except Exception as e:
        print(f"Error in edit_exercise_page: {e}")
        flash("VIRHE: muokattavaa harjoitetta ei löytynyt.", "error")
        return redirect("/")

##
# API
##

# User

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

# Exercise

@app.route("/api/exercise", methods=["POST"])
@require_login
def new_exercise():
    user_id = session["user_id"]
    title = request.form["title"]
    set_amount = request.form["set_amount"]
    rep_amount = request.form["rep_amount"]
    weight = request.form["weight"]
    description = request.form["description"]

    try:
        exerciseService.create_exercise(user_id, title, set_amount, rep_amount, weight, description)
        flash("Lisäys onnistui!", "success")
        return redirect("/uusi")
    
    except:
        flash("VIRHE: Joku meni vikaan lisäyksessä. Kokeile uudestaan.", "error")
        return redirect("/uusi")

@app.route("/api/exercise/delete", methods=["POST"])
@require_login
def delete_exercise():
    exercise_id = request.form["exercise_id"]
    user_id = session["user_id"]
    referrer = request.referrer
    try:
        exerciseService.delete_exercise(exercise_id, user_id)
        flash("Harjoite poistettu.", "success")
        return redirect(referrer)
    except:
        flash("VIRHE: Joku meni vikaan lisäyksessä. Kokeile uudestaan.", "error")
        return redirect(referrer)

@app.route("/api/exercise/<int:exercise_id>", methods=["POST"])
@require_login
def edit_exercise(exercise_id):
    if not exercise_id:
        flash("VIRHE: Joku meni vikaan muokkauksessa. Kokeile uudestaan.", "error")
        return redirect("/")
    
    user_id = session["user_id"]
    title = request.form["title"]
    set_amount = request.form["set_amount"]
    rep_amount = request.form["rep_amount"]
    weight = request.form["weight"]
    description = request.form["description"]

    try:
        exerciseService.edit_exercise(exercise_id, user_id, title, set_amount, rep_amount, weight, description)
        flash("Lisäys onnistui!", "success")
        return redirect(f"/harjoitteet/{exercise_id}/muokkaa")
    
    except Exception as e:
        print(f"Error in edit_exercise api: {e}")
        flash("VIRHE: Joku meni vikaan lisäyksessä. Kokeile uudestaan.", "error")
        return redirect(f"/harjoitteet/{exercise_id}/muokkaa")

if __name__ == "__main__":
    app.run(debug=True)