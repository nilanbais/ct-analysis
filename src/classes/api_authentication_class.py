"""
Class used for the functionaly of authentication of the api's used.
The urls of the requests differ from eachother when making different api
calls, so the definition of these urls have to be done in the classes
dedicated to one signle api.
This class should only be used as a parent class.
"""
import dotenv
import requests

class ApiAuthentication:

    def __init__(self, bearer_token_name) -> None:
        self.__config = dotenv.dotenv_values('./res/authentication.env')
        self.bearer_token_name = bearer_token_name  # has to be set by the child class as input variable
        self.header = None  # set by create_header
        self.url = None  # set by create_url
        self.query_parameters = None  # set by create_parameters
    
    def _bearer_oauth(self, header) -> dict:
        header_oath = header.copy()  # Copy to make sure the token isn't added to the header attribute
        header_oath["Authorization"] = "Bearer {}".format(self.__config[self.bearer_token_name])
        return header_oath
    
    def connect_to_endpoint(self, url, header, params: dict = {}) -> dict:
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

        response = requests.request("GET", url, headers=self._bearer_oauth(header), params=params)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()


def main():
    api = ApiAuthentication()
    api.connect_to_endpoint(api.url, api.header)
    print(api.header)
    

if __name__ == '__main__':
    main()