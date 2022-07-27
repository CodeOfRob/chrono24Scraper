from datetime import datetime


class WatchTimestamp:

    def __init__(self, currency: str, offers_count: int, price_stats: object):
        self.timestamp = datetime.now()
        self.currency = currency
        self.offers_count = offers_count 
        self.p_mean = price_stats["p_mean"] 
        self.p_med = price_stats["p_med"]
        self.p_lowest = price_stats["p_lowest"]
        self.p_highest = price_stats["p_highest"]

    def pushable(self):
        return {
            "timestamp": self.timestamp,
            "currency": self.currency,
            "offers_count": self.offers_count ,
            "p_mean": self.p_mean ,
            "p_med": self.p_med,
            "p_lowest": self.p_lowest,
            "p_highest": self.p_highest
        }

    def __str__(self): 
        return self.pushable().__str__()
