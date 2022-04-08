"""
This script is responsible for both the interaction with the Twitter API and all the trasformations that
need to happen on this data, recieved as a response from the API.
"""
import dotenv

from api_authentication_class import ApiAuthentication


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
    api.create_header()
    api.create_url()
    api.connect_to_endpoint(api.url, api.header)
    print(api.header)

if __name__ == '__main__':
    main()