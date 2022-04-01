"""
This script is responsible for the communication with the database that is used for storing the extracted/collected data. 
The goal is to shape this script in a way that it stays flexible in the appliance of the script. Think about a class that uses
some parameters to connect to the db. Also assume that the structure of the database is set in stone, so it's possible to write
some functions that isolate/extract some specific pieces of data. And write funcitonality that updates the data structure automaticly
by just giving it the piece of data that needs to be updated.

[x] - install PyMongo package (source: https://pymongo.readthedocs.io/en/stable/)
[] - use PyMongo as python mongodb client 

[] - write a class responisble for the connection with the database.
[] - (optional) write functionality that tests the connection before each action.

[] - write a class that is resposible for the transformation of the data in the database AND uses the class for the db connection.
[] - use as many input variables as possible for the methods in the class. 
"""
import dotenv
import pymongo

# Classes
class DataBaseConnection():
    """
    Class responsible for handling all the database connection actions.
    """
    def __init__(self) -> None:
        # env variables
        self.__config = dotenv.dotenv_values('./res/.env')  

    def init_client(self):
        client = pymongo.MongoClient("mongodb+srv://m001-student:{0}@sandbox.5yy1m.mongodb.net/{1}?retryWrites=true&w=majority".format(self.__config['DB_PASSWORD'],self.__config['DB_NAME']))
        db = client.sample_training
        companies_collection = db.get_collection('companies')
        print(companies_collection.find_one())


class DataBaseActions(DataBaseConnection):
    """
    Class responsible for handling the transormations of the data in the database.
    THIS CLASS NEEDS TO INHERET THE CONNECTION CLASS FUNCTIONALITY (WHY? DON'T REALLY KNOW BUT TRY TO UNDERSTAND INHERETANCE)
    """
    pass

def main():
    dbc = DataBaseConnection()
    dbc.init_client()

if __name__ == '__main__':
    main()