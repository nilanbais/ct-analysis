"""
This script is for the extraction of the tweets of one user for a given time range. This script has to
be executed multiple times to extract the tweets of the whole list of users, obtained by executing the 
extract_followers.py script.

[x] - get tweets using api endpoint
[x] - get the time of tweet with the tweet itself
[x] - be able to return tweets as collections (dtype: list of dicts) strings (as-is) of a single user.
[] - be able to extract all the tweet within a given/specified time range of one user and combining the 
     multiple response packages to one single package.
[] - be able to import the script or functions in other scripts.

"""
import requests
import dotenv
import json
from datetime import datetime, timedelta
from typing import Union

# env variables
__config = dotenv.dotenv_values('./res/.env')
__BEARER_TOKEN = __config["BEARER_TOKEN"]
__USERNAME = __config["USERNAME"]

# Input variables
user_id = "969716112752553985"  # first from ct_accounts.json
most_recent_time = '2021-10-22T10:30:01Z'  # HAS TO BE format like YYYY-MM-DDTHH:mm:ssZ

# Functions
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {__BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2UserTweetsPython"  # all endpoints have different user-agents.
    return r

def create_url(user_id: str):
    url = "https://api.twitter.com/2/users/{}/{}?{}={}".format(user_id, 'tweets', 'max_results', 100)
    return url

def get_params() -> dict:
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {'end_time': most_recent_time, 'tweet.fields': 'created_at'}

def connect_to_endpoint(url, params):
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
    with open('./data/tweets_user_{}.json'.format(user_id), 'w') as json_file:
        json.dump(json_data, json_file)

def get_timedelta(time_range: str = 'day') -> timedelta:
    """
    Based on the input this functions returns a timedelta object of the specified time range. default value = 1 day
    """
    x = 1.0
    if time_range == 'day':
        return timedelta(days=x)
    elif time_range == 'hour':
        return timedelta(hours=x)
    else:
        raise Exception('Please specify one of the following time_ranges: \'day\', \'hour\'.')

def isolate_time_oldest_object(oldest_id: str, response_data: list) -> Union[datetime, bool]:
    """
    Isolates the object with the given id from the given response data.
    """
    for item in response_data[:-1]:
        if item['id'] == oldest_id:
            return datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        else:
            pass
    return False

def get_tweets(user_id: str, time_range: str = 'day'):
    """
    The function extracts the tweets of a given/specified user, within the given time range.
    """
    # Get the oldest time in a datetime object
    dt_timedelta = get_timedelta(time_range=time_range)
    dt_most_recent = datetime.strptime(most_recent_time, "%Y-%m-%dT%H:%M:%SZ")
    dt_stop_time = dt_most_recent - dt_timedelta

    # Prepare the api request
    url = create_url(user_id=user_id)
    params = get_params()

    # Make the api request
    json_response = connect_to_endpoint(url, params)

    # Extract the oldest object id 'oldest_id' from the metadata of the response
    oldest_id = json_response['meta']['oldest_id']

    # Extract the oldest time seen in the api response
    oldest_time_response_data = isolate_time_oldest_object(oldest_id=oldest_id, response_data=json_response['data'])

    # Checking if the oldest seen time in response is older then the time we actually need (outside of specified time range)
    seen_time_within_range = False if (dt_stop_time - oldest_time_response_data <= timedelta(0)) else True

    """
    Pick it up here.

    You've got the check if the oldest seen time is within the specified timerange or outside of it.
    Based on the result of that check, you have to specify what needs to be done after
        when within time_range -> do another request
        when outside time_range -> drop all the older objects and store the correct objects.

    Idea: explore the possibility of using recursion
    """
    pass

def main():
    x = get_tweets(user_id=user_id)
    print(x)
    
    # url = create_url(user_id=user_id)
    # params = get_params()
    # json_response = connect_to_endpoint(url, params)
    # print(json_response)
    # clean_response = transform_response(original_response=json_response, user_id=user_id)
    # store_response(json_data=clean_response)



if __name__ == '__main__':
    main()