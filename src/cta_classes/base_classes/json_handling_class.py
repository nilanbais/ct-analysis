"""
class to be inhereted by classes to gain standard read/write json methods
"""
import json


class JsonHandler:

    def __init__(self) -> None:
        pass

    def _read_json(self, file_name: str, folder_name: str) -> dict:
        """
        Base method (a method that will be extrended to specific use cases)
        """
        with open("./{}/{}".format(folder_name, file_name), 'r') as json_file:
            return json.load(json_file)