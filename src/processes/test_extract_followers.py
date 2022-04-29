"""
This script is used when building the workflow for the extraction of the followed accounts by the base_user.
The code needs to do the following:
- [] get the list of followed accounts by the base_user
- [] prep the data structure user_document.py for each user
- [] upload the data to the database (or print if no upload method available yet) 
"""
from .. import cta_classes as cta

upload_followed_accounts_base_user = cta.Pipeline()