def cakes(recipe, available):
    return min(available.get(ingredient, 0) // required for ingredient, required in recipe.items())


if __name__ == '__main__':
    recipe = {"flour": 500, "sugar": 200, "eggs": 1}
    available = {"flour": 1200, "sugar": 1200, "eggs": 5, "milk": 200}
    assert cakes(recipe, available) == 2, 'Wrong result for example #1'

    recipe = {"apples": 3, "flour": 300, "sugar": 150, "milk": 100, "oil": 100}
    available = {"sugar": 500, "flour": 2000, "milk": 2000}
    assert cakes(recipe, available) == 0, 'Wrong result for example #2'
