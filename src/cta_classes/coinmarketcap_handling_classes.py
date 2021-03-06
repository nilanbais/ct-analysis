"""
This script is responsible for both the interaction with the CoinMarketCap API and all the trasformations that
need to happen on this data, recieved as a response from the API.

The API works using a specified user account maintained for the porpose of the automation. The code 
and comments will refer to this account as the base_user.
"""
import json
import dotenv
from pprint import pprint

from cta_classes.base_classes.api_response_class import ApiAuthentication, APICommunicator
from cta_classes.base_classes.data_transformer_class import DataTransformer
from cta_classes.base_classes.data_reader_writer import Reader, EnvVarReader


class CoinMarketCapAPI_v2:

    def __init__(self) -> None:
        self.communicator = APICommunicator(auth_token_name='CMC_API_KEY')
        self.API_URL_MAP = Reader().read_resource(file_name=EnvVarReader().get_value("CMC_API_URL_MAP_FILE"))

    def get_url(self, endpoint: str) -> str:
        mode_options = [key for key in self.API_URL_MAP.keys()]

        if endpoint.lower() in mode_options:
            self.communicator.url = next((url for key, url in self.API_URL_MAP.items() if key == endpoint))
        else:
            raise Exception(
                "The endpoint you selected werkt niet neef. Please see documentation for the available points."
            )
    
    def extract_coin_categories(self) -> dict:
        """Returns the categories available on CoinMarketCap"""
        url = self.get_url(endpoint='coin categories')

        json_response = self.communicator.connect_to_endpoint(url=url)
        return json_response['data']
    
    def get_symbol_id_list(self, specified_symbols: list = []) -> dict:
        """Returns a list of coin ids. 
            If a list given, it returns the is of the specified coins.
            If no list given, the method will do a standard request.
        """

        prepped_parameter_dict = {"symbol": DataTransformer().list_to_string(input_list=specified_symbols)} if len(specified_symbols) > 0 else {}

        url = self.get_url(endpoint='idmap')

        json_response = self.communicator.connect_to_endpoint(url=url, query_parameters=prepped_parameter_dict)
        return json_response["data"]



class CoinMarketCapAPI(ApiAuthentication):

    def __init__(self) -> None:
        super().__init__('CMC_API_KEY')
        self.__config = dotenv.dotenv_values('./res/.env')
        self.__CMC_API_URL_MAP = self.__config["CMC_API_URL_MAP_FILE"]

        self.API_URL_MAP = Reader.read_resource(file_name=self.__CMC_API_URL_MAP)

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
    Methods to get a response from the API
    """
    def extract_coin_categories(self) -> dict:
        """Returns the categories available on CoinMarketCap"""
        self.create_header()
        self.create_query_parameters()
        self.create_url(mode='coin categories')

        json_response = self.connect_to_endpoint(authentication='api key', url=self.url, header=self.header, params=self.query_parameters)
        return json_response['data']

    def get_symbol_id_list(self, specified_symbols: list = []) -> dict:
        """Returns a list of coin ids. 
            If a list given, it returns the is of the specified coins.
            If no list given, the method will do a standard request.
        """

        prepped_parameter_dict = {"symbol": self.data_trandform.list_to_string(input_list=specified_symbols)} if len(specified_symbols) > 0 else {}

        self.create_header()
        self.create_query_parameters(parameter_dict=prepped_parameter_dict)  # specified symbols toeveogen
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
    data = cmc_api.get_symbol_id_list(specified_symbols=['BTC', 'QNT'])
    pprint(data)

if __name__ == '__main__':
    main()
