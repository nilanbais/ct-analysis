"""
This script is responsible for both the interaction with the Twitter API and all the trasformations that
need to happen on this data, recieved as a response from the API.

The API works using a specified user account maintained for the porpose of the automation. The code 
and comments will refer to this account as the base_user.
"""
import dotenv
import json

from datetime import datetime, timedelta

from api_authentication_class import ApiAuthentication

from typing import Union


class TwitterAPI(ApiAuthentication):
    def __init__(self) -> None:
        super().__init__('TWITTER_BEARER_TOKEN')
        self.__config = dotenv.dotenv_values('./res/.env')
        self.__TWITTER_API_TIME_FORMAT = self.__config["TWITTER_API_TIME_FORMAT"]
        self.__TWITTER_API_URL_MAP_FILE = self.__config["TWITTER_API_URL_MAP_FILE"]

        self.API_URL_MAP = self.read_resource(file_name=self.__TWITTER_API_URL_MAP_FILE)
    
    """
    Methods to override attributes in ApiAthentication
    """
    def create_header(self, header_dict: dict) -> None: 
        self.header = header_dict.copy()
    
    def create_parameters(self, parameter_dict: dict) -> None:
        """
        MIND YOUR STEP

        de methofd is belangrijk in de recursieve method get_tweets (komt nog). Bouw deze 
        gelijk goed in. 
        """
        self.parameters = parameter_dict.copy()
    
    # def create_url_v1(self) -> str:
    #     """
    #     MIND YOUR STEP

    #     extract_followers_url = "https://api.twitter.com/2/users/{}/following?{}={}".format(__USER_ID, "max_results", 1000)
    #     get_tweets_single_users_url = "https://api.twitter.com/2/users/{}/{}?{}={}".format(user_id, 'tweets', 'max_results', 10)
    #     """
    #     __USER_ID = self.__config["USER_ID"]
    #     self.url = "https://api.twitter.com/2/users/{}/following?{}={}".format(__USER_ID, "max_results", 1000)
        
    def create_url(self, mode: str = 'auto') -> None:
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
        # Extracting base URL using header data
        if mode == 'auto':
            url_base = next((url for user_agent, url in self.API_URL_MAP.items() if user_agent == self.header["User-Agent"]))
        elif mode == 'following':
            url_base = next((url for user_agent, url in self.API_URL_MAP.items() if user_agent == "v2FollowingLookupPython"))
        elif mode == 'user tweets':
            url_base = next((url for user_agent, url in self.API_URL_MAP.items() if user_agent == "v2UserTweetsPython"))
        else:
            raise Exception(
                "The mode you selected werkt niet neef. Please see documentation for the available modes."
            )

        # Completing the base URL using the parameter data
        print(url_base)
        

    """
    Methods to manage reading and writing the data
    """
    def read_json(file_name: str, folder_name: str) -> dict:
        """
        Base method (a method that will be extrended to specific use cases)
        """
        with open("./{}/{}".format(folder_name, file_name), 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def read_resource(file_name: str) -> dict:
        with open('./res/{}'.format(file_name)) as res_file:
            return json.load(res_file)

    @staticmethod
    def store_response(json_data: dict, file_name: str) -> None:
        """
        THIS METHOD IS GOING TO BE REPLACED WITH THE COMMUNICATION WITH THE MONGODB DATABASE.
        """
        with open('./data/{}'.format(file_name), 'w') as json_file:
            json.dump(json_data, json_file)

    """
    Methods to get a response from the API
    """
    # todo: functie ombouwen tot gebruik self
    def extract_follers_list(self):
        self.create_header(header_dict={"User-Agent": "v2FollowingLookupPython"})
        url = self.create_url()
        params = {}
        json_response = self.connect_to_endpoint(url, params)
        return json_response

    def get_tweets(self, user_id: str, start_search_time: Union[str, datetime] = None, stop_search_time: Union[str, datetime] = None):
        """
        The function extracts the tweets of a given/specified user, within the given time range.
        """
        print('running get_tweets()')
        # Get the oldest time in a datetime object
        dt_most_recent = datetime.strptime(start_search_time, self.__TWITTER_API_TIME_FORMAT) if isinstance(start_search_time, str) else start_search_time
        dt_most_recent_string = self.get_RFC_timestamp(dt_object=dt_most_recent)

        dt_stop_time = datetime.strptime(stop_search_time, self.__TWITTER_API_TIME_FORMAT) if isinstance(stop_search_time, str) else stop_search_time
        dt_stop_time_string = self.get_RFC_timestamp(dt_object=dt_stop_time)

        # Prepare the api request
        self.create_header(
            header_dict={"User-Agent": "v2UserTweetsPython"}
        )
        self.create_parameters(
            parameter_dict={
                'user_id': user_id,
                'end_time': dt_most_recent_string, 
                'tweet.fields': 'created_at'}
        )
        self.create_url()

        # Make the api request
        json_response = self.connect_to_endpoint(self.url, self.parameters)

        # Extract the oldest object id 'oldest_id' from the metadata of the response
        oldest_id = json_response['meta']['oldest_id']

        # Extract the oldest time seen in the api response
        oldest_time_response_data = self.isolate_time_oldest_object(oldest_id=oldest_id, response_data=json_response['data'])
        # print(oldest_time_response_data, type(oldest_time_response_data))

        # Checking if the oldest seen time in response is older then the time we actually need (outside of specified time range)
        oldest_time_within_range = False if (dt_stop_time - oldest_time_response_data <= timedelta(0)) else True
        
        # Filtering the json_response to only contain the times within the time range
        return_data = [item for item in json_response['data'] if (datetime.strptime(item['created_at'], self.__TWITTER_API_TIME_FORMAT) - dt_stop_time) >= timedelta(0)]
        # print(return_data, len(return_data))
        
        # break case of the recursive function
        if oldest_time_within_range:
            return return_data
        
        return return_data + self.get_tweets(start_search_time=oldest_time_response_data, stop_search_time=stop_search_time)
    
    """
    Methods supporting the workflow for transorming the data received in the response
    """
    @staticmethod
    def get_RFC_timestamp(dt_object: datetime):
        """
        returns a string that is a valid RFC3339 date and time notation
        """
        __stamp_format = "%Y-%m-%dT%H:%M:%S.000Z"
        return datetime.strftime(dt_object, __stamp_format)
    
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

    """
    Methods for transforming the data received in the response
    """
    def transform_response(original_response: dict, user_id: str) -> dict:
        """
        Function to transform the original response data so it's a combination of the following datapoints.
        - user_id
        - tweet_id
        - created_at
        - text
        """
        # Original data
        _og_package = original_response.copy()
        _og_data = _og_package['data']
        _og_meta = _og_package['meta']

        # Creating var for the result of the tranformation
        transformed_data = list()

        # iter over the items in the data
        for item in _og_data:
            # Assign the item.vars to the right iter.vars
            created_at = item['created_at']
            tweet_id = item['id']
            text = item['text']

            # Appending the new data object
            transformed_data.append({"user_id": user_id, "tweet_id": tweet_id, "created_at": created_at, 'text': text})

        return {'data': transformed_data, 'meta': _og_meta}

def main():
    user_id = "969716112752553985"  # first from ct_accounts.json

    api = TwitterAPI()

    most_recent_time = '2021-10-22T10:30:01.000Z'  # HAS TO BE format like YYYY-MM-DDTHH:mm:ss.000Z
    stop_search_time = api.get_stop_search_time(start_time=most_recent_time)

    print(f'start time : {most_recent_time}, stop time : {stop_search_time}')
    x = api.get_tweets(
        user_id=user_id,
        start_search_time=most_recent_time,
        stop_search_time=stop_search_time
    )

    print(x, len(x))

def test():
    user_id = "969716112752553985"  # first from ct_accounts.json

    test_url = "https://api.twitter.com/2/users/%s/tweets?%s=%s"
    test_data = (user_id, 'tweet.fields', 'created_at')

    print(test_url % test_data)

if __name__ == '__main__':
    # main()
    test()