"""
This script is for the extraction of the tweets of one user for a given time range. This script has to
be executed multiple times to extract the tweets of the whole list of users, obtained by executing the 
extract_followers.py script.

[x] - get tweets using api endpoint
[x] - get the time of tweet with the tweet itself
[] - be able the specify a time range for the tweets to recieve.
[] - be able to save or return tweets as collections (dtype: still unknkown) strings (as-is) of a single user.
[] - be able to import the script or functions in other scripts.

"""
import requests
import dotenv

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

def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    print(json_response)


if __name__ == '__main__':
    main()