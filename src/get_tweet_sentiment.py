"""
This script focesses on assigning a sentiment to a given text, using the TextBlob package. In
a later script this functionality will be expended to returning the sentiment of multiple
tweets in a specific data structure. With that it can be possible to automaticly add the
sentiment score as an extra column.
(package info: https://textblob.readthedocs.io/en/dev/index.html)

[] - have one single function call that returns the sentiment score of a text.
[] - have the ability to analyse emoji's and other unitext based characters
[] - (optional??) have the ability to use multiple input structures
"""
import textblob

def get_text_sentiment(input_text: str):
    # Creating a text object
    text_object = textblob.TextBlob(text=input_text)
    # Assigning the sentiment attribute to it's own variable + returning variable
    senitment_object = text_object.sentiment
    return senitment_object