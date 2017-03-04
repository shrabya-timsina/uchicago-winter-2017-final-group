# cs122 project 
#
# analyze user data to get suggestions

import sys
import crawler
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np
import sqlite3 as sql
import pandas as pd
import data_process as dProc

# SQLite3
DB_FILENAME = 'teamcs122db.db'

def vectorize_sql_profile(user_url):

    connect = sql.connect(DB_FILENAME)
    user_vectors = pd.read_sql('SELECT DISTINCT username from beer_user_info', connect)
    usernames = user_vectors
    for index, row in usernames.iterrows():
        username = row['username']
        beers = pd.read_sql('SELECT beer_id, rating, count from beer_user_info where username like ' + '\'' + str(username) + '\'', connect)
        total_count = beers['count'].values.sum()
        for sub_index, sub_row in beers.iterrows():
            beer = int(sub_row['beer_id'])
            rating = float(sub_row['rating']) / 5
            rel_freq = float(sub_row['count']) / total_count
            if beer not in list(user_vectors.columns.values):
                user_vectors[int(beer)] = 0
                user_vectors.ix[index, beer] = float(rating * rel_freq)
            else:
                user_vectors.ix[index, beer] = float(rating * rel_freq)

    user_vectors.set_index('username', drop=True, inplace=True)
    test_dict = crawler.profile_scraper(user_url)
    username = test_dict['username']
    test_vector = pd.DataFrame(columns=list(user_vectors.columns.values), index=[0])
    test_vector.fillna(0, inplace=True)
    total_count = 0
    
    for beer in test_dict['beers'].keys():
        beer_id = int(test_dict['beers'][beer]['beer id'])
        count = int(test_dict['beers'][beer]['count'])
        rating = float(test_dict['beers'][beer]['beer rating'])
        total_count += count
        if beer_id not in list(user_vectors.columns.values):
            user_vectors[beer_id] = 0
            test_vector[beer_id] = float(count * rating / 5) 
        else: 
            test_vector[beer_id] = float(count * rating)
    
    test_vector = test_vector.divide(total_count, axis='index')
    n = len(user_vectors)
    distance_matrix = np.zeros((n, 1))
    
    test_matrix = test_vector.as_matrix()
    user_matrix = user_vectors.as_matrix()
    i = 0
    for row in user_matrix:
        distance_matrix[i,0] = cosine_similarity(test_matrix, row)
        i += 1
    distance_df = pd.DataFrame(distance_matrix, index=user_vectors.index.tolist(), columns=['score']).sort(columns='score', ascending=False)
    print(distance_df)

    connect.close()









