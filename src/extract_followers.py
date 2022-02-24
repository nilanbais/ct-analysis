"""
User-agent voor verschillende endpoints:
looking up users using username = v2UserLookupPython
looking up following by user id = v2FollowingLookupPython

[x] - saving the followed accounts to the data folder.
"""
import json
import dotenv
import requests

# env variables
__config = dotenv.dotenv_values('./res/.env')
__BEARER_TOKEN = __config["BEARER_TOKEN"]
__USERNAME = __config["USERNAME"]

# Functions
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {__BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FollowingLookupPython"  # all endpoints have different user-agents.
    return r

def create_url():
    __USER_ID = __config["USER_ID"]
    url = "https://api.twitter.com/2/users/{}/following?{}={}".format(__USER_ID, "max_results", 1000)
    return url

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

def store_response(json_data):
    with open('./data/ct_accounts.json', 'w') as json_file:
        json.dump(json_data, json_file)

def main():
    url = create_url()
    params = {}
    json_response = connect_to_endpoint(url, params)
    store_response(json_data=json_response)


if __name__ == '__main__':
    main()