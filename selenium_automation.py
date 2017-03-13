# Untappd Login Information
# username: cs122
# password: csproject

#run the following on terminal before running selenium - every time
#on terminal: export PATH=$PATH:/home/student/team-cs122-project
#make sure geckodriver is in same directory as this file
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from  bs4 import BeautifulSoup


def demo_for_graders():
    browser = webdriver.Firefox()
    login_to_untapped(browser)
    get_full_page_from_user_url('https://untappd.com/user/Em11/beers', browser)    

def open_browser():
    browser = webdriver.Firefox()
    return browser

def login_to_untapped(browser):
    home_page = 'https://untappd.com/'
    browser.get(home_page)
    delay = 10
    browser.find_element_by_link_text('Sign In').click()
    element_present = EC.presence_of_element_located((By.ID, 'username'))
    WebDriverWait(browser, delay).until(element_present)
    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    username.send_keys("cs122")
    password.send_keys("csproject")
    password.submit()

def get_full_page_from_user_url(user_beers_url, browser):
    '''
    automate clicking through "show more" button on user profile feed
    '''
    browser.get(user_beers_url)
    delay = 10
    x = 0
    # even when show more button no longer appears in browser, the button still exists in html (see page source)
    # so no problem with running the loop too many times
    while x < 15:
        element_present = EC.presence_of_element_located((By.LINK_TEXT, 'Show More'))
        WebDriverWait(browser, delay).until(element_present)
        # code from http://stackoverflow.com/questions/36987006/how-to-click-a-javascript-button-with-selenium
        browser.execute_script("document.getElementsByClassName('button yellow more more_beers track-click')[0].click()")
        x += 1
    
    soup = BeautifulSoup(browser.page_source, "html.parser")

    return soup

def get_full_page_from_beer_url(beer_url, browser):
    '''
    automate clicking through "show more" button on beer page feed
    '''
    browser.get(beer_url)
    delay = 10
    x = 0
    # even when show more button no longer appears in browser, the button still exists in html (see page source)
    # so no problem with running the loop too many times
    while x < 7:
        element_present = EC.presence_of_element_located((By.LINK_TEXT, 'Show More'))
        WebDriverWait(browser, delay).until(element_present)
        # code from http://stackoverflow.com/questions/36987006/how-to-click-a-javascript-button-with-selenium
        browser.execute_script("document.getElementsByClassName('more_checkins button yellow track-click more_checkins_logged')[0].click()")
        x += 1
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    return soup




