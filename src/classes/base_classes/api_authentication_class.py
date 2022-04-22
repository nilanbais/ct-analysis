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

        user_id moet altijd de eerst parameter zijn, omdat deze zijn eigen plaats heeft in de query path
        De overige query parameters kunnnen toegevoegd worden volgens de uitbeidingen :parameter1=:waarde&:parameter2=:waarde&etc
        """
        self.query_parameters = parameter_dict.copy()

def main():
    api = ApiAuthentication()
    api.connect_to_endpoint(api.url, api.header)
    print(api.header)
    

if __name__ == '__main__':
    main()