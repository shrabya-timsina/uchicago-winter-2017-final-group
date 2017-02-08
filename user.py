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
    props - some other properties 
    '''
    def _init_(self, username, beer_dict, props):
        self.username = None
        self.beer_dict = {}
        self.props = None

    @property
    def username(self):
        return self.username

    @property
    def beer_dict(self):
        return self.beer_dict

    @property
    def props(self):
        return self.props

    @username.setter
    def username(self, name):
        self.username = name

    @beer_dict.setter
    def beer_dict(self, b_dict):
        self.beer_dict = b_dict

    
    
    
    
    
    
    
