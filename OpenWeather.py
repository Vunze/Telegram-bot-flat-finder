import requests


class WeatherQuery:
    def __init__(self):
        with open('OpenWeatherAPI.txt') as f:
            token = f.read()
        self.key = token
        self.temp = 0
        self.feels_like = 0
        self.temp_min = 0
        self.temp_max = 0
        self.wind_direction = "South"
        self.query_page = "http://api.openweathermap.org/data/2.5/weather?q=city&appid=key&units=metric"
        self.weather = "Clear"
        self.weather_desc = "Clear sky"
        self.success = False
        self.city = "moscow"

    @staticmethod
    def get_wind_direction(degrees):
        if degrees == 0:
            return "North"
        if degrees == 90:
            return "East"
        if degrees == 180:
            return "South"
        if degrees == 270:
            return "West"
        if 0 < degrees < 90:
            return "North-East"
        if 90 < degrees < 180:
            return "South-East"
        if 180 < degrees < 270:
            return "South-West"
        return "North-West"

    def query(self, city):
        self.city = city
        result_link = self.query_page.replace("city", city).replace("key", self.key)
        response = requests.get(result_link)
        # print(response.json())
        if len(response.json()) > 2:
            self.success = True
        else:
            return
        self.temp = response.json()["main"]["temp"]
        self.feels_like = response.json()["main"]['feels_like']
        self.temp_min = response.json()["main"]['temp_min']
        self.temp_max = response.json()["main"]['temp_max']
        self.wind_direction = self.get_wind_direction(response.json()['wind']['deg'])
        self.weather = response.json()['weather'][0]['main']
        self.weather_desc = response.json()['weather'][0]['description']


weather = WeatherQuery()
weather.query("asdasdasdasdasd")
# print("temp is", weather.temp, "max temp is", weather.temp_max, "min temp is", weather.temp_min, "temp feels like",
# weather.feels_like, "wind blows to", weather.wind_direction, "the weather is", weather.weather, "and", weather.weather_desc, "expected\n")
