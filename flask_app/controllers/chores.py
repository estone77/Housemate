from flask_app import app
from flask_app.models.chore import Chore
from flask_app.models.user import User
from flask_app.models.comment import Comment
from flask import flash, render_template, redirect, request, session
from pprint import pprint


@app.route("/home")
def chores():
    """This route displays home."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    chores = Chore.find_all_with_users()
    user = User.find_by_id(session["user_id"])
    # context = {"chores": chores, "user": user}
    return render_template("home.html", user=user, chores=chores)


@app.route("/chores/all")
def all_chores():
    """This route displays all chores."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    chores = Chore.find_all_with_users()
    # user = User.find_by_id(session["user_id"])
    # context = {"chores": chores, "user": user}
    return render_template("all_chores.html", chores=chores)  # user=user,


@app.route("/chores/new")
def new_chore():
    """This route displays the new chore form."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.find_by_id(session["user_id"])
    return render_template("new_chore.html", user=user)


@app.post("/chores/create")
def create_chore():
    """The route that processes the form."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    if not Chore.form_is_valid(request.form):
        return redirect("/home")

    # print(request.form)
    chore_id = Chore.create_chore(request.form)
    pprint("THIS IS THE NEW CHORE'S ID: " + str(chore_id))
    return redirect("/chores/all")


@app.get("/chores/<int:chore_id>")
def chore_details(chore_id):
    """This route displays one chore's details"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    chore = Chore.find_by_id_with_comments(chore_id)
    # users = User.find_all_users()
    user = User.find_by_id(session["user_id"])

    return render_template("chore_details.html", user=user, chore=chore)


@app.get("/chores/<int:chore_id>/edit")
def edit_chore(chore_id):
    """This route displays the edit form"""

    chore = Chore.find_by_id(chore_id)
    if chore == None:
        return "Chore does not exist"

    user = User.find_by_id(session["user_id"])
    # users = User.find_all_users()
    return render_template("edit_chore.html", user=user, chore=chore)


@app.post("/chores/update")
def update_chore():
    """This route processes the edit form"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    chore_id = request.form["chore_id"]
    if not Chore.update_form_is_valid(request.form):
        return redirect(f"/chores/{chore_id}/edit")

    Chore.update(request.form)
    return redirect(f"/chores/{chore_id}")


@app.post("/chores/<int:chore_id>/delete")
def delete_chore(chore_id):
    """This route deletes a chore"""
    Chore.delete_by_id(chore_id)
    return redirect("/chores/all")
