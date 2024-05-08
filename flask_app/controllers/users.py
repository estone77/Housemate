from flask_app import app, bcrypt
from flask_app.models.user import User
from flask import redirect, render_template, request, session, flash


@app.get("/")
def index():
    """This route displays the login and registration forms."""

    return render_template("index.html")


@app.post("/users/register")
def register():
    """This route process the register form."""

    # if form not valid redirect
    if not User.register_form_is_valid(request.form):
        return redirect("/")

    # check if user exists, redirect
    potential_user = User.find_by_email(request.form["email"])

    # if user doesnt exist redirect
    if potential_user != None:
        flash("Email in use. Please log in.", "register")
        return redirect("/")

    # user does not exist, safe to create and hash password
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "username": request.form["username"],
        "full_name": request.form["full_name"],
        "email": request.form["email"],
        "password": hashed_pw,
        "favorite_movie": request.form["favorite_movie"],
        "hobby": request.form["hobby"],
    }
    user_id = User.register(user_data)

    # save user id in session (log them in)
    session["user_id"] = user_id
    return redirect("/chores/all")
    # B/c the user's id is in session, the user is "authenticated"


@app.post("/users/login")
def login():
    """This route process the login form."""

    # if form not valid redirect
    if not User.login_form_is_valid(request.form):
        return redirect("/")

    # does user exist?
    potential_user = User.find_by_email(request.form["email"])

    # user does not exist, redirect
    if potential_user == None:
        flash("Invalid credentials.", "login")
        return redirect("/")

    # The user exists!
    user = potential_user

    # Check the password
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials.", "login")
        return redirect("/")

    # save user id in session (log them in)
    session["user_id"] = user.id
    return redirect("/chores/all")


@app.get("/users/logout")
def logout():
    """This route clears session"""
    session.clear()
    return redirect("/")


@app.get("/users/all")
def all():
    """This route displays the user dahsboard"""
    if "user_id" not in session:
        flash("You must be logged in to view this page.", "login")
        return redirect("/")

    user = User.find_by_id(session["user_id"])
    return render_template("all.html", user=user)
