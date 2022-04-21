"""
This script contains a class responsible for all the data transformations that need to happen.

Each method in the class needs to take an input package and maybe some additional information
and return a new object that contains the transformed data.
"""
from datetime import datetime

from sentiment_analysis_class import SentimentAnalysis

class DataTransformer:

    def __init__(self) -> None:
        self.sentiment = SentimentAnalysis()
        self.__RFC3339_format = "%Y-%m-%dT%H:%M:%S.000Z"
        
    
    def get_RFC_timestamp(self, dt_object: datetime):
        """
        Returns a string that is a valid RFC3339 date and time notation.
        """
        return datetime.strftime(dt_object, self.__RFC3339_format)

    def get_datetime_object(self, rfc_timestamp: str) -> datetime:
        """
        Returns a datatime object from a RFC3339 timestamp.
        """
        return datetime.strptime(rfc_timestamp, self.__RFC3339_format)

    def clean_get_tweets_response(self, input_data: list, additional_data: dict) -> list:
        """
        This method is used for cleaning the response received from TwitterAPI.get_tweets().
        It takes the input data and builds a data structure like the following:
        
        "timestamp": "(datetime object) timestamp in twitterformat (?)",
        "user_id": "(int)",
        "username": "(string)",
        "user_tweets": [
            {
                "tweet_id": "(int)",
                "tweet_text": "(string)",
                "mentioned_crypto_symbols": (list),
                "senitment_score": "(int or float) (depending on score scale)"
            }
        ]
        """
        return_package = list()
        tweet_list = input_data.copy()
        user_info = additional_data.copy()

        for tweet in tweet_list:
            sentiment_object = self.sentiment.get_text_sentiment(input_text=tweet['text'])
            
            return_package.append({       
                "timestamp": tweet['created_at'],
                "user_id": user_info['id'],
                "tweet_id": tweet['id'],
                "tweet_text": tweet['text'],
                "sentiment": float(sentiment_object.polarity),
                "subjectivity": float(sentiment_object.subjectivity)})
            
        return return_package