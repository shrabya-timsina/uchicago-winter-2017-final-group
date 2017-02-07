import queue
import bs4
import requests
import urllib.parse


def crawler(starting_url):
    '''
    Crawl the college catalog and generate a dictionary with course 
    identifiers mapped to words as key-value pairs

    Inputs:
        starting_url: string, the first url to visit, given
        limiting_domain: string, the limiting_domain of all urls
        course_map_filename: a json file
    Outputs:
        index_dictionary: dictionary, with course identifiers mapped to
                        words as key-value pairs
    '''
    
    user_beers_url = starting_url + "/beers"
    request = get_request(user_beers_url)
    soup = convert_to_soup(request)
    tag_list = soup.find_all("p", "name")
    beers_urls_list = []
    for tag in tag_list:
        beer_url = tag.contents[0].get('href')
        absolute_beer_url = convert_if_relative_url(user_beers_url, beer_url)
        beers_urls_list.append(absolute_beer_url)

    users_to_crawl = []
    for beer_url in beers_urls_list:
        request = get_request(beer_url)
        if request == None:
            continue
        else:
            soup = convert_to_soup(request)
            tag_list = soup.find_all("div","avatar-holder")[:-2]
            for user in tag_list:
                user_url = user.find('a').get('href')
                absolute_user_url = convert_if_relative_url(beer_url, user_url)
                if (absolute_user_url != starting_url) and (absolute_user_url not in users_to_crawl):
                    users_to_crawl.append(absolute_user_url)

    return users_to_crawl



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