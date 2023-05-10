import json
import logging
import re
from urllib import request
import gate_api
from gate_api.exceptions import ApiException, GateApiException

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)

def get_gateio_listed_coins_details():
    try:
        # List all currencies' details
        api_response = api_instance.list_currencies()
        coins = []
        for curr in api_response:
            if '_' not in curr.currency and '3' not in curr.currency and '5' not in curr.currency:
                coin = re.sub("[^A-Za-z]","", curr.currency)
                coins.append(coin)
        return coins
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_currencies: %s\n" % e)

def get_listed_coins():
    try:
        res = api_instance.list_currency_pairs()
        return res
    except GateApiException as ex:
        logging.exception("Exception while getting all listed pairs: " + ex)

def process_listed_coins():
    coin_list = get_listed_coins()
    print(len(coin_list))
    list_of_substrings = ['2L', '2S', '3S', '3L', '4L', '4S', '5L', '5S']
    if coin_list == None: return []
    try:
        coin_list = list(filter(lambda coin: coin.quote =='USDT', coin_list))
        coins = [coin for coin in coin_list]
        filtered_coins = list(filter(lambda coin: not any(substring in coin.base for substring in list_of_substrings), coins))
        print(len(filtered_coins))
        return filtered_coins 
    except Exception as e:
        logging.exception(e)
        return []

process_listed_coins()