import json
from . import mysql

def execute_mysql_query(query_string):
    """Executes a MySQL query

    Parameters
    ----------
    query_string : str
        MySQL query to execute

    Returns
    -------
    tuple
        MySQL query results
    """
    db_cursor = mysql.connection.cursor()
    db_cursor.execute(query_string)
    results = db_cursor.fetchall()
    return results


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
    from .variables import tag_list, tag_list_backend
    parsed_tags = {}
    for tag in tag_list:
        if tag in tags:
            parsed_tags[tag.replace('/', '_')] = "1"
        else:
            parsed_tags[tag.replace('/', '_')] = "0"
    return parsed_tags