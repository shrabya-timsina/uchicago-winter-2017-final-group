from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://untappd.com/thepub')

"""
https://automatetheboringstuff.com/chapter11/
Pseudo
#finding the element
browser.find_elements_by_class_name(name) # - might have to use another find type

##clicking on it 
linkElem.click()

### repeat above two continously, while gathering user profiles
