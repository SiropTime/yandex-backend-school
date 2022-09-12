import logging
import sys
import datetime

logger = logging.getLogger('__main__')
handler = logging.StreamHandler(stream=sys.stdout)
logging.basicConfig(format='[%(asctime)s %(levelname)s]:%(message)s', handlers=[handler], level=logging.DEBUG)

FILE, FOLDER = "FILE", "FOLDER"
TYPES = [FILE, FOLDER]


class Node:
    def __init__(self, id: int, url: str, parent_id: int, size: int, update_date: str):
        self.id = id
        self.url = url
        self.parent_id = parent_id
        self.size = size
        self.update_date = datetime.datetime.strptime(update_date, "%Y-%m-%dT%H:%M:%S.%f")

    
