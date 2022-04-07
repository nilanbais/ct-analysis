"""
Class used for the functionaly of authentication of the api's used.
The urls of the requests differ from eachother when making different api
calls, so the definition of these urls have to be done in the classes
dedicated to one signle api.
"""
import dotenv
import requests

class ApiAuthentication:

    def __init__(self, bearer_token_name) -> None:
        self.__config = dotenv.dotenv_values('./res/.env')
        self.bearer_token_name = bearer_token_name  # has to be set by the child class as input variable
        self.header = None  # set by create_header
        self.url = None  # set by create_url
    
    def _bearer_oauth(self, header) -> dict:
        header_oath = header.copy()  # Copy to make sure the token isn't added to the header attribute
        header_oath["Authorization"] = "Bearer {}".format(self.__config[self.bearer_token_name])
        return header_oath
    
    def connect_to_endpoint(self, url, header, params: dict = {}) -> dict:
        if self.header is None:
            raise Exception(
                "No header is created."
            )
        elif self.url is None:
            raise Exception(
                "No url is created."
            )

        response = requests.request("GET", url, headers=self._bearer_oauth(header), params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

class TwitterAPI(ApiAuthentication):
    def __init__(self) -> None:
        super().__init__('TWITTER_BEARER_TOKEN')
        self.__config = dotenv.dotenv_values('./res/.env')
    
    def create_header(self) -> dict:
        self.header = {"User-Agent": "v2FollowingLookupPython"}

    def create_url(self) -> str:
        __USER_ID = self.__config["USER_ID"]
        self.url = "https://api.twitter.com/2/users/{}/following?{}={}".format(__USER_ID, "max_results", 1000)
        return self.url


def main():
    api = TwitterAPI()
    url = api.create_url()
    api.create_header()
    api.connect_to_endpoint(url, api.header)
    print(api.header)
    

if __name__ == '__main__':
    main()