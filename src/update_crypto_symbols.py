"""
Script that can be run to update the list of known crpyto synbols, extracted from
CoinMarketCap. The file is stored locally in the resource data (res) folder.
"""
import json
from pprint import pprint
import dotenv

from typing import List

from cta_classes.pipeline import Pipeline
from cta_classes.coinmarketcap_handling_classes import CoinMarketCapAPI, CMCDataTransformer, CoinMarketCapAPI_v2

update_crypto_symbols = Pipeline()

cmc_api = CoinMarketCapAPI_v2()
cmc_data_transformer = CMCDataTransformer()

@update_crypto_symbols.task()
def get_a_fresh_list() -> List[dict]:
    """Gets a list of all the crypto symbols.
    """
    return cmc_api.get_symbol_id_list()

@update_crypto_symbols.task(depends_on=get_a_fresh_list)
def pprint_result(input_data: List[dict]) -> None:
    """Pritty prints some shit
    """
    pprint(type(input_data))

@update_crypto_symbols.task(depends_on=get_a_fresh_list)
def clean_result(input_data: List[dict]) -> List[dict]:
    """Clean the input list based on sme specified keys to keep.
    """
    keys2keep = ["id", "name", "symbol"]
    
    raw_result = input_data
    clean_result = []
    for rresult in raw_result:
        clean_item = {key: rresult[key] for key in rresult.keys() if key in keys2keep}
        clean_result.append(clean_item)

    return clean_result

def store_json(json_data: List[dict], file_name: str, folder_name: str) -> None:
    with open('./{}/{}'.format(folder_name, file_name), 'w') as json_file:
        json.dump(json_data, json_file)

@update_crypto_symbols.task(depends_on=clean_result)
def store_fresh_list(input_data: List[dict]) -> None:
    """Stores the fresh list in the right place.
    """
    __fresh_file_name = dotenv.dotenv_values("./res/.env")["KNOWN_CRYPTO_SYMBOLS_FILE"]
    store_json(json_data=input_data, file_name=__fresh_file_name, folder_name='res')
    print("Done my dude")

result = update_crypto_symbols.run()