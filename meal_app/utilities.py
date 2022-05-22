import json
import os
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