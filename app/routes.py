from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
    redirect,
    url_for,
    current_app,
)
from bson.objectid import ObjectId

main = Blueprint("main", __name__)


def redirect_url():
    return request.args.get("next") or request.referrer or url_for("main.list")


@main.route("/")
def home():
    return redirect(url_for("main.list"))


@main.route("/uncompleted")
def tasks():
    todos = current_app.db.todo.find({"done": "no"})
    return render_template(
        "index.html", todos=todos, h="Tâches en cours", t="ToDo App - Tâches en cours"
    )


@main.route("/completed")
def completed():
    todos = current_app.db.todo.find({"done": "yes"})
    return render_template(
        "index.html", todos=todos, h="Tâches terminées", t="ToDo App - Terminées"
    )


@main.route("/list")
def list():
    todos = current_app.db.todo.find()
    return render_template(
        "index.html",
        todos=todos,
        h="Liste globale des tâches",
        t="ToDo App - Liste des taches",
    )


@main.route("/done")
def done():
    id = request.values.get("_id")
    try:
        task = current_app.db.todo.find_one({"_id": ObjectId(id)})
        if task["done"] == "yes":
            current_app.db.todo.update_one(
                {"_id": ObjectId(id)}, {"$set": {"done": "no"}}
            )
        else:
            current_app.db.todo.update_one(
                {"_id": ObjectId(id)}, {"$set": {"done": "yes"}}
            )
        return redirect(request.referrer or url_for("main.list"))
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return redirect(url_for("main.list"))


@main.route("/search")
def search():
    key = request.args.get("key", "")
    refer = request.args.get("refer", "name")

    if not key:
        return redirect(url_for("main.list"))

    filter_query = {}
    if refer == "name":
        filter_query = {"name": {"$regex": f".*{key}.*", "$options": "i"}}
    elif refer == "desc":
        filter_query = {"desc": {"$regex": f".*{key}.*", "$options": "i"}}
    elif refer == "date":
        filter_query = {"date": key}
    elif refer == "pr":
        filter_query = {"pr": {"$regex": f".*{key}.*", "$options": "i"}}

    cursor = current_app.db.todo.find(filter_query)
    todos = [task for task in cursor]

    return render_template(
        "search.html",
        todos=todos,
        query=key,
        refer=refer,
        h="Résultats de recherche",
        t="ToDo App - Recherche",
    )


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


@main.route("/update")
def update():
    try:
        id = request.values.get("_id")
        task = current_app.db.todo.find_one({"_id": ObjectId(id)})
        if task:
            return render_template(
                "update.html",
                task=task,
                h="Modifier la tâche",
                t="ToDo App - Modification",
            )
        return redirect(url_for("main.tasks"))
    except Exception as e:
        print(f"Erreur lors de la mise à jour: {str(e)}")
        return redirect(url_for("main.tasks"))


@main.route("/action3", methods=["POST"])
def action3():
    try:
        id = request.values.get("_id")
        name = request.values.get("name")
        desc = request.values.get("desc")
        date = request.values.get("date")
        pr = request.values.get("pr")

        current_app.db.todo.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"name": name, "desc": desc, "date": date, "pr": pr}},
        )
        return redirect(url_for("main.tasks"))
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {str(e)}")
        return redirect(url_for("main.tasks"))
