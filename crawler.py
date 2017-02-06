import queue
import bs4
import requests
import urllib.parse


def crawler(starting_url, limiting_domain, course_map_filename):
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

    course_code_identifier_map = open_json_key(course_map_filename)
    urls_to_crawl = queue.Queue()

    urls_crawled = set()

    urls_processed = set() 

    urls_to_crawl.put(starting_url)
    urls_crawled.add(starting_url)
    crawl_count = 0
    index_dictionary = {}
    
    while (not urls_to_crawl.empty()) and (crawl_count < 1000):
        
        next_to_crawl = urls_to_crawl.get()
        request = get_request(next_to_crawl)
        
        if request is not None:
            real_url = get_request_url(request)

            if real_url is not None:
                
                if real_url not in urls_crawled:
                    urls_crawled.add(real_url)
                    
                if real_url not in urls_processed:
                    urls_processed.add(real_url)
                    soup = convert_to_soup(request)

                    if soup is not None:

                        #update the dictionary
                        index_dictionary = build_dict(soup, index_dictionary, 
                                                   course_code_identifier_map)

                        #check for potential links in current page 
                        #and update the queue
                        list_of_urls_in_page = soup.find_all('a', href=True)

                        for link in list_of_urls_in_page:
                            url = extract_url(link, real_url)

                            if url is not None:

                                if (url not in urls_crawled):

                                    if is_url_ok_to_follow(url, 
                                                           limiting_domain):

                                        urls_to_crawl.put(url)
                                        urls_crawled.add(url)
 

        crawl_count += 1 

    return index_dictionary 

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


def is_url_ok_to_follow(url, limiting_domain):
    '''
    Inputs:
        url: absolute URL
        limiting domain: domain name

    Outputs: 
        Returns True if the protocol for the URL is HTTP, the domain
        is in the limiting domain, and the path is either a directory
        or a file that has no extension or ends in .html. URLs
        that include an "@" are not OK to follow.

    Examples:
        is_url_ok_to_follow("http://cs.uchicago.edu/pa/pa1", "cs.uchicago.edu") yields
            True

        is_url_ok_to_follow("http://cs.cornell.edu/pa/pa1", "cs.uchicago.edu") yields
            False
    '''

    if "mailto:" in url:
        return False

    if "@" in url:
        return False

    if url[:LEN_ARCHIVES] == ARCHIVES:
        return False

    parsed_url =  urllib.parse.urlparse(url)
    if parsed_url.scheme != "http" and parsed_url.scheme != "https":
        return False

    if parsed_url.netloc == "":
        return False

    if parsed_url.fragment != "":
        return False

    if parsed_url.query != "":
        return False


    loc = parsed_url.netloc
    ld = len(limiting_domain)
    trunc_loc = loc[-(ld+1):]
    if not (limiting_domain == loc or (trunc_loc == "." + limiting_domain)):
        return False

    # does it have the right extension
    (filename, ext) = os.path.splitext(parsed_url.path)
    return (ext == "" or ext == ".html")

 #####################################################################################

def convert_to_soup(url):
    '''
    Convert a given request object to soup

    Inputs:
        request: a request object
    Outputs:
        returns soup of request object if request is read,
        returns None otherwise    
    '''

    pm = urllib3.PoolManager()

    html = pm.urlopen(url=myurl, method="GET").data
    soup = bs4.BeautifulSoup(html, "lxml")

def extract_url(tag, absolute_url):
    '''
    Given a tag with an attribute href=True, will return an absolute url
    of the tag

    Inputs:
        tag: a tag with an href attribute
        absolute_url: string, the full url address of the tag

    Outputs:
        url: string, the link provided in the tag
    '''
    
    url = tag.get('href')
    url = remove_fragment(url)
    url = convert_if_relative_url(absolute_url, url)
    return url