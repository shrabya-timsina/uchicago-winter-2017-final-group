import queue
import bs4
import requests
import urllib.parse
import user
import string
import httplib2


def get_compassionate_soup_from_url(url):
    '''
    compassionate scraping method to get bs4 object from url
    '''
    conn = httplib2.Http(".cache")
    
    page = conn.request(url, "GET")

    soup = bs4.BeautifulSoup(page[1], 'html.parser')

    return soup
    


def user_dict_and_crawl_list(starting_url, soup):
    '''

    '''
    user_beers_url = starting_url + "/beers"

    beer_tag_list = soup.find_all("div", "cont user_profile")[0].find_all("div", "top")
    user_dict = profile_scraper(starting_url)
    if user_dict == None:
        return {}

    beers_urls_list = []
    users_to_crawl = []

    # original search code

    for tag in beer_tag_list:
        beer_url = tag.find_all("a", "label")[0].get("href")
        absolute_beer_url = convert_if_relative_url(user_beers_url, beer_url)
        beers_urls_list.append(absolute_beer_url)

    for beer_url in beers_urls_list:
        if beer_url == "http://help.untappd.com/kb/using-untappd/why-is-this-beer-flagged-for-deletion":
            continue
        request = get_request(beer_url)
        if request == None:
            print("request is none")
            continue
        else:
            '''
            ### Selenium code ###
            soup = sel.get_full_page_from_beer_url(beer_url, browser)
            '''
            beer_soup = convert_to_soup(request)
            if beer_soup == None:
                print("no beer soup")
                continue
            else:
                beer_words = beer_words_collector(beer_soup)

    
                user_dict["beer words"].append(beer_words)
                # pull user information
                tag_list = beer_soup.find_all("div","avatar-holder")[:-2] #last two dont contain user links
                for user in tag_list:
                    user_url = user.find('a').get('href')
                    absolute_user_url = convert_if_relative_url(beer_url, user_url)
                    if (absolute_user_url != starting_url) and (absolute_user_url not in users_to_crawl):
                         users_to_crawl.append(absolute_user_url)
    
    return user_dict, users_to_crawl


def get_user_dicts_list(starting_url, max_links_num, starting_soup):
    '''
    use priority queue to generate and process x number of profiles and corresponding x user dictionaries
    return list of user dictionaries
    '''
    # iniailize list of all user dicts
    all_user_dicts = []
    #keep track of profiles to visit
    need_process_links = []
    # keep track of visited profiles
    processed_links = []

    #starting_soup = get_compassionate_soup_from_url(starting_url)
    if starting_soup == None:
        print("use a different starting url")
        return None

    first_user_dict, users_to_crawl_list = user_dict_and_crawl_list(starting_url, starting_soup)
    if (first_user_dict == {}) or (users_to_crawl_list == []):
        print("use different starting url")
        return None
    all_user_dicts.append(first_user_dict)
    
    i = 0
    for link in users_to_crawl_list:
            if link not in processed_links:
                need_process_links.append(link)

    while (len(all_user_dicts) < max_links_num) and (need_process_links != []):
        current_link = need_process_links.pop()
        if current_link in processed_links:
            continue
        processed_links.append(current_link)
        current_soup = get_compassionate_soup_from_url(current_link)
        current_user_dict, current_user_link_branches = user_dict_and_crawl_list(current_link, current_soup)
        all_user_dicts.append(current_user_dict)
        i += 1
        print(i)
        need_process_links = need_process_links + current_user_link_branches 

    return all_user_dicts



def beer_words_collector(soup):
    '''
    '''
    beer_words = []
    if type(soup.find("div", "beer-descrption-read-less")) is None :
        return ''
    beer_desc = soup.find("div", "beer-descrption-read-less").get_text(" ", strip=True)
    beer_desc = ''.join(word.strip(string.punctuation) for word in beer_desc)
    [beer_words.append(word.lower()) for word in beer_desc.split()]

    beer_comments = soup.find_all("p", "checkin-comment")
    for comment in beer_comments:
        comment_tag = comment.find("span")
        if comment_tag != None:
            comment_text = str(comment_tag.previousSibling).strip()
        if comment_text != "":
            comment_text = ''.join(word.strip(string.punctuation) for word in comment_text)
            [beer_words.append(word.lower()) for word in comment_text.split()]
    
    return beer_words


def profile_scraper(starting_url):
    '''
    starting_object - either a url or a soup object
    '''
    user_beers_url = starting_url + "/beers"
    request = get_request(user_beers_url)
    beers_soup = convert_to_soup(request)

    user_dict = {}
    user_dict["styles"] = {}
    user_dict["countries"] = {}
    user_dict["breweries"] = {}
    user_dict["beers"] = {}
    user_dict["beer words"] = []

    user_dict["name"] = beers_soup.find("div", "cont").find("div", "info").h1.string
    user_dict["username"] = beers_soup.find("div", "cont").find("div", "info").find("span", "username").string

    styles_list = beers_soup.find("select", id="style_picker").find_all("option")
    for tag in styles_list:
        style_string = tag.string
        if style_string != "All Styles":
            style = style_string[:style_string.find("(") - 1]
            count = style_string[style_string.rfind("(")+1:style_string.rfind(")")]
            user_dict["styles"][style] = count
    
    country_list = beers_soup.find("select", id="country_picker").find_all("option")
    for tag in country_list:
        country_string = tag.string
        if country_string != "All Countries":
            country = country_string[:country_string.find("(") - 1]
            count = country_string[country_string.rfind("(")+1:country_string.rfind(")")]
            user_dict["countries"][country] = count

    brewery_list = beers_soup.find("select", id="brewery_picker").find_all("option")
    for tag in brewery_list:
        brewery_string = tag.string
        if brewery_string != "All Breweries":
            brewery = brewery_string[:brewery_string.find("(") - 1]
            count = brewery_string[brewery_string.rfind("(")+1:brewery_string.rfind(")")]
            user_dict["breweries"][brewery] = count

    beer_list = beers_soup.find("div", "distinct-list-list").find_all("div", "beer-item")
    for tag in beer_list:
        beer_id = tag.get("data-bid")
        beer_name = tag.find("p", "name").get_text(" ", strip=True)
        beer_brewery = tag.find("p", "brewery").string
        beer_style = tag.find("p", "style").string
        beer_timestamp = tag.find("abbr", "date-time").string
        beer_rating_unprocessed = tag.find("div", "ratings").p.string
        beer_rating_processed = beer_rating_unprocessed[beer_rating_unprocessed.find("(")+1:beer_rating_unprocessed.find(")")]
        beer_abv_str = tag.find("p", "abv").get_text(" ", strip=True)
        
        if beer_abv_str != "No ABV":
            beer_abv_num = float(beer_abv_str[:-5]) * 0.01
        else: 
            beer_abv_num = 0
        
        beer_count = tag.find("p", "check-ins").string.strip()[7:]
        user_dict["beers"][beer_name] = {}
        user_dict["beers"][beer_name]["beer id"] = beer_id
        user_dict["beers"][beer_name]["brewery name"] = beer_brewery
        user_dict["beers"][beer_name]["beer style"] = beer_style
        user_dict["beers"][beer_name]["beer timestamp"] = beer_timestamp
        user_dict["beers"][beer_name]["beer rating"] = beer_rating_processed
        user_dict["beers"][beer_name]["abv"] = beer_abv_num
        user_dict["beers"][beer_name]["count"] = beer_count

    return user_dict


########from util#############################################################################

def get_request(url):
    '''
    Open a connection to the specified URL and if successful
    read the data.

    Inputs:
        url: must be an absolute URL
    
    Outputs: 
        request object or None

    Examples:
        get_request("http://www.cs.uchicago.edu")
    '''

    if is_absolute_url(url):
        try:
            r = requests.get(url)
            if r.status_code == 404 or r.status_code == 403:
                r = None
        except:
            # fail on any kind of error
            r = None
    else:
        r = None

    return r

def read_request(request):
    '''
    Return data from request object.  Returns result or "" if the read
    fails..
    '''

    try:
        return request.text.encode('iso-8859-1')
    except:
        print("read failed: " + request.url)
        return ""


def get_request_url(request):
    '''
    Extract true URL from the request
    '''
    return request.url

def is_absolute_url(url):
    '''
    Is url an absolute URL?
    '''
    if url == "":
        return False
    return urllib.parse.urlparse(url).netloc != ""

def remove_fragment(url):
    '''remove the fragment from a url'''

    (url, frag) = urllib.parse.urldefrag(url)
    return url


def convert_if_relative_url(current_url, new_url):
    '''
    Attempt to determine whether new_url is a relative URL and if so,
    use current_url to determine the path and create a new absolute
    URL.  Will add the protocol, if that is all that is missing.

    Inputs:
        current_url: absolute URL
        new_url: 

    Outputs:
        new absolute URL or None, if cannot determine that
        new_url is a relative URL.

    Examples:
        convert_if_relative_url("http://cs.uchicago.edu", "pa/pa1.html") yields 
            'http://cs.uchicago.edu/pa/pa.html'

        convert_if_relative_url("http://cs.uchicago.edu", "foo.edu/pa.html") yields
            'http://foo.edu/pa.html'
    '''
    if new_url == "" or not is_absolute_url(current_url):
        return None

    if is_absolute_url(new_url):
        return new_url

    parsed_url = urllib.parse.urlparse(new_url)
    path_parts = parsed_url.path.split("/")

    if len(path_parts) == 0:
        return None

    ext = path_parts[0][-4:]
    if ext in [".edu", ".org", ".com", ".net"]:
        return "http://" + new_url
    elif new_url[:3] == "www":
        return "http://" + new_path
    else:
        return urllib.parse.urljoin(current_url, new_url)


 #####################################################################################


def convert_to_soup(request):
    '''
    Convert a given request object to soup

    Inputs:
        request: a request object
    Outputs:
        returns soup of request object if request is read,
        returns None otherwise    
    '''

    html = read_request(request)
    if html is not None:
        soup = bs4.BeautifulSoup(html, 'lxml')
        return soup
    else:
        return None