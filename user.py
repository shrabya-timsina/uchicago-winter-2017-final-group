# user object for cs122 project
#
# Sandeep Malladi

import sys
import util
import beer.py as beer


class user(object):
    '''
    username - string
    beer dict - dictionary of beers with hash as key, attributes as values
    venues_dict - dictionary of venues visited with key as venue name string
        and value as url
    '''
    def _init_(self, username, beer_dict, venues_dict):
        self.username = None
        self.beer_dict = {}
        self.venues_dict = {}
        # self.props = None

    @property
    def username(self):
        return self.username

    @property
    def beer_dict(self):
        return self.beer_dict

    @property
    def venues_dict(self):
        return self.venues_dict

    '''
    @property
    def props(self):
        return self.props
    '''
    
    @username.setter
    def username(self, name):
        self.username = name

    @beer_dict.setter
    def beer_dict(self, b_dict):
        self.beer_dict = b_dict

    @venues_dict.setter
    def venues_dict(self, v_dict):
        self.venues_dict = v_dict

    
    
    
    
    
    
