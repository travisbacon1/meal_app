# class meals:
#     def __init__(self, name, staples, book='', page=float("NaN"), website='',ingredients):
#         self.name = name
#         self.staple = staple
#         self.book = book.name()
#         self.page = book.page()
#         self.website = website
#         self.ingredients = ingredients

# class book:
#     def __init__(self, name, page):
#         self.name = name
#         self.page = page

# class ingredients(meals):
#     def __init__(self, staple, ingredients):
#         super().__init__(staple, ingredients, fresh_ingredients, tinned_ingredients, dairy_ingredients, dry_ingredients)
#         self.fresh_ingredients = fresh_ingredients
#         self.tinned_ingredients = tinned_ingredients
#         self.dairy_ingredients = dairy_ingredients
#         self.dry_ingredients = dry_ingredients


# staples_list = meals('',sorted(['', 'Bread', 'Cous Cous', 'Pasta', 'Pastry', 'Potato', 'Rice']),'')

def variable_printer(variable_name, variable):
    """Prints the name, type and contents of a variable to aid debugging
    
    Parameters
    -------
    variable_name: string\n
    variable: any

    Returns
    ------
    None
    """
    print(variable_name, "type:", type(variable), "content:")
    print(variable)

book_list = sorted(
    [
        '',
        'Bosh 1',
        'Bosh 2',
        'Jamie Oliver',
        "Nigel Slater AW",
        'Ultimate Pasta',
        'Riverford SS',
        'Riverford AW'
    ]
)

staples_list = sorted(
    [
        '',
        'Beans',
        'Bread',
        'Cereal',
        'Cous Cous',
        'Noodles',
        'Orzo',
        'Pasta',
        'Potato',
        'Rice',
        'Risotto'
    ]
)

fresh_ingredients = sorted(
    [
        ['Asparagus', 'spears'],
        ['Aubergine', ''],
        ['Broccoli', ''],
        ['Butternut Squash', ''],
        ['Carrots', ''],
        ['Celery', ''],
        ['Cherry Tomatoes', 'g'],
        ['Chestnuts', 'g'],
        ['Chilli Peppers', ''],
        ['Clementines', ''],
        ['Courgettes', ''],
        ['Garlic', 'cloves'],
        ['Green Beans', 'g'],
        ['Kale', 'g'],
        ['Leek', ''],
        ['Lemon', ''],
        ['Lime', ''],
        ['Mushrooms', 'g'],
        ['Onions (White)', ''],
        ['Onions (Red)', ''],
        ['Parsnips', ''],
        ['Pastry', 'sheets'],
        ['Peppers (Green)', ''],
        ['Peppers (Red)', ''],
        ['Pepper (Yellow)', ''],
        ['Potatoes (Baking)', ''],
        ['Potatoes (Maris Piper)', 'g'],
        ['Potatoes (New)', 'g'],
        ['Potatoes (Sweet)', ''],
        ['Spinach', 'balls'],
        ['Spring Onions', ''],
        ['Swede', 'g'],
        ['Tomatoes', ''],
        ['Vegetarian Mozzarella Burgers', ''],
        ['Vegetarian Chorizo', ''],
        ['Vegetarian Sausages', '']
    ]
)

tinned_ingredients = sorted(
    [
        ['Baked Beans', 'tins'],
        ['Black Beans', 'tins'],
        ['Black Eyed Beans', 'tins'],
        ['Butter Beans', 'tins'],
        ['Cannellini Beans', 'tins'],
        ['Green Lentils', 'tins'],
        ['Harissa Paste', 'jars'],
        ['Kidney Beans', 'tins'],
        ['Mixed Beans', 'tins'],
        ['Pesto (Red)', 'jars'],
        ['Pesto (Green)', 'jars'],
        ['Plum Tomatoes', 'tins'],
        ['Sun-dried Tomatoes', 'jars'],
        ['Thai Red Curry Paste', 'g']
    ]
)

dry_ingredients = sorted(
    [
        ['Bread', 'slices'],
        ['Bread Rolls', ''],
        ['Coconut Flakes', 'g'],
        ['Coconut Sugar', 'g'],
        ['Cous Cous', 'g'],
        ['Dried Apricots', 'g'],
        ['Dried Cranberries', 'g'],
        ['Flour (Chickpea)', 'g'],
        ['Flour (Self-raising)', 'g'],
        ['Naan Bread', ''],
        ['Noodles', 'nests'],
        ['Nuts (Brazil)', 'g'],
        ['Nuts (Hazelnuts)', 'g'],
        ['Nuts (Pecans)', 'g'],
        ['Nuts (Flaked Almonds)', 'g'],
        ['Nuts (Walnuts)', 'g'],
        ['Nuts (Whole Almonds)', 'g'],
        ['Oats', 'g'],
        ['Orzo', 'g'],
        ['Panko Breadcrumbs', 'g'],
        ['Pasta (Lasagne)', 'sheets'],
        ['Pasta (Penne)', 'g'],
        ['Pasta (Spaghetti)', 'g'],
        ['Pitta Bread', ''],
        ['Red Lentils', 'g'],
        ['Rice (Arborio)', 'g'],
        ['Rice (Brown)', 'g'],
        ['Rice (Long Grain)', 'g'],
        ['Suet', 'g'],
        ['Tortilla Wraps', ''],
    ]
)

dairy_ingredients = sorted(
    [
        ['Cheese (Cheddar)', 'g'],
        ['Cheese (Mozzarella)', 'g'],
        ['Eggs', ''],
        ['Milk', 'ml']
    ]
)

extras = sorted(
    [
        'Apple Cider Vinegar',
        'Apples',
        'Balsamic Vinegar',
        'Baked Beans',
        'Bananas',
        'Breadsticks',
        'Butter',
        'Cheese (Parmesan)',
        'Chocolate',
        'Clementines',
        'Coconut Oil',
        'Coffee Beans',
        'Cornflakes',
        'Crackers (Cream)',
        'Crackers (Flatbreads)',
        'Crackers (Multi-grain)',
        'Crackers (Poppy Seed)',
        'Crackers (Rosemary)',
        'Flour (Pasta)',
        'Flour (Plain)',
        'Flour (Self-raising)',
        'Flour (Strong White Bread)',
        'Flour (Wholemeal Bread)',
        'Flour (Wholemeal)',
        'Frozen Peas',
        'Frozen Blueberries',
        'Frozen Raspberries',
        'Frozen Strawberries',
        'Golden Syrup',
        'Grapes',
        'Gravy Granules',
        'Herbs & Spices',
        'Hoisin Sauce',
        'Ice Cream',
        'Mackerel',
        'Maple Syrup',
        'Marmite',
        'Mustard (English)',
        'Mustard (Wholegrain)',
        'Nairns',
        'Nutritional Yeast',
        'Nuts (Peanuts)',
        'Nuts (Pistachios)',
        'Nuts (Cashews)',
        'Nuts (Whole Almonds)',
        'Nuts (Flaked Almonds)',
        'Olive Oil',
        'Sesame Oil',
        'Stuffing',
        'Sunflower Oil',
        'Soy Sauce',
        'Sultanas',
        'Tea Bags',
        'Tomato Purèe',
        'Vegetable Stock'
    ]
)

gram_list = sorted(
    [
        'Cheese (Cheddar)',
        'Cheese (Mozzarella)',
        'Cherry Tomatoes',
        'Chestnuts',
        'Coconut Flakes',
        'Coconut Sugar',
        'Cous Cous',
        'Dried Apricots',
        'Dried Cranberries',
        'Flour (Chickpea)',
        'Flour (Self-raising)',
        'Green Beans',
        'Kale',
        'Mushrooms',
        'Nuts (Brazil)',
        'Nuts (Hazelnuts)',
        'Nuts (Pecans)',
        'Nuts (Flaked Almonds)',
        'Nuts (Walnuts)',
        'Nuts (Whole Almonds)',
        'Oats',
        'Orzo',
        'Panko Breadcrumbs',
        'Pasta (Lasagne)',
        'Pasta (Penne)',
        'Pasta (Spaghetti)',
        'Potatoes (Maris Piper)',
        'Potatoes (New)',
        'Red Lentils',
        'Rice (Arborio)',
        'Rice (Brown)',
        'Rice (Long Grain)',
        'Swede',
        'Suet',
        'Sun-dried Tomatoes'
    ]
)