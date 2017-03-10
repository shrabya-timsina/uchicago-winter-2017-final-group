from django.shortcuts import render
#superuse admin username: cs122
#password: cs-project
# Create your views here.
from django.http import HttpResponse
from django import forms
import pandas as pd
import bs4
import unicodedata
from data_analysis_copy import get_suggestions_from_topk
import crawler_copy #for beautiful soup request processing
import string


COLUMN_NAMES = dict(
        beer_id='Beer ID',
        beer_name='Name',
        brewery='Brewery',
        style='Style',
        country='Country',
        ABV='ABV',
        ratings='Ratings',
)


def index(request):
    context = {}
    if request.method == 'GET':
        form = Input_form(request.GET)
        if form.is_valid():
            context['valid_form'] = True
            if form.cleaned_data['username']:
                beer_suggestions_df = get_suggestions_from_topk(form.cleaned_data['username'], 5)
                ##### FIX THIS HARDCODE - CHECK IF USERNAME IN DATABASE #####
                if form.cleaned_data['username']=="waddup": beer_suggestions_df = None
            else:
               beer_suggestions_df = None 
        else:
            beer_suggestions_df = None 
            context['valid_form'] = False 
    
    else:
        form = Input_form()
    
    if beer_suggestions_df is None:
        context['valid_username'] = False    
    else:
        image_column = []
        for i, beer in beer_suggestions_df.iterrows():
            name_url_section = get_url_section(beer['name'])          
            brewery_url_section = get_url_section(beer['brewery']) 
            url = "https://untappd.com/b/" +  brewery_url_section + "-" + name_url_section + "/" + str(beer['beer_id'])
            #print("$$$$$$$$$ $$$$$$$$$$     ", url)
            bs4_request = crawler_copy.get_request(url)
            soup = crawler_copy.convert_to_soup(bs4_request)
            if not soup:
               image_link = "default"
            else:
                tag_list = soup.find("div", "basic")
                image_link = tag_list.find("img")["src"]

            image_column.append(image_link)
        beer_suggestions_df["Image"] = image_column
        
        context['valid_username'] = True
        context['column_names'] = list(beer_suggestions_df.columns)
        context['beers'] = beer_suggestions_df.values.tolist()
        context['num_results'] = len(beer_suggestions_df.values.tolist())
        
    context['form'] = form

    return render(request, 'index.html', context)

class Input_form(forms.Form):
    username = forms.CharField(label='Utappd Usename', help_text = 'e.g. Hanz84', required=True)

def get_url_section(input_string):
    '''
    Given a string returns it in lower-case,
    with punctuation removed and only in ascii characters,
    with its individual words connected by a '-'
    '''
    url_section = input_string.lower() #convert to lower case
    url_section = url_section.translate(url_section.maketrans("","", string.punctuation)) #remove punctuations
    url_section = unicodedata.normalize('NFD', url_section).encode('ascii', 'ignore') #convert to ascii characters
    url_section = str(url_section,'utf-8') #converting byte instance back to regular string
    url_section = "-".join(url_section.split())
    return url_section



#this function needs to be customized
def _valid_result(res):
    """Validates results returned by find_courses"""
    (HEADER, RESULTS) = [0,1]
    ok = (isinstance(res, (tuple, list)) and 
        len(res) == 2 and
        isinstance(res[HEADER], (tuple, list)) and
        isinstance(res[RESULTS], (tuple, list)))
    if not ok:
        return False

    n = len(res[HEADER])
    def _valid_row(row):
        return isinstance(row, (tuple, list)) and len(row) == n
    return reduce(and_, (_valid_row(x) for x in res[RESULTS]), True)

