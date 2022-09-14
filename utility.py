import logging
import sys
import datetime
import typing

# Logging setup
logger = logging.getLogger('__main__')
handler = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(format='[%(asctime)s %(levelname)s]:%(message)s', handlers=[handler], level=logging.DEBUG)

# Constants
FILE, FOLDER = "FILE", "FOLDER"
TYPES = [FILE, FOLDER]


# Parent class for all types
class Node:
    def __init__(self, id: str, url: str, parent_id: str, size: int, update_date: str):
        self.id = id
        self.url = url
        self.parent_id = parent_id
        self.size = size
        self.update_date = datetime.datetime.strptime(update_date, "%Y-%m-%dT%H:%M:%S.%f")

    def get_information(self) -> dict:
        pass

    def get_size(self) -> int:
        pass


class File(Node):
    def __init__(self, id: str, url: str, parent_id: str, size: int, update_date: str):
        super().__init__(id, url, parent_id, size, update_date)

    def __del__(self):
        logger.info("Deleted file with id: " + self.id)

    def get_information(self) -> dict:
        return {"update_date": self.update_date, "size": self.size, "parent_id": self.parent_id}

    def get_size(self) -> int:
        return self.size
    


class Folder(Node):
    def __init__(self, id: str, parent_id: str, update_date: str):
        super().__init__(id, "", parent_id, 0, update_date)
        self.children = []  # id: node

    def __del__(self):
        for _ in self.children.values():
            del _
        logger.info("Deleted folder with id: " + self.id)

    def get_size(self) -> int:
        return sum([item.get_size() for item in self.children.values()])

    def get_information(self) -> dict:
        return {"update_date": self.update_date, "size": self.get_size(), "parent_id": self.parent_id}


# Get all input nodes and sort them to given parent
def find_and_add_children(nodes: typing.Dict[str, Node], parent: Node):
    pass
