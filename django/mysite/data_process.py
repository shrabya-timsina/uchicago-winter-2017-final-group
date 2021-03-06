# cs122 project 
#
# Data Processing File

import sys
from crawler import get_compassionate_soup_from_url, user_dict_and_crawl_list
import pandas as pd
import json
import sqlite3 as sql
import data_analysis


#### temporary method to store and use user dictionaries ####
# get json file that has 100 user dictionaries branching from https://untappd.com/user/madwood1
# dict_list = crawler_copy.get_user_dicts_list('https://untappd.com/user/madwood1', 500)
# def read_json(json):
#     with open(json, 'r') as f:
#         dict_list = json.load(f)

    
def get_country_counts_df(dict_list):
    '''
    given a list of user dictionaries, get the counts for each country
    of origin per user and return information in a dataframe
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
    given a list of user dictionaries, get the counts for each style
    of beer per user and return information in a dataframe
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
    given a list of user dictionaries, get the counts for each brewery
    per user and return information in a dataframe
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
    given a list of user dictionaries, get the counts for each word used
    in beer descriptions per user and return information in a dataframe
    '''
    headers = ["username", "word", "count"]
    user_word_rows = []

    for user_dict in dict_list:
        username = user_dict["username"]
        all_words = [word for sublist in user_dict["beer words"] for word in sublist]
        unique_word_set = set(all_words)

        for word in unique_word_set:
            count = user_dict["beer words"].count(word)
            user_word_rows.append([username] + [word] + [count])
    
    word_counts_df = pd.DataFrame(user_word_rows, columns=headers)

    return word_counts_df


def user_beer_id_matrix(dict_list):
    '''
    create and return two dataframes: one that stores beer id, rating, and counts
    per beer per user, and another that stores pertinent information about each 
    beer, such as abv and style. beer ids are unique and generated by
    untappd
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
    '''
    given a list of user dictionaries, generate relevant dataframes using functions
    above and write them to teamcs122db.db database (appending to existing data)
    '''

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

    connect.close()   
    
    return None


def crawl_and_make_db(starting_url, max_links_num):
    '''
    from a starting user url, crawl untappd to get connected user profiles,
    process user profiles in fifo order, generate user dictionaries and store
    data in the teamcs122db database
    '''
    #keep track of profiles to visit
    need_process_links = []
    # keep track of visited profiles
    processed_links = []

    starting_soup = get_compassionate_soup_from_url(starting_url)
    if starting_soup is None:
        return None

    first_user_dict, users_to_crawl_list = user_dict_and_crawl_list(starting_url, starting_soup)
    if (first_user_dict == {}) or (users_to_crawl_list == []):
        return None

    dict_list_to_db([first_user_dict])
    
    for link in users_to_crawl_list:
            if link not in processed_links:
                need_process_links.append(link)
    # initialize counter
    i = 0

    while (i < max_links_num) and (need_process_links != []):
        current_link = need_process_links.pop()
        if current_link in processed_links:
            continue
        processed_links.append(current_link)
        current_soup = get_compassionate_soup_from_url(current_link)
        if current_soup is None:
            continue
        current_user_dict, current_user_link_branches = user_dict_and_crawl_list(current_link, current_soup)
        if (current_user_dict == {}) or (current_user_link_branches == []):
            continue
        else:
            dict_list_to_db([current_user_dict])
            i += 1
            need_process_links = need_process_links + current_user_link_branches 

    # because the data collection process only guarantees unique user profiles
    # within the max_links_num number of profiles scraped, generate a table of
    # unique users in the entire database
    build_unique_username_table('teamcs122db.db')

    return None


def build_vector_csvs(database, agg='style'):
    '''
    to make user profile vector analysis faster, store user vectors in
    a csv file
    '''
    data_analysis.create_agg_vectors(database, agg)
    #data_analysis.create_beer_vectors(database)

    return None


def build_unique_username_table(database):
    '''
    Build table with only unique usernames from beer_user_info table
    in database
    '''
    connect = sql.connect(database)
    cursor = connect.cursor()
    cursor.execute('DROP TABLE IF EXISTS unique_users;')
    cursor.execute('CREATE TABLE unique_users as SELECT DISTINCT username from beer_user_info')
    connect.close()
    return None


