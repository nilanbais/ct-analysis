"""
Script that can be run to update the list of known crpyto synbols, extracted from
CoinMarketCap. The file is stored locally in the resource data (res) folder.
"""
from pprint import pprint

from cta_classes.pipeline_class import Pipeline
from cta_classes.coinmarketcap_handling_classes import CoinMarketCapAPI, CMCDataTransformer

update_crypto_symbols = Pipeline()

cmc_api = CoinMarketCapAPI()
cmc_data_transformer = CMCDataTransformer()

