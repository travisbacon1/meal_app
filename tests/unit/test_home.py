
def test_homepage_buttons_example(client, session):
    print("Running test 1")
    response = client.get("/")
    buttons = [
        "Add Ingredient",
        "Add Meal",
        "Edit Meal",
        "Get Meal Info",
        "Search Ingredients",
        "List Meals",
        "Create Meal Plan",
        "Load Meal Plan",
        "Delete Meal Plan"
    ]
    for button in buttons:
        assert bytes(f'<input class="homepagebutton" id="{button}" name="submit" type="submit" value="{button}">', 'utf-8') in response.data
