import logging
import sys
import datetime
import typing

logger = logging.getLogger('__main__')
handler = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(format='[%(asctime)s %(levelname)s]:%(message)s', handlers=[handler], level=logging.DEBUG)

FILE, FOLDER = "FILE", "FOLDER"
TYPES = [FILE, FOLDER]


class Node:
    def __init__(self, id: str, url: str, parent_id: str, size: int, update_date: str):
        self.id = id
        self.url = url
        self.parent_id = parent_id
        self.size = size
        self.update_date = datetime.datetime.strptime(update_date, "%Y-%m-%dT%H:%M:%S.%f")


class File(Node):
    def __init__(self, id: str, url: str, parent_id: str, size: int, update_date: str):
        super().__init__(id, url, parent_id, size, update_date)

    def __del__(self):
        logger.info("Deleted file with id: " + self.id)


class Folder(Node):
    def __init__(self, id: str, parent_id: str, update_date: str):
        super().__init__(id, "", parent_id, 0, update_date)
        self.children = []  # id: node

    def __del__(self):
        for _ in self.children.values():
            del _
        logger.info("Deleted folder with id: " + self.id)
