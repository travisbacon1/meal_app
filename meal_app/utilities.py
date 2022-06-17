from flask import render_template, request
import os
import json
import MySQLdb
import MySQLdb.cursors

def execute_mysql_query(query_string, fetch_results=True, commit=False):
    """Executes a MySQL query
    Parameters
    -------
    query_string: string\n

    Returns
    ------
    result: tuple
    """
    database = MySQLdb.connect(
        host=os.environ['MYSQL_HOSTNAME'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'],
        cursorclass=MySQLdb.cursors.DictCursor
    )
    db_cursor = database.cursor()
    db_cursor.execute(query_string)
    if fetch_results:
        results = db_cursor.fetchall()
        return results
    elif commit == True:
        db_cursor.connection.commit()


def parse_ingredients(ingredients_dict, filter_word, remove_prefix=False):
    """Parses an ingredients dictionary to create a new dictionary based on the filter_word as the key
    
    Parameters
    -------
    ingredients_dict: dict\n
    filter_word: string

    Returns
    ------
    parsed_ingredient_dict: dict
    """
    parsed_ingredient_dict = {}
    for key in list(ingredients_dict.keys()):
        if filter_word in key and ingredients_dict[key] != '':
            if remove_prefix == False:
                new_key = key.replace(filter_word, '')
            else:
                new_key = key.removeprefix(filter_word)
            parsed_ingredient_dict[new_key] = ingredients_dict[key]
    return json.dumps(parsed_ingredient_dict)


def get_tag_keys(tags):
    tag_list = []
    for tag_dict in tags:
        if list(tag_dict.values())[0] == 1:
            tag_list.append(list(tag_dict.keys())[0])
    return tag_list


def get_tags(tags):
    from .variables import tag_list
    parsed_tags = {}
    for tag in tag_list:
        if tag in tags:
            parsed_tags[tag.replace('/', '_')] = "1"
        else:
            parsed_tags[tag.replace('/', '_')] = "0"
    return parsed_tags


def append_current_ingredients(dict_1, dict_2):
    current_ingredients = list(dict_2.keys())
    for idx, ingredient_dict in enumerate(dict_1):
        try:
            current_ingredients.index(ingredient_dict['Ingredient'])
            dict_1[idx]['Quantity'] = (dict_2[ingredient_dict['Ingredient']])
        except ValueError:
            pass
    return dict_1


def meal_confirmation(meal):
    if request.method == "GET":
        query_string = f"""
                        SELECT
                            Name,
                            Staple,
                            Book,
                            Page,
                            Website,
                            Fresh_Ingredients,
                            Tinned_Ingredients,
                            Dry_Ingredients,
                            Dairy_Ingredients,
                            JSON_OBJECT(
                                'Spring_Summer', Spring_Summer,
                                'Autumn_Winter', Autumn_Winter,
                                'Quick_Easy', Quick_Easy,
                                'Special', Special)
                            AS Tags
                        FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name = '{meal}';"""
        result = execute_mysql_query(query_string)[0]
        location_details = {}
        if result['Website'] == None or result['Website'] == '':
            location_details['Book'] = result['Book']
            location_details['Page'] = result['Page']
        else:
            location_details['Website'] = result['Website']
        ingredients = []
        for ingredient_type in ["Fresh", "Dairy", "Dry", "Tinned"]:
            ingredients.extend(list(json.loads(result[f'{ingredient_type}_Ingredients']).keys()))
        ingredients = "'" + "', '".join(ingredients) + "'"
        query_string = f"""SELECT 
                            Type,
                            JSON_ARRAYAGG(JSON_OBJECT('Ingredient',
                                            Name,
                                            'Unit',
                                            Unit,
                                            'Quantity',
                                            '')) AS Ingredient_data
                        FROM
                            {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_INGREDIENTS_TABLE']}
                        WHERE Name in ({ingredients})
                        GROUP BY Type;
                        """
        all_ingredient_data = execute_mysql_query(query_string)
        current_ingredients = {}
        for ingredient_type in all_ingredient_data:
            current_ingredients[ingredient_type['Type']] = append_current_ingredients(json.loads(ingredient_type['Ingredient_data']), json.loads(result[f'{ingredient_type["Type"]}_Ingredients']))

        current_tags = [tag_key.replace("_","/") for (tag_key, tag_value) in json.loads(result['Tags']).items() if tag_value == 1]
        return render_template('meal_confirmation.html', meal_name=meal,
                                location_details=location_details, location_keys=location_details.keys(),
                                staple=result['Staple'],
                                current_ingredients=current_ingredients,
                                current_tags=current_tags)