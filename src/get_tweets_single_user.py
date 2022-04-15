"""
This script is for the extraction of the tweets of one user for a given time range. This script has to
be executed multiple times to extract the tweets of the whole list of users, obtained by executing the 
extract_followers.py script.

[x] - get tweets using api endpoint
[x] - get the time of tweet with the tweet itself
[x] - be able to return tweets as collections (dtype: list of dicts) strings (as-is) of a single user.
[x] - be able to extract all the tweet within a given/specified time range of one user and combining the 
     multiple response packages to one single package.
[] - store the tweets of the different users in a database (prob mongodb)
"""
import requests
import dotenv
import json
from datetime import datetime, timedelta
from typing import Union

# env variables
__config = dotenv.dotenv_values('./res/.env')
__bconfig = dotenv.dotenv_values('./res/bearer_tokens.env')
__BEARER_TOKEN = __bconfig["TWITTER_BEARER_TOKEN"]
__USERNAME = __config["USERNAME"]

__TWITTER_API_TIME_FORMAT = __config['TWITTER_API_TIME_FORMAT']

# Input variables
user_id = "969716112752553985"  # first from ct_accounts.json
most_recent_time = '2021-10-22T10:30:01.000Z'  # HAS TO BE format like YYYY-MM-DDTHH:mm:ss.000Z

# Functions
def bearer_oauth(r):
    """
    Overgezet naar ApiAuthentication
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {__BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2UserTweetsPython"  # all endpoints have different user-agents.
    return r

def create_url(user_id: str):
    """
    Overgezet naar TwitterAPI
    """
    url = "https://api.twitter.com/2/users/{}/{}?{}={}".format(user_id, 'tweets', 'max_results', 10)
    return url

def get_params(end_time: str) -> dict:
    """
    Overgezet naar TwitterAPI
    
    MIND YOUR STEP
    Let op het commentaar dat hier bij de functie nog is toegevoegd. Neem dit mee in eventuele documnentatie.
    
    """
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {'end_time': end_time, 'tweet.fields': 'created_at'}

def connect_to_endpoint(url, params):
    """
    Overgezet naar ApiAuthentication
    """
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def transform_response(original_response: dict, user_id: str) -> dict:
    """
    Overgezet naar TwitterApi

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

def store_response(json_data: dict):
    """
    Overgezet naar TwitterApi
    """
    with open('./data/tweets_user_{}.json'.format(user_id), 'w') as json_file:
        json.dump(json_data, json_file)

def get_stop_search_time(start_time: Union[str, datetime], time_range: str = 'day') -> timedelta:
    """
    Based on the input this functions returns a stop time to use as input in the recursive search for tweets
    """
    start_time = datetime.strptime(start_time, __TWITTER_API_TIME_FORMAT) if isinstance(start_time, str) else start_time

    if time_range == 'day':
        return start_time - timedelta(days=1)
    elif time_range == 'hour':
        return start_time - timedelta(hours=1)
    else:
        raise Exception('Please specify one of the following time_ranges: \'day\', \'hour\'.')

def isolate_time_oldest_object(oldest_id: str, response_data: list) -> Union[datetime, bool]:
    """
    Overgezet naar TwitterApi

    Isolates the object with the given id from the given response data.
    """
    for item in response_data[::-1]:
        if item['id'] == oldest_id:
            return datetime.strptime(item['created_at'], __TWITTER_API_TIME_FORMAT)
        else:
            pass
    return False

def get_tweets(user_id: str, start_search_time: Union[str, datetime] = None, stop_search_time: Union[str, datetime] = None):
    """
    Overgezet naar TwitterApi

    The function extracts the tweets of a given/specified user, within the given time range.
    """
    print('running get_tweets()')
    # Get the oldest time in a datetime object
    dt_most_recent = datetime.strptime(start_search_time, __TWITTER_API_TIME_FORMAT) if isinstance(start_search_time, str) else start_search_time
    dt_most_recent_string = get_RFC_timestamp(dt_object=dt_most_recent)

    dt_stop_time = datetime.strptime(stop_search_time, __TWITTER_API_TIME_FORMAT) if isinstance(stop_search_time, str) else stop_search_time
    dt_stop_time_string = get_RFC_timestamp(dt_object=dt_stop_time)

    # Prepare the api request
    url = create_url(user_id=user_id)
    params = get_params(end_time=dt_most_recent_string)

    # Make the api request
    json_response = connect_to_endpoint(url, params)

    # Extract the oldest object id 'oldest_id' from the metadata of the response
    oldest_id = json_response['meta']['oldest_id']

    # Extract the oldest time seen in the api response
    oldest_time_response_data = isolate_time_oldest_object(oldest_id=oldest_id, response_data=json_response['data'])
    # print(oldest_time_response_data, type(oldest_time_response_data))

    # Checking if the oldest seen time in response is older then the time we actually need (outside of specified time range)
    oldest_time_within_range = False if (dt_stop_time - oldest_time_response_data <= timedelta(0)) else True
    
    # Filtering the json_response to only contain the times within the time range
    return_data = [item for item in json_response['data'] if (datetime.strptime(item['created_at'], __TWITTER_API_TIME_FORMAT) - dt_stop_time) >= timedelta(0)]
    # print(return_data, len(return_data))
    print(type(return_data))

    # break case of the recursive function
    if oldest_time_within_range:
        return return_data
    
    return return_data + get_tweets(user_id=user_id, start_search_time=oldest_time_response_data, stop_search_time=stop_search_time)

def get_RFC_timestamp(dt_object: datetime):
    """
    Overgezet naar TwitterApi

    returns a string that is a valid RFC3339 date and time notation
    """
    __stamp_format = "%Y-%m-%dT%H:%M:%S.000Z"
    return datetime.strftime(dt_object, __stamp_format)
    

def main():
    stop_search_time = get_stop_search_time(start_time=most_recent_time)
    print(f'start time : {most_recent_time}, stop time : {stop_search_time}')
    x = get_tweets(
        user_id=user_id, 
        start_search_time=most_recent_time, 
        stop_search_time=stop_search_time)

    print(x, len(x))
    
    # url = create_url(user_id=user_id)
    # params = get_params()
    # json_response = connect_to_endpoint(url, params)
    # print(json_response)
    # clean_response = transform_response(original_response=json_response, user_id=user_id)
    # store_response(json_data=clean_response)

if __name__ == '__main__':
    main()