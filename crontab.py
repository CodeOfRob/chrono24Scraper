import json
import bs4
import requests

from DBClient import DBClient
from WatchOffer import WatchOffer
from app import DB_URI, TG_API_KEY, TG_CHAT_ID, URL, create_watchTimestamp, extract_prices
from telegram.telegram import TelegramService

def fetch_timestamps(db, tg, doc):
    # extract watchTimestamps
    [prices, currency] = extract_prices(doc)

    # create watchTimestamp
    watchTimestamp = create_watchTimestamp(prices, currency)

    # push data to database
    db.push_watchTimestamp(watchTimestamp)

    # print success
    print("successful upload:", watchTimestamp)
    tg.send_msg(f"new watchtimestamp:\n {watchTimestamp}")

def fetch_offers(db, tg, doc):
    
    soup = bs4.BeautifulSoup(doc, "lxml")
    offers_container = json.loads(soup.find("script", type="application/ld+json").contents[0])
    aggregate_offers = offers_container["@graph"][1]
    currency = aggregate_offers["priceCurrency"]
    offers = aggregate_offers["offers"]

    db.drop_watchOfferSnapshots()

    count = 0
    for offer in offers:
        new_offer = WatchOffer(offer["url"], offer["name"], float(offer["price"]),currency)
        db.push_watchOfferSnapshot(new_offer)
        count += 1

    print("pushed", count, "new offer snapshots")
    tg.send_msg(f"pushed {count} new offer snapshots")


def main():

    db = DBClient(DB_URI)

    tg = TelegramService(TG_API_KEY, TG_CHAT_ID)
    
    res = None
    try:
        res = requests.get(URL)
    except Exception as e:
        print("Error while fetching website content")
        tg.send_msg("WTs:\nError while fetching website content:\n{e}")
    
    if not res or not res.ok: 
        return

    doc = res.content

    fetch_timestamps(db, tg, doc)

    fetch_offers(db, tg, doc)

if __name__ == "__main__":
    main()