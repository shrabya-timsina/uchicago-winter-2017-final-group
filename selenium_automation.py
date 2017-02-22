# Untappd Login Information
# username: cs122
# password: csproject
#
"""
if anyone wants torun selenium -use Vm and on terminal enter the following two 
lines update your VM, which will update firefox too:
sudo apt-update
sudo apt-upgrade
___________
turning sth into an executable - for future reference
chmod +x firefox
chmod +x firefox-bin
./firefox
"""

#run the following on terminal before running selenium - every time
#we need to make a script later which runs both the following and our entire project
#on terminal: export PATH=$PATH:/home/student/team-cs122-project
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from  bs4 import BeautifulSoup

user_beers_url = 'https://untappd.com/user/Em11/beers'

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

def get_full_page_from_user_url(user_beers_url, ):
    '''
    automate clicking through "show more" button on user profile feed
    '''
    browser = webdriver.Firefox()
    login_to_untapped(browser)
    browser.get(user_beers_url)
    delay = 10
    
    
    x = 0
    # temporary hard code loop until dynamic loop in place
    # even when show more button no longer appears in browser, the button still exists in html (see page source)
    # so no problem with running the loop too many times
    while x < 15:
        element_present = EC.presence_of_element_located((By.LINK_TEXT, 'Show More'))
        WebDriverWait(browser, delay).until(element_present)
        # code from http://stackoverflow.com/questions/36987006/how-to-click-a-javascript-button-with-selenium
        browser.execute_script("document.getElementsByClassName('button yellow more more_beers track-click')[0].click()")
        print("step",x)

        x += 1
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.quit()
    return soup




"""
https://automatetheboringstuff.com/chapter11/
Pseudo
#finding the element
browser.find_elements_by_class_name(name) # - might have to use another find type

##clicking on it 
linkElem.click()

### repeat above two continously, while gathering user profiles

### this code updates the feed after clicking "show more"
### from untappd source code
$(document).ready(function() {
		$(".more_checkins_logged").on("click", function() {
			var _this = $(this);
			$(_this).hide();
			$(".stream-loading").addClass("active");

			var offset = $("#main-stream .item:last").attr('data-checkin-id');
			var user = $(this).attr("data-user-name");

			$.ajax({
				url: "/profile/more_feed/"+user+"/"+offset+"?v2=true",
				type: "GET",
				error: function(xhr)
				{
					$(".stream-loading").removeClass("active");
					$(_this).show();
					$.notifyBar({
						html: "Hmm. Something went wrong. Please try again!",
						delay: 2000,
						animationSpeed: "normal"
					});
				},
				success: function(html)
				{
					$(".stream-loading").removeClass("active");

					if (html == "") {
						$(".more_checkins").hide();
					}
					else {
						$(_this).show();
						$("#main-stream").append(html);
						$("img.lazy").lazyload();
						$(".tip").tipsy({fade: true});
						refreshTime(".timezoner", "D MMM YY");
					}
				}
			});

			return false;
		});
	});
"""