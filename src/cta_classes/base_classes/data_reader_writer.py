"""
Classes dedicated to reading and writing data.
"""
import json
from typing import Protocol
import dotenv



class Reader():

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


class VarReaderProtocol(Protocol):

    def __init__(self) -> None:
        ...
    
    def get_value(self, variable_name: str) -> str:
        ...

class EnvVarReader:
    
    def __init__(self) -> None:
        self.__config = dotenv.dotenv_values('./res/.env')

    def get_value(self, variable_name: str) -> str:
        return self.__config[variable_name]


class SecretVarReader:

    def __init__(self) -> None:
        self.__config = dotenv.dotenv_values('./res/authentication.env')

    def get_value(self, variable_name: str) -> str:
        return self.__config[variable_name]