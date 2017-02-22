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
from time import sleep
from  bs4 import BeautifulSoup

user_url = 'https://untappd.com/user/Em11'


def go():
    browser = webdriver.Firefox()
    browser.get(user_url)
    browser.find_element_by_link_text('Sign In').click()
    sleep(1)

    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    username.send_keys("cs122")
    password.send_keys("csproject")
    password.submit()


def get_full_page_from_user_url(user_url):
    '''
    automate clicking through "show more" button on user profile feed
    '''
    browser = webdriver.Firefox()
    browser.get(user_url)
    # login
    browser.find_element_by_link_text('Sign In').click()
    # next 5 lines from http://stackoverflow.com/questions/21186327/fill-username-and-password-using-selenium-in-python
    sleep(1)
    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    username.send_keys("cs122")
    password.send_keys("csproject")
    password.submit()
    sleep(1)
    
    # after login, browser redirects to user_url page -- need to see if selenium prevents that somehow
    #update: works fine
    # click on show more until the full feed is visible
    
    x = 0
    # temporary hard code loop until dynamic loop in place
    # even when show more button no longer appears in browser, the button still exists in html (see page source)
    # so no problem with running the loop too many times
    while x < 15:
        print("step",x)
        sleep(1)
        # code from http://stackoverflow.com/questions/36987006/how-to-click-a-javascript-button-with-selenium
        browser.execute_script("document.getElementsByClassName('yellow button more_checkins more_checkins_logged track-click')[0].click()")
        x += 1
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
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