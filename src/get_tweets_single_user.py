"""
This script is for the extraction of the tweets of one user for a given time range. This script has to
be executed multiple times to extract the tweets of the whole list of users, obtained by executing the 
extract_followers.py script.

[x] - get tweets using api endpoint
[x] - get the time of tweet with the tweet itself
[x] - be able to return tweets as collections (dtype: list of dicts) strings (as-is) of a single user.
[] - be able to import the script or functions in other scripts.

"""
import requests
import dotenv
import json

# env variables
__config = dotenv.dotenv_values('./res/.env')
__BEARER_TOKEN = __config["BEARER_TOKEN"]
__USERNAME = __config["USERNAME"]

# Input variables
user_id = "969716112752553985"  # first from ct_accounts.json
time_range = ""  # the time range of 24 hours

# Functions
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {__BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2UserTweetsPython"  # all endpoints have different user-agents.
    return r

def create_url():
    __USER_ID = __config["USER_ID"]
    url = "https://api.twitter.com/2/users/{}/{}?{}={}".format(user_id, 'tweets', 'max_results', 100)
    return url

def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {'tweet.fields': 'created_at'}

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
    _og_package = original_response.copy()
    _og_data = _og_package['data']
    _og_meta = _og_package['meta']
    transformed_data = list()

    for item in _og_data:

        created_at = item['created_at']
        tweet_id = item['id']
        text = item['text']

        transformed_data.append({"user_id": user_id, "tweet_id": tweet_id, "created_at": created_at, 'text': text})

    return {'data': transformed_data, 'meta': _og_meta}

def store_response(json_data: dict):
    with open('./data/tweets_user_{}.json'.format(user_id), 'w') as json_file:
        json.dump(json_data, json_file)

def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    clean_response = transform_response(original_response=json_response, user_id=user_id)
    store_response(json_data=clean_response)



if __name__ == '__main__':
    main()