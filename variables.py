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
        'Asparagus',
        'Aubergine',
        'Broccoli',
        'Butternut Squash',
        'Carrots',
        'Celery',
        'Cherry Tomatoes',
        'Chestnuts',
        'Chilli Peppers',
        'Clementines',
        'Courgettes',
        'Garlic',
        'Green Beans',
        'Kale',
        'Leek',
        'Lemon',
        'Lime',
        'Mushrooms',
        'Onions (White)',
        'Onions (Red)',
        'Parsnips',
        'Pastry',
        'Peppers (Green)',
        'Peppers (Red)',
        'Pepper (Yellow)',
        'Potatoes (Baking)',
        'Potatoes (Maris Piper)',
        'Potatoes (New)',
        'Potatoes (Sweet)',
        'Spinach',
        'Spring Onions',
        'Swede',
        'Tomatoes',
        'Vegetarian Chorizo',
        'Vegetarian Sausages'
    ]
)

tinned_ingredients = sorted(
    [
        'Black Beans',
        'Black Eyed Beans',
        'Butter Beans',
        'Cannellini Beans',
        'Green Lentils',
        'Harissa Paste',
        'Kidney Beans',
        'Mixed Beans',
        'Pesto (Red)',
        'Pesto (Green)',
        'Plum Tomatoes',
        'Sun-dried Tomatoes',
        'Thai Red Curry Paste'
    ]
)

dry_ingredients = sorted(
    [
        'Bread',
        'Bread Rolls',
        'Coconut Flakes',
        'Coconut Sugar',
        'Cous Cous',
        'Dried Apricots',
        'Dried Cranberries',
        'Flour (Chickpea)',
        'Flour (Self-raising)',
        'Naan Bread',
        'Noodles',
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
        'Pitta Bread',
        'Red Lentils',
        'Rice (Arborio)',
        'Rice (Brown)',
        'Rice (Long Grain)',
        'Suet',
        'Tortilla Wraps'
    ]
)

dairy_ingredients = sorted(
    [
        'Cheese (Cheddar)',
        'Cheese (Mozzarella)',
        'Eggs',
        'Milk'
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
        'Crackers',
        'Flour (Pasta)',
        'Flour (Plain)',
        'Flour (Self-raising)',
        'Flour (Strong White Bread)',
        'Flour (Wholemeal Bread)',
        'Flour (Wholemeal)',
        'Frozen Peas',
        'Frozen Mixed Berries',
        'Frozen Blueberries',
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