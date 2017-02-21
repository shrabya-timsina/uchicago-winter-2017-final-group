# Untappd Login Information
# username: cs122
# password: csproject
#

#on terminal: export PATH=$PATH:/home/shrabya/team-cs122-project
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

user_url = 'https://untappd.com/user/Em11'
def get_full_page_from_user_url(user_url):
    '''
    automate clicking through "show more" button on user profile feed
    '''
    binary = FirefoxBinary('/home/shrabya/team-cs122-project')
    browser = webdriver.Firefox(firefox_binary=binary)
    browser.get(user_url)
    # login
    browser.execute_script("document.getElementsByClassName('sign_in track-click')[0].click()")
    # next 5 lines from http://stackoverflow.com/questions/21186327/fill-username-and-password-using-selenium-in-python
    username = browser.find_element_by_id("username")
    password = browser.find_element_by_id("password")
    username.send_keys("cs122")
    password.send_keys("csproject")
    browser.find_element_by_name("submit").click()
    # after login, browser redirects to user_url page -- need to see if selenium prevents that somehow

    # click on show more until the full feed is visible
    x = 0
    # temporary hard code loop until dynamic loop in place
    # even when show more button no longer appears in browser, the button still exists in html (see page source)
    # so no problem with running the loop too many times
    while x < 15:
        # code from http://stackoverflow.com/questions/36987006/how-to-click-a-javascript-button-with-selenium
        browser.execute_script("document.getElementsByClassName('yellow button more_checkins more_checkins_logged track-click')[0].click()")
        x += 1




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