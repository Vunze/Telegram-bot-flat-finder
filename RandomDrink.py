import requests


class RandomDrinkQuery:
    def __init__(self):
        self.url = "http://www.thecocktaildb.com/api/json/v1/1/random.php"
        self.ingredients = ""
        self.name = ""
        self.alcoholic = ""
        self.instructions = ""
        self.image = ""

    def query(self):
        res = requests.get(self.url)
        # to return: Name (strDrink), alcoholic (strAlcoholic), Instructions (strInstructions)
        # Image (strDrinkThumb), ingredients (while not None: get strIngredient{i}), Measures
        ingredient = "strIngredient"
        measure = "strMeasure"
        for i in range(1, 16):
            if res.json()['drinks'][0][ingredient + str(i)]:
                new_ingredient = work_with_none_measure(res.json()['drinks'][0][measure + str(i)])\
                                 + res.json()['drinks'][0][ingredient + str(i)]
                self.ingredients = ', '.join([self.ingredients, new_ingredient])
            else:
                break

        self.image = res.json()['drinks'][0]['strDrinkThumb']
        self.name = res.json()['drinks'][0]['strDrink']
        self.alcoholic = res.json()['drinks'][0]['strAlcoholic']
        self.instructions = res.json()['drinks'][0]['strInstructions']


def work_with_none_measure(measure):
    if not measure:
        return ""
    else:
        return measure
