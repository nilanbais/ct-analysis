"""
This script contains a class that is responsible for doing a sentiment analysis on some input
and returning a sentiment score.
"""
import textblob


class SentimentAnalysis:

    def __init__(self) -> None:
        pass
    
    def get_text_sentiment(input_text: str):
        """
        Function returns a sentiment object with the following scores.
        - polarity score -> how possitive or negative a text is.
        - subjectivity score -> how factual a text is. (or how much of an opinion)
        """
        # Creating a text object
        text_object = textblob.TextBlob(text=input_text)
        # Assigning the sentiment attribute to it's own variable + returning variable
        senitment_object = text_object.sentiment
        return senitment_object