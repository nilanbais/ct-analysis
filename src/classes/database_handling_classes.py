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
import dotenv
import pymongo

from typing import List

from pymongo import MongoClient
from pymongo.database import Database


class DataBaseConnection():
    """
    Class responsible for handling all the database connection actions. This also contains managing the 
    active database and the active collection. With that the class is also extended with functionalities
    to list the available databases and collections and to check if the given database/collection name.
    """
    def __init__(self) -> None:
        # env variables
        self.__config = dotenv.dotenv_values('./res/.env')

        self.active_database = None  # set by set_active_database in DataBaseActions
        self.active_collection = None  # set by set_active_collection in DataBaseActions

    """
    # Connection Methods
    """
    def init_client(self) -> MongoClient:
        client = pymongo.MongoClient("mongodb+srv://m001-student:{0}@sandbox.5yy1m.mongodb.net/{1}?retryWrites=true&w=majority".format(self.__config['DB_PASSWORD'],self.__config['DB_NAME']))
        return client
    
    def test_connection():
        """
        Methode for testing the connection with the database
        """
        pass


class DataBaseActions:
    """
    Class responsible for handling the transormations of the data in the database like adding new data and stuff. 
    THIS CLASS NEEDS TO HAVE THE FUNCTIONALITY FOR THE CONNECTION ISOLATED AS AN ATTRUBITE. MIND THAT THIS DOESN'T INCLUDE
    THE FUNCTIONALITIES OF LISTING THE DATABASES AND SETTING AN ACTIVE DATABASE. THESE METHODS HAVE TO BE SEEN AS AN
    ACTION COMPLETED ON THE DATABASE, NOT PART OF THE DATABASE CONNECTION.
    """
    def __init__(self) -> None:
        self.connection = DataBaseConnection()
        self.client = self.connection.init_client()
    
    """
    # Database Selection Methods
    """
    def list_databases(self, client: MongoClient) -> list:
            return client.list_database_names()

    def set_active_database(self, client: MongoClient, database_name: str) -> None:
        check_bool = self.check_database_available(database_name)
        
        if check_bool:
            self.connection.active_database = client.get_database(database_name)
        elif not check_bool:
            raise Exception("You're trying to connect to a database that doesn't exists, fam. Use the method 'list_databases' to see the available databases")

    def check_database_available(self, database_name: str) -> bool:
        db_available = True if database_name in [name for name in self.list_databases(self.client)] else False
        return db_available
    
    """
    # Collection Selection Methods
    """
    def list_collections(self, database: Database) -> list:
        return database.list_collection_names()

    def set_active_collection(self, database: Database, collection_name: str):
        check_bool = self.check_collection_in_database(collection_name)

        if check_bool:
            self.connection.active_collection = database.get_collection(collection_name)
        elif not check_bool:
            raise Exception("You're trying to activate a collection that doesn't exists in the selected database, cuh. Use the method 'list_collections' to see the available colletions in a database")

    def check_collection_in_database(self, collection_name: str) -> bool:
        collection_available = True if collection_name in [name for name in self.list_collections(self.active_database)] else False
        return collection_available

    """
    Insert/Extract Methods
    """
    def insert_one(self, document: dict, database_name: Database = None, collection_name: str = None) -> None:
        """Checks if the given database and collection are the active ones (if specified).
        Inserts a new document into the active or specified collection.
        """
        # Check active database and set if needed
        if database_name is not None and database_name != self.connection.active_database.name:
            self.set_active_database(database_name=database_name)
        
        # Check active collection and set if needed
        if collection_name is not None and collection_name != self.connection.active_collection.name:
            self.set_active_collection(database=self.connection.active_database, collection_name=collection_name)
        
        # Insert document into active collection
        self.connection.active_collection.insert_one(document)

    def insert_many(self, documents: List[dict], database_name: Database = None, collection_name: str = None) -> None:
        """Checks if the given database and collection are the active ones (if specified).
        Inserts multiple new documents into the active or specified collection.
        """
        # Check active database and set if needed
        if database_name is not None and database_name != self.connection.active_database.name:
            self.set_active_database(database_name=database_name)
        
        # Check active collection and set if needed
        if collection_name is not None and collection_name != self.connection.active_collection.name:
            self.set_active_collection(database=self.connection.active_database, collection_name=collection_name)
        
        # Insert document into active collection
        self.connection.active_collection.insert_many(documents)

    """
    Create Replace Update Delete (CRUD) Methods
    """
    

def main():
    dba = DataBaseActions()
    print(dba.list_databases(dba.client))

    dba.set_active_database(client=dba.client, database_name='x')


if __name__ == '__main__':
    main()