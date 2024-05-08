from flask_app import app
from flask_app.models.event import Event
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session
from pprint import pprint


@app.route("/events/all")
def events():
    """This route displays all events."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    events = Event.find_all_with_users()
    user = User.find_by_id(session["user_id"])
    # context = {"events": events, "user": user}
    return render_template("all_events.html", user=user, events=events)


@app.route("/events/new")
def new_event():
    """This route displays the new event form."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.find_by_id(session["user_id"])
    return render_template("new_event.html", user=user)


@app.post("/events/create")
def create_event():
    """The route that processes the form."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    if not Event.form_is_valid(request.form):
        return redirect("/events/new")

    # print(request.form)
    event_id = Event.create_event(request.form)
    pprint("THIS IS THE NEW EVENT'S ID: " + str(event_id))
    return redirect("/events/all")


@app.get("/events/<int:event_id>")
def event_details(event_id):
    """This route displays one event's details"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    event = Event.find_by_id_with_user_and_comments(event_id)
    user = User.find_by_id(session["user_id"])

    return render_template("event_details.html", user=user, event=event)


@app.get("/events/<int:event_id>/edit")
def edit_event(event_id):
    """This route displays the edit form"""

    event = Event.find_by_id(event_id)
    if event == None:
        return "Event does not exist"

    user = User.find_by_id(session["user_id"])
    return render_template("edit_event.html", user=user, event=event)


@app.post("/events/update")
def update_event():
    """This route processes the edit form"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    event_id = request.form["event_id"]
    if not Event.form_is_valid(request.form):
        return redirect(f"/events/{event_id}/edit")

    Event.update(request.form)
    return redirect(f"/events/{event_id}")


@app.post("/events/<int:event_id>/delete")
def delete_event(event_id):
    """This route deletes a event"""
    Event.delete_by_id(event_id)
    return redirect("/events/all")
