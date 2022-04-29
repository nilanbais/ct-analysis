"""
This script is used when building the workflow for the extraction of the followed accounts by the base_user.
The code needs to do the following:
- [] get the list of followed accounts by the base_user
- [] prep the data structure user_document.py for each user
- [] upload the data to the database (or print if no upload method available yet) 
"""
import pprint

from matplotlib.pyplot import get
from cta_classes.pipeline_class import Pipeline
from cta_classes.twitter_handling_classes import TwitterAPI, TwitterDataTransformer

get_followed_acc_line = Pipeline()

twitter_api = TwitterAPI()
twitter_data_transformer = TwitterDataTransformer()

@get_followed_acc_line.task()
def get_list():
    return twitter_api.extract_follers_list()

@get_followed_acc_line.task(depends_on=get_list)
def print_result(input_data):
    pprint(input_data)


result = get_followed_acc_line.run()