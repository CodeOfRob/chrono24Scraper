import time
import json
import typing
import requests
import bs4
import numpy
import dotenv

from DBClient import DBClient
from WatchTimestamp import WatchTimestamp

ENV = dotenv.dotenv_values()
DB_URI = ENV["DB_URI"]
URL = ENV["URL"]
TG_API_KEY = ENV["TELEGRAM_API_KEY"]
TG_CHAT_ID = ENV["CHAT_ID"]

TIMEOUT_SECONDS = 60*60

def extract_prices(doc: int) -> typing.Union[typing.List[float], str]:

    soup = bs4.BeautifulSoup(doc, "lxml")

    offers_container = json.loads(soup.find("script", type="application/ld+json").contents[0])
    aggregate_offers = offers_container["@graph"][1]
    offers = aggregate_offers["offers"]
    currency = aggregate_offers["priceCurrency"]

    return [[float(offer["price"]) for offer in offers], currency]


def create_watchTimestamp(prices: typing.List[int], currency: str) -> WatchTimestamp:
    
    offers_count = len(prices)

    price_stats = {
        "p_mean": float(numpy.mean(prices)),
        "p_med": float(numpy.median(prices)),
        "p_lowest": float(numpy.amin(prices)),
        "p_highest": float(numpy.amax(prices))
    }

    return WatchTimestamp(currency, offers_count, price_stats)

if __name__ == "__main__":

    db = DBClient(DB_URI)

    while True:

        # fetch website content
        res = None
        try:
            res = requests.get(URL)
        except:
            print("Error while fetching website content")
            time.sleep(TIMEOUT_SECONDS)
        
        if not res or not res.ok: continue

        doc = res.content

        # extract watchTimestamps
        [prices, currency] = extract_prices(doc)

        # create watchTimestamp
        watchTimestamp = create_watchTimestamp(prices, currency)

        # push data to database
        db.push_watchTimestamp(watchTimestamp)

        # print success
        print("successful upload:", watchTimestamp)

        # wait 1 hour
        time.sleep(TIMEOUT_SECONDS)
