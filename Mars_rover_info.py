import requests
import random


class RoverQuery:
    def __init__(self):
        with open('TokenNASA.txt') as f:
            token = f.read()
        self.key = token
        self.query_page = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?"

    @staticmethod
    def random_sol() -> int:
        return random.randrange(1, 1000)

    def query(self):
        sol = self.random_sol()
        result_link = self.query_page + "sol=" + str(sol) + "&page=1&api_key=" + self.key
        response = requests.get(result_link)
        response_size = len(response.json()['photos'])
        if response_size > 0:
            random_photo = response.json()['photos'][random.randrange(1, response_size)]
            # print(random_photo)
            # print(random_photo['camera']['full_name'])
            # print(random_photo['rover']['name'])
            return random_photo["img_src"], random_photo["earth_date"], random_photo['rover']['name'], random_photo['camera']['full_name']
            # return random_photo["img_src"], random_photo["earth_date"]
        else:
            return None


rover = RoverQuery()
rover.query()
