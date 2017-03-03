# cs122 project 
#
# Data Processing File

import sys
import crawler
import pandas as pd
import json
import sqlite3 as sql



# get json file that has 100 user dictionaries branching from https://untappd.com/user/madwood1
#json_dict_file = open('result.json')
#json_file_str = json_dict_file.read()
#son_dict_list = json.loads(json_file_str)


def get_total_df(dict_list):
    '''
    '''
    user_rows = []

    for user_dict in dict_list:
        username = user_dict["username"]
        styles = list(user_dict["styles"].keys())
        breweries = list(user_dict["breweries"].keys())
        brewery_counts = list(user_dict["breweries"].values())
        beers = user_dict["beers"].keys()
        countries = user_dict["countries"].keys()
        country_counts = user_dict["countries"].values()
        beer_words = user_dict["beer words"]

        user_rows.append([username, styles, breweries, brewery_counts, beers, countries, country_counts, beer_words])

    headers = ["username", "styles", "breweries", "brewery counts", "beers", "countries", "country counts", "beer words"]
    df = pd.DataFrame(user_rows, columns=headers)

    return df

    
def get_country_counts_df(dict_list):
    '''
    '''
    headers = ["username", "country", "count"]
    user_country_rows = []

    for user_dict in dict_list:
        username = user_dict["username"]

        for country, count in user_dict["countries"].items():
           user_country_rows.append([username] + [country] + [int(count)])

    country_counts_df = pd.DataFrame(user_country_rows, columns=headers)

    return country_counts_df


def get_style_counts_df(dict_list):
    '''
    '''
    headers = ["username", "style", "count"]
    user_style_rows = []

    for user_dict in dict_list:
        username = user_dict["username"]

        for style, count in user_dict["styles"].items():
            user_style_rows.append([username] + [style] + [int(count)])
        
    style_counts_df = pd.DataFrame(user_style_rows, columns=headers)

    return style_counts_df


def get_brewery_counts_df(dict_list):
    '''
    '''
    headers = ["username", "brewery", "count"]
    user_brewery_rows = []

    for user_dict in dict_list:
        username = user_dict["username"]

        for brewery, count in user_dict["breweries"].items():
            user_brewery_rows.append([username] + [brewery] + [int(count)])
        
    brewery_counts_df = pd.DataFrame(user_brewery_rows, columns=headers)

    return brewery_counts_df


def get_word_counts_df(dict_list):
    '''
    '''
    headers = ["username", "word", "count"]
    user_word_rows = []

    for user_dict in dict_list:
        username = user_dict["username"]
        unique_word_set = set(user_dict["beer words"])

        for word in unique_word_set:

            count = user_dict["beer words"].count(word)
            user_word_rows.append([username] + [word] + [count])
    
    # word_counts_df = pd.DataFrame(user_rows, columns=headers)
    word_counts_df = pd.DataFrame(user_word_rows, columns=headers)

    return word_counts_df


def user_beer_id_matrix(dict_list):
    '''
    '''
    # For User-Beer Cross Matrix
    user_matrix = []
    user_headers = ["user_beer_key", "username", "beer_id", "rating", "count"]
    # For General Beer Matrix
    beer_matrix = []
    beer_headers = ["beer_id", "name", "abv", "style", "brewery"]
 
    for user_dict in dict_list:
        for beername, beer_dict in user_dict["beers"].items():
            
            concat_user_beer = str(user_dict["username"]) + "|" + str(beer_dict["beer id"])
            username = user_dict["username"]
            beer_id = int(beer_dict["beer id"])
            rating = beer_dict["beer rating"]
            count = int(beer_dict["count"])
            user_row = [concat_user_beer, username, beer_id, rating, count] 
            user_matrix.append(user_row)
            
            if not beer_dict["abv"]:
                abv = 0
            else:
                abv = beer_dict["abv"]
            style = beer_dict["beer style"]
            brewery = beer_dict["brewery name"]
            beer_row = [beer_id, beername, abv, style, brewery]
            if beer_row not in beer_matrix:
                beer_matrix.append(beer_row)
   
    user_matrix_df = pd.DataFrame(user_matrix, columns=user_headers)
    beer_matrix_df = pd.DataFrame(beer_matrix, columns=beer_headers)

    return user_matrix_df, beer_matrix_df


def dict_list_to_db(dict_list):
    
    
    total_df = get_total_df(dict_list)

    brewery_counts_df = get_brewery_counts_df(dict_list)
    style_counts_df = get_style_counts_df(dict_list)
    country_counts_df = get_country_counts_df(dict_list)
    word_counts_df = get_word_counts_df(dict_list)
    user_matrix_df, beer_matrix_df = user_beer_id_matrix(dict_list)
    
    # write to sql database
    connect = sql.connect('teamcs122db.db')
    
    brewery_counts_df.to_sql("brewery_counts", connect, if_exists='append')
    style_counts_df.to_sql("style_counts", connect, if_exists='append')
    country_counts_df.to_sql("country_counts", connect, if_exists='append')
    word_counts_df.to_sql("word_counts", connect, if_exists='append')
    user_matrix_df.to_sql("beer_user_info", connect, if_exists='append')
    beer_matrix_df.to_sql("beer_general_info", connect, if_exists='append')
    
    
    return None



#dict_list = crawler.get_user_dicts_list('https://untappd.com/user/madwood1', 500)
