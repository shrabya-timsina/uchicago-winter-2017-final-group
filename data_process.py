# cs122 project 
#
# Data Processing File

import sys
import crawler
import pandas as pd
import json
import sqlite3 as sql

#temp_dict_list = crawler.get_user_dicts_list('https://untappd.com/user/madwood1', 5)

# get json file that has 100 user dictionaries branching from https://untappd.com/user/madwood1
json_dict_file = open('beer_dict.json')
json_file_str = json_dict_file.read()
json_dict_list = json.loads(json_file_str)


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


def gen_countries_list(dict_list):
    '''
    '''
    country_list = []
    for user_dict in dict_list:
    	countries = user_dict["countries"].keys()
    	for country in countries:
    		if country not in country_list:
    			country_list.append(country)

    return country_list


def get_country_counts_df(dict_list):
    '''
    '''
    country_list = gen_countries_list(dict_list)
    '''
    country_list = ['Bahamas', 'Dominican Republic', 'United States', 'Finland', 'Hong Kong', 'Ireland', 'Kenya',
                    'Norway', 'Canada', 'Switzerland', 'Brazil', 'Belgium', 'Sri Lanka', 'Portugal', 'France', 'Jamaica',
                    'Trinidad and Tobago', 'Peru', 'New Zealand', 'Italy', 'Netherlands', 'Luxembourg', 'Austria', 'Poland',
                    'Channel Islands', "China / People's Republic of China", 'United States', 'Virgin Islands', 'Iceland', 'England',
                    'Australia', 'Sweden', 'Denmark', 'Thailand', 'Wales', 'Cyprus', 'Japan', 'Germany', 'Vietnam', 'Scotland',
                    'Mexico', 'Spain', 'Czech Republic']
    '''
    headers = ["username"] + country_list
    user_rows = []

    for user_dict in dict_list:
    	username = user_dict["username"]
    	counts = [0] * len(country_list)
    	for country in country_list:
    		if country in user_dict["countries"].keys():
    			counts[country_list.index(country)] = user_dict["countries"][country]
    	user_rows.append([username] + counts)

    country_counts_df = pd.DataFrame(user_rows, columns=headers)

    return country_counts_df


def gen_style_list(dict_list):
    '''
    '''
    style_list = []
    for user_dict in dict_list:
    	styles = user_dict["styles"].keys()
    	for style in styles:
    		if style not in style_list:
    			style_list.append(style)

    return style_list


def get_style_counts_df(dict_list):
    '''
    '''
    styles_list = gen_style_list(dict_list)
    headers = ["username"] + styles_list
    user_rows = []

    for user_dict in dict_list:
    	username = user_dict["username"]
    	counts = [0] * len(styles_list)
    	for style in styles_list:
    		if style in user_dict["styles"].keys():
    			counts[styles_list.index(style)] = user_dict["styles"][style]
    	user_rows.append([username] + counts)

    #print(user_rows)
    style_counts_df = pd.DataFrame(user_rows, columns=headers)

    return style_counts_df


def gen_breweries_list(dict_list):
    '''
    '''
    brewery_list = []
    for user_dict in dict_list:
    	breweries = user_dict["breweries"].keys()
    	for brewery in breweries:
    		if brewery not in brewery_list:
    			brewery_list.append(brewery)

    return brewery_list


def get_brewery_counts_df(dict_list):
    '''
    '''
    breweries_list = gen_breweries_list(dict_list)
    headers = ["username"] + breweries_list
    user_rows = []

    for user_dict in dict_list:
    	username = user_dict["username"]
    	counts = [0] * len(breweries_list)
    	for brewery in breweries_list:
    		if brewery in user_dict["breweries"].keys():
    			counts[breweries_list.index(brewery)] = user_dict["breweries"][brewery]
    	user_rows.append([username] + counts)

    brewery_counts_df = pd.DataFrame(user_rows, columns=headers)

    return brewery_counts_df


def gen_words_list(dict_list):
    '''
    '''
    word_list = []
    for user_dict in dict_list:
    	words = user_dict["beer words"]
    	for word in words:
    		if word not in word_list:
    			word_list.append(word)

    return word_list


def get_word_counts_df(dict_list):
    '''
    '''
    words_list = gen_words_list(dict_list)
    headers = ["username"] + words_list
    user_rows = []

    for user_dict in dict_list:
    	username = user_dict["username"]
    	counts = [0] * len(words_list)
    	for word in words_list:
    		if word in user_dict["beer words"]:
    			counts[words_list.index(word)] = user_dict["beer words"].count(word)
    	user_rows.append([username] + counts)

    word_counts_df = pd.DataFrame(user_rows, columns=headers)

    return word_counts_df


def user_beer_id_matrix(dict_list):
    '''
    '''
    # For User-Beer Cross Matrix
    user_matrix = []
    user_headers = ["user_beer_key", "username", "beer_id", "rating", "count"]
    # For General Beer Matrix
    beer_matrix = []
    beer_headers = ["beer_id", "abv", "style", "brewery"]
 
    for user_dict in dict_list:
        for beer in user_dict["beers"].keys():
            concat_user_beer = str(user_dict["username"]) + "|" + str(user_dict["beers"][beer]["beer id"])
            username = user_dict["username"]
            beer_id = user_dict["beers"][beer]["beer id"]
            rating = user_dict["beers"][beer]["beer rating"]
            count = user_dict["beers"][beer]["count"]
            user_row = [concat_user_beer, username, beer_id, rating, count] 
            user_matrix.append(user_row)
            
            if not user_dict["beers"][beer]["abv"]:
                abv = 0
            else:
                abv = user_dict["beers"][beer]["abv"]
            style = user_dict["beers"][beer]["beer style"]
            brewery = user_dict["beers"][beer]["brewery name"]
            beer_row = [beer_id, abv, style, brewery]
            if beer_row not in beer_matrix:
                beer_matrix.append(beer_row)
   
    user_matrix_df = pd.DataFrame(user_matrix, columns=user_headers)
    beer_matrix_df = pd.DataFrame(beer_matrix, columns=beer_headers)

    return user_matrix_df, beer_matrix_df


def dict_list_to_db(dict_list):
    '''
    '''
    total_df = get_total_df(dict_list)
    total_df["styles"] = total_df["styles"].astype('str')
    total_df["breweries"] = total_df["breweries"].astype('str')
    total_df["brewery counts"] = total_df["brewery counts"].astype('str')
    total_df["beers"] = total_df["beers"].astype('str')
    total_df["countries"] = total_df["countries"].astype('str')
    total_df["country counts"] = total_df["country counts"].astype('str')
    total_df["beer words"] = total_df["beer words"].astype('str') 

    brewery_counts_df = get_brewery_counts_df(dict_list)
    print(brewery_counts_df.head())
    style_counts_df = get_style_counts_df(dict_list)
    #print(style_counts_df.head())
    country_counts_df = get_country_counts_df(dict_list)
    #print(country_counts_df.head())
    word_counts_df = get_word_counts_df(dict_list)
    user_matrix_df, beer_matrix_df = user_beer_id_matrix(dict_list)
    
    
    # write everything to own csv
    total_df.to_csv('total.csv')
    brewery_counts_df.to_csv('brewery_counts.csv')
    style_counts_df.to_csv('style_counts.csv')
    country_counts_df.to_csv('country_counts.csv')
    word_counts_df.to_csv('word_counts.csv')
    user_matrix_df.to_csv('user_beer_info.csv')
    beer_matrix_df.to_csv('general_beer_info.csv')

    
    # write to sql database
    connect = sql.connect('teamcs122db.db')
    total_df.to_sql("all_info", connect, if_exists='replace')
    
    # Dataframes need to be rewritten - cannot have thousands of columns
    '''
    brewery_counts_df.to_sql("brewery_counts", connect, if_exists='replace')
    style_counts_df.to_sql("style_counts", connect, if_exists='replace')
    country_counts_df.to_sql("country_counts", connect, if_exists='replace')
    word_counts_df.to_sql("word_counts", connect, if_exists='replace')
    user_matrix_df.to_sql("beer_user_info", connect, if_exists='replace')
    beer_matrix_df.to_sql("beer_general_info", connect, if_exists='replace')
    '''
    
    return None
