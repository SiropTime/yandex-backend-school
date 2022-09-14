import flask
from flask import Flask, request, abort, Response
from flask_sqlalchemy import SQLAlchemy

from utility import *

app = Flask(__name__)
app.config.from_pyfile("config.cfg")
parent_node = Folder("0", "", "2003-07-01T00:00:00Z")
db = SQLAlchemy(app)


# DTO
class FileDB(db.Model):
    id = db.Column(db.Text, primary_key=True)
    type = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, unique=True, nullable=False)
    parent_id = db.Column(db.Text, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    update_date = db.Column(db.Text, nullable=False)

    def __init__(self, id, type, url, parent_id, size, update_date):
        self.id = id
        self.type = type
        self.url = url
        self.parent_id = parent_id
        self.size = size
        self.update_date = update_date

    def __repr__(self):
        return f"<{FILE if self.type == FILE else FOLDER}, %r, %r>" % (self.id, self.url)


def on_init():
    results = FileDB.query.all()
    for item in results:
        parent_node.children[item.id] = File(item.id, item.url, item.parent_id, item.size, item.update_date) \
            if item.type == FILE else Folder(item.id, item.parent_id, item.update_date)


@app.route('/')
def home():
    logger.info("Successfully got the request")
    return flask.render_template('index.html')


@app.route('/imports', methods=["POST"])
def imports():
    data = request.get_json()
    current_items = []
    try:
        current_items = data["items"]
    except KeyError as ex:
        try:
            for r in data:
                current_items += r["items"]
        except KeyError as ex:
            return abort(Response("Validation failed. There is no items in JSON", 400))

    for item in current_items:
        node = None
        try:
            e = item["parentId"]
            e = item["id"]
        except KeyError as ex:
            return abort(Response(f"Validation failed. There is no {ex.args[0]} at all", 400))
        if item["id"] == item["parentId"]:
            return abort(Response("Validation failed. Item's id and its parent's id are similar", 400))

        elif item["parentId"] is None:
            item["parentId"] = ""
            logger.info(f"Item {id} has no parent. Added in main folder")

        if item["type"] == FOLDER:
            try:
                node = Folder(item["id"], item["parentId"], data["updateDate"])
            except KeyError as ex:
                return abort(Response(f"Validation failed. '{ex.args[0]}' is required", 400))

            node.children = dict([(n["id"], File(n["id"], n["url"], n["parentId"], n["size"], data["updateDate"]
            if n["type"] == FILE else Folder(n["id"], n["parentId"], data["updateDate"]))) for n in
                                  filter(lambda d: d["parentId"] == node.id, current_items)])
            logger.info(node.children)
            parent_node.children[item["id"]] = node
            db.session.add(FileDB(node.id, FOLDER, node.url, node.parent_id, node.get_size(), node.update_date))

        elif item["type"] == FILE:
            try:
                node = File(item["id"], item["url"], item["parentId"], item["size"], data["updateDate"])
            except KeyError as ex:
                return abort(Response(f"Validation failed. '{ex.args[0]}' is required", 400))

            parent_node.children[item["id"]] = node
            db.session.add(FileDB(node.id, FILE, node.url, node.parent_id, node.size, node.update_date))

        else:
            return abort(Response("Validation failed. There is no needed type for imported files"), 400)

    db.session.commit()
    return Response("Successfully added items", 200)


@app.route('/delete/<id>', methods=["DELETE"])
def delete(id: str):
    try:
        delete_date = request.args.get("date")
    except Exception:
        return abort(Response("Validation failed"), 400)

    try:
        FileDB.query.filter(FileDB.id == id).delete()
        for i in parent_node.children[id].children.keys():
            FileDB.query.filter(FileDB.id == i).delete()
        del parent_node.children[id]
        db.session.commit()
        logger.info(f"Succesfully deleted item with id {id}")
    except KeyError as ex:
        return abort(Response("Item not found", 404))

    return Response("", 200)


@app.route('/nodes/<id>', methods=["GET"])
def nodes(id: str):
    pass


@app.route('/updates', methods=["GET"])
def updates():
    pass


@app.route('/node/<id>/history', methods=["GET"])
def node_history(id: str):
    pass
