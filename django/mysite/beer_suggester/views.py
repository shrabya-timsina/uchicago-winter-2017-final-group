#superuser admin username: cs122
#password: cs-project
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import bs4
import unicodedata
from data_analysis import get_suggestions_from_topk
import crawler #for beautiful soup request processing
import string


def index(request):
    context = {}
    if request.method == 'GET':
        form = Input_form(request.GET)
        if form.is_valid():
            context['valid_form'] = True
            if form.cleaned_data['username']:
                user_url = "https://untappd.com/user/" + form.cleaned_data['username'] + "/beers"
                user_page_request = crawler.get_request(user_url)
                if not user_page_request:
                    context['valid_username'] = False  
                else:
                    context['valid_username'] = True 
                    user_soup = crawler.convert_to_soup(user_page_request)
                    beer_number = int(user_soup.find("span", "stat").text.replace(',', ''))
                    if beer_number < 5:
                        context['enough_beers'] = False 
                    else:
                        context['enough_beers'] = True
                        # k is the number of other users to get suggestions from
                        k = 5 
                        beer_suggestions_df = get_suggestions_from_topk(form.cleaned_data['username'], k)
                        
                        if beer_suggestions_df is not None:
                            context['valid_database'] = True
                            beer_page_urls = []
                            image_column = []
                            for i, beer in beer_suggestions_df.iterrows():
                                name_url_section = get_url_section(beer['name'])          
                                brewery_url_section = get_url_section(beer['brewery']) 
                                url = "https://untappd.com/b/" +  brewery_url_section + "-" + name_url_section + "/" + str(beer['beer_id'])
                                beer_page_request = crawler.get_request(url)
                                beer_soup = crawler.convert_to_soup(beer_page_request)
                                if not beer_soup:
                                    beer_link = "No beer page"
                                    image_link = "default"
                                else:
                                    beer_link = url
                                    tag_list = beer_soup.find("div", "basic")
                                    image_link = tag_list.find("img")["src"]
                                beer_page_urls.append(beer_link)
                                image_column.append(image_link)
                            beer_suggestions_df["Image"] = image_column
                        
                            context['column_names'] = list(beer_suggestions_df.columns)
                            context['beers'] = zip(beer_page_urls, beer_suggestions_df.values.tolist())
                            context['num_results'] = len(beer_suggestions_df.values.tolist())  
                            context['beer_page_urls'] = beer_page_urls    
                        else:
                            context['valid_database'] = False

            else:
               context['valid_username'] = False 
        else:
            context['valid_form'] = False 
    else:
        form = Input_form()
       
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


