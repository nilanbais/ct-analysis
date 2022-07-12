
from cta_classes.api.communication import APICommunicator
from cta_classes.data.transformer import DataTransformer
from cta_classes.file_handling.env_reader import ResourceReader, EnvVarReader

class CoinMarketCapAPI:

    def __init__(self) -> None:
        self.communicator = APICommunicator(auth_token_name='CMC_API_KEY')
        self.API_URL_MAP = ResourceReader().read_resource(file_name=EnvVarReader().get_value("CMC_API_URL_MAP_FILE"))

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
