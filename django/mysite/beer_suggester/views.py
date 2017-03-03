from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django import forms

def index(request):
    return HttpResponse("Hello, world. You're at the beer_suggester index.")




class input_form(forms.Form):
	username = forms.Charfield(label='Utappd Usename', help_text = 'e.g. Hanz84', required=False)



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