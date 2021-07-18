import telebot
from telebot import types
import Mars_rover_info
import OpenWeather
import Collect_flat_data
import transliterate
import RandomDrink


class FlatFinder:
    def __init__(self, price_min, price_max):
        self.price_min = price_min
        self.price_max = price_max
        f = open("TokenTelegram.txt")
        self.bot = telebot.TeleBot(f.read())
        self.rover = Mars_rover_info.RoverQuery()
        self.weather = OpenWeather.WeatherQuery()
        self.current_city = 'Moscow'


load = FlatFinder(0, 500000000)


@load.bot.message_handler(commands=['current'])
def load_settings(message):
    send_mess = f"<b>Price range: from {load.price_min} rub to {load.price_max} rub.\n" \
                f" Current search city is {load.current_city}</b>\n"
    load.bot.send_message(message.chat.id, send_mess, parse_mode='html')


@load.bot.message_handler(commands=['change'])
def change_settings(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    button1 = types.KeyboardButton('Change price range')
    button2 = types.KeyboardButton('Change city')
    markup.add(button1, button2)
    load.bot.send_message(message.chat.id, "<b>Choose setting to change.</b>\n", parse_mode='html', reply_markup=markup)


@load.bot.message_handler(commands=['help'])
def helper(message):
    send_mess = f"<b>Use /current to view current settings\n" \
                f"Use /change to change your settings\n" \
                f"Use /get to load the list of flats\n" \
                f"To get a recipe of a random drink enter /RandomDrink\n" \
                f"To get a photo from mars rover enter /RoverPhoto\n" \
                f"To get the weather of a city enter /weather</b>\n"
    load.bot.send_message(message.chat.id, send_mess, parse_mode='html')


@load.bot.message_handler(commands=['get'])
def get_flats(message):
    load.bot.send_message(message.chat.id, f"<b>This might take a while. Please, be patient</b>.\n", parse_mode='html')
    loader = Collect_flat_data.FlatsFinder(load.price_min, load.price_max, load.current_city)
    result = loader.load()
    send_mess = f"<b>The list of flats in given price range:\n"
    counter = 0
    for res in result:
        counter += 1
        send_mess += f"{counter}) {res[0]}, price {res[1]}"
        if counter % 10 == 0:
            load.bot.send_message(message.chat.id, send_mess + "</b>", parse_mode='html')
            send_mess = f"<b>"
    if counter == 0:
        load.bot.send_message(message.chat.id, f"<b>Sorry, it seems like there are no new offers, please try again"
                                               f" later.</b>\n",
                              parse_mode='html')


@load.bot.message_handler(commands=['RandomDrink'])
def drink(message):
    drink_man = RandomDrink.RandomDrinkQuery()
    drink_man.query()
    load.bot.send_photo(message.chat.id, drink_man.image)
    send_mess = f"<b>This drink is called {drink_man.name}. It is {drink_man.alcoholic}.\n" \
                f"For it you need {drink_man.ingredients[1:]}.\n" \
                f"Instructions: {drink_man.instructions}.</b>\n"
    load.bot.send_message(message.chat.id, send_mess, parse_mode='html')


@load.bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    if not user_name:
        user_name = ''
    if not user_surname:
        user_surname = ''
    send_mess = f"<b>Hello {user_name} {user_surname}!\n" \
                f"Use /current to view current settings\n" \
                f"Use /change to change your settings\n" \
                f"Use /get to load the list of flats\n" \
                f"To get a recipe of a random drink enter /RandomDrink\n" \
                f"To get a photo from mars rover enter /RoverPhoto\n" \
                f"To get the weather of a city enter /weather</b>\n"
    load.bot.send_message(message.chat.id, send_mess, parse_mode='html')


@load.bot.message_handler(commands=['RoverPhoto'])
def rover_photo(message):
    result = None
    while not result:
        result = load.rover.query()
    load.bot.send_photo(message.chat.id, result[0])
    load.bot.send_message(message.chat.id, f"<b>Photo taken on {result[1]}"
                                           f" by {result[2]} rover with {result[3]}</b>!\n", parse_mode='html')


def generate_weather_answer(weather):
    if weather.success:
        result = f"<b>The temperature in {weather.city} is {str(weather.temp)}." \
                 f" Feels like {str(weather.feels_like)}.\nThe" \
                 f" minimal temperature is {str(weather.temp_min)} and" \
                 f" the maximum temperature is {str(weather.temp_max)}.\nThe di" \
                 f"rection of wind is {weather.wind_direction}.\nThe we" \
                 f"ather is {weather.weather} and {weather.weather_desc} expected.\n</b>"
        weather.success = False
    else:
        result = "<b>City not found.</b>\n"
    return result


@load.bot.message_handler(commands=['weather'])
def get_weather_city(message):
    send_mess = f"<b>Enter a city in format \"city (your city)\".</b>\n"
    load.bot.send_message(message.chat.id, send_mess, parse_mode='html')


@load.bot.message_handler(content_types=['text'])
def change_price(message):
    get_message = message.text.strip()
    if get_message.find("city ") != -1:
        load.weather.query(get_message[5:])
        send_mess = generate_weather_answer(load.weather)
    elif get_message.find("change to") != -1:
        load.current_city = transliterate.translit(get_message[10:], reversed=True)
        send_mess = f"<b>City successfully changed, use /help for other commands!</b>\n"
    elif get_message == "Change price range":
        send_mess = f"<b>Enter your price range in format min-max (example: 20000-50000).</b>\n"
    elif get_message == "Change city":
        send_mess = f"<b>Enter new city in format \"change to (city)\" (example: change to Москва).</b>\n"
    else:
        if get_message.find('-') != -1:
            res_split_dash = get_message.split('-')
            load.price_min = res_split_dash[0]
            load.price_max = res_split_dash[1]
        send_mess = f"<b>Price range successfully changed, use /help for other commands!</b>\n"
    if send_mess:
        load.bot.send_message(message.chat.id, send_mess, parse_mode='html')


load.bot.polling(none_stop=True)
