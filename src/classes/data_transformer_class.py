"""
This script contains a class responsible for all the data transformations that need to happen.

Each method in the class needs to take an input package and maybe some additional information
and return a new object that contains the transformed data.
"""
from datetime import datetime

class DataTransformer:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_RFC_timestamp(dt_object: datetime):
        """
        Returns a string that is a valid RFC3339 date and time notation.
        """
        __RFC3339_format = "%Y-%m-%dT%H:%M:%S.000Z"
        return datetime.strftime(dt_object, __RFC3339_format)
