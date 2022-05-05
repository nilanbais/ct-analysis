"""
class to be inhereted by classes to gain standard read/write json methods
"""
import json
import bson


class JsonHandler:

    def __init__(self) -> None:
        pass

    """ JSON file mehtods
    """
    def read_json(self, file_name: str, folder_name: str) -> dict:
        """
        Base method (a method that will be extrended to specific use cases)
        """
        with open("./{}/{}".format(folder_name, file_name), 'r') as json_file:
            return json.load(json_file)
    
    def store_json(self, json_data: dict, file_name: str, folder_name: str) -> None:
        with open('./{}/{}'.format(folder_name, file_name), 'w') as json_file:
            json.dump(json_data, json_file)
        print('Done my dude')
    
    """ BSON file mehtods
    """
    def store_bson(self, bson_data: bytes, file_name: str, folder_name: str) -> None:
        with open("./{}/{}".format(folder_name, file_name), 'wb') as bson_file:
            bson_file.write(bson_data)