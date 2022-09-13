from flask import Flask, request

from utility import *


app = Flask(__name__)
app.config.from_pyfile("config.cfg")
parent_node = Folder("0", "", "2010-02-03T00:00:00Z")


@app.route('/')
def home():
    logger.info("Successfully got the request")
    return 'Test'


@app.route('/imports', methods=["POST"])
def imports():
    data = request.get_json()
    for item in data["items"]:
        node = ""
        if item["type"] == FOLDER:
            node = Folder(item["id"], item["parentId"], data["updateDate"])
            parent_node.children[item["id"]] = node
        elif item["type"] == FILE:
            pass

    return "Success"


@app.route('/delete/<id>', methods=["DELETE"])
def delete(id: str):
    pass


@app.route('/nodes/<id>', methods=["GET"])
def nodes(id: str):
    pass


@app.route('/updates', methods=["GET"])
def updates():
    pass


@app.route('/node/<id>/history', methods=["GET"])
def node_history(id: str):
    pass

