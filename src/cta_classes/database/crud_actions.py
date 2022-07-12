
from typing import List
from pymongo.database import Database, Collection

from cta_classes.database.connection import DataBaseConnection

class DataBaseActions:
    """
    Class responsible for handling the transormations of the data in the database like adding new data and stuff. 
    THIS CLASS NEEDS TO HAVE THE FUNCTIONALITY FOR THE CONNECTION ISOLATED AS AN ATTRUBITE. MIND THAT THIS DOESN'T INCLUDE
    THE FUNCTIONALITIES OF LISTING THE DATABASES AND SETTING AN ACTIVE DATABASE. THESE METHODS HAVE TO BE SEEN AS AN
    ACTION COMPLETED ON THE DATABASE, NOT PART OF THE DATABASE CONNECTION.
    """
    def __init__(self) -> None:
        self.__connection = DataBaseConnection()
    
    """
    # Database Selection Methods
    """
    def list_databases(self) -> list:
        """Returns databases available in the client
        """
        return self.__connection.client.list_database_names()
    
    def check_database_available(self, database_name: str) -> bool:
        db_available = True if database_name in [name for name in self.list_databases()] else False
        return db_available

    def set_active_database(self, database_name: str) -> None:
        """Sets the active database if the given database is available.
        """
        check_bool = self.check_database_available(database_name)
        
        if check_bool:
            self.__connection.active_database = self.__connection.client[database_name]
        elif not check_bool:
            raise Exception(f"You're trying to connect to a database that doesn't exists, fam. Bellow are the available databases.\n{self.list_databases()}")
    
    def get_active_database(self) -> Database:
        """Returns the active database.
        """
        return self.__connection.active_database

    """
    # Collection Selection Methods
    """
    def list_collections(self) -> list:
        """Returns a list of the available collections in the active database.
        """
        return self.__connection.active_database.list_collection_names()
    
    def check_collection_in_database(self, collection_name: str) -> bool:
        """Checks if the given collection is available in the database.
        """
        collection_available = True if collection_name in [name for name in self.list_collections()] else False
        return collection_available

    def set_active_collection(self, collection_name: str) -> None:
        """Sets the active collection if the given collection is available.
        """
        check_bool = self.check_collection_in_database(collection_name)

        if check_bool:
            self.__connection.active_collection = self.__connection.active_database[collection_name]
        elif not check_bool:
            raise Exception(f"You're trying to activate a collection that doesn't exists in the selected database, cuh. Bellow are the available collections.\n{self.list_collections()}")

    def get_active_collection(self) -> Collection:
        """Returns the active database.
        """
        return self.__connection.active_collection

    """
    Insert/Extract Methods
    """
    def insert_one(self, document: dict, database_name: Database = None, collection_name: str = None) -> None:
        """Checks if the given database and collection are the active ones (if specified).
        Inserts a new document into the active or specified collection.
        """
        # Check active database and set if needed
        if database_name is not None and database_name != self.__connection.active_database.name:
            self.set_active_database(database_name=database_name)
        
        # Check active collection and set if needed
        if collection_name is not None and collection_name != self.__connection.active_collection.name:
            self.set_active_collection(collection_name=collection_name)
        
        # Insert document into active collection
        self.__connection.active_collection.insert_one(document)

    def insert_many(self, documents: List[dict], database_name: Database = None, collection_name: str = None) -> None:
        """Checks if the given database and collection are the active ones (if specified).
        Inserts multiple new documents into the active or specified collection.
        """
        # Check active database and set if needed
        if database_name is not None and database_name != self.__connection.active_database.name:
            self.set_active_database(database_name=database_name)
        

        print(self.__connection.active_collection, type(self.__connection.active_collection))
        # Check active collection and set if needed
        if collection_name is not None and collection_name != self.__connection.active_collection:
            self.set_active_collection(collection_name=collection_name)
        
        # Insert document into active collection
        self.__connection.active_collection.insert_many(documents)

    """
    Create Replace Update Delete (CRUD) Methods
    """
    def delete_many_documents(self, collection_name: str, query: dict) -> None:
        """Private method to delete the queried documents from the given collection.
        """
        database = self.__connection.client["cta-database"]
        database[collection_name].delete_many(query)

    def _empty_collection(self, collection_name: str) -> None:
        """Private method to empty a given collection from the cta_databse.
        """
        user_input = input(f"{'-'*20}WARING{'-'*20}\nYou're about the empty the collection {collection_name}.\nDo you want to proceed? y/n\n")
        if user_input in ['y', 'yes']:
            self.delete_many_documents(collection_name=collection_name, 
                                       query={})
            print("Done my dude")
        elif user_input in ['n', 'no']:
            print("Nothing happend. No worries.")
        else:
            print("I don't understand what you mean so I'm aborting the mission.")