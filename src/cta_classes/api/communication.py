import imp
import requests
from typing import Optional
from cta_classes.api.authentication import Authenticator
from cta_classes.api.exceptions import APIExceptions


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

        APIExceptions().raise_request_exception(header=self.header, url=self.url, query_parameters=self.query_parameters)
        
        response = requests.request("GET", self.url, headers=self.__authed_header, params=self.query_parameters)

        APIExceptions().check_response_status(response)

        return response.json()

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