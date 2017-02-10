# beer object for cs122 project
#
# Sandeep Malladi

import sys

class beer(object):
    def _init_(self, name, abv, brewery, style, avg_rating):
        '''
        name - string
        abv - decimal
        brewery - string
        style - string
        avg_rating - two decimal places num between 0 and 5
        '''
        self.name = None
        self.abv = 0
        self.brewery = None
        self.style = None
        self.avg_rating = 0
    
    @property
    def name(self):
        return self.name

    @property
    def avg_rating(self):
        return self.avg_rating
    
    @property
    def abv(self):
        return self.abv

    @property
    def style(self):
        return self.style

    @property
    def brewery(self):
        return self.brewery

    @name.setter
    def name(self, name_str):
        self.name = name_str
    
    @avg_rating.setter
    def avg_rating(self, rating):
        self.avg_rating = rating
    
    @abv.setter
    def abv(self, pct_abv):
        self.abv = pct_abv

    @style.setter
    def style(self, style_name):
        self.style = style_name

    @brewery.setter
    def brewery(self, brewery_name):
        self.brewery = brewery_name

    # make class hashable - using http://stackoverflow.com
    # /questions/12512511/automatically-making-a-class-hashable
    
    def __key(self):
        return (self.name, self.abv, self.style, self.avg_rating, self.brewery)

    def __eq__(x, y):
        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())







