from app import app

from utility import logger


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


@app.route('nodes/{id}', methods=["GET"])
def nodes():
    pass


@app.route('/updates', methods=["GET"])
def updates():
    pass


@app.route('/node/{id}/history', methods=["GET"])
def node_history():
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
