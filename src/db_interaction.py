"""
This script is responsible for the communication with the database that is used for storing the extracted/collected data. 
The goal is to shape this script in a way that it stays flexible in the appliance of the script. Think about a class that uses
some parameters to connect to the db. Also assume that the structure of the database is set in stone, so it's possible to write
some functions that isolate/extract some specific pieces of data. And write funcitonality that updates the data structure automaticly
by just giving it the piece of data that needs to be updated.

[] - write a class responisble for the connection with the database.
[] - (optional) write functionality that tests the connection before each action.

[] - write a class that is resposible for the transformation of the data in the database AND uses the class for the db connection.
[] - use as many input variables as possible for the methods in the class. 
"""
import dotenv

# env variables
__config = dotenv.dotenv_values('./res/.env')

# Classes
class DataBaseConnection():
    """
    Class responsible for handling all the database connection actions.
    """
    pass

class DataBaseActions(DataBaseConnection):
    """
    Class responsible for handling the transormations of the data in the database.
    THIS CLASS NEEDS TO INHERET THE CONNECTION CLASS FUNCTIONALITY (WHY? DON'T REALLY KNOW BUT TRY TO UNDERSTAND INHERETANCE)
    """
    pass