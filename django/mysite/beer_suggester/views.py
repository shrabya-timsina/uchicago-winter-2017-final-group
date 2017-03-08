from django.shortcuts import render
#superuse admin username: cs122
#password: cs-project
# Create your views here.
from django.http import HttpResponse
from django import forms
import pandas as pd
import bs4
import urllib3

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
                beer_suggestions_df = get_beer_suggestions(form.cleaned_data['username'])
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
        pm = urllib3.PoolManager()
        image_column = []
        for i, beer in beer_suggestions_df.iterrows():
            name_url_section = "-".join(beer['Name'].lower().split())
            brewery__url_section = "-".join(beer['Brewery'].lower().split())
            myurl = "https://untappd.com/b/" +  brewery__url_section + "-" + name_url_section + "/" + str(beer['ID'])
            html = pm.urlopen(url=myurl, method="GET").data
            soup = bs4.BeautifulSoup(html, "lxml")
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



def get_beer_suggestions(username):
    # https://untappd.com/b/goose-island-beer-co-goose-ipa/1353
    beer_name = ["Goose IPA", "IPA"]
    beer_id = [1353,4509]
    brewery = ["Goose Island Beer Co.", "Lagunitas Brewing Company"]
    beer_df = pd.DataFrame({"ID":beer_id, "Name": beer_name, "Brewery": brewery})
    return beer_df



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

