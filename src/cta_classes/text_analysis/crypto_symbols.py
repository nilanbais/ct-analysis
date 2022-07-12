import re
from typing import List, Union

from cta_classes.file_handling.env_reader import EnvVarReader
from cta_classes.file_handling.json_handler import JsonHandler

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
        self.__resource_folder_name = EnvVarReader().get_value("RESOURCE_FOLDER")
        self.__known_crypto_symbols_file_name = EnvVarReader().get_value("KNOWN_CRYPTO_SYMBOLS_FILE")

        self.known_crypto_symbols = self.__init_know_crypto_symbols()


    def __init_know_crypto_symbols(self) -> list:
        """Returns a list of all the known crypto symbols.
        """
        file_data = JsonHandler().read_json(file_name=self.__known_crypto_symbols_file_name,
                                            folder_name=self.__resource_folder_name)
        clean_data = [file_data[_]["symbol"] for _ in range(len(file_data))]
        return clean_data

    def find_crypto_symbols(self, input_text: str) -> Union[List[str], str]:
        """
        Method used to find a crypto symbol and returns the symbols found

        The method doesn't take context into account, so results cal be cluttered with symbols that 
        represent common words in all caps, like 'ALL' (as in: 'ALL OF IT')

        First version of this method only matches symbols that contain the signature '$' before the
        symbol.
        """
        # regex_string = r'\$[A-Z]{3}|[A-Z]{3}'
        regex_string = r'\$[A-Z]{3}'

        match = re.search(regex_string, input_text)
        print(match)
        if match is None:
            return []

        x = match.span()[0]
        y = match.span()[-1]

        match_result = input_text[x:y]
        symbol = match_result[1:]

        # If a symbol is found that is unknown, if doesn't take it into account now
        # Functionality has to be extended, but somewhere else (maybe a pipeline or some)
        if symbol not in self.known_crypto_symbols: 
            return [] + self.find_crypto_symbols(input_text=input_text[y:])

        return [symbol] + self.find_crypto_symbols(input_text=input_text[y:])

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