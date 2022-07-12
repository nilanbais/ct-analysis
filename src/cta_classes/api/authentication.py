
from typing import Union
from abc import ABC, abstractmethod
from cta_classes.file.env_reader import SecretVarReader

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