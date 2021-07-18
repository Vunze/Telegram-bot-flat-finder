import csv
from parser_cian import Parser
import transliterate


class FlatsFinder:
    def __init__(self, min_price, max_price, city):
        self.min_price = min_price
        self.max_price = max_price
        self.city = city
        self.city_id = get_id(city)

    def load(self):
        parser = Parser(self.min_price, self.max_price, self.city_id)
        parser.run()
        for flat in parser.result:
            res = flat.split(',')
            yield res


def get_id(town):
    with open("cities.csv", encoding="utf8") as f:
        reader_cities = csv.reader(f)
        for city in reader_cities:
            if transliterate.translit(city[0], reversed=True) == town:
                return city[1]
