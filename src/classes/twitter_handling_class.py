"""
This script is responsible for both the interaction with the Twitter API and all the trasformations that
need to happen on this data, recieved as a response from the API.

The API works using a specified user account maintained for the porpose of the automation. The code 
and comments will refer to this account as the base_user.
"""
import json
import dotenv

from typing import Union
from pprint import pprint
from datetime import datetime, timedelta

from api_authentication_class import ApiAuthentication
from data_transformer_class import DataTransformer


class TwitterAPI(ApiAuthentication):
    def __init__(self) -> None:
        super().__init__('TWITTER_BEARER_TOKEN')
        self.__config = dotenv.dotenv_values('./res/.env')
        self.__TWITTER_API_TIME_FORMAT = self.__config["TWITTER_API_TIME_FORMAT"]
        self.__TWITTER_API_URL_MAP_FILE = self.__config["TWITTER_API_URL_MAP_FILE"]

        self.API_URL_MAP = self.read_resource(file_name=self.__TWITTER_API_URL_MAP_FILE)

        self.DT = DataTransformer()
    
    """
    Methods to override attributes in ApiAthentication
    """
    # def create_header(self, header_dict: dict) -> None: 
    #     self.header = header_dict.copy()
    
    # def create_query_parameters(self, parameter_dict: dict) -> None:
    #     """
    #     MIND YOUR STEP

    #     de method is belangrijk in de recursieve method get_tweets (komt nog). Bouw deze 
    #     gelijk goed in. 

    #     user_id moet altijd de eerst parameter zijn, omdat deze zijn eigen plaats heeft in de query path
    #     De overige query parameters kunnnen toegevoegd worden volgens de uitbeidingen :parameter1=:waarde&:parameter2=:waarde&etc
    #     """
    #     self.query_parameters = parameter_dict.copy()
        
    def create_url(self, user_id: int, mode: str = 'auto') -> None:
        """
        Method for creating the url for the request.
        keyword arg 'mode' options
            'auto' -> method uses "User-Agent" from the header to create the url.
            'following' -> creates url to extract the folling accounts of the base_user.
            'user tweets' -> creates url to extract tweets from a given user (not base_user).

        MIND THAT YOU HAVE TO CREATE THE HEADER BEFORE THE URL WHEN USING AUTO MODE

        When you want to be able to use this method more freely, change the completion of the url_base to **kwargs
        will be handled correctly and are added to the parmeters_dict.
        Ever query parameter will be seperated using '&'. name=values to include&name2=value to include2&etc
        """
        # Extracting URL template using header data
        if mode == 'auto':
            url_template = next((url for user_agent, url in self.API_URL_MAP.items() if user_agent == self.header["User-Agent"]))
        elif mode == 'following':
            url_template = next((url for user_agent, url in self.API_URL_MAP.items() if user_agent == "v2FollowingLookupPython"))
        elif mode == 'user tweets':
            url_template = next((url for user_agent, url in self.API_URL_MAP.items() if user_agent == "v2UserTweetsPython"))
        else:
            raise Exception(
                "The mode you selected werkt niet neef. Please see documentation for the available modes."
            )

        # Adding user_id to the URL to make a base URL
        url_base = url_template.format(user_id)

        # If any query parameters, add them to the end of the URL following the right conventions
        if len(self.query_parameters.keys()) > 0:
            url = url_base + '?'

            # Defining loop with skip statement
            first_loop_done = False
            for key, val in self.query_parameters.items():

                if first_loop_done:
                    url = url + '&'

                url = url + key + '=' + str(',').join([obj for obj in [val]])

                # Changing val of skip statement
                first_loop_done = True
        
            self.url = url
        else:
            self.url = url_base

    """
    Methods to manage reading and writing the data
    """
    def read_json(self, file_name: str, folder_name: str) -> dict:
        """
        Base method (a method that will be extrended to specific use cases)
        """
        with open("./{}/{}".format(folder_name, file_name), 'r') as json_file:
            return json.load(json_file)

    def store_json(self, json_data: dict, file_name: str, folder_name: str) -> None:
        """
        THIS METHOD IS GOING TO BE REPLACED WITH THE COMMUNICATION WITH THE MONGODB DATABASE.
        """
        with open('./{}/{}'.format(folder_name, file_name), 'w') as json_file:
            json.dump(json_data, json_file)


    def read_resource(self, file_name: str) -> dict:
        return self.read_json(file_name=file_name, folder_name='res')

    def store_response(self, json_data: dict, file_name: str) -> None:
        return self.store_json(json_data=json_data, file_name=file_name, folder_name='data')

    """
    Methods to get a response from the API
    """
    # todo: functie ombouwen tot gebruik self
    def extract_follers_list(self, user_id: Union[None, int] = None, base_user: bool = True):
        """
        Method for extracting a list of the accounts a user follows.
        build in a way it can be applied for any user, but when not specified it used the base_user
        """ 
        if base_user:
            user_id = self.__config['USER_ID']

        self.create_header(header_dict={"User-Agent": "v2FollowingLookupPython"})
        self.create_query_parameters()
        self.create_url(user_id=user_id)

        json_response = self.connect_to_endpoint(self.url, self.query_parameters)
        return json_response['data']

    def get_tweets(self, user_id: str, start_search_time: Union[str, datetime] = None, stop_search_time: Union[str, datetime] = None):
        """
        The function extracts the tweets of a given/specified user, within the given time range.
        """
        print('running get_tweets()')
        # Get the oldest time in a datetime object
        dt_most_recent = datetime.strptime(start_search_time, self.__TWITTER_API_TIME_FORMAT) if isinstance(start_search_time, str) else start_search_time
        dt_most_recent_string = self.DT.get_RFC_timestamp(dt_object=dt_most_recent)

        dt_stop_time = datetime.strptime(stop_search_time, self.__TWITTER_API_TIME_FORMAT) if isinstance(stop_search_time, str) else stop_search_time
        dt_stop_time_string = self.DT.get_RFC_timestamp(dt_object=dt_stop_time)

        # Prepare the api request
        self.create_header(
            header_dict={"User-Agent": "v2UserTweetsPython"}
        )
        self.create_query_parameters(
            parameter_dict={
                'end_time': dt_most_recent_string,  # bepaald de meest recente tweet die gelezen moet worden
                'tweet.fields': 'created_at'}
        )
        self.create_url(user_id=user_id)

        # Make the api request
        json_response = self.connect_to_endpoint(self.url, self.query_parameters)
        # pprint(f"response = {json_response}")

        # Check if the response contains any data. if not return empty list
        if json_response['meta']['result_count'] == 0:
            return []  # Returning an empty list

        # Extract the oldest object id 'oldest_id' from the metadata of the response
        oldest_id = json_response['meta']['oldest_id']

        # Extract the oldest time seen in the api response
        oldest_time_response_data = self.isolate_time_oldest_object(oldest_id=oldest_id, response_data=json_response['data'])
        # print(f"oldest time in response data: {oldest_time_response_data}")

        # Checking if the oldest seen time in response is older then the time we actually need (outside of specified time range)
        oldest_time_within_range = False if (dt_stop_time - oldest_time_response_data <= timedelta(0)) else True
        # print(f"oldest time within timerange {start_search_time} {stop_search_time}: {oldest_time_within_range}")
        
        # Filtering the json_response to only contain the times within the time range
        return_data = [item for item in json_response['data'] if (datetime.strptime(item['created_at'], self.__TWITTER_API_TIME_FORMAT) - dt_stop_time) >= timedelta(0)]
        # pprint(return_data)
        
        # break case of the recursive function
        if oldest_time_within_range:
            return return_data
        
        return return_data + self.get_tweets(user_id=user_id, start_search_time=oldest_time_response_data, stop_search_time=stop_search_time)
    
    def get_follower_count(self, user_id: int) -> dict:
        """
        Retruns a dictionary like bellow. This structure can be editted over time.

        {
            followers: (int)
        }

        """
        pass

    """
    Methods supporting the workflow for transorming the data received in the response
    """   
    def get_stop_search_time(self, start_time: Union[str, datetime], time_range: str = 'day') -> timedelta:
        """
        Based on the input this functions returns a stop time to use as input in the recursive search for tweets
        """
        start_time = datetime.strptime(start_time, self.__TWITTER_API_TIME_FORMAT) if isinstance(start_time, str) else start_time

        if time_range == 'day':
            return start_time - timedelta(days=1)
        elif time_range == 'hour':
            return start_time - timedelta(hours=1)
        else:
            raise Exception('Please specify one of the following time_ranges: \'day\', \'hour\'.')

    def isolate_time_oldest_object(self, oldest_id: str, response_data: list) -> Union[datetime, bool]:
        """
        Isolates the object with the given id from the given response data.
        """
        for item in response_data[::-1]:
            if item['id'] == oldest_id:
                return datetime.strptime(item['created_at'], self.__TWITTER_API_TIME_FORMAT)
            else:
                pass
        return False

def main():
    user_id = "899558268795842561"  # first from ct_accounts.json

    api = TwitterAPI()
    
    following = api.extract_follers_list()
    pprint(following)

    most_recent_time = '2021-10-22T10:30:01.000Z'  # HAS TO BE format like YYYY-MM-DDTHH:mm:ss.000Z
    stop_search_time = api.get_stop_search_time(start_time=most_recent_time)

    print(f'start time : {most_recent_time}, stop time : {stop_search_time}')
    x = api.get_tweets(
        user_id=user_id,
        start_search_time=most_recent_time,
        stop_search_time=stop_search_time
    )

    pprint(x)

def test():
    user_id = "899558268795842561"  # first from ct_accounts.json
    api = TwitterAPI()
    dt = DataTransformer()

    following = {'id': '899558268795842561', 'name': 'Cred', 'username': 'CryptoCred'}

    most_recent_time = '2021-10-22T10:30:01.000Z'  # HAS TO BE format like YYYY-MM-DDTHH:mm:ss.000Z
    stop_search_time = api.get_stop_search_time(start_time=most_recent_time)
    x = api.get_tweets(
        user_id=user_id,
        start_search_time=most_recent_time,
        stop_search_time=stop_search_time
    )
    pprint(x)
    transformed_data = dt.clean_get_tweets_response(input_data=x, additional_data=following)
    pprint(transformed_data)

if __name__ == '__main__':
    # main()
    test()