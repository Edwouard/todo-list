from flask import Blueprint, jsonify, request, render_template, redirect, url_for, current_app
from bson.objectid import ObjectId

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/uncompleted")
def tasks():
    todos = current_app.db.todo.find({"done": "no"})
    return render_template("index.html", todos=todos)


@main.route("/completed")
def completed():
    todos = current_app.db.todo.find({"done": "yes"})
    return render_template("index.html", todos=todos)


@main.route("/action", methods=["POST"])
def action():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    current_app.db.todo.insert_one(
        {"name": name, "desc": desc, "date": date, "pr": pr, "done": "no"}
    )
    return redirect("/list")


@main.route("/remove")
def remove():
    key = request.values.get("_id")
    current_app.db.todo.delete_one({"_id": ObjectId(key)})
    return redirect("/")
