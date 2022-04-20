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

class CryptoSymbolFinder:

    def __init__(self) -> None:
        pass

    def find_crypto_symbol(self, input_text: str) -> str:
        """
        Method used to find a crypto symbol and returns the symbols found
        """
        pass

