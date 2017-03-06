from django.shortcuts import render
#superuse admin username: cs122
#password: cs-project
# Create your views here.
from django.http import HttpResponse
from django import forms
import pandas as pd

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
                beer_suggestions_db = get_beer_suggestions(form.cleaned_data['username'])
                if form.cleaned_data['username']=="waddup": beer_suggestions_db = None
            else:
               beer_suggestions_db = None 
        else:
            beer_suggestions_db = None 
            context['valid_form'] = False 
    
    else:
        form = Input_form()
    
    if beer_suggestions_db is None:
        context['valid_username'] = False    
    else:
        context['valid_username'] = True
        context['column_names'] = list(beer_suggestions_db.columns)
        context['beers'] = beer_suggestions_db.values.tolist()
        context['num_results'] = len(beer_suggestions_db.values.tolist())

    context['form'] = form
    return render(request, 'index.html', context)

class Input_form(forms.Form):
    username = forms.CharField(label='Utappd Usename', help_text = 'e.g. Hanz84', required=True)


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

def get_beer_suggestions(username):
    beer_name = ["ale", "stout"]
    beer_id = [1,2]
    beer_df = pd.DataFrame({"ID":beer_id, "Name": beer_name})
    return beer_df

