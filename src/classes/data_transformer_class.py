"""
This script contains a class responsible for all the data transformations that need to happen.

Each method in the class needs to take an input package and maybe some additional information
and return a new object that contains the transformed data.
"""
from datetime import datetime

from sentiment_analysis_class import SentimentAnalysis

class DataTransformer:

    def __init__(self) -> None:
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
