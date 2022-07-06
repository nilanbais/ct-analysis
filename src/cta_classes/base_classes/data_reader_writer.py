"""
Classes dedicated to reading and writing data.
"""
import json

class Reader():

    """
    Methods to manage reading and writing the data
    """
    def _read_json(self, file_name: str, folder_name: str) -> dict:
        """
        Base method (a method that will be extrended to specific use cases)
        """
        with open("./{}/{}".format(folder_name, file_name), 'r') as json_file:
            return json.load(json_file)

    def read_resource(self, file_name: str) -> dict:
        """Returns data from a file from the resource folder.
        """
        return self._read_json(file_name=file_name, folder_name='res')