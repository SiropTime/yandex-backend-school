from flask import Flask

from utility import logger


app = Flask(__name__)
app.config.from_pyfile("config.cfg")


@app.route('/')
def home():
    logger.info("Successfully got the request")
    return 'Test'


@app.route('/imports', methods=["POST"])
def imports():
    pass


@app.route('/delete/{id}', methods=["DELETE"])
def delete():
    pass


@app.route('/nodes/{id}', methods=["GET"])
def nodes():
    pass


@app.route('/updates', methods=["GET"])
def updates():
    pass


@app.route('/node/{id}/history', methods=["GET"])
def node_history():
    pass

