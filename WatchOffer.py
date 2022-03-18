from datetime import datetime
from requests_html import HTMLSession
import bs4

class WatchOffer:

    def __init__(self, url: str, title: str, price: int, currency: str):
        self.timestamp = datetime.now()
        self.url = url
        self.title = title
        self.currency = currency
        self.price = price

        self.condition = None
        self.productionyear = None
        self.has_original_box = None
        self.has_original_papers = None
        self.location = None
        self.description = None

        self.fetch_details()

    def fetch_details(self):
        print("fetching:", self.url)
        session = HTMLSession()
        doc = session.get(self.url)
        doc.html.render(timeout=60)

        page_content = bs4.BeautifulSoup(doc.html.raw_html, "lxml")
        # print(page_content)
        main_section = page_content.find("main")
        specs_section = main_section.find("section", {"id":"jq-specifications"})

        tables = specs_section.find_all("table")

        specs = tables[0]
        desc = tables[1]

        spec_rows = specs.find_all("tr")
        for row in spec_rows:
            if "Zustand" in row.text:    
                cols = row.find_all("td")
                self.condition = cols[1].find("a").text.strip()

            elif "Lieferumfang" in row.text:
                cols = row.find_all("td")
                content = cols[1].text.strip().lower()
                elements = content.split(",")

                for element in elements:
                    cond = True if "mit" in element else False

                    if "original-box" in element:
                        self.has_original_box = cond
                    elif "original-papiere" in element:
                        self.has_original_papers = cond
                    else:
                        print("error while parsing box and papers")

            elif "Herstellungsjahr" in row.text:
                cols = row.find_all("td")
                self.productionyear = cols[1].text.strip()

            elif "Standort" in row.text:
                cols = row.find_all("td")
                self.location = cols[1].text.strip()

       
        desc_rows = desc.find_all("tr")
        self.description = desc_rows[1].text.strip()
