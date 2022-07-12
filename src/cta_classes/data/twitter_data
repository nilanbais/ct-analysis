from typing import List
from cta_classes.data.transformer import DataTransformer
from cta_classes.text_analysis.sentiment import SentimentAnalysis


class TwitterDataTransformer:

    def __init__(self) -> None:
        self.general = DataTransformer()
        self.sentiment = SentimentAnalysis()

    @staticmethod
    def clean_followers_list(input_list: List[dict]) -> List[dict]:
        """Changes the dicts in the list of accounts followed by the base_user, to keep
        the id, username, name, and followers_count.
        """
        result_list = list()
        for item in input_list:
            public_metrics = item["public_metrics"]
            result_list.append({
                "id": item["id"],
                "username": item["username"],
                "name": item["name"],
                "followers_count": public_metrics["followers_count"]
            })
        return result_list

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