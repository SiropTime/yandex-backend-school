from flask import Flask, request, abort, Response

from utility import *


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
parent_node = Folder("0", "", "2003-07-01T00:00:00Z")


@app.route('/')
def home():
    logger.info("Successfully got the request")
    return 'Test'


@app.route('/imports', methods=["POST"])
def imports():
    data = request.get_json()
    try:
        current_items = data["items"]
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

            node.children = dict([(n.id, n) for n in filter(lambda d: d["parentId"] == node.id, current_items)])
            parent_node.children[item["id"]] = node

        elif item["type"] == FILE:
            try:
                node = File(item["id"], item["url"], item["parentId"], item["size"], data["updateDate"])
            except KeyError as ex:
                return abort(Response(f"Validation failed. '{ex.args[0]}' is required", 400))

            parent_node.children[item["id"]] = node

        else:
            return abort(Response("Validation failed. There is no needed type for imported files"), 400)


    return Response("Successfully added items", 200)


@app.route('/delete/<id>', methods=["DELETE"])
def delete(id: str):
    try:
        delete_date = request.args.get("date")
    except Exception:
        return abort(Response("Validation failed"), 400)

    try:
        del parent_node.children[id]
        logger.info(f"Succesfully deleted item with id {id}")
    except KeyError as ex:
        return abort(Response("Item not found", 404))


@app.route('/nodes/<id>', methods=["GET"])
def nodes(id: str):
    pass


@app.route('/updates', methods=["GET"])
def updates():
    pass


@app.route('/node/<id>/history', methods=["GET"])
def node_history(id: str):
    pass

