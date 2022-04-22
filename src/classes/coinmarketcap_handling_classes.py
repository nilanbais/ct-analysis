"""
This script is responsible for both the interaction with the CoinMarketCap API and all the trasformations that
need to happen on this data, recieved as a response from the API.

The API works using a specified user account maintained for the porpose of the automation. The code 
and comments will refer to this account as the base_user.
"""
import json
import dotenv
from pprint import pprint

from base_classes.api_authentication_class import ApiAuthentication
from base_classes.data_transformer_class import DataTransformer

class CoinMarketCapAPI(ApiAuthentication):

    def __init__(self) -> None:
        super().__init__('CMC_API_KEY')
        self.__config = dotenv.dotenv_values('./res/.env')
        self.__CMC_API_URL_MAP = self.__config["CMC_API_URL_MAP_FILE"]

        self.API_URL_MAP = self.read_resource(file_name=self.__CMC_API_URL_MAP)

        self.data_trandform = DataTransformer()  # bij CMCDataTransform of iets met deze dubbeling ??

    """
    Methods to override attributes in ApiAthentication
    """
    def create_url(self, mode: str) -> None:
        """Sets the self.url attribute inherited from ApiAuthentication. """

        mode_options = [key for key in self.API_URL_MAP.keys()]

        if mode.lower() in mode_options:
            self.url = next((url for key, url in self.API_URL_MAP.items() if key == mode))
        else:
            raise Exception(
                "The mode you selected werkt niet neef. Please see documentation for the available modes."
            )

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

    """
    Methods to get a response from the API
    """
    def extract_coin_categories(self) -> dict:
        """Returns the categories available on CoinMarketCap"""
        self.create_header()
        self.create_query_parameters()
        self.create_url(mode='coin categories')

        json_response = self.connect_to_endpoint(authentication='api key', url=self.url, header=self.header, params=self.query_parameters)
        return json_response['data']

    def extract_symbol_id_list(self, specified_symbols: list = None) -> dict:
        """Returns a list of coin ids. 
            If a list given, it returns the is of the specified coins.
            If no list given, the method will do a standard request.
        """
        self.create_header()
        self.create_query_parameters(
            parameter_dict={"symbol": self.data_trandform.list_to_string(input_list=specified_symbols)}
        )  # specified symbols toeveogen
        self.create_url(mode='idmap')

        json_response = self.connect_to_endpoint(authentication='api key', url=self.url, header=self.header, params=self.query_parameters)
        return json_response['data']
    
    def get_symbol_data(self, symbol_id: str) -> dict:
        """Returns a dict with information of the symbols specified."""
        pass


class CMCDataTransformer:
    
    def __init__(self) -> None:
        self.general = DataTransformer()


def main() -> None:
    cmc_api = CoinMarketCapAPI()
    data = cmc_api.extract_symbol_id_list(specified_symbols=['BTC', 'QNT'])
    pprint(data)

if __name__ == '__main__':
    main()
