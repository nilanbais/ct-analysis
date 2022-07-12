"""
This script is responsible for the communication with the database that is used for storing the extracted/collected data. 
The goal is to shape this script in a way that it stays flexible in the appliance of the script. Think about a class that uses
some parameters to connect to the db. Also assume that the structure of the database is set in stone, so it's possible to write
some functions that isolate/extract some specific pieces of data. And write funcitonality that updates the data structure automaticly
by just giving it the piece of data that needs to be updated.

[x] - install PyMongo package (source: https://pymongo.readthedocs.io/en/stable/)
[x] - use PyMongo as python mongodb client
[] - Close the connection when done with database actions 

[x] - write a class responisble for the connection with the database.
[] - (optional) write functionality that tests the connection before each action.

[x] - write a class that is resposible for the transformation of the data in the database AND uses the class for the db connection.
[] - use as many input variables as possible for the methods in the class. 
"""

import pymongo

from pymongo import MongoClient

from cta_classes.file_handling.env_reader import EnvVarReader, SecretVarReader


class DataBaseConnection:
    """
    Class responsible for handling all the database connection actions. This also contains managing the 
    active database and the active collection. With that the class is also extended with functionalities
    to list the available databases and collections and to check if the given database/collection name.
    """
    __default_database = EnvVarReader().get_value('DEFAULT_DATABASE')

    def __init__(self) -> None:
        # env variables
        self.client = self.init_client()

        self.active_database = self.client[DataBaseConnection.__default_database]  # set by set_active_database in DataBaseActions
        self.active_collection = None  # set by set_active_collection in DataBaseActions

    """
    # Connection Methods
    """
    # --- LET OP ---
    # ADMIN ACCOUNT WORDT IN DEVELOPMENT GEBRUIKT, MAAR MOET OMGESCHREVEN WORDEN NAAR READWRITEUSER
    def init_client(self) -> MongoClient:
        __config = SecretVarReader().get_value
        client = pymongo.MongoClient(__config("DB_CONNECTION_STRING").format(__config('DB_ADMIN_PASSWORD'), __config('DB_ADMIN_NAME')))
        return client
    
    def test_connection():
        """
        Methode for testing the connection with the database
        """
        pass