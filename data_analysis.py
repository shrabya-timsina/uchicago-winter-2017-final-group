# cs122 project 
#
# analyze user data to get suggestions

import sys
import crawler
import numpy as np
import sqlite3
import pandas as pd
import data_process as dProc

# SQLite3
DB_FILENAME = 'teamcs122db.db'


def get_top_user_characteristics(username):
    '''
    username - string
    k - integer
    '''
    user_link = 'https://untappd.com/user/' + username 
    user_dict, immediate_profiles_list = crawler.user_dict_and_crawl_list(user_link)
    
    # list of user profile links to username strings list
    immediate_usernames = [''.join(link[26:]) for link in immediate_profiles_list]
    
    # get user dfs to get summary statistics
    brewery_counts_df = dProc.get_brewery_counts_df([user_dict])
    style_counts_df = dProc.get_style_counts_df([user_dict])
    country_counts_df = dProc.get_country_counts_df([user_dict])
    word_counts_df = dProc.get_word_counts_df([user_dict])
    user_matrix_df, beer_matrix_df = dProc.user_beer_id_matrix([user_dict])
    
    # drop values with counts in the lowest quartile of counts
    user_brewery_df = brewery_counts_df.loc[brewery_counts_df["count"] > int(brewery_counts_df.describe().loc['25%'].values)]
    user_style_df = style_counts_df.loc[style_counts_df["count"] > int(style_counts_df.describe().loc['25%'].values)]
    user_country_df = country_counts_df.loc[country_counts_df["count"] > int(country_counts_df.describe().loc['25%'].values)]
    user_words_df = word_counts_df.loc[word_counts_df["count"] > int(word_counts_df.describe().loc['25%'].values)]
    max_beer_count = int(user_matrix_df["count"].describe().loc['max'])
    if max_beer_count < 5:
    	user_beer_df = user_matrix_df
    else:
        user_beer_df = user_matrix_df.loc[user_matrix_df["count"] > int(user_matrix_df["count"].describe().loc['25%'])]
    
    # get weighted average preferred abv for user
    user_total_beer_count = pd.to_numeric(user_beer_df["count"]).sum()
    user_weighted_abv = 0
    for index, row in user_beer_df.iterrows():
    	beer_weight = int(row["count"])/ (user_total_beer_count * 1.0)
    	beer_id = row["beer_id"]
    	abv = float(beer_matrix_df.loc[beer_matrix_df["beer_id"] == int(beer_id)]["abv"].values)
    	user_weighted_abv += (beer_weight * abv)
    	extra = (beer_weight * abv)
    	
    # find beers with abv less than a standard deviation below user_weighted_abv
    beer_ids = []
    for index, row in beer_matrix_df.iterrows():
    	abv = row["abv"]
    	if abv >= user_weighted_abv:
    		beer_ids.append(row["beer_id"])

    user_beer_df = user_beer_df.loc[user_beer_df["beer_id"].isin(beer_ids)]

    # get highest preference beer styles by weight
    #user_style_df = user_style_df.loc[user_style_df['username'] == username]
    user_total_style_count = pd.to_numeric(user_style_df["count"]).sum()
    relevant_styles = []
    for index, row in user_style_df.iterrows():
    	style_weight = int(row["count"])/user_total_style_count
    	if style_weight > 0.05:
    		relevant_styles.append(row["style"])

    # narrow df to get list of beers well rated by user (i.e. rating above 3 stars)
    user_beer_df = user_beer_df.loc[pd.to_numeric(user_beer_df["rating"]) >= 3.0]

    # return user dataframe, and list of relevant beers/styles/etc. *** NEED TO UPDATE ***

    return user_beer_df, relevant_styles