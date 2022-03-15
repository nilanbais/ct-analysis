"""
This script builds on the functionalities used when extracting the tweets of a single user. Here it combines these functions
to extract the tweets of all the users that the corresponding account follows.

[] - get tweets using api endpoint
[] - get the time of tweet with the tweet itself
[] - be able to return tweets as collections (dtype: list of dicts) strings (as-is) of a single user.
[] - be able to extract all the tweet within a given/specified time range of one user and combining the 
        multiple response packages to one single package.
[] - store the tweets of the different users in a database (prob mongodb)
"""
from extract_followers import extract_follers_list, store_response
from get_tweets_single_user import get_tweets

