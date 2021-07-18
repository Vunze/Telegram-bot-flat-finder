import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Parser:
    def __init__(self, min_price, max_price, city_id=4593):
        self.fake_user = UserAgent()
        self.headers = {
                'User-Agent': self.fake_user.chrome
        }
        self.result = []
        self.url = ''
        self.city_id = city_id
        self.min_price = min_price
        self.max_price = max_price

    def get_page(self, i):
        self.url = f"https://cian.ru/cat.php?deal_type=rent&engine_version=" \
                   f"2&offer_type=flat&p={i}&maxprice={self.max_price}&" \
                   f"minprice={self.min_price}&region={self.city_id}&type=4"
        res = requests.get(url=self.url, headers=self.headers)
        return res.text

    def parse_page(self, html: str):
        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception:
            soup = BeautifulSoup(html, 'html.parser')

        offers = soup.select("div[data-name='Offers'] > article[data-name='CardComponent']")
        for flats in offers:
            self.parse_flat(flats)

    def parse_flat(self, new_flat):
        link = new_flat.select("div[data-name='LinkArea']")[0].select("a")[0].get('href')
        price_long = new_flat.select("div[data-name='LinkArea']")[0].select("div[data-name='ContentRow']")[1].text
        price_per_month = "".join(price_long[:price_long.find("₽/мес") - 1].split())
        self.result.append(price_per_month + ',' + link + "\n")

    def run(self):
        # change this range to control the amount of flats being parsed
        for i in range(1, 4):
            try:
                html = self.get_page(i)
                self.parse_page(html)
            except Exception:
                break
