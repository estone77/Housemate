from flask_app import app
from flask_app.models.comment import Comment
from flask import flash, render_template, redirect, request, session
from pprint import pprint


# another change 2
@app.post("/comments/create")
def create_comment():
    """Process the new comment form."""

    Comment.create(request.form)
    chore_id = request.form["chore_id"]
    return redirect(f"/chores/{chore_id}")


@app.post("/comments/delete")
def delete_comment():
    """Process the delete comment form."""

    Comment.delete(request.form)
    chore_id = request.form["chore_id"]
    return redirect(f"/chores/{chore_id}")
