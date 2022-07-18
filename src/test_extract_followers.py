"""
This script is used when building the workflow for the extraction of the followed accounts by the base_user.
The code needs to do the following:
- [] get the list of followed accounts by the base_user
- [] prep the data structure user_document.py for each user
- [] upload the data to the database (or print if no upload method available yet) 
"""
from pprint import pprint

from cta_classes.pipeline import Pipeline
from cta_classes.twitter_handling_classes import TwitterAPI, TwitterDataTransformer, TwitterAPI_v2
from cta_classes.database_handling_classes import DataBaseActions

get_followed_acc_pipeline = Pipeline()

# db_actions = DataBaseActions()

twitter_api = TwitterAPI_v2()
twitter_data_transformer = TwitterDataTransformer()


@get_followed_acc_pipeline.task()
def get_list():
    return twitter_api.extract_following_list()

@get_followed_acc_pipeline.task(depends_on=get_list)
def clean_list(input_list):
    return twitter_data_transformer.clean_followers_list(input_list=input_list)

# @get_followed_acc_pipeline.task(depends_on=clean_list)
# def insert_documents_into_collection(input_list) -> None:
#     db_actions.insert_many(documents=input_list,
#                            database_name='cta-database',
#                            collection_name='users')
#     print("Done inserting my dude.")

@get_followed_acc_pipeline.task(depends_on=clean_list)
def print_result(input_data):
    pprint(input_data)


result = get_followed_acc_pipeline.run()