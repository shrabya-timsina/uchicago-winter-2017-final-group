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


def gather_usernames(connection):
    '''
    Gathers unique usernames in database.
    Returns two dataframes.
    '''
    user_vectors = pd.read_sql('SELECT username from unique_users', 
                               connection)
    usernames = user_vectors.copy()
    return user_vectors, usernames

def create_agg_vectors(database, agg):
    '''
    Creates the vectors for each user in the database based on the unique 
    styles present in the databased for all users. Each coordinate corresponds
    to a unique beer style and the positional value is weighted based on the 
    relative frequency of the style. 
    Returns dataframe of user vectors.
    '''
    connect = sql.connect(database)
    user_vectors, usernames = gather_usernames(connect)
    table = str(agg) + '_counts'
    for index, row in usernames.iterrows():
        username = row['username']
        agg_df = pd.read_sql('SELECT username,' + str(agg) + ', count FROM ' + str(table) + ' where username like ' + '\'' + str(username) + '\'',
                             connect)
        total_count = agg_df['count'].values.sum()
        for sub_index, sub_row in agg_df.iterrows():
            agg_value = sub_row[agg]
            rel_freq = float(sub_row['count']) / total_count
            if agg_value not in list(user_vectors.columns.values):
                user_vectors[agg_value] = 0
                user_vectors.ix[index, agg_value] = float(rel_freq)
            else:
                user_vectors.ix[index, agg_value] = float(rel_freq)
    
    connect.close()
    user_vectors.set_index('username', drop=True, inplace=True)
    return user_vectors    


def create_beer_vectors(database):
    '''
    Creates the vectors for each user in the database based on the unique 
    beers present in the databased for all users. Each coordinate corresponds
    to a unique beer and the positional value is weighted based on the 
    relative frequency of the beer times the rating. 
    Returns dataframe of user vectors.
    '''
    connect = sql.connect(database)
    user_vectors, usernames = gather_usernames(connect)

    for index, row in usernames.iterrows():
        username = row['username']
        beers = pd.read_sql('SELECT beer_id, rating, count from beer_user_info where username like ' + '\'' + str(username) + '\'',
                            connect)
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

    connect.close()
    user_vectors.set_index('username', drop=True, inplace=True)
    return user_vectors


def prepare_testvector(username, columns):
    '''
    Prepares an empty input user vector to be filled.
    Returns test vector and user dictionary. 
    '''
    user_url = 'https://untappd.com/user/' + str(username)
    test_dict = crawler.profile_scraper(user_url)
    username = test_dict['username']
    test_vector = pd.DataFrame(columns=columns, index=[username])
    test_vector.fillna(0, inplace=True)
    return test_vector, test_dict
    

def calc_cos_simil(test_vector, user_vectors):
    '''
    Calculates the pairwise cosine similarity scores for 1 user vector against 
    n user vectors. 
    '''
    i = 0
    n = len(user_vectors)
    
    distance_matrix = np.zeros((n, 1))
    test_matrix = test_vector.as_matrix()
    user_matrix = user_vectors.as_matrix()
    
    for row in user_matrix:
        distance_matrix[i,0] = cosine_similarity(test_matrix, row)
        i += 1

    distance_df = pd.DataFrame(distance_matrix, index=user_vectors.index.tolist(), columns=['score']).sort(columns='score', ascending=False)
    return distance_df



def topk_profiles_agg(username, topk, agg):
    '''
    Creates an input user aggregate statistic vector. Calculates the 
    cosine similarity scores against all users in the database. 
    Ranks users based on cosine similarity scores and returns 
    an ordered dataframe of usernames and associated cosine similarities.
    '''
    user_vectors = create_agg_vectors(DB_FILENAME, agg)
    columns = list(user_vectors.columns.values)
    test_vector, test_dict = prepare_testvector(username, columns)
    total_count = 0

    if agg == 'style':
        dict_key = 'styles'
    else: 
        dict_key = 'breweries'
    
    for agg in test_dict[dict_key].keys():
        count = int(test_dict[dict_key][agg])
        total_count += count
        if agg not in list(user_vectors.columns.values):
            user_vectors[agg] = 0
            test_vector[agg] = float(count) 
        else: 
            test_vector[agg] = float(count)

    test_vector = test_vector.divide(total_count, axis='index')
    distance_df = calc_cos_simil(test_vector, user_vectors)
    
    if str(username) in distance_df.index.values:
        distance_df.drop(str(username), inplace=True)

    return distance_df.head(topk)

    

def topk_profiles_beers(username, topk):
    '''
    Creates an input user beer vector. Calculates the cosine similarity
    scores against all users in the database. Ranks users based on cosine 
    similarity scores and returns an ordered dataframe of usernames 
    and associated cosine similarities.
    '''
    user_vectors = create_beer_vectors(DB_FILENAME)
    columns = list(user_vectors.columns.values)
    test_vector, test_dict = prepare_testvector(username, columns)
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
    distance_df = calc_cos_simil(test_vector, user_vectors)
    
    if str(username) in distance_df.index.values:
        distance_df.drop(str(username), inplace=True)

    return distance_df.head(topk)


#### suggestion/output functions ###


def get_suggestions_from_topk(username, k):
    '''
    topk df is a k row dataframe containing usernames and their corresponding 
    cosine distances to an initial input-user. This function queries the profiles
    database and returns beer ids corresponding to suggestions from top k profiles
    '''

    topk_df = topk_profiles_beers(username, k)

    usernames = topk_df.index.tolist()
    converted_users = ['\'' + str(user) + '\'' for user in usernames]

    connect = sql.connect(DB_FILENAME)
    beers_df = pd.read_sql("SELECT username, beer_id, rating, count FROM beer_user_info WHERE username IN (" + ",".join(converted_users) + ")", connect)
    connect.close()


    topk_beer_ids = []
    
    beers_df.sort(columns='rating', ascending=False, inplace=True, kind='quicksort')
    top_beers_df = beers_df[pd.to_numeric(beers_df['rating']) >= 3.5]

    beer_id_list = top_beers_df['beer_id'].tolist()

    print("asdf")

    top_k_beer_ids = list(set(beer_id_list))
    if 0 in top_k_beer_ids:
        top_k_beer_ids = top_k_beer_ids.remove(0)

    #get beer_ids of input user
    input_user_beer_ids = []
    user_url = 'https://untappd.com/user/' + str(username)
    input_user_dict = crawler.profile_scraper(user_url)
    for beer in input_user_dict["beers"].keys():
        #print(beer)
        input_user_beer_ids.append(input_user_dict["beers"][beer]["beer id"])
  
    #print(top_k_beer_ids)
    # remove overlapping beers
    for beer in top_k_beer_ids:
        if beer in input_user_beer_ids:
            top_k_beer_ids.remove(beer)

    #suggest at most 20 beers
    if len(top_k_beer_ids) < 20:
        return top_k_beer_ids
    else:
        return top_k_beer_ids[:20]
    




def get_beer_details(beer_id):
    '''
    Queries in SQL database with the given beer_id
    and stores beer information into a pandas dataframe
    '''
    connect = sql.connect(DB_FILENAME)
    suggested_beers = pd.read_sql('SELECT DISTINCT beer_id, name, abv, style, brewery from beer_general_info where beer_id =' + str(beer_id),
                            connect)
    connect.close()
    return suggested_beers