"""
Class used for the functionaly of authentication of the api's used.
The urls of the requests differ from eachother when making different api
calls, so the definition of these urls have to be done in the classes
dedicated to one signle api.
This class should only be used as a parent class.
"""
from typing import Optional, Union
from abc import ABC, abstractmethod
from cta_classes.base_classes.data_reader_writer import SecretVarReader

import dotenv
import requests


class GetAuth(ABC):

    @abstractmethod
    def get_authed_header(self, header) -> dict:
        """Method to return an authenticated header"""


class BearerOAuth(GetAuth):

    def __init__(self, authentication_token_name) -> None:
        self.authentication_token_name = authentication_token_name

    def get_authed_header(self, header: dict) -> dict:
        """Returns a header with the correct authentication bearer token."""
        header_oath = header.copy()  # Copy to make sure the token isn't added to the header attribute
        header_oath["Authorization"] = "Bearer {}".format(SecretVarReader().get_value(variable_name=self.authentication_token_name))
        return header_oath


class ApiKeyAuth(GetAuth):

    def __init__(self, authentication_token_name) -> None:
        self.authentication_token_name = authentication_token_name

    def get_authed_header(self, header: dict) -> dict:
        """Returns a header with the correct authentication key, val pair."""
        header_auth = header.copy()
        header_auth["X-CMC_PRO_API_KEY"] = SecretVarReader().get_value(variable_name=self.authentication_token_name)
        return header_auth


class AuthObject:

    def __init__(self, auth_token_name: str) -> None:
        self.auth_object = self.__set_auth_object(auth_token_name)
    
    @staticmethod
    def __set_auth_object(auth_token_name: str) -> Union[BearerOAuth, ApiKeyAuth]:
        """Method to retrun a correct authentication object.
        """
        __auth_token = SecretVarReader().get_value(auth_token_name)

        if len(__auth_token) <= 100:
            return ApiKeyAuth(auth_token_name)
        elif len(__auth_token) > 100:
            return BearerOAuth(auth_token_name)


class Authenticator:

    def __init__(self, auth_token_name: str) -> None:
        self._auth_obj = AuthObject(auth_token_name).auth_object
        # self.header = self.get_atheredised_header()

    def get_atheredised_header(self, header: str) -> dict:
        """Method to auterise the header.
            Returns dict with the correct autherization, based on the needed autherisation.
        """
        authed_header = self._auth_obj.get_authed_header(header)
        return authed_header
        

class APICommunicator:

    def __init__(self, auth_token_name: str) -> None:
        self.__auth_object = Authenticator(auth_token_name)
        self.__authed_header = None
        self.header = None
        self.url = None
        self.query_parameters = None
        
        
    def connect_to_endpoint(self, header: dict = {}, url: str = "", query_parameters: dict = {}):
        """Returns the response of the API call."""
        self.set_header(header)
        self.set_query_parameters(query_parameters)
        self.set_url(url)

        self.validate_request()
        response = requests.request("GET", self.url, headers=self.__authed_header, params=self.query_parameters)
        self.check_response_status(response)
        return response.json()


    def validate_request(self):
        """Valiodates when needed"""
        if self.header is None:
            raise Exception(
                "No header created."
            )
        elif self.url is None:
            raise Exception(
                "No url created."
            )
        elif self.query_parameters is None:
            raise Exception(
                "No parameter object created."
            )

    def check_response_status(self, response) -> Optional[ValueError]:
        """
        check the response code
        """
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )

    """
    Methods to override attributes in ApiAthentication
    """
    def __set_authed_header(self) -> None:
        self.__authed_header = self.__auth_object.get_atheredised_header(self.header)

    def set_header(self, header_dict) -> None: 
        self.header = header_dict.copy()
        self.__set_authed_header()
    
    def set_query_parameters(self, parameter_dict) -> None:
        self.query_parameters = parameter_dict.copy()

    def set_url(self, url: str) -> None: 
        self.url = url
    



class ApiAuthentication:

    def __init__(self, authentication_token_name) -> None:
        self.__config = dotenv.dotenv_values('./res/authentication.env')
        self.authentication_token_name = authentication_token_name  # has to be set by the child class as input variable
        self.header = None  # set by create_header
        self.url = None  # set by create_url
        self.query_parameters = None  # set by create_parameters
    
    def _api_key_auth(self, header) -> dict:
        """Returns a header with the correct authentication key, val pair."""
        header_auth = header.copy()
        header_auth["X-CMC_PRO_API_KEY"] = self.__config[self.authentication_token_name]
        return header_auth
    
    def _bearer_oauth(self, header) -> dict:
        """Returns a header with the correct authentication bearer token."""
        header_oath = header.copy()  # Copy to make sure the token isn't added to the header attribute
        header_oath["Authorization"] = "Bearer {}".format(self.__config[self.authentication_token_name])
        return header_oath
    
    def connect_to_endpoint(self, authentication: str, url: str, header: dict, params: dict = {}) -> dict:
        """Returns the response of the API call."""
        if self.header is None:
            raise Exception(
                "No header created."
            )
        elif self.url is None:
            raise Exception(
                "No url created."
            )
        elif self.query_parameters is None:
            raise Exception(
                "No parameter object created."
            )
        
        if authentication.lower() == "bearer token":
            response = requests.request("GET", url, headers=self._bearer_oauth(header), params=params)
        elif authentication.lower() == "api key":
            response = requests.request("GET", url, headers=self._api_key_auth(header), params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

    """
    Methods to override attributes in ApiAthentication
    """
    def create_header(self, header_dict: dict = {}) -> None: 
        self.header = header_dict.copy()
    
    def create_query_parameters(self, parameter_dict: dict = {}) -> None:
        """
        MIND YOUR STEP

        de method is belangrijk in de recursieve method get_tweets (komt nog). Bouw deze 
        gelijk goed in. 
        """
        self.query_parameters = parameter_dict.copy()


def main():
    api = ApiAuthentication()
    api.connect_to_endpoint(api.url, api.header)
    print(api.header)
    

if __name__ == '__main__':
    main()