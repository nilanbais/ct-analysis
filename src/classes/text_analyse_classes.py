"""
Classes focussing on text analysis.
"""
import textblob


class CryptoSymbolFinder:
    """
    This script contains a class that is used in finding crypto symbols in text. 

    With that comes the possibility to extend this class to a wider text analysis 
    applicaitons. when that happens, think about making SentimentAnalysis a parent
    class.

    A crypto symbol is a short name mostly consisting of three cap letters, 
    like BTC or ETH. Twitter has a functionality where you can search the 
    platform for tweets containing crypto symbols using a '$' in front of the 
    symbols.

    """
    def __init__(self) -> None:
        pass

    def find_crypto_symbol(self, input_text: str) -> str:
        """
        Method used to find a crypto symbol and returns the symbols found
        """
        pass


class SentimentAnalysis:
    """
    This script contains a class that is responsible for doing a sentiment analysis on some input
    and returning a sentiment score.
    """
    def __init__(self) -> None:
        pass
    
    def get_text_sentiment(self, input_text: str):
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

class TextAnalysis:
    """
    Class that combines the other classes to one big one that can be imported to get all functionalities.
    """
    def __init__(self) -> None:
        self.sentiment = SentimentAnalysis()
        self.symbol_finder = CryptoSymbolFinder()