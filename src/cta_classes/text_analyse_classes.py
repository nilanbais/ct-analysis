"""
Classes focussing on text analysis.
"""
from fileinput import filename
import re
import textblob
import dotenv

from typing import Union, List
from cta_classes.base_classes.json_handling_class import JsonHandler


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


class CryptoSymbolFinder(JsonHandler, SentimentAnalysis):
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
        self.__resource_folder_name = dotenv.dotenv_values('./res/.env')["RESOURCE_FOLDER"]
        self.__known_crypto_symbols_file_name = dotenv.dotenv_values('./res/.env')["KNOWN_CRYPTO_SYMBOLS_FILE"]

        self.known_crypto_symbols = self.__init_know_crypto_symbols()


    def __init_know_crypto_symbols(self) -> list:
        """Returns a list of all the known crypto symbols.
        """
        file_data = self._read_json(file_name=self.__known_crypto_symbols_file_name,
                                    folder_name=self.__resource_folder_name)
        clean_data = [file_data[_]["symbol"] for _ in range(len(file_data))]
        return clean_data

    def find_crypto_symbol(self, input_text: str) -> Union[List[str], str]:
        """
        Method used to find a crypto symbol and returns the symbols found

        The method doesn't take context into account, so results cal be cluttered with symbols that 
        represent common words in all caps, like 'ALL' (as in: 'ALL OF IT')

        """
        regex_string = r'\$[A-Z]{3}|[A-Z]{3}'

        match = re.search(regex_string, input_text)
        if match is None:
            return []

        x = match.span()[0]
        y = match.span()[-1]

        symbol = [input_text[x:y]]

        if symbol[0] in self.known_crypto_symbols:  # The if-statement needs to exclude words like 'ALL' with some context or sentiment or some.
            return symbol + self.find_crypto_symbol(input_text=input_text[y:])

        return [] + self.find_crypto_symbol(input_text=input_text[y:])

    def kill_non_exsisting_symbols(input_list: list) -> list:
        """Returns a list from which the regex fault are removed.
        """
        raw_list = input_list.copy()



        """
        Bovenstaande kan waasschijnlijk recursief. Neem daarbij de startindex van de tekst als veranderende waarde in de recursive call. 
        break_statement is wanneer de start en eind index zo dicht bij elkaar liggen dat het gegarandeerd geen crypto symbool is.

        Waarschijnlijk is het qua prestatie beter om eerst recursief een lijst met mogelijke crypto symbolen te verzamelen, en vervolgens deze te filteren
        op de daadwerkelijke symbolen en de ruis die mee kwam door de regex string (QNT en het woord 'ALL' geven beide een hit). Voor de faya kan ook een
        method gebouwd worden die het filteren tijdens de recursieve werking doet, om vervolgens de prestaties van beide methods te timen.

        """


class TextAnalysis:
    """
    Class that combines the other classes to one big one that can be imported to get all functionalities.
    """
    def __init__(self) -> None:
        self.sentiment = SentimentAnalysis()
        self.symbol_finder = CryptoSymbolFinder()

def main():
    test_text = "ALL OF IT"
    test_text2 = "I've got a good bag of ALL"

    sa = SentimentAnalysis()
    [sentiment_1, sentiment_2] = [sa.get_text_sentiment(test_text), sa.get_text_sentiment(test_text2)]
    print([sentiment_1, sentiment_2])

def test():
    test_text = """
                So to prevent QNT people from trading against him further, he reserves all the margin.

                ALL OF IT

                You couldn't borrow any LTC on spot anywhere. 
                Since futures prices are marked against an index of spot prices, it became tough to move prices BTC enough to hit his liquidation.
                """
    test_text2 = """
                So to prevent people from trading against him further, he reserves all the margin.

                 OF IT

                You couldn't borrow any on spot anywhere. 
                Since futures prices are marked against an index of spot prices, it became tough to move prices enough to hit his liquidation.
                """
    csf = CryptoSymbolFinder()
    print(csf.find_crypto_symbol(input_text=test_text))


if __name__ == '__main__':
    main()
    # test()