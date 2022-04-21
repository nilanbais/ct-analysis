"""
This script is responsible for both the interaction with the CoinMarketCap API and all the trasformations that
need to happen on this data, recieved as a response from the API.

The API works using a specified user account maintained for the porpose of the automation. The code 
and comments will refer to this account as the base_user.
"""
import dotenv
from api_authentication_class import ApiAuthentication

class CoinMarketCapAPI(ApiAuthentication):

    def __init__(self) -> None:
        super().__init__('CMC_API_KEY')
        self.__config = dotenv.dotenv_values('./res/.env')