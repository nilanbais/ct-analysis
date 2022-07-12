

from typing import Union
from datetime import datetime, timedelta

from cta_classes.api.communication import APICommunicator
from cta_classes.data.transformer import DataTransformer
from cta_classes.file_handling.env_reader import ResourceReader, EnvVarReader


class TwitterAPI():

    def __init__(self) -> None:
        self.communicator = APICommunicator(auth_token_name='TWITTER_BEARER_TOKEN')
        self.__TWITTER_API_TIME_FORMAT = EnvVarReader().get_value("TWITTER_API_TIME_FORMAT")

        self.API_URL_MAP = ResourceReader().read_resource(file_name=EnvVarReader().get_value("TWITTER_API_URL_MAP_FILE"))

    def get_url(self, user_id: int, endpoint: str = "") -> None:
        """
        Method for creating the url for the request.
        """
        # Extracting URL template using header data
        endpoint_options = [key for key in self.API_URL_MAP.keys()]

        if endpoint.lower() in endpoint_options:
            url_template = next((url for key, url in self.API_URL_MAP.items() if key == endpoint))
        else:
            raise Exception(
                "The mode you selected werkt niet neef. Please see documentation for the available modes."
            )

        # Adding user_id to the URL to complete the url
        return url_template.format(user_id)


    def extract_following_list(self, user_id: Union[None, int] = None, addidional_header_vals: dict = {}, additional_query_parameter_vals: dict = {}) -> dict:
            """
            Method for extracting a list of the accounts a user follows.
            build in a way it can be applied for any user, but when not specified it used the base_user
            """ 
            custom_header = DataTransformer().extend_dict_object(base_dict={"User-Agent": "v2FollowingLookupPython"}, additional_values=addidional_header_vals)
            custom_params = DataTransformer().extend_dict_object(base_dict={"user.fields": "public_metrics"}, additional_values=additional_query_parameter_vals)

            if user_id is None:
                user_id = EnvVarReader().get_value("TWITTER_USER_ID")

            custom_url = self.get_url(user_id, endpoint="following")

            json_response = self.communicator.connect_to_endpoint(url=custom_url, header=custom_header, query_parameters=custom_params)
            return json_response['data']


    def get_tweets(self, user_id: str, start_search_time: Union[str, datetime] = None, stop_search_time: Union[str, datetime] = None, 
        additional_header_vals: dict = {}, additional_query_parameter_vals: dict = {}) -> dict:
        """
        The function extracts the tweets of a given/specified user, within the given time range.
        """
        print('running get_tweets()')
        # Get the oldest time in a datetime object
        dt_most_recent = datetime.strptime(start_search_time, self.__TWITTER_API_TIME_FORMAT) if isinstance(start_search_time, str) else start_search_time
        dt_most_recent_string = DataTransformer().get_RFC_timestamp(dt_object=dt_most_recent)

        dt_stop_time = datetime.strptime(stop_search_time, self.__TWITTER_API_TIME_FORMAT) if isinstance(stop_search_time, str) else stop_search_time
        # dt_stop_time_string = DataTransformer().get_RFC_timestamp(dt_object=dt_stop_time)  # Unused

        # Prepare the api request
        custom_header = DataTransformer().extend_dict_object(base_dict={"User-Agent": "v2UserTweetsPython"}, additional_values=additional_header_vals)
        custom_params = DataTransformer().extend_dict_object(base_dict={'end_time': dt_most_recent_string,  # bepaald de meest recente tweet die gelezen moet worden
                                                            'tweet.fields': 'created_at'},
                                                            additional_values=additional_query_parameter_vals)
        custom_url = self.get_url(user_id, endpoint="user_tweets")

        # Make the api request
        json_response = self.communicator.connect_to_endpoint(url=custom_url, header=custom_header, query_parameters=custom_params)
        # pprint(f"response = {json_response}")

        # Check if the response contains any data. if not return empty list
        if json_response['meta']['result_count'] == 0:
            return []  # Returning an empty list

        # Extract the oldest object id 'oldest_id' from the metadata of the response
        oldest_id = json_response['meta']['oldest_id']

        # Extract the oldest time seen in the api response
        oldest_time_response_data = isolate_time_oldest_object(oldest_id=oldest_id, response_data=json_response['data'])
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