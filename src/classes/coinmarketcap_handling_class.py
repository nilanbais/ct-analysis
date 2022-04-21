"""
This script is responsible for both the interaction with the CoinMarketCap API and all the trasformations that
need to happen on this data, recieved as a response from the API.

The API works using a specified user account maintained for the porpose of the automation. The code 
and comments will refer to this account as the base_user.
"""
import json
import dotenv
from api_authentication_class import ApiAuthentication

class CoinMarketCapAPI(ApiAuthentication):

    def __init__(self) -> None:
        super().__init__('CMC_API_KEY')
        self.__config = dotenv.dotenv_values('./res/.env')
        self.__CMC_API_URL_MAP = self.__config["CMC_API_URL_MAP_FILE"]

        self.API_URL_MAP = self.read_resource(file_name=self.__CMC_API_URL_MAP)

    """
    Methods to manage reading and writing the data
    """
    def read_json(self, file_name: str, folder_name: str) -> dict:
        """
        Base method (a method that will be extrended to specific use cases)
        """
        with open("./{}/{}".format(folder_name, file_name), 'r') as json_file:
            return json.load(json_file)

    def store_json(self, json_data: dict, file_name: str, folder_name: str) -> None:
        """
        THIS METHOD IS GOING TO BE REPLACED WITH THE COMMUNICATION WITH THE MONGODB DATABASE.
        """
        with open('./{}/{}'.format(folder_name, file_name), 'w') as json_file:
            json.dump(json_data, json_file)


    def read_resource(self, file_name: str) -> dict:
        return self.read_json(file_name=file_name, folder_name='res')

    def store_response(self, json_data: dict, file_name: str) -> None:
        return self.store_json(json_data=json_data, file_name=file_name, folder_name='data')
