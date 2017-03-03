# cs122 project 
#
# analyze user data to get suggestions

import sys
import crawler
import sklearn 
import numpy as np
import sqlite3 as sql
import pandas as pd
import data_process as dProc

# SQLite3
DB_FILENAME = 'teamcs122db.db'



def vectorize_sql_profile(userprofile):
    connect = sql.connect(DB_FILENAME)
    user_vectors = pd.read_sql('SELECT DISTINCT username from beer_user_info', connect)
    usernames = user_vectors
    for index, row in usernames.iterrows():
        username = row['username']
        beers = pd.read_sql('SELECT DISTINCT beer_id, avg(rating) as rating, count as count from beer_user_info where username like ' + '\'' + str(username) + '\'', connect)
        total_count = beers['count'].values.sum()
        for sub_index, sub_row in beers.iterrows():
            beer = sub_row['beer_id']
            rating = sub_row['rating'] / 5
            rel_freq = sub_row['count'] / total_count
            if beer not in list(user_vectors.columns.values):
                user_vectors[int(beer)] = 0
                user_vectors[beer].iloc[index] = rating * rel_freq
            else:
                user_vectors[beer].iloc[index] = rating * rel_freq

    (list(user_vectors.columns.values))

            
    connect.close()









