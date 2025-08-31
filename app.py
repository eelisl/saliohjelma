from functools import wraps
from flask import Flask, render_template, session, redirect, request, flash, abort
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

def require_csrf(f):
    @wraps(f)
    def check_csrf(*args, **kwargs):
        if request.form["csrf_token"] != session["csrf_token"]:
            abort(403)
        return f(*args, **kwargs)
    return check_csrf

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
    query = request.args.get("query")
    # Reason: if no exercises are added, there might be an error. We don't want the front page to stop working because of this.
    try:
        exercises = exerciseService.get_user_exercises(session["user_id"], query)
    except:
        exercises = []

    return render_template("index.html", exercises=exercises, query=query)

@app.route("/uusi", methods=["GET"])
@require_login
def new_exercise_page():
    return render_template("new_exercise.html")

@app.route("/harjoitteet/<int:exercise_id>/muokkaa", methods=["GET"])
@require_login
def edit_exercise_page(exercise_id):
    # Reason: if user has stale session and is not able to fetch, we need to have graceful error handling
    try:
        print(exercise_id, session["user_id"])
        exercise = exerciseService.get_exercise(exercise_id, session["user_id"])
        if not exercise:
            abort(404)
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
    
    if not 3 < len(username) < 20:
        flash("VIRHE: käyttäjätunnuksen pitää olla 3-20 merkkiä pitkä", "error")
        return redirect("/register")
    
    return userService.create_user(username, userService.generate_password_hash(password))

# Exercise

@app.route("/api/exercise", methods=["POST"])
@require_login
@require_csrf
def new_exercise():
    user_id = session["user_id"]
    title = request.form["title"]
    set_amount = request.form["set_amount"]
    rep_amount = request.form["rep_amount"]
    weight = request.form["weight"]
    description = request.form["description"]

    if not title or not 1 < len(title) < 150:
        flash("Harjoitteen nimen tulee olla vähintään 1 ja enintään 150 merkkiä pitkä.", "error")
        redirect("/uusi")
    
    if not set_amount or not 1 < int(set_amount) < 5:
        flash("Settejä tulee olla vähintään 1 ja enintään 5.", "error")
        redirect("/uusi")

    if not rep_amount or not 1 < int(rep_amount) < 50:
        flash("Toistoja tulee olla vähintään 1 ja enintään 50.", "error")
        redirect("/uusi")
    
    if not int(weight) < 200:
        flash("Okei iso poika, luulet itsestäsi liikoja, laske kiloja :D", "error")
        redirect("/uusi")

    # Reason: if session is stale, we want to gracefully throw error
    try:
        exerciseService.create_exercise(user_id, title, set_amount, rep_amount, weight, description)
        flash("Lisäys onnistui!", "success")
        return redirect("/uusi")
    except:
        flash("VIRHE: Joku meni vikaan lisäyksessä. Kokeile uudestaan.", "error")
        return redirect("/uusi")

@app.route("/api/exercise/delete", methods=["POST"])
@require_login
@require_csrf
def delete_exercise():
    exercise_id = request.form["exercise_id"]
    user_id = session["user_id"]
    referrer = request.referrer

    exerciseService.delete_exercise(exercise_id, user_id)
    flash("Harjoite poistettu.", "success")
    return redirect(referrer)


@app.route("/api/exercise/<int:exercise_id>", methods=["POST"])
@require_login
@require_csrf
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


    if not title or not 1 < len(title) < 150:
        flash("Harjoitteen nimen tulee olla vähintään 1 ja enintään 150 merkkiä pitkä.", "error")
        redirect(f"/harjoitteet/{exercise_id}/muokkaa")
    
    if not set_amount or not 1 < int(set_amount) < 5:
        flash("Settejä tulee olla vähintään 1 ja enintään 5.", "error")
        redirect(f"/harjoitteet/{exercise_id}/muokkaa")

    if not rep_amount or not 1 < int(rep_amount) < 50:
        flash("Toistoja tulee olla vähintään 1 ja enintään 50.", "error")
        redirect(f"/harjoitteet/{exercise_id}/muokkaa")
    
    if not int(weight) < 200:
        flash("Okei iso poika, luulet itsestäsi liikoja, laske kiloja :D", "error")
        redirect(f"/harjoitteet/{exercise_id}/muokkaa")


    # Reason: if session is stale, we want to gracefully throw error
    try:
        exerciseService.edit_exercise(exercise_id, user_id, title, set_amount, rep_amount, weight, description)
        flash("Muokkaus onnistui!", "success")
        return redirect(f"/")
    except Exception as e:
        print(f"Error in edit_exercise api: {e}")
        flash("VIRHE: Joku meni vikaan lisäyksessä. Kokeile uudestaan.", "error")
        return redirect(f"/harjoitteet/{exercise_id}/muokkaa")

if __name__ == "__main__":
    app.run(debug=True)