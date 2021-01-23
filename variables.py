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
        'Bread',
        'Cous Cous',
        'Pasta',
        'Pastry', 
        'Potato',
        'Rice'
    ]
)

fresh_ingredients = sorted(
    [
        'Aubergine',
        'Broccoli',
        'Butternut Squash',
        'Carrots',
        'Cherry Tomatoes',
        'Chilli Peppers',
        'Clementines',
        'Courgettes',
        'Garlic',
        'Kale',
        'Leek',
        'Lemon',
        'Lime',
        'Onions (White)',
        'Onions (Red)',
        'Peppers (Green)',
        'Peppers (Red)',
        'Pepper (Yellow)',
        'Potatoes (Baking)',
        'Potatoes (Marris Piper)',
        'Potatoes (New)',
        'Potatoes (Sweet)',
        'Spinach',
        'Spring Onions'
    ]
)

tinned_ingredients = sorted(
    [
        'Butter Beans',
        'Canneloni Beans',
        'Kidney Beans',
        'Mixed Beans',
        'Plum Tomatoes'
    ]
)

dry_ingredients = sorted(
    [
        'Cous Cous',
        'Naan Bread',
        'Orzo',
        'Pasta (Lasagne)',
        'Pasta (Penne)',
        'Pasta (Spaghetti)',
        'Rice (Arborio)',
        'Rice (Long Grain)'
    ]
)

dairy_ingredients = sorted(
    [
        'Cheese (Cheddar)',
        'Cheese (Mozzarella)',
        'Milk'

    ]
)