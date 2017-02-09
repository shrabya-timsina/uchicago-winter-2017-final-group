# cs122 project 
#
# Sandeep Malladi

import sys
import util
import crawler
import beer
import user


def get_user_from_url(url):
    '''
    given a url string that links to a user page, 
    collect relevant data, build & return user object
    '''
    request = crawler.get_request(url)
    soup = crawler.convert_to_soup(request)
    
    
    
    
def get_beer_from_url(url):
    '''
    given a url string that links to a beer page,
    collect relevant data, build & return beer object
    '''
    request = crawler.get_request(url)
    soup = crawler.convert_to_soup(request)

    
    
    
    
