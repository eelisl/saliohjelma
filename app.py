"""Main application"""
from functools import wraps
from math import ceil
import time
import datetime
from flask import Flask, render_template, session, redirect, request, flash, abort
from flask import g
import markupsafe
import config
import services.user as userService
import services.exercise as exerciseService
import services.category as categoryService

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.before_request
def before_request():
    """Save request start time to global"""
    g.start_time = time.time()

@app.after_request
def after_request(response):
    """Print elapsed time from the saved start time"""
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

def require_login(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def check_id(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return check_id

def require_csrf(f):
    """Decorator to check if form has csrf"""
    @wraps(f)
    def check_csrf(*args, **kwargs):
        if request.form["csrf_token"] != session["csrf_token"]:
            abort(403)
        return f(*args, **kwargs)
    return check_csrf

@app.template_filter()
def show_lines(content):
    """Template filter to keep the row change in the UI"""
    print(content)
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    print(content)
    return markupsafe.Markup(content)

##
# PAGES
##

@app.route("/login", methods=["GET"])
def login_page():
    """Login page"""
    return render_template("login.html", hide_navigation=True)

@app.route("/register", methods=["GET"])
def register_page():
    """Register page"""
    return render_template("register.html", hide_navigation=True)

@app.route("/logout", methods=["GET"])
def logout():
    """Logout page"""
    del session["user_id"]
    return redirect("/")

@app.route("/", methods=["GET"])
@require_login
def front_page():
    """Front page"""

    query = request.args.get("query")
    exercises = exerciseService.get_user_exercises(session["user_id"], query)
    return render_template("index.html", exercises=exercises, query=query)

@app.route("/uusi", methods=["GET"])
@require_login
def new_exercise_page():
    """Exercise creation page"""

    categories = categoryService.get_categories()
    return render_template("new_exercise.html", categories=categories)

@app.route("/harjoitteet/<int:exercise_id>", methods=["GET"])
@require_login
def single_exercise_page(exercise_id):
    """Single exercise page"""

    referrer = request.args.get("referrer")
    exercise = exerciseService.get_exercise(exercise_id, session["user_id"])
    categories = categoryService.get_categories()
    print(exercise["description"])
    if not exercise:
        abort(404)
    return render_template(
        "single.html", 
        exercise=exercise,
        categories=categories,
        referrer=referrer
    )


@app.route("/harjoitteet/<int:exercise_id>/muokkaa", methods=["GET"])
@require_login
def edit_exercise_page(exercise_id):
    """Exercise editor page"""

    referrer = request.args.get("referrer")
    exercise = exerciseService.get_exercise(exercise_id, session["user_id"])
    categories = categoryService.get_categories()
    if not exercise:
        abort(404)
    return render_template(
        "edit_exercise.html", 
        exercise=exercise,
        categories=categories,
        referrer=referrer
    )

@app.route("/profiili", methods=["GET"])
@require_login
def profile_page():
    """Profile page"""

    page_size = 10
    query = request.args.get("query")
    page = int(request.args.get("page")) if request.args.get("page") else 1
    exercises = exerciseService.get_user_exercises_with_stats(
        session["user_id"],
        query,
        page_size,
        page
    )
    stats = exerciseService.get_profile_stats(session["user_id"])

    total = exerciseService.count_user_exercises_with_stats(session["user_id"], query)
    page_count = max(1, ceil(total / page_size))

    return render_template(
        "profile.html",
        exercises=exercises,
        stats=stats,
        page=page,
        page_count=page_count
    )

@app.route("/harjoittele", methods=["GET"])
@require_login
def exercise_page():
    """Exercise page"""

    query = request.args.get("query")
    exercises = exerciseService.get_user_exercises_with_today_stats(session["user_id"], query)
    today_end_time = datetime.datetime.combine(
        datetime.date.today(), datetime.time(23, 59, 59)
    ).strftime("%Y-%m-%d %H:%M:%S")

    return render_template(
        "exercise.html", 
        exercises=exercises,
        query=query,
        today_end_time=today_end_time
    )

@app.route("/harjoitteet", methods=["GET"])
@require_login
def all_exercises_page():
    """All exercises page"""

    page_size = 10
    query = request.args.get("query")
    page = int(request.args.get("page")) if request.args.get("page") else 1
    exercises = exerciseService.get_exercises(query, page_size, page)

    total = exerciseService.count_exercises(query)
    categories = categoryService.get_categories()
    page_count = max(1, ceil(total / page_size))

    return render_template(
        "all_exercises.html",
        exercises=exercises,
        query=query,
        page=page,
        page_count=page_count,
        categories=categories
    )
##
# API
##

# User

@app.route("/api/login", methods=["POST"])
def login():
    """API route: login"""

    username = request.form["username"]
    password = request.form["password"]
    return userService.get_user(username, password)

@app.route("/api/register", methods=["POST"])
def register():
    """API route: register"""

    username = request.form["username"]
    password = request.form["password1"]
    password_again = request.form["password2"]

    if password != password_again:
        flash("VIRHE: salasanat eivät ole samat", "error")
        return redirect("/register")

    if not 3 < len(username) < 20:
        flash("VIRHE: käyttäjätunnuksen pitää olla 3-20 merkkiä pitkä", "error")
        return redirect("/register")

    if not 8 <= len(password):
        flash("VIRHE: salasanan pitää olla vähintään 8 merkkiä pitkä.", "error")
        return redirect("/register")

    return userService.create_user(username, userService.generate_password_hash(password))

# Exercise

@app.route("/api/exercise", methods=["POST"])
@require_login
@require_csrf
def new_exercise():
    """API route: new exercise"""

    user_id = session["user_id"]
    title = request.form["title"]
    set_amount = request.form["set_amount"]
    rep_amount = request.form["rep_amount"]
    weight = request.form["weight"]
    description = request.form["description"]
    category_id = request.form["category_id"]

    if not title or not 1 < len(title) < 40:
        flash("Harjoitteen nimen tulee olla vähintään 1 ja enintään 40 merkkiä pitkä.", "error")
        return redirect("/uusi")

    if not set_amount or not 1 < int(set_amount) < 5:
        flash("Settejä tulee olla vähintään 1 ja enintään 5.", "error")
        return redirect("/uusi")

    if not rep_amount or not 1 < int(rep_amount) < 50:
        flash("Toistoja tulee olla vähintään 1 ja enintään 50.", "error")
        return redirect("/uusi")

    if int(weight) >= 200:
        flash("Okei iso poika, luulet itsestäsi liikoja, laske kiloja :D", "error")
        return redirect("/uusi")

    exerciseService.create_exercise([
        user_id,
        title,
        set_amount,
        rep_amount,
        weight,
        description,
        category_id
    ])

    flash("Lisäys onnistui!", "success")
    return redirect("/uusi")

@app.route("/api/exercise/delete", methods=["POST"])
@require_login
@require_csrf
def delete_exercise():
    """API route: delete exercise"""

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
    """API route: edit exercise"""

    if not exercise_id:
        flash("VIRHE: Joku meni vikaan muokkauksessa. Kokeile uudestaan.", "error")
        return redirect("/")

    user_id = session["user_id"]
    title = request.form["title"]
    set_amount = request.form["set_amount"]
    rep_amount = request.form["rep_amount"]
    weight = request.form["weight"]
    description = request.form["description"]
    category_id = request.form["category_id"]
    referrer = request.form["referrer"]

    if not title or not 1 < len(title) < 150:
        flash("Harjoitteen nimen tulee olla vähintään 1 ja enintään 150 merkkiä pitkä.", "error")
        redirect(referrer)

    if not set_amount or not 1 < int(set_amount) < 5:
        flash("Settejä tulee olla vähintään 1 ja enintään 5.", "error")
        redirect(referrer)

    if not rep_amount or not 1 < int(rep_amount) < 50:
        flash("Toistoja tulee olla vähintään 1 ja enintään 50.", "error")
        redirect(referrer)

    if int(weight) >= 200:
        flash("Okei iso poika, luulet itsestäsi liikoja, laske kiloja :D", "error")
        redirect(referrer)


    exerciseService.edit_exercise([
        exercise_id,
        user_id,
        title,
        set_amount,
        rep_amount,
        weight,
        description,
        category_id
    ])

    flash("Muokkaus onnistui!", "success")
    return redirect(referrer)

@app.route("/api/exercise/<int:exercise_id>/done", methods=["POST"])
@require_login
@require_csrf
def new_exercise_stats(exercise_id):
    """API route: update exercise to be done"""

    user_id = session["user_id"]
    set_amount = request.form["set_amount"]
    rep_amount = request.form["rep_amount"]
    weight = request.form["weight"]

    if not set_amount or not 1 < int(set_amount) < 5:
        flash("Settejä tulee olla vähintään 1 ja enintään 5.", "error")
        redirect("/harjoittele")

    if not rep_amount or not 1 < int(rep_amount) < 50:
        flash("Toistoja tulee olla vähintään 1 ja enintään 50.", "error")
        redirect("/harjoittele")

    if int(weight) >= 200:
        flash("Okei iso poika, luulet itsestäsi liikoja, laske kiloja :D", "error")
        redirect("/harjoittele")

    exerciseService.add_exercise_stats(user_id, exercise_id, set_amount, rep_amount, weight)
    flash("Lisäys onnistui!", "success")
    return redirect("/harjoittele")

@app.route("/api/exercise/<int:exercise_id>/category", methods=["POST"])
@require_login
@require_csrf
def edit_exercise_category(exercise_id):
    """API Route: update category of an exercise"""

    category_id = request.form["category_id"]
    page = request.form["page"]

    if not category_id:
        flash("Pitäisi olla joku kategoria", "error")
        redirect("/harjoitteet")

    exerciseService.edit_category(exercise_id, category_id)
    flash("Kategorian muutos onnistui!", "success")
    return redirect(f"/harjoitteet?page={page}")

# Assets
@app.route("/assets/logo")
def serve_logo():
    """Serve logo asset"""

    return app.send_static_file("logo.png")

if __name__ == "__main__":
    app.run(debug=True)
