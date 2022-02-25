import time 
import requests

from DBClient import DBClient
from app import DB_URI, TG_API_KEY, TG_CHAT_ID, URL, create_watchTimestamp, extract_prices
from telegram.telegram import TelegramService

def main():

    db = DBClient(DB_URI)

    tg = TelegramService(TG_API_KEY, TG_CHAT_ID)

    # fetch website content
    res = None
    try:
        res = requests.get(URL)
    except Exception as e:
        print("Error while fetching website content")
        tg.send_msg("WTs:\nError while fetching website content:\n{e}")
    
    if not res or not res.ok: 
        return

    doc = res.content

    # extract watchTimestamps
    [prices, currency] = extract_prices(doc)

    # create watchTimestamp
    watchTimestamp = create_watchTimestamp(prices, currency)

    # push data to database
    db.push_watchTimestamp(watchTimestamp)

    # print success
    print("successful upload:", watchTimestamp)
    tg.send_msg(f"new watchtimestamp:\n {watchTimestamp}")

if __name__ == "__main__":
    main()