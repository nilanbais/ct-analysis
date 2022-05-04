"""
Classes focussing on text analysis.
"""
import re
import textblob

from typing import Union, List


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

    def find_crypto_symbol(self, input_text: str) -> Union[List[str], str]:
        """
        Method used to find a crypto symbol and returns the symbols found
        """
        regex_string = r'\$[A-Z]{3}|[A-Z]{3}'
        return re.search(regex_string, input_text)
        """
        Bovenstaande kan waasschijnlijk recursief. Neem daarbij de startindex van de tekst als veranderende waarde in de recursive call. 
        break_statement is wanneer de start en eind index zo dicht bij elkaar liggen dat het gegarandeerd geen crypto symbool is.

        Waarschijnlijk is het qua prestatie beter om eerst recursief een lijst met mogelijke crypto symbolen te verzamelen, en vervolgens deze te filteren
        op de daadwerkelijke symbolen en de ruis die mee kwam door de regex string (QNT en het woord 'ALL' geven beide een hit).

        """


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

def main():
    pass

def test():
    test_text = """
                So to prevent QNT people from trading against him further, he reserves all the margin.

                ALL OF IT

                You couldn't borrow any LTC on spot anywhere. 
                Since futures prices are marked against an index of spot prices, it became tough to move prices BTC enough to hit his liquidation.
                """
    csf = CryptoSymbolFinder()
    print(csf.find_crypto_symbol(input_text=test_text))


if __name__ == '__main__':
    # main()
    test()